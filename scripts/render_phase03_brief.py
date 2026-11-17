"""Render readable Phase 0-3 findings from the verified input/derived CSVs."""
from pathlib import Path
from analyse_sponsor import calculate

ROOT=Path(__file__).resolve().parents[1]


def main():
    data, calculated, funding=calculate()
    metrics={(r['period'],r['metric']):r['value'] for r in calculated}
    funds={r['item']:r['amount_sgd'] for r in funding}
    def n(value): return f'{value:,.0f}'
    def v(period,key): return data[period][key]
    def m(period,key): return metrics[(period,key)]
    years=['FY2023','FY2024','FY2025']
    def annual_input(label,key):
        return '| '+label+' | '+' | '.join(n(v(y,key)) for y in years)+' |'
    def annual_metric(label,key,unit='amount'):
        def f(x):
            return f'{100*x:.1f}%' if unit=='pct' else (f'{x:.2f}x' if unit=='times' else n(x))
        return '| '+label+' | '+' | '.join(f(m(y,key)) for y in years)+' |'
    table=['| S$ million unless a ratio | FY2023 original | FY2024 restated | FY2025 |',
           '| --- | ---: | ---: | ---: |']
    table += [annual_input(label,key) for label,key in [
        ('Revenue','revenue'),('Gross profit','gross_profit'),('Management EBITDA','ebitda_management'),
        ('Management adjusted EBITDA','adjusted_ebitda_management'),('Profit attributable to owners, total','patmi_total'),
        ('Operating cash flow','ocf')]]
    table += [annual_metric(label,key,unit) for label,key,unit in [
        ('Cash capex','cash_capex','amount'),('OCF less cash capex, before interest','ocf_less_cash_capex','amount'),
        ('Post-interest cash-surplus proxy¹','post_interest_cash_surplus_proxy','amount'),
        ('Gross borrowings, excluding leases','gross_debt_ex_leases','amount'),
        ('Net debt, excluding leases','net_debt_ex_leases','amount')]]
    table += [annual_input('Total equity','equity')]
    table += [annual_metric(label,key,unit) for label,key,unit in [
        ('Gross margin','gross_margin','pct'),
        ('Management EBITDA margin','management_ebitda_margin','pct'),
        ('Net debt / management EBITDA','net_debt_to_management_ebitda','times'),
        ('Net debt / adjusted EBITDA','net_debt_to_management_adjusted_ebitda','times'),
        ('Management EBITDA / finance costs','management_ebitda_interest_coverage','times'),
        ('P&L interest-coverage proxy²','pnl_interest_coverage_proxy','times'),
        ('Current ratio, including held for sale','current_ratio_including_held_for_sale','times')]]

    rev_change=(v('FY2025','revenue')/v('FY2024','revenue')-1)*100
    ocf_change=(v('FY2025','ocf')/v('FY2024','ocf')-1)*100
    netdebt25=m('FY2025','net_debt_ex_leases')
    netdebt26=m('1H2026','net_debt_ex_leases')
    equity=funds['permanent_equity_commitment']/1e6
    assessment=f'''# Sponsor assessment — Phase 2

**As of 17 November 2026 | Sembcorp Industries consolidated group.**

Assessment boundary: sponsor financial capacity and risks only. This is not a bank rating, a probability of default, a project debt-capacity conclusion or a lending decision. All source IDs resolve in the source register. Calculations are reproduced by the supplied Python scripts.

## Annual financial history

{chr(10).join(table)}

Sources: FY2023 observations from S02; FY2024 restated and FY2025 observations from S01. FY2023 is not recast onto the later investment-property fair-value policy. Opening 2024 restated assets/equity are separately preserved in `restatement_bridge.csv`. Cash-flow scope can include discontinued operations; revenue is continuing operations. Management EBITDA is a sourced non-GAAP measure with issuer adjustments.

¹ OCF − cash PPE/investment-property capex − cash intangible capex + cash dividends received − cash interest − lease principal. This is not company-reported FCF and excludes acquisitions, JV capital contributions, shareholder distributions and other flows. The full expression and dependency IDs are in `sponsor_metrics.csv`.

² (PBT + gross finance costs − finance income − share of associates/JV profits) / gross finance costs. It still includes non-operating items; do not label it recurring operating EBIT coverage.

## Profitability and cash generation

FY2025 revenue changed by {rev_change:.1f}% against FY2024; management EBITDA margin moved from {100*m('FY2024','management_ebitda_margin'):.1f}% to {100*m('FY2025','management_ebitda_margin'):.1f}%. Reported owner profit and non-GAAP underlying earnings should not be interchanged. The issuer attributes changes across segments to different operating conditions; its FY2025 results release discusses weaker gas earnings and contributions from renewables/urban operations [S06]. That explanation is issuer commentary, not an independent causal estimate.

OCF declined {abs(ocf_change):.1f}% in FY2025. OCF less cash capex was S${n(m('FY2025','ocf_less_cash_capex'))}m before financing interest. Including dividends received, then deducting cash interest and lease principal, leaves a narrower S${n(m('FY2025','post_interest_cash_surplus_proxy'))}m proxy before the excluded investments/distributions. Company-reported FCF is not used as a substitute for this definition. These differences matter when judging incremental equity support.

## Leverage, liquidity and refinancing

Net debt / management EBITDA rose from {m('FY2023','net_debt_to_management_ebitda'):.2f}x in FY2023 to {m('FY2025','net_debt_to_management_ebitda'):.2f}x in FY2025. Gross borrowings exclude leases; the separate lease-inclusive net-debt sensitivity is S${n(m('FY2025','lease_inclusive_net_debt'))}m. Associated/JV earnings can help group profitability while their cash distributions differ from accounting profits. Consequently adjusted EBITDA leverage and coverage deserve a cash-flow qualification.

At December 2025, borrowings due within one year were S${n(v('FY2025','debt_current'))}m; maturities in years one to five were S${n(v('FY2025','debt_1to5'))}m and beyond five years S${n(v('FY2025','debt_over5'))}m. Cash-flow-statement cash was S${n(v('FY2025','cash_cfs'))}m, compared with S${n(v('FY2025','cash_bs'))}m balance-sheet cash. The difference is pledged/restricted cash in the cash-flow reconciliation [S01].

The S${n(v('FY2025','undrawn_committed'))}m undrawn committed facility figure is dated December 2025 [S01, pp14–15]. It cannot be carried unchanged into the post-Alinta position. Uncommitted facilities and debt-programme limits are not equivalent to immediately drawable committed cash. Neither consolidated cash nor facility headroom proves funds are legally available to the parent or this SPV.

The standalone parent's disclosed cash was S${n(v('1H2026','parent_cash_bs'))}m in June 2026 versus S${n(v('FY2025','parent_cash_bs'))}m at December 2025 [S03, Company columns]. Its intra-group financial guarantees covered S${n(v('1H2026','parent_intragroup_guarantees'))}m of facilities, with S${n(v('1H2026','parent_guaranteed_debt_drawn'))}m drawn [S03, p15]. These overlap group financing and must not be added mechanically to consolidated debt. Standalone cash is a relevant constraint, but it is not an available-support certificate: other obligations, upstream distributions and facility conditions still need diligence.

## Latest interim update: acquisition changes the credit context

| S$ million | December 2025 / FY2025 | June 2026 / 1H2026 | Interpretation |
| --- | ---: | ---: | --- |
| Gross borrowings | {n(m('FY2025','gross_debt_ex_leases'))} | {n(m('1H2026','gross_debt_ex_leases'))} | Acquisition funding and consolidated acquired debt |
| Company-style net debt | {n(netdebt25)} | {n(netdebt26)} | Increase of S${n(netdebt26-netdebt25)}m |
| Balance-sheet cash | {n(v('FY2025','cash_bs'))} | {n(v('1H2026','cash_bs'))} | Not all freely upstreamable |
| Cash excluding pledged balances | {n(v('FY2025','cash_cfs'))} | {n(v('1H2026','cash_cfs'))} | Still a consolidated figure |
| Current borrowings | {n(v('FY2025','debt_current'))} | {n(v('1H2026','debt_current'))} | Other current obligations also matter |
| Total equity | {n(v('FY2025','equity'))} | {n(v('1H2026','equity'))} | Provisional acquisition accounting |

| S$ million | 1H2025 | 1H2026 |
| --- | ---: | ---: |
| Revenue | {n(v('1H2025','revenue'))} | {n(v('1H2026','revenue'))} |
| Owner profit, reported | {n(v('1H2025','patmi_total'))} | {n(v('1H2026','patmi_total'))} |
| Owner profit, underlying | {n(v('1H2025','underlying_patmi'))} | {n(v('1H2026','underlying_patmi'))} |
| Operating cash flow | {n(v('1H2025','ocf'))} | {n(v('1H2026','ocf'))} |
| OCF less cash capex, before interest | {n(m('1H2025','ocf_less_cash_capex'))} | {n(m('1H2026','ocf_less_cash_capex'))} |
| Post-interest cash-surplus proxy | {n(m('1H2025','post_interest_cash_surplus_proxy'))} | {n(m('1H2026','post_interest_cash_surplus_proxy'))} |

Sources: S03/S04. Interim figures are unaudited and unreviewed. Alinta was consolidated from 1 June for accounting purposes, while the completion announcement is dated 11 June [S03,S10]. Do not annualise one month of acquired earnings against the full acquired debt balance. S05 separately reports management annualised, underlying pro-forma net debt / adjusted EBITDA of **5.3x** and net debt / EBITDA of **6.1x**, excluding certain environmental-certificate earnings. Those are management measures, not independently reconstructed cash-capacity tests.

## Commitments and subsequent events

June 2026 maturity buckets are S${n(v('1H2026','debt_current'))}m within one year, S${n(v('1H2026','debt_1to5'))}m in years one to five and S${n(v('1H2026','debt_over5'))}m thereafter. Disclosed external financial guarantees are S${n(v('1H2026','guarantees_external'))}m after release of the former SEIL guarantees. They should not be added again to consolidated borrowings without considering scope. Parent intra-group guarantees are disclosed separately and can overlap consolidated obligations. Unprovided commitments total S${n(v('1H2026','total_commitments'))}m, including S${n(v('1H2026','capex_commitments'))}m for contracted PPE [S03, pp14–15,29].

The 28 October COD of a 600 MW plant is evidence of an operational milestone [S22], not a basis to invent post-June profit or deleveraging. Official October gas-disruption remarks describe supply mitigation at system level [S23]; company-specific earnings impact is not quantified here. The interim issuer release also identifies China curtailment/resource/tariff pressures [S07]. Treat these as risks and issuer explanations rather than assigned loss estimates.

## Implication for the hypothetical financing

The sponsor has operating scale and disclosed earnings/cash generation, but its post-acquisition leverage and competing commitments make reliance on an unspecified parent backstop inappropriate. S${equity:.0f}m of proposed permanent equity is a simulation funding requirement, not an actual demonstrated Sembcorp commitment. Additional capped support is also fictional and must be tested explicitly.

Require project CFADS, realistic offtaker/site diligence and legally documented support before a real lending conclusion. In this case study, proceed to modelling under transparent assumptions; do not infer approval or rejection from sponsor reputation, a single ratio or the balanced budget.
'''
    (ROOT/'docs/sponsor_assessment.md').write_text(assessment,encoding='utf-8')
    brief=f'''# Project B — Phase 0–3 completion brief

**17 November 2026 | Independent educational simulation**

## What is now defined

A hypothetical Singapore SPV develops **120 MWp of commercial rooftop solar**. The proposed lender is DBS; the assumed sponsor is Sembcorp. Neither company is involved in this independent case study. No actual asset, agreement or loan approval is asserted.

The planning funding envelope is **S${funds['total_permanent_uses']/1e6:.0f}m**, comprising **S${funds['senior_commitment']/1e6:.0f}m senior commitment** and **S${equity:.0f}m permanent equity**. Revenue assumes 80% contracted generation under 20-year fixed-price PPAs and 20% merchant exposure. Construction lasts 18 months; base COD is 1 July 2028. Debt amortises over 15 operating years to fixed maturity on 30 June 2043.

All project costs, tariffs, yields, timelines, counterparties and financing terms are hypothetical. Verified public sponsor data and official market observations are kept in separate datasets, linked by source IDs. The assumption register contains 70 classified inputs with rationales and relevant public context.

## Completed phases

| Phase | Delivered |
| --- | --- |
| 0 | Frozen case definition, local project folders, audit-trail registers and decision log. |
| 1 | FY2023–25 financial observations, 1H2026 update, market benchmarks, restatement bridge and source/conflict review. |
| 2 | Sponsor financial analysis with reproducible profitability, cash-flow, leverage, interest-coverage and liquidity metrics. |
| 3 | Balanced planning budget, operating assumptions, proposed loan/hedge terms, reserves, limited support and illustrative covenants. |

## Main sponsor findings

- FY2025 revenue was **S${n(v('FY2025','revenue'))}m**, with OCF of **S${n(v('FY2025','ocf'))}m** and company-style net debt of **S${n(netdebt25)}m** [S01].
- Annual net debt / management EBITDA was **{m('FY2025','net_debt_to_management_ebitda'):.2f}x**. OCF less cash capex was **S${n(m('FY2025','ocf_less_cash_capex'))}m before cash interest**; it is not the company's reported FCF measure.
- June 2026 net debt reached **S${n(netdebt26)}m** following the acquisition and consolidation of Alinta. Interim OCF was **S${n(v('1H2026','ocf'))}m**, versus **S${n(v('1H2025','ocf'))}m** in 1H2025 [S03/S04].
- Parent support capacity is not established merely by consolidated cash, group size or earnings. The proposed equity and capped facilities remain explicit simulation assumptions.

These are sponsor findings, not a project credit decision. The detailed assessment explains scope, adjustments and cash-flow definitions.

## Material limits retained

FY2023 is not recast; FY2024 is restated. Interim statements are unaudited and unreviewed. June debt and acquired earnings have different consolidation exposure, so reported half-year EBITDA is not simply annualised. Conflicting source observations are quarantined. No site-level resource report, actual PPAs, cost quotes, legal rights, tax opinion or sponsor commitment exists. Public PDF text was inspected, but no original PDF binaries or visual source assurance are included.

## Next phase

Build the linked Excel base case using the handoff instructions, then test actual funding needs, DSCR and stresses. **No project DSCR, sustainable debt amount, valuation, final loan recommendation or memo PDF has been produced.** A balanced planning budget does not establish bankability.

Start with [the project README](../README.md), [sponsor assessment](sponsor_assessment.md), [financing brief](financing_structure.md) and [Phase 4 handoff](model_handoff.md).
'''
    (ROOT/'docs/PHASE_0_3_BRIEF.md').write_text(brief,encoding='utf-8')
    print('Rendered sponsor assessment and Phase 0-3 brief.')


if __name__=='__main__':
    main()
