"""Reproduce on a private copy; never invoke mutating analyses in the original."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,importlib.metadata,os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:
 os.environ[key]='2'
A=Path(__file__).resolve().parent; R=A.parent/'repository'; C=A/'reproduction/repository'
def manifest(root):
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
before=manifest(R)
(A/'source_manifest_before.json').write_text(json.dumps(before,indent=1))
(A/'environment.txt').write_text(sys.version+'\n'+'\n'.join(f'{x}=={importlib.metadata.version(x)}' for x in ['numpy','pandas','scikit-learn','scipy','torch','pyarrow']))
if not C.exists():
 shutil.copytree(R,C,ignore=shutil.ignore_patterns('Recenzii','Colocviu','__pycache__'))
for name in ['reproduce_analyses','verify_hash_lists']:
 with (A/f'{name}.log').open('w',encoding='utf8') as out:
  p=subprocess.run([sys.executable,'-I',f'Stadiul0/{name}.py'],cwd=C,stdout=out,stderr=subprocess.STDOUT)
 print(name,'exit',p.returncode,flush=True)
after=manifest(R)
(A/'source_integrity.json').write_text(json.dumps({'files':len(before),'unchanged':before==after},indent=1))
print('Source unchanged:',before==after,flush=True)
