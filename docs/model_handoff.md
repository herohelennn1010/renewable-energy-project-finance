# Phase 4 handoff

**Historical planning record from the Phase 0–3 handoff.** Phases 4–6 are now complete. For the implemented model, validation and current recommendation, read [model implementation](model_implementation.md) and [progress](progress.md). The instructions below preserve the original build specification.

Begin with the case definition, assumptions register and financing brief. Preserve the original S$100m request until the initial base case and stresses have been evaluated. No Excel model or credit decision currently exists.

1. Read the spreadsheet workflow. Build ReadMe, Sources, Assumptions and Sponsor_History, mapping stable input IDs to cells or named ranges. Preserve annual/interim and restatement warnings.
2. Build monthly construction from January 2027 through actual COD/longstop, then quarterly operation through the 25-year asset life. Separate fixed deadlines from COD-linked dates.
3. Implement capex, equity-first funding, actual interest/fees, senior commitment cap, capped GST bridge and capped completion support. Do not use budget IDC as a calculated expense or fill funding gaps automatically.
4. Implement yield, availability, curtailment and degradation. Contracted share becomes zero after 20 years. Merchant price stress must not change the fixed PPA tariff.
5. Build opex, year-12 replacement, working capital, book depreciation, tax allowances/losses, cash-tax lag and GST timing. Test the S$0.4m liquidity and S$15m GST-bridge envelopes.
6. Build baseline amortisation, ACT/365 interest and the 70% amortising hedge. Under delay, preserve final maturity and recalculate remaining repayment dates. Flag longstop waivers rather than assume them.
7. Calculate CFADS, next-two-quarter DSRA target, payment shortfalls and organic DSCR. Show cure liquidity separately. Sponsor and reserve cash never inflate CFADS.
8. Reconcile cash, debt and reserves every period. Recalculate in a supported spreadsheet engine before claiming model completion.

Candidate Phase 5 ranges, **not yet analysed or probability-calibrated**: merchant reference −30%/+20%; floating benchmark +100/+200 bp; recurring opex +10%/+20%; COD +3/+6/+12 months; yield −10%/−20%; EPC +10%/+20%. Define combined scenarios later. PPA default/repricing is a separate structural shock, not a merchant-price change applied to contracted production.

The dashboard should show commitment, actual debt, minimum DSCR and date, funding gaps, reserve adequacy and breaches. Budget leverage below 70% must never trigger an automatic approval label. Sustainable debt and the recommendation belong to Phases 5–6.
