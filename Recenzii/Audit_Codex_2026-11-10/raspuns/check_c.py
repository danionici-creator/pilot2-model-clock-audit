"""Independent endpoint recomputation and counterexamples; no writes to sources."""
from pathlib import Path
import numpy as np,json
from scipy.stats import t
R=Path(__file__).resolve().parents[1]/'repository/Stadiul0/runs'
for clock in ['eta_m','eta','steps']:
 d=[]
 for s in range(7301,7306):
  a=np.load(R/f'ta/tau/s{s}/evals.npz')['acc'][-1].mean()
  b=np.load(R/f'ta/{clock}/s{s}/evals.npz')['acc'][-1].mean();d.append(a-b)
 d=np.array(d); h=t.ppf(.975,4)*d.std(ddof=1)/np.sqrt(5)
 print('T-A',clock,d.mean(),[d.mean()-h,d.mean()+h])
d=[]
for s in range(7401,7404):
 a=np.load(R/f'sni/tau/s{s}/evals.npz')['loss'][-1].mean()
 b=np.load(R/f'sni/eta_m/s{s}/evals.npz')['loss'][-1].mean();d.append((a-b)/a)
d=np.array(d);h=t.ppf(.975,2)*d.std(ddof=1)/np.sqrt(3)
print('S2',d.mean(),[d.mean()-h,d.mean()+h])
# Four balanced points: X and residual Z are orthogonal. y is 99% reconstructible,
# yet Z (and therefore y conditional on X) perfectly determines functional outcome.
x=np.array([-1.,-1.,1.,1.]); z=np.array([-1.,1.,-1.,1.]); y=x+.1*z
print('Counterexample reconstruction R2',1-sum((y-x)**2)/sum((y-y.mean())**2))
print('Outcome z recovered from residual',np.allclose((y-x)/.1,z))
theta=np.float32(1e8); update=np.float32(-1.)
print('Floating update: ideal',update,'actual stored parameter difference',np.float32(theta+update)-theta)
print('Skipped step with nonzero old moments: actual update 0; algebra without skip flag remains nonzero')
