# STREAM-like memory bandwidth test with torch on CPU (copy and triad), threads and processes.
# Arrays of 2^26 float32 (256 MB) each, far larger than the L3 cache (18 MB on i5-12500H).
import sys, time, os
import multiprocessing as mp

N = 1 << 26  # elements per array
B = N * 4    # bytes per array


def kernel(nthreads, reps=8):
    import torch
    torch.set_num_threads(nthreads)
    a = torch.ones(N); b = torch.full((N,), 2.0); c = torch.empty(N)
    best_copy = best_triad = 0.0
    for _ in range(reps):
        t = time.perf_counter(); c.copy_(a); dt = time.perf_counter() - t
        best_copy = max(best_copy, 2 * B / dt / 1e9)
        t = time.perf_counter(); torch.add(a, b, alpha=3.0, out=c); dt = time.perf_counter() - t
        best_triad = max(best_triad, 3 * B / dt / 1e9)
    assert float(c[12345]) == 7.0
    return best_copy, best_triad


def worker(barrier, q, reps):
    import torch
    torch.set_num_threads(1)
    a = torch.ones(N); b = torch.full((N,), 2.0); c = torch.empty(N)
    torch.add(a, b, alpha=3.0, out=c)
    barrier.wait()
    t = time.perf_counter()
    for _ in range(reps):
        torch.add(a, b, alpha=3.0, out=c)
    q.put(reps * 3 * B / (time.perf_counter() - t) / 1e9)


if __name__ == "__main__":
    print("threads | copy GB/s | triad GB/s (best of 8, one process)")
    for th in [1, 2, 4, 8, 12]:
        cp, tr = kernel(th)
        print(f"{th:7d} | {cp:9.1f} | {tr:10.1f}")
    print("\nprocesses (1 thread each, simultaneous triad) | total GB/s | per process")
    for P in [1, 2, 4, 6, 8]:
        bar = mp.Barrier(P); q = mp.Queue()
        ps = [mp.Process(target=worker, args=(bar, q, 12)) for _ in range(P)]
        [p.start() for p in ps]; r = [q.get() for _ in ps]; [p.join() for p in ps]
        print(f"{P:46d} | {sum(r):10.1f} | {sum(r)/P:.1f}")
