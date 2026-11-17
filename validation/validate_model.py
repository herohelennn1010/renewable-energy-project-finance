"""Independent numerical checks and exported XLSX feature/cached-value inspection."""
from pathlib import Path
import json,csv,math,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def main():
 b=json.loads((ROOT/'model/base_values.json').read_text())
 cases=json.loads((ROOT/'model/scenario_results.json').read_text())
 with (ROOT/'docs/assumptions_register.csv').open(newline='') as f:a={r['name']:r['value'] for r in csv.DictReader(f)}
 def v(n):return float(a[n])
 def c(n):
  s=''
  while n:n,k=divmod(n-1,26);s=chr(65+k)+s
  return s
 def x(s,r,q):return b[s][c(q+4)+str(r)]
 checks=[]
 def check(name,ok,detail=''):
  checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
 def near(x,y,tol=.01):return abs(x-y)<=tol
 # Generation and prices computed directly from physical inputs, independent of cell formulas.
 generation=v('dc_capacity_mwp')*v('specific_yield')*v('availability')*(1-v('curtailment'))
 check('First full operating-year generation',near(sum(x('Operations',20,q) for q in range(1,5)),generation))
 ppa=generation*v('contracted_generation_share')*v('PPA_price')
 merchant=generation*(1-v('contracted_generation_share'))*v('merchant_reference')*v('merchant_capture_factor')
 check('First-year contracted revenue',near(sum(x('Operations',24,q) for q in range(1,5)),ppa))
 check('First-year merchant revenue',near(sum(x('Operations',28,q) for q in range(1,5)),merchant))
 check('Fixed PPA expires after year 20',x('Operations',22,80)==.8 and x('Operations',22,81)==0)
 check('Construction spending sums to original EPC',near(sum(b['Construction'][c(i+4)+'24'] for i in range(1,37)),132e6))
 check('Unused contingency is not fabricated capex',near(sum(b['Construction'][c(i+4)+'24'] for i in range(1,37)),v('dc_capacity_mwp')*1000*v('EPC_cost_per_kwp')))
 # Independent interest and CFADS spot checks, including the exceptional quarter.
 debt=cases[0]['Actual debt drawn at COD']
 first_interest=debt*(v('benchmark_assumed')+v('margin'))*92/365
 check('First-quarter ACT/365 interest',near(x('Debt',17,1),first_interest))
 check('First-quarter equal principal',near(x('Debt',14,1),debt/60))
 replacement=132e6*v('replacement_cost_fraction')*(1+v('annual_escalation'))**(v('replacement_operating_year')-1)
 check('Year-12 replacement cost independently recomputed',near(x('Operations',39,48),replacement))
 check('Replacement included once only',near(sum(x('Operations',39,q) for q in range(1,102)),replacement))
 for q in [1,12,48,60,81,100,101]:
  cfads=x('Operations',37,q)-x('Operations',49,q)-x('Operations',46,q)-x('Operations',41,q)+x('Operations',48,q)
  check(f'CFADS components quarter {q}',near(x('Operations',50,q),cfads))
  ds=x('Debt',18,q)
  check(f'DSCR denominator quarter {q}',near(x('Operations',52,q),cfads/ds,1e-8) if ds>0 else x('Operations',52,q)=='n.a.')
 check('Debt fully amortised by final contractual payment',near(x('Debt',19,60),0) and near(sum(x('Debt',14,q) for q in range(1,102)),debt))
 check('No floating residue creates post-maturity DSCR',all(x('Operations',52,q)=='n.a.' for q in range(61,102)))
 check('Book value depreciates to zero',near(x('Tax',14,100),0))
 check('No final trade receivables or payables',near(x('Operations',43,101),0) and near(x('Operations',44,101),0))
 check('Operating GST timing nets to zero after run-off',near(sum(x('Operations',48,q) for q in range(1,102)),0))
 for q in range(1,102):
  cash=x('Cash_Flow',10,q)+x('Operations',50,q)+x('Cash_Flow',19,q)+x('Cash_Flow',20,q)+x('Cash_Flow',30,q)-x('Cash_Flow',21,q)-x('Cash_Flow',29,q)-x('Cash_Flow',34,q)
  if not near(cash,x('Cash_Flow',35,q)):check('All-period cash roll-forward',False,f'Quarter {q}');break
 else:check('All-period cash roll-forward',True)
 for case in cases:
  check(case['case']+' reconciliations',all(isinstance(z,(int,float)) and abs(z)<.01 for z in case['checks']))
 check('Base replacement breach not hidden',cases[0]['Minimum quarterly organic DSCR']<0 and cases[0]['Quarters below covenant']==1)
 check('Base covenant breach distinguished from payment failure',cases[0]['Peak unpaid debt service']==0)
 check('Downside payment shortfall remains visible',cases[2]['Peak unpaid debt service']>0)
 check('Severe completion failure remains visible',cases[3]['Peak construction funding gap']>0 and cases[3]['COD beyond construction longstop']==1)
 # Check actual OpenXML: formulas, cached results, native tables, chart bindings and no external links.
 ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
 with zipfile.ZipFile(ROOT/'model/renewable_project_finance.xlsx') as z:
  names=z.namelist();xmls=[n for n in names if n.startswith('xl/worksheets/sheet') and n.endswith('.xml')]
  check('Exported XLSX is intact',z.testzip() is None)
  dt=[];formula_errors=[];cached=0
  for name in xmls:
   tree=ET.fromstring(z.read(name))
   for cell in tree.findall('.//m:c',ns):
    formula=cell.find('m:f',ns);value=cell.find('m:v',ns)
    if formula is not None and value is not None:cached+=1
    if cell.attrib.get('t')=='e':formula_errors.append((name,cell.attrib['r'],value.text if value is not None else None))
    if formula is not None and formula.attrib.get('t')=='dataTable':dt.append(formula.attrib)
  check('No cached Excel formula errors',not formula_errors,str(formula_errors[:5]))
  check('Calculated formula caches are present',cached>0,'Saved results available without first recalculation.')
  check('Two native What-If Data Tables exported',len(dt)==2,str(dt))
  check('Native chart exported',any('/charts/chart' in n and n.endswith('.xml') for n in names))
  check('No external workbook links',not any(n.startswith('xl/externalLinks/') for n in names))
  check('No embedded VBA macros',not any(n.endswith('vbaProject.bin') for n in names))
  wb=ET.fromstring(z.read('xl/workbook.xml'));calc=wb.find('m:calcPr',ns)
  check('Iterative calculation not enabled',calc is None or calc.attrib.get('iterate','0') in ['0','false'])
 engine=json.loads((ROOT/'validation/engine_tests.json').read_text())
 checks.extend(engine)
 result={'as_of':'2026-11-17','passed':sum(x['status']=='PASS' for x in checks),'failed':sum(x['status']=='FAIL' for x in checks),'checks':checks,'coverage':'Artifact Tool calculation engine, independent numeric checks and exported OpenXML. Native Microsoft Excel application recalculation not performed.','limitations':['Source facts retain the Phase 0-3 source-access and comparability limits.','Native Excel application behavior is not independently verified.','Post-payment-default penalty interest, acceleration and recovery are outside this model.','Operations in a construction-funding-gap case are conditional diagnostics.']}
 (ROOT/'validation/model_validation.json').write_text(json.dumps(result,indent=2)+'\n')
 md=['# Financial model validation','',f'**{result["passed"]} checks passed; {result["failed"]} failed.**','',result['coverage'],'','| Check | Result |','| --- | --- |']+['| '+r['name']+' | '+r['status']+' |' for r in checks]+['','## Limits','']+['- '+s for s in result['limitations']]
 (ROOT/'validation/model_validation.md').write_text('\n'.join(md)+'\n')
 print(f'{result["passed"]} passed; {result["failed"]} failed.')
 for r in checks:
  if r['status']=='FAIL':print('FAIL:',r['name'],r.get('detail',''))
 if result['failed']:raise SystemExit(1)
if __name__=='__main__':main()
