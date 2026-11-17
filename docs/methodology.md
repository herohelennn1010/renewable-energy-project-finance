# Methodology and calculation contract

## Provenance

Each financial observation has an F_ID, source/page, period, unit, cutoff and classification. Project inputs have A_IDs and remain hypothetical even when informed by a verified B_ID benchmark. Source IDs map to the source register. Derived outputs retain expressions and dependency IDs. The future workbook must calculate outputs from central inputs rather than hardcode ratios or conclusions.

## Sponsor calculations

Financial inputs are SGD million; expenses and capex are positive magnitudes. Gross margin = gross profit / revenue. Management EBITDA is a sourced non-GAAP measure with issuer exclusions, not cash profit. Adjusted EBITDA adds the disclosed share of associates/JV profits, which is not equivalent to cash dividends.

Gross debt = current + non-current borrowings, excluding leases. Company-style net debt subtracts balance-sheet cash, including pledged balances. A second proxy subtracts only cash-flow-statement cash excluding pledged balances; that still does not establish free parent cash or upstreamability. Lease-inclusive net debt adds separately disclosed leases, without pretending EBITDA has been recast for IFRS 16.

Annual net debt / EBITDA uses annual issuer measures. EBITDA / gross finance costs and adjusted EBITDA / gross finance costs are separate ratios. The P&L coverage proxy is **(PBT + finance costs − finance income − associate/JV profit) / finance costs**. It excludes equity-accounted profit but can retain non-operating items; do not label it recurring operating EBIT coverage.

**OCF less cash capex** subtracts cash PPE/investment-property and intangible purchases. Because interest is classified in financing, this is before cash interest. A supplementary post-interest cash-surplus proxy adds cash dividends received, then deducts cash interest and lease principal. It still excludes acquisitions, equity investments, owner distributions and other flows. Neither proxy is company-reported FCF or the change in cash. Do not deduct financing interest twice.

Current ratio includes separately displayed held-for-sale assets and liabilities on both sides. Cash / current borrowings is a limited liquidity indicator; it excludes other near-term obligations. FY2023 is not recast; FY2024 is restated. Cash-flow scope may include discontinued operations while revenue is continuing operations.

Compare interim flows half-year against half-year. June 2026 debt includes full Alinta consolidation, while reported interim earnings include one acquisition month. Do not annualise that reported half-year earnings base to assess leverage. Management's annualised underlying pro-forma ratios from S05 are separately labelled and retain their exclusions.

## Future project model

Production MWh = DC MWp × 1,000 × specific yield / 1,000 × period-year fraction × degradation, followed by availability and curtailment once. Contracted revenue uses metered generation, contracted share and PPA tariff; merchant revenue uses the remaining generation, reference price and capture factor. Explicitly distinguish SGD/MWh from SGD/kWh.

EBITDA = revenue − cash operating costs. Taxable profit deducts assumed eligible capital allowances and interest rather than book depreciation. Maintain separate tax-loss, cash-tax-lag and GST schedules; do not create cash refunds for losses. Future rates and project-specific eligibility remain assumptions.

**CFADS = EBITDA − cash income tax − increase in operating working capital − maintenance/replacement capex**, with operating GST timing explicitly reconciled. Construction capex, debt/equity inflows and reserve movements are outside CFADS. DSCR divides CFADS by scheduled principal plus net cash interest, including normal hedge settlements. Reserve funding and discretionary sweeps are excluded from that denominator. Periods without debt service are N/A. Minimum DSCR uses actual service quarters.

LTV remains N/A without a defensible independent valuation. Commitment / permanent funded cost is a structural construction check; it differs from outstanding debt. LLCR is optional for a later phase and needs an explicit discount rate and cash scope.

For monthly construction interest, use opening debt plus half of current-month drawings under a stated mid-month assumption. Pay actual interest through the funding schedule and disclose deficits rather than use unexplained iteration or force debt beyond commitment. During operation, use opening debt until quarter-end principal repayment, with ACT/365. Reconcile actual IDC, reserve and working-capital needs to planning envelopes.

## Validation scope

The supplied scripts reproduce sponsor metrics and the Phase 3 planning budget. Checks cover identifiers, sources, historical identities, maturity buckets, restatement bridges, classification and budget arithmetic. They do not establish bankability, verify legal conditions or test workbook formulas that do not yet exist.

## Implemented model and validation

Phases 4-6 are complete. The future-model section above records the original design contract; resolved implementation choices and scope limits are in `model_implementation.md`. The workbook is the calculation authority for project results. The original Phase 0-3 Python checks remain historical input checks; current project validation is in `validation/model_validation.md`.
