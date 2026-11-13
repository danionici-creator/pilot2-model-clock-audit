from pathlib import Path
import runpy,hashlib,re,json,subprocess,sys
A=Path(__file__).resolve().parent; R=A.parent/'repository'
m=runpy.run_path(str(R/'Stadiul0/reproduce_analyses.py'))
print('Comparator finite versus NaN:',m['same_json']({'x':1.0},{'x':float('nan')}))
print('Comparator missing empty container:',m['same_json']({'x':[]},{}))
lists=list((R/'Stadiul0/runs').glob('*_sha256.txt'))
print('Hash list files',len(lists),'recognized lines',sum(bool(re.fullmatch(r'[0-9a-f]{64} \*.+',s.strip())) for p in lists for s in p.read_text().splitlines()))
bad=[];n=0
for line in (R/'SHA256SUMS.txt').read_text(encoding='utf8').splitlines():
 if not line.strip():continue
 h,rel=line.split(maxsplit=1);rel=rel.lstrip('*');p=R/rel;n+=1
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:bad.append(rel)
print('Release manifest',n,'entries; mismatches',bad)
# Adversarial fixtures are NEW files exclusively in _audit.
F=A/'hash_fixture'; (F/'runs').mkdir(parents=True,exist_ok=True)
(F/'verify_hash_lists.py').write_bytes((R/'Stadiul0/verify_hash_lists.py').read_bytes())
(F/'runs/malformed_sha256.txt').write_text('not a valid checksum entry\n')
p=subprocess.run([sys.executable,'-I',str(F/'verify_hash_lists.py')],capture_output=True,text=True,encoding='utf8')
print('Malformed-only list exit',p.returncode,'output:',p.stdout)
