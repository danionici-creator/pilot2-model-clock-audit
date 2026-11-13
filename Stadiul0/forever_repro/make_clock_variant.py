# Builds src/finetune_cl_our_qwen_clock.py from their src/finetune_cl_our_qwen.py: ONLY the clock that drives replay changes.
from pathlib import Path
s = Path("src/finetune_cl_our_qwen.py").read_text(encoding="utf-8")
patches = [
    ("        self.tau += float(delta_t)\n        self.step += 1\n        self.prev_vec = curr_vec\n",
     "        # CLOCK SWAP (Pilot 2, 7 Nov 2026): 'tau' (the replay-driving clock) advances by FOREVER_CLOCK's increment;\n"
     "        # the true update norm is kept in tau_true; mu (replay strength) still uses delta_t, as in the original.\n"
     "        clock = os.environ.get(\"FOREVER_CLOCK\", \"tau\")\n"
     "        if clock == \"tau\":\n"
     "            inc = float(delta_t)\n"
     "        else:\n"
     "            opt = kwargs.get(\"optimizer\"); lr = getattr(self, \"_lr_at_step_begin\", None)\n"
     "            if lr is None:\n"
     "                lr = opt.param_groups[0][\"lr\"]\n"
     "            if clock == \"eta\":\n"
     "                inc = float(lr)\n"
     "            else:  # 'eta_m': lr * |m_hat| (bias-corrected first moment of AdamW)\n"
     "                sq, k = 0.0, None\n"
     "                for group in opt.param_groups:\n"
     "                    for p in group[\"params\"]:\n"
     "                        st = opt.state.get(p, {})\n"
     "                        if \"exp_avg\" in st:\n"
     "                            sq += float((st[\"exp_avg\"].float() ** 2).sum()); k = float(st[\"step\"])\n"
     "                inc = float(lr) * (sq ** 0.5) / (1 - 0.9 ** k) if k else 0.0\n"
     "        self.tau_true = getattr(self, \"tau_true\", 0.0) + float(delta_t)\n"
     "        self.tau += inc\n"
     "        self.step += 1\n"
     "        self.prev_vec = curr_vec\n"),
    ('f.write("step,delta_t,tau\\n")', 'f.write("step,delta_t,tau,tau_true\\n")'),
    ('f.write(f"{self.step},{delta_t},{self.tau}\\n")', 'f.write(f"{self.step},{delta_t},{self.tau},{self.tau_true}\\n")'),
    ("    def on_step_end(self, args, state, control, **kwargs):\n        model = kwargs[\"model\"]",
     "    def on_step_begin(self, args, state, control, **kwargs):  # CLOCK SWAP: lr applied at this step\n"
     "        opt = kwargs.get(\"optimizer\")\n"
     "        self._lr_at_step_begin = opt.param_groups[0][\"lr\"] if opt is not None else None\n\n"
     "    def on_step_end(self, args, state, control, **kwargs):\n        model = kwargs[\"model\"]"),
]
for old, new in patches:
    n = s.count(old)
    assert n == 1, (n, old[:60])
    s = s.replace(old, new)
Path("src/finetune_cl_our_qwen_clock.py").write_text(s, encoding="utf-8")
print("ok: clock variant written")
