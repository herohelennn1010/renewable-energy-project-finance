"""Meaningful consistency checks on Phase 0-3 evidence and budget, not bankability."""
from pathlib import Path
from collections import defaultdict
from datetime import date
import csv, json, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from analyse_sponsor import calculate, read_csv


def main():
    data,metrics,funding=calculate()
    checks=[]
    def check(name, condition, detail=''):
        checks.append(dict(check=name,status='PASS' if condition else 'FAIL',detail=detail))
    near=lambda a,b:abs(a-b)<0.00001
    src=read_csv('docs/source_register.csv')
    sourceids={r['source_id'] for r in src}
    inputs=read_csv('data/processed/sponsor_financial_inputs.csv')
    assumptions=read_csv('docs/assumptions_register.csv')
    ids=[r['input_id'] for r in inputs]
    aids=[r['assumption_id'] for r in assumptions]
    check('unique financial observation IDs',len(ids)==len(set(ids)))
    check('unique assumption IDs',len(aids)==len(set(aids)))
    check('all public observations have a registered source',all(r['source_id'] in sourceids for r in inputs))
    check('all public observations have a locator and unit',all(r['locator'] and r['unit'] for r in inputs))
    check('hypothetical project inputs are not labelled facts',all(r['classification']=='hypothetical_assumption' for r in assumptions))
    check('source publications are within cutoff',all(not r['publication_date'] or date.fromisoformat(r['publication_date'])<=date(2026,11,17) for r in src))
    check('hypothetical context sources exist',all(not r['context_source_id'] or all(i in sourceids for i in r['context_source_id'].split(';')) for r in assumptions))
    for period,d in data.items():
        check(period+' revenue less costs equals gross profit',near(d['revenue']-d['cost_of_sales'],d['gross_profit']))
        eb='ebitda_management' if period.startswith('FY') else 'ebitda_underlying'
        adj='adjusted_ebitda_management' if period.startswith('FY') else 'adjusted_ebitda_underlying'
        check(period+' management adjusted EBITDA identity',near(d[eb]+d['associate_jv_profit'],d[adj]))
        if 'assets' in d:
            check(period+' assets equal liabilities plus equity',near(d['assets'],d['liabilities']+d['equity']))
            check(period+' debt maturity buckets tie',near(d['debt_1to5']+d['debt_over5'],d['debt_noncurrent']))
            check(period+' balance-sheet cash at least CFS cash',d['cash_bs']>=d['cash_cfs'])
    check('no half-year annualised debt/EBITDA outputs',not any(r['period'].startswith('1H') and r['metric'].startswith('net_debt_to_management') for r in metrics))
    known_ids=set(ids)
    check('metric dependencies are valid observations',all(set(r['dependency_ids'].split(';'))<=known_ids for r in metrics))
    for row in read_csv('data/processed/restatement_bridge.csv'):
        check('restatement '+row['date']+' '+row['metric'],near(float(row['original'])+float(row['adjustment']),float(row['restated'])))
    a={r['name']:r['value'] for r in assumptions}
    check('construction spending fractions sum to one',near(sum(float(n) for n in a['construction_draw_profile'].split(';')),1))
    check('PPA plus initial merchant production shares equal one',0<=float(a['contracted_generation_share'])<=1)
    check('hedge fraction is bounded',0<=float(a['hedged_fraction'])<=1)
    fb={r['item']:r['amount_sgd'] for r in funding}
    check('permanent sources equal permanent budget uses',near(fb['senior_commitment']+fb['permanent_equity_commitment'],fb['total_permanent_uses']))
    check('requested commitment within assumed debt-to-cost ceiling',fb['senior_commitment']/fb['total_permanent_uses']<=float(a['maximum_debt_to_cost']),
          'Structural budget check only; no inference about debt capacity or approval.')
    check('fixed maturity precedes base PPA expiry',date.fromisoformat(a['fixed_maturity'])<date(2048,6,30))
    check('rights outlast base operating life',date.fromisoformat(a['site_rights_end'])>date(2053,6,30))
    result=dict(as_of='2026-11-17',scope='Phases0-3 data and budget consistency only; not source assurance or project credit approval',
                passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),checks=checks,
                disclosed_limitations=['FY2023 not recast; FY2024 restated', 'Interim statements unaudited and unreviewed',
                'No original PDF binaries or visual verification', 'Project contracts, site rights and sponsor facilities are hypothetical',
                'This evidence/budget script does not compute project DSCR; use the separate final model validation'])
    (ROOT/'validation/phase03_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print('%d checks passed; %d failed.'%(result['passed'],result['failed']))
    for c in checks:
        if c['status']=='FAIL': print('FAIL:',c['check'])
    return bool(result['failed'])


if __name__=='__main__':
    raise SystemExit(main())
