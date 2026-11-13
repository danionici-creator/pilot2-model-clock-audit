"""Independent, read-only code/data checks. Run with _audit/venv/Scripts/python -I."""
from pathlib import Path
import ast,json,math
import numpy as np
import pandas as pd
R=Path(__file__).resolve().parents[1]/'repository/Stadiul0'
print('SUPERNI epoch accounting: stored current/calibration rows versus per-epoch batches')
for p in sorted((R/'runs/sni/tau').glob('*/steps.npz')):
 z=np.load(p); d=pd.DataFrame(z['data'],columns=z['cols'])
 print(p.parent.name, d[d.counted==1].groupby('task').size().to_dict())
print('Example n=1000, batch=32, epochs=3: code',math.ceil(1000/32*3),'generator',math.ceil(1000/32)*3)
print('C6 correlation in original preview (not an independent predictor):')
for tag in ['tech3_lr3e-4/F2_s9004','tech3_lr3e-4/F3_s9004']:
 d=pd.read_parquet(R/'runs'/tag/'triplets.parquet')
 print(tag, d[['rate_ce_D1','C6_post_m_first','C6_post_m_last']].corr().to_dict())
print('FOREVER in-sample versus independently held-out task prediction')
for arm in ['eta_m','eta_m_A1']:
 xs=[];ys=[]
 for p in sorted((R/f'forever_repro/ckpt_{arm}').glob('*/*/drift_log.csv')):
  if arm.endswith('A1') and p.parent.name.startswith('0-'):continue
  d=pd.read_csv(p); n=len(d)//8*8
  x=np.diff(np.r_[0,d.tau.to_numpy()])[:n].reshape(-1,8).sum(1)
  y=d.delta_t.to_numpy()[:n].reshape(-1,8).sum(1)
  xs.append(x);ys.append(y)
 for i in range(len(xs)):
  trainx=np.concatenate([x for j,x in enumerate(xs) if j!=i]); trainy=np.concatenate([y for j,y in enumerate(ys) if j!=i])
  coef=np.linalg.lstsq(np.c_[np.ones(len(trainx)),trainx],trainy,rcond=None)[0]
  pred=np.c_[np.ones(len(xs[i])),xs[i]]@coef
  print(arm,i,'held-out-task R2',1-sum((ys[i]-pred)**2)/sum((ys[i]-ys[i].mean())**2))
print('Tie diagnostic records:')
j=json.loads((R/'runs/forever_eval_tie_diagnostic_posthoc.json').read_text())
print('items',len(j),'reproduced',sum(x['reproduced'] for x in j),'ties',sum(x.get('tie',False) for x in j))
print('Clock swap omitted skip check:', 'optimizer_step_was_skipped' not in (R/'forever_repro/make_clock_variant.py').read_text())
