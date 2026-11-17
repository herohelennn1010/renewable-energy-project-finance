# Model implementation and additional controls

Completed 17 November 2026. The Phase 3 assumption register is preserved as the original design. Additional workbook controls and choices below are hypothetical, not public project facts.

| Control | Interpretation |
| --- | --- |
| Assumptions E4 | One case selector: Base, Upside, Downside, Severe. |
| Assumptions E81 | Fixed S$53m permanent equity. No automatic stress-case equity plug. |
| Assumptions E82 | Capped hypothetical construction support enabled. |
| Assumptions E83 | Operating cures disabled by default; S$10m capacity is not automatically drawn. |
| Sensitivity E4:E7 | Neutral price/yield multipliers 1/1, rate shock 0, opex multiplier 1. |
| Assumptions E90:I95 | Active selection and original case drivers. |
| Assumptions E100:E105 | Numeric decomposition of the original construction-stage profile. |

## Model mechanics

- Contingency is a budget envelope, not automatic spending. Base EPC spend is S$132m. Stress changes actual cost; unused commitment is not forced into cash.
- Current-month drawings, half-draw construction interest, undrawn fees and initial DSRA funding are solved algebraically. Debt/availability and sponsor-support caps apply; residual gaps remain visible. Iteration is not enabled.
- Monthly construction ends before actual COD. A six-month delay gives 1 January 2029, just beyond the fixed 31 December 2028 COD longstop, requiring a waiver. Delays do not automatically extend maturity.
- Generation is weighted by days in the actual operating year, then separately adjusted for availability, curtailment and degradation. A full operating year ties to the assumed electrical yield.
- Rate shocks affect all construction debt and the unhedged 30% after COD. The swap strike and margin stay unchanged.
- Final contractual principal clears numerical residuals. Scheduled DSCR is N/A after maturity; actual principal and interest arrears stay separately visible.
- Operating GST follows cash trade collections/payments and lagged accrual settlement. One run-off quarter settles final trades/tax/GST. Construction GST uses a separately capped, assumed interest-free sponsor bridge.
- Original EPC and replacement equipment are assumed eligible for three-year tax allowances. No invented allowance is assigned to development, fees or IDC. Book depreciation is separate. Real project tax eligibility remains unverified.
- CFADS deducts replacement and decommissioning costs. Reserve movements and sponsor injections are financing, never CFADS.
- Distribution lockups reflect trailing/forward DSCR, arrears, reserve deficits and unresolved completion gaps. Retained cash can reduce payment failures without curing an organic covenant breach.
- Following a missed payment, interest remains on the contractual forecast path. Arrears and actual principal are tracked, but penalty interest, acceleration, enforcement and recoveries are outside scope. This is not a default-workout model.

## Deterministic scenarios

| Driver | Base | Upside | Downside | Severe |
| --- | ---: | ---: | ---: | ---: |
| Merchant reference multiplier | 1.00 | 1.20 | 0.70 | 0.60 |
| Generation multiplier | 1.00 | 1.05 | 0.90 | 0.80 |
| Benchmark change | 0 bp | -50 bp | +100 bp | +200 bp |
| Recurring opex multiplier | 1.00 | 0.95 | 1.10 | 1.20 |
| EPC multiplier | 1.00 | 0.95 | 1.10 | 1.20 |
| Delay | 0 months | 0 months | 3 months | 6 months |

Memo/CSV comparisons come from recalculating the same workbook and restoring Base. They are saved analytical outputs, not hardcoded forecast results. Re-run the builder or recalculate/export each case to refresh those external comparison files after changing inputs.

Native sensitivities change actual price/yield and rate/opex model inputs. They display minimum DSCR excluding replacement so ordinary headroom is readable; the full minimum remains on Dashboard. Representative non-base table points were checked against direct model recalculation.

## Sizing and interpretation limits

The full covenant fails in Base. With a negative numerator, a higher interest denominator can make DSCR less negative; that does not establish lower risk. Assess ordinary coverage, payment shortfalls, reserves and construction funding together.

Severe operations are conditional on completion despite its funding gap and missed longstop. Blocked distributions retain more cash, so zero conditional arrears does not make it safer than Downside.

`breakpoints.json` separates ordinary-quarter coverage limits, the already-failing full covenant and a locally bracketed payment-failure threshold. The latter is not a global monotonic boundary because retention policy is piecewise. A downside equity/debt diagnostic reaches 1.20x outside replacement but still has a full breach and temporary arrears. It is not an approvable debt capacity estimate. No independent valuation or LTV is produced.

The 36-month construction and 101-quarter operating grids cover the original horizon and tested delays. Asset life beyond 25 years or delays beyond 18 months require extending the grids. No probability is assigned to scenarios or deterministic breakpoints.
