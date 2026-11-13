from pathlib import Path
from pypdf import PdfReader
A=Path(__file__).resolve().parent; root=A.parent
p=next((root/'documents').glob('*Perspective*.pdf'))
pages=PdfReader(p).pages
(A/'perspective.txt').write_text('\n\n'.join('PAGE '+str(i+1)+'\n'+x.extract_text() for i,x in enumerate(pages)),encoding='utf8')
files=list((root/'repository/Stadiul0').glob('*.py'))+list((root/'repository/Stadiul0/lm').glob('*.py'))+list((root/'repository/Stadiul0/forever_repro').glob('*.py'))+list((root/'repository/Stadiul0/p2').glob('*.py'))+[root/'documents/Pilot2_closure_report_draft_v0.1.md',A/'perspective.txt']
out=[]
for p in files:
 out.append('\nFILE '+str(p.relative_to(root)))
 out.extend(f'{i}: {s}' for i,s in enumerate(p.read_text(encoding='utf8').splitlines(),1))
(A/'numbered_sources.txt').write_text('\n'.join(out),encoding='utf8')
