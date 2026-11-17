"""Reproduce Phase 2 sponsor calculations and Phase 3 funding-budget arithmetic.

No project cash-flow forecast, bank rating, probability of default, or loan decision.
Python 3.9+; standard library only. Inputs: positive expense/capex magnitudes, SGDm.
"""
from pathlib import Path
from collections import defaultdict
import csv

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with (ROOT / path).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    with (ROOT / path).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def calculate():
    observations = read_csv('data/processed/sponsor_financial_inputs.csv')
    data = defaultdict(dict)
    for row in observations:
        data[row['period']][row['metric']] = float(row['value'])
    results = []

    def put(period, metric, value, unit, expression, dependencies, limitation=''):
        results.append(dict(period=period, metric=metric, value=round(value, 8),
                            unit=unit, classification='derived_calculation',
                            expression=expression,
                            dependency_ids=';'.join('F_'+period+'_'+d for d in dependencies),
                            limitation=limitation))

    for period, d in data.items():
        def p(metric, value, unit, expr, deps, note=''):
            put(period, metric, value, unit, expr, deps, note)

        p('gross_margin', d['gross_profit']/d['revenue'], 'fraction',
          'gross_profit/revenue', ['gross_profit', 'revenue'])
        p('patmi_total_margin', d['patmi_total']/d['revenue'], 'fraction',
          'patmi_total/revenue', ['patmi_total', 'revenue'],
          'Total PATMI may include discontinued operations; revenue is continuing operations.')
        p('pre_finance_profit_excluding_equity_accounted',
          d['pbt']+d['finance_cost']-d['finance_income']-d['associate_jv_profit'],
          'SGD million', 'pbt+finance_cost-finance_income-associate_jv_profit',
          ['pbt','finance_cost','finance_income','associate_jv_profit'],
          'P&L proxy; still includes non-operating items; not recurring operating EBIT.')
        p('pnl_interest_coverage_proxy',
          (d['pbt']+d['finance_cost']-d['finance_income']-d['associate_jv_profit'])/d['finance_cost'],
          'times', '(pbt+finance_cost-finance_income-associate_jv_profit)/finance_cost',
          ['pbt','finance_cost','finance_income','associate_jv_profit'],
          'Non-operating items remain; gross finance costs include more than bank-loan interest.')
        cashcapex = d['ppe_ip_cashcapex']+d['intangible_cashcapex']
        p('cash_capex', cashcapex, 'SGD million',
          'ppe_ip_cashcapex+intangible_cashcapex', ['ppe_ip_cashcapex','intangible_cashcapex'])
        pre = d['ocf']-cashcapex
        p('ocf_less_cash_capex', pre, 'SGD million',
          'ocf-ppe_ip_cashcapex-intangible_cashcapex',
          ['ocf','ppe_ip_cashcapex','intangible_cashcapex'],
          'Before cash interest; excludes acquisitions, equity investments, dividends received and other investing flows.')
        post = pre+d['dividends_received']-d['interest_paid']-d['lease_principal_paid']
        p('post_interest_cash_surplus_proxy', post, 'SGD million',
          'ocf-ppe_ip_cashcapex-intangible_cashcapex+dividends_received-interest_paid-lease_principal_paid',
          ['ocf','ppe_ip_cashcapex','intangible_cashcapex','dividends_received','interest_paid','lease_principal_paid'],
          'Not company FCF; excludes acquisitions, equity investments, shareholder distributions and other investing/financing flows.')
        eb = 'ebitda_management' if period.startswith('FY') else 'ebitda_underlying'
        adj = 'adjusted_ebitda_management' if period.startswith('FY') else 'adjusted_ebitda_underlying'
        p('management_ebitda_margin', d[eb]/d['revenue'], 'fraction', eb+'/revenue',
          [eb,'revenue'], 'Management non-GAAP basis; interim underlying earnings are separately labelled.')
        p('management_ebitda_interest_coverage', d[eb]/d['finance_cost'], 'times',
          eb+'/finance_cost', [eb,'finance_cost'], 'Not project DSCR or cash interest coverage.')
        p('management_adjusted_ebitda_interest_coverage', d[adj]/d['finance_cost'], 'times',
          adj+'/finance_cost', [adj,'finance_cost'], 'Includes equity-accounted profits, which are not equivalent to dividends received.')

        if 'assets' not in d:
            continue
        grossdebt=d['debt_current']+d['debt_noncurrent']
        netdebt=grossdebt-d['cash_bs']
        leases=d['lease_current']+d['lease_noncurrent']
        p('gross_debt_ex_leases',grossdebt,'SGD million',
          'debt_current+debt_noncurrent',['debt_current','debt_noncurrent'])
        p('net_debt_ex_leases',netdebt,'SGD million',
          'debt_current+debt_noncurrent-cash_bs',['debt_current','debt_noncurrent','cash_bs'],
          'Subtracts balance-sheet cash, including pledged cash; does not establish upstreamability.')
        p('cash_excluded_from_cfs',d['cash_bs']-d['cash_cfs'],'SGD million',
          'cash_bs-cash_cfs',['cash_bs','cash_cfs'],
          'Pledged/restricted-cash reconciliation; cash_cfs is not necessarily freely distributable parent cash.')
        p('net_debt_less_cfs_cash',grossdebt-d['cash_cfs'],'SGD million',
          'debt_current+debt_noncurrent-cash_cfs',['debt_current','debt_noncurrent','cash_cfs'])
        p('lease_liabilities',leases,'SGD million',
          'lease_current+lease_noncurrent',['lease_current','lease_noncurrent'])
        p('lease_inclusive_net_debt',netdebt+leases,'SGD million',
          'debt_current+debt_noncurrent+lease_current+lease_noncurrent-cash_bs',
          ['debt_current','debt_noncurrent','lease_current','lease_noncurrent','cash_bs'],
          'Definition sensitivity only; EBITDA has not been recast for IFRS16.')
        p('debt_to_equity',grossdebt/d['equity'],'times',
          '(debt_current+debt_noncurrent)/equity',['debt_current','debt_noncurrent','equity'])
        p('gross_debt_to_capital',grossdebt/(grossdebt+d['equity']),'fraction',
          '(debt_current+debt_noncurrent)/(debt_current+debt_noncurrent+equity)',
          ['debt_current','debt_noncurrent','equity'])
        p('cash_to_current_borrowings',d['cash_cfs']/d['debt_current'],'times',
          'cash_cfs/debt_current',['cash_cfs','debt_current'],
          'Not total short-term obligations coverage; consolidated cash may be trapped.')
        p('current_ratio_including_held_for_sale',
          (d['current_assets']+d['assets_held_for_sale'])/(d['current_liabilities']+d['liabilities_held_for_sale']),
          'times','(current_assets+assets_held_for_sale)/(current_liabilities+liabilities_held_for_sale)',
          ['current_assets','assets_held_for_sale','current_liabilities','liabilities_held_for_sale'])
        if period.startswith('FY'):
            p('net_debt_to_management_ebitda',netdebt/d[eb],'times',
              '(debt_current+debt_noncurrent-cash_bs)/'+eb,
              ['debt_current','debt_noncurrent','cash_bs',eb])
            p('net_debt_to_management_adjusted_ebitda',netdebt/d[adj],'times',
              '(debt_current+debt_noncurrent-cash_bs)/'+adj,
              ['debt_current','debt_noncurrent','cash_bs',adj])
        # Do not annualise 1H2026 EBITDA: only one month of Alinta is consolidated.
    write_csv('data/processed/sponsor_metrics.csv',results)

    a={r['name']:r for r in read_csv('docs/assumptions_register.csv')}
    def v(name): return float(a[name]['value'])
    funding=[]
    def use(item, amount, expr, ids):
        funding.append(dict(item=item,amount_sgd=round(amount,2),classification='derived_calculation',
                            expression=expr,dependency_ids=ids,scope='planning envelope, not forecast actuals'))
    epc=v('dc_capacity_mwp')*1000*v('EPC_cost_per_kwp')
    use('EPC',epc,'dc_capacity_mwp*1000*EPC_cost_per_kwp','A001;A024')
    use('contingency',epc*v('contingency_fraction'),'EPC*contingency_fraction','A001;A024;A025')
    use('development',v('development_cost'),'development_cost','A026')
    use('upfront_fee',v('loan_commitment')*v('upfront_fee'),'loan_commitment*upfront_fee','A049;A028')
    for item,key,aid in [('IDC_envelope','IDC_budget','A029'),('liquidity_envelope','initial_liquidity_budget','A030'),('reserve_envelope','DSRA_budget','A031')]:
        use(item,v(key),key,aid)
    total=sum(r['amount_sgd'] for r in funding)
    use('total_permanent_uses',total,'SUM(permanent use rows)','A001;A024;A025;A026;A028;A029;A030;A031;A049')
    use('senior_commitment',v('loan_commitment'),'loan_commitment','A049')
    use('permanent_equity_commitment',total-v('loan_commitment'),'total_permanent_uses-senior_commitment',
        'A001;A024;A025;A026;A028;A029;A030;A031;A049')
    write_csv('data/processed/funding_budget.csv',funding)
    return data, results, funding


if __name__=='__main__':
    d, r, f=calculate()
    print('Recalculated %d sponsor metrics and %d funding-budget lines.'%(len(r),len(f)))
