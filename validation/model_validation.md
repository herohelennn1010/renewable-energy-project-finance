# Financial model validation

**55 checks passed; 0 failed.**

Artifact Tool calculation engine, independent numeric checks and exported OpenXML. Native Microsoft Excel application recalculation not performed.

| Check | Result |
| --- | --- |
| First full operating-year generation | PASS |
| First-year contracted revenue | PASS |
| First-year merchant revenue | PASS |
| Fixed PPA expires after year 20 | PASS |
| Construction spending sums to original EPC | PASS |
| Unused contingency is not fabricated capex | PASS |
| First-quarter ACT/365 interest | PASS |
| First-quarter equal principal | PASS |
| Year-12 replacement cost independently recomputed | PASS |
| Replacement included once only | PASS |
| CFADS components quarter 1 | PASS |
| DSCR denominator quarter 1 | PASS |
| CFADS components quarter 12 | PASS |
| DSCR denominator quarter 12 | PASS |
| CFADS components quarter 48 | PASS |
| DSCR denominator quarter 48 | PASS |
| CFADS components quarter 60 | PASS |
| DSCR denominator quarter 60 | PASS |
| CFADS components quarter 81 | PASS |
| DSCR denominator quarter 81 | PASS |
| CFADS components quarter 100 | PASS |
| DSCR denominator quarter 100 | PASS |
| CFADS components quarter 101 | PASS |
| DSCR denominator quarter 101 | PASS |
| Debt fully amortised by final contractual payment | PASS |
| No floating residue creates post-maturity DSCR | PASS |
| Book value depreciates to zero | PASS |
| No final trade receivables or payables | PASS |
| Operating GST timing nets to zero after run-off | PASS |
| All-period cash roll-forward | PASS |
| Base reconciliations | PASS |
| Upside reconciliations | PASS |
| Downside reconciliations | PASS |
| Severe reconciliations | PASS |
| Base replacement breach not hidden | PASS |
| Base covenant breach distinguished from payment failure | PASS |
| Downside payment shortfall remains visible | PASS |
| Severe completion failure remains visible | PASS |
| Exported XLSX is intact | PASS |
| No cached Excel formula errors | PASS |
| Calculated formula caches are present | PASS |
| Two native What-If Data Tables exported | PASS |
| Native chart exported | PASS |
| No external workbook links | PASS |
| No embedded VBA macros | PASS |
| Iterative calculation not enabled | PASS |
| Blank unselected case does not alter base | PASS |
| Selected missing input is exposed | PASS |
| Zero senior loan makes DSCR not applicable | PASS |
| Zero generation is not replaced by a healthy base | PASS |
| Hedge reduces exposed interest increase | PASS |
| Scenario and sensitivity changes leave verified history unchanged | PASS |
| Inputs restored to the original base | PASS |
| Native price/yield table agrees with direct model recalculation | PASS |
| Native rate/opex table agrees with direct model recalculation | PASS |

## Limits

- Source facts retain the Phase 0-3 source-access and comparability limits.
- Native Excel application behavior is not independently verified.
- Post-payment-default penalty interest, acceleration and recovery are outside this model.
- Operations in a construction-funding-gap case are conditional diagnostics.
