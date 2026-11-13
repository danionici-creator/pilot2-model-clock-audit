"""Hardware watchdog for unattended rounds (6 Nov 2026). Run with the CPU environment:
    python -I hw_watchdog.py --until "2026-11-09 08:00"

Every 30 s it logs GPU (nvidia-smi: temperature, power, SM clock, utilisation, thermal slowdown flags), the ACPI thermal
zone (typeperf: temperature in kelvin, % passive limit = firmware throttling), CPU performance %, AC power and free space
on D: to runs/_hw/hw_log_<date>.csv. It keeps Windows awake until --until (SetThreadExecutionState; no setting changed).
It stops the training processes (lm_forever_run.py, the synthetic-world runs) and writes runs/_HW_STOP when, for the stated
number of consecutive samples:
  GPU >= 87 C (3) | GPU hardware/software thermal slowdown (3) | thermal zone >= 370 K = 97 C (3)
  | passive limit < 100% (6) | on battery (2) | D: free < 10 GB (1).
Then it exits with one line saying why (the caller is notified). Launchers check runs/_HW_STOP before each run.
"""
import argparse, ctypes, csv, datetime as dt, os, shutil, subprocess, sys, time
from pathlib import Path

RUNS = Path(r"D:\Time\02_Pilot2\Stadiul0\runs"); HW = RUNS / "_hw"; STOP = RUNS / "_HW_STOP"
RULES = {"gpu_hot": 3, "gpu_slowdown": 3, "tz_hot": 3, "passive": 6, "battery": 2, "disk": 1}
NV = ["temperature.gpu", "power.draw", "clocks.sm", "utilization.gpu", "memory.used",
      "clocks_event_reasons.hw_thermal_slowdown", "clocks_event_reasons.sw_thermal_slowdown"]

class SPS(ctypes.Structure):
    _fields_ = [("ACLineStatus", ctypes.c_byte), ("BatteryFlag", ctypes.c_byte), ("BatteryLifePercent", ctypes.c_byte),
                ("SystemStatusFlag", ctypes.c_byte), ("BatteryLifeTime", ctypes.c_ulong), ("BatteryFullLifeTime", ctypes.c_ulong)]

def sample():
    r = {"time": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    try:
        out = subprocess.run(["nvidia-smi", f"--query-gpu={','.join(NV)}", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=20).stdout.strip().split(", ")
        r.update(gpu_t=float(out[0]), gpu_w=float(out[1]), gpu_mhz=float(out[2]), gpu_util=float(out[3]),
                 gpu_mem=float(out[4]), gpu_slow=int(any(x.strip() == "Active" for x in out[5:7])))
    except Exception as e:
        r.update(gpu_t=float("nan"), gpu_err=str(e)[:60])
    try:
        out = subprocess.run(["typeperf", r"\Thermal Zone Information(*)\Temperature",
                              r"\Thermal Zone Information(*)\% Passive Limit",
                              r"\Processor Information(_Total)\% Processor Performance", "-sc", "1"],
                             capture_output=True, text=True, timeout=30).stdout.splitlines()
        vals = [float(v.strip('"')) for v in out[2].split(",")[1:]]
        r.update(tz_k=vals[0], passive=vals[1], cpu_perf=vals[2])
    except Exception:
        r.update(tz_k=float("nan"), passive=float("nan"), cpu_perf=float("nan"))
    s = SPS(); ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(s))
    r.update(ac=int(s.ACLineStatus == 1), batt=int(s.BatteryLifePercent))
    r["d_free_gb"] = round(shutil.disk_usage("D:\\").free / 2**30, 1)
    return r

def flags(r):
    return {"gpu_hot": r.get("gpu_t", 0) >= 87, "gpu_slowdown": r.get("gpu_slow", 0) == 1,
            "tz_hot": r.get("tz_k", 0) >= 370, "passive": r.get("passive", 100) < 100,
            "battery": r["ac"] == 0, "disk": r["d_free_gb"] < 10}

def stop_training(reason):
    STOP.write_text(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {reason}\n", encoding="utf-8")
    ps = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { $_.CommandLine -match "
          "'lm_forever_run|p2[.\\\\/]run|launch\\.py|run_one' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; $_.ProcessId }")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=60).stdout.split()
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--until", required=True); ap.add_argument("--every", type=int, default=30)
    a = ap.parse_args(); until = dt.datetime.strptime(a.until, "%Y-%m-%d %H:%M")
    HW.mkdir(parents=True, exist_ok=True)
    ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
    streak = {k: 0 for k in RULES}; fields = None
    while dt.datetime.now() < until:
        r = sample(); f = flags(r)
        path = HW / f"hw_log_{dt.date.today():%Y%m%d}.csv"; new = not path.exists()
        cols = ["time", "gpu_t", "gpu_w", "gpu_mhz", "gpu_util", "gpu_mem", "gpu_slow", "tz_k", "passive", "cpu_perf",
                "ac", "batt", "d_free_gb"]
        with open(path, "a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            if new: w.writeheader()
            w.writerow(r)
        for k in RULES:
            streak[k] = streak[k] + 1 if f[k] else 0
        hit = [k for k in RULES if streak[k] >= RULES[k]]
        if hit:
            pids = stop_training(",".join(hit))
            print(f"OPRIRE HARDWARE {r['time']}: {hit}; GPU {r.get('gpu_t')} C, zona termica {r.get('tz_k')} K, "
                  f"limita pasiva {r.get('passive')}%, priza {r['ac']}, D: {r['d_free_gb']} GB; procese oprite: {pids}", flush=True)
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            sys.exit(2)
        time.sleep(a.every)
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    print(f"paznic terminat normal la {dt.datetime.now():%Y-%m-%d %H:%M}", flush=True)

if __name__ == "__main__":
    main()
