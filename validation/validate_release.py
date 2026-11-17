from pathlib import Path
import json,re,zipfile,hashlib
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def ck(name,ok):checks.append({'name':name,'status':'PASS' if ok else 'FAIL'})
model=json.loads((ROOT/'validation/model_validation.json').read_text());early=json.loads((ROOT/'validation/phase03_validation.json').read_text());cases=json.loads((ROOT/'model/scenario_results.json').read_text())
ck('All 55 model checks pass',model['passed']==55 and model['failed']==0)
ck('All 44 evidence/budget checks pass',early['passed']==44 and early['failed']==0)
pdf=PdfReader(ROOT/'memo/credit_committee_memo.pdf');text=' '.join(p.extract_text() for p in pdf.pages)
ck('Memo is exactly five pages',len(pdf.pages)==5)
for c in cases:
 vals=[f"{c['Actual debt drawn at COD']/1e6:,.2f}",f"{c['Minimum quarterly organic DSCR']:.2f}x",f"{c['Minimum DSCR excluding replacement']:.2f}x",f"{c['Peak construction funding gap']/1e6:,.2f}"]
 ck(c['case']+' rounded scenario outputs appear in memo',all(v in text for v in vals))
ck('Downside arrears agree with memo',f"{cases[2]['Peak unpaid debt service']/1e6:.2f}" in text)
ck('Memo preserves negative recommendation','decline the request as currently structured' in text)
ck('Memo preserves native Excel limitation','Native Microsoft Excel application recalculation was not independently verified' in text)
paths=['README.md','docs/viewing_guide.md','docs/contribution_statement.md','docs/model_implementation.md','docs/progress.md']
broken=[]
for name in paths:
 for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',(ROOT/name).read_text()):
  if not re.match(r'https?://|#|mailto:',link) and not ((ROOT/name).parent/link.split('#')[0]).exists():broken.append((name,link))
ck('Viewer-facing relative file links resolve',not broken)
ck('Public data and hypothetical project inputs are distinguished','hypothetical' in (ROOT/'README.md').read_text() and 'classification' in (ROOT/'docs/assumptions_register.csv').read_text())
ck('AI contribution disclosure is included','substantial ai assistance' in (ROOT/'docs/contribution_statement.md').read_text().lower())
ck('Dashboard and sensitivity previews are readable PNG files',all((ROOT/'assets'/f).read_bytes().startswith(b'\x89PNG\r\n\x1a\n') for f in ['dashboard.png','sensitivity.png']))
# This is a targeted secret-pattern scan, not an assurance about all possible secret formats.
pattern=re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
leaks=[]
for directory in ['docs','scripts','data','model','validation']:
 for p in (ROOT/directory).rglob('*'):
  if p.is_file() and p.suffix in ['.md','.csv','.py','.mjs','.json'] and pattern.search(p.read_text()):leaks.append(str(p.relative_to(ROOT)))
ck('No detected GitHub token/private-key patterns in release text',not leaks)
result={'as_of':'2026-11-17','passed':sum(c['status']=='PASS' for c in checks),'failed':sum(c['status']=='FAIL' for c in checks),'checks':checks,'publication':'Public repository created after explicit user approval; uploaded release is verified separately by its publication receipt.','repository':'herohelennn1010/renewable-energy-project-finance','limitations':['Native Microsoft Excel application opening/recalculation not independently verified.','55 model checks and 44 evidence/budget checks are reused for unchanged numerical artifacts; release checks do not independently reperform all source research.','Targeted secret scan is not exhaustive secret detection.']}
(ROOT/'validation/release_validation.json').write_text(json.dumps(result,indent=2)+'\n')
md=['# Portfolio release validation','','17 November 2026. Analysis and packaging complete. Public GitHub publication was explicitly approved by the user.','',f"**{result['passed']} release checks passed; {result['failed']} failed.** Separately, the model has 55 passing checks and the evidence/budget layer has 44.",'','| Check | Result |','| --- | --- |']+['| '+c['name']+' | '+c['status']+' |' for c in checks]+['','## Publication status','','Public repository: [renewable-energy-project-finance](https://github.com/herohelennn1010/renewable-energy-project-finance). The user explicitly approved public visibility after the initial approval block. The repository was created successfully. Remote release verification and its commit are recorded in the publication receipt distributed with the release package.','','## Review coverage','','The numerical XLSX and PDF are unchanged from the validated Phase 6 outputs. Every workbook sheet and all five PDF pages were visually reviewed during their creation. This release fixes Markdown table formatting in the editable narrative, includes its evidence notes, and adds documentation and preview images. The PDF content and financial calculations are unchanged.','','## Limitations','']+['- '+s for s in result['limitations']]+['','The rejection recommendation concerns the simulated original structure. Lifecycle reserve restructuring and a revised approvable debt size have not been validated. Real site, contract, tax and sponsor-support diligence remains outstanding.']
(ROOT/'validation/release_validation.md').write_text('\n'.join(md)+'\n')
print(f"{result['passed']} release checks passed; {result['failed']} failed.")
if broken:print('Broken links:',broken)
if result['failed']:raise SystemExit(1)
