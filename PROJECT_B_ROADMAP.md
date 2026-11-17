# Project B — Renewable Energy Project Finance & Credit Assessment

Agent execution roadmap | Created: 17 November 2026 | Updated: 17 November 2026 | Status: Phases 0–7 complete; verification limits disclosed

## 1. Mandate and stopping point

Prepare a portfolio-ready independent case study assessing whether a hypothetical DBS lender should extend a S$100 million project-finance facility to a hypothetical solar project sponsored by Sembcorp Industries.

Final deliverables:

1. An auditable Excel model with linked sponsor analysis, project forecasts, debt schedules, credit metrics, scenarios and sensitivities.
2. A 3–5-page PDF credit committee memo, supported by model outputs and referenced public evidence.
3. A GitHub repository containing documentation, source references, assumptions, methodology, reproducible calculation/validation materials and final deliverables.

**Current authorization: complete Phases 0–7.** Research, sponsor assessment, the linked Excel model, scenarios/sensitivities and the five-page credit memo are complete. The simulated recommendation is to decline the request as currently structured, with a documented restructuring path. Calculation and export checks are complete; native Excel application recalculation was not independently verified. Public visibility was subsequently explicitly approved by the user. Repository: https://github.com/herohelennn1010/renewable-energy-project-finance. The release commit and remote content verification are recorded in `validation/publication_receipt.json`. The final receipt commit is identified by the repository history. See `docs/progress.md` and the validation reports.

Label the final case prominently: independent educational simulation; no affiliation with, endorsement by, or access to confidential information from DBS or Sembcorp. Do not imply an actual financing transaction or actual bank policy.

## 2. Decisions to settle before calculations

Record these in `docs/case_definition.md` at the start of execution:

| Decision | Working direction / question to resolve |
| --- | --- |
| Borrower | Hypothetical ring-fenced project SPV; Sembcorp is the sponsor, not automatically the borrower or guarantor. |
| Location and asset | Start by testing a Singapore solar case for plausibility; choose a defined utility-scale or aggregated rooftop portfolio. Validate the scale required by a S$100m facility. If another location is materially more credible, document the choice and its currency/regulatory implications. |
| Facility amount | S$100m requested commitment. Separate commitment, actual drawings, debt outstanding and sustainable debt capacity. Do not force the project to support the request. |
| Revenue structure | Specify contracted PPA, merchant exposure or a mixture; define offtaker, tenor and pricing assumptions. A merchant-price stress must affect only exposed revenue. |
| Recourse | Define construction support, cost-overrun funding and post-completion recourse. Sponsor strength alone does not create legally committed support. |
| Time horizon | Cover development/construction, operation, full debt maturity and any relevant remaining contracted life. Include a debt tail. |
| Granularity | Prefer monthly construction and quarterly debt service; annual presentation summaries. Match forecast and DSCR periods to actual assumed payment dates. |
| Information cutoff | Freeze an explicit as-of date before collection. Use only information published by that date and distinguish publication dates from financial periods. |
| Accounting and funding | Set reporting currency, treatment of leases, taxes, depreciation, working capital, reserves, fees, construction interest and funding order. |

**Gate:** A coherent case definition exists before numerical assumptions are selected. Any unresolved choice has a documented provisional assumption and impact.

## 3. Execution phases and completion gates

### Phase 0 — Set up the case and audit trail

- Create the repository structure proposed below, initially local.
- Write the case definition and an issues/decisions log.
- Set up a source register and assumption register before entering numbers.
- Classify each input as **verified public fact**, **hypothetical assumption**, or **derived calculation**. Separately record confidence and verification status.
- For each input retain ID, value, unit, currency, financial period, as-of date, source/page/table, extraction notes, rationale, workbook location and applicable scenario.
- Maintain a progress log: completed work, exact artifact versions, unresolved items and next executable task.

**Gate:** Every material number will have a defined evidence or assumption trail; no financial conclusion has been selected in advance.

### Phase 1 — Collect and verify public evidence

- Obtain the latest available audited Sembcorp annual report as of the cutoff, plus enough earlier reports for a consistent three-year history. Add subsequent interim results and material announcements available by that date, separately labelled.
- Research the issuer's official investor-relations materials, SGX filings, and relevant official Singapore energy-market statistics, regulations and solar information. Prefer primary sources; browse and verify during this phase.
- Gather evidence relevant to solar scale, generation, pricing structures, operating costs and financing assumptions. Public market data can inform a hypothetical project without establishing its actual economics.
- Record original versus restated comparatives; use consistent reporting scope and flag discontinued operations, disposals and material accounting changes.
- Cross-check material extracted financial figures against the statements and notes. Preserve source links, publication/access dates, page references and permitted source copies.
- Treat unavailable information as unavailable. Explain and label any proxy; do not silently fill gaps.

**Gate:** All historical financial inputs are traceable and reconciled; hypothetical project inputs are visibly distinct from reported company data.

### Phase 2 — Assess the sponsor

- Analyse revenue, operating profitability, net profit, operating cash flow, capex, free cash flow, liquidity, borrowings, cash, net debt and maturity profile.
- Calculate relevant leverage and interest-coverage measures with explicit definitions and reconciliations. Distinguish reported measures from independently calculated measures.
- Review refinancing exposure, contingent commitments, guarantees and disclosed project-level/non-recourse debt where available.
- Explain material changes using disclosures. Do not attribute causes without evidence.
- Assess the sponsor's capacity to contribute equity and provide the specific support assumed in this case, while acknowledging limits of consolidated information.

**Gate:** A standalone sponsor assessment exists, with transparent adjustments. It does not substitute consolidated sponsor cash flow for project debt-service capacity.

### Phase 3 — Establish project assumptions and financing structure

- Define capacity, construction milestones, commercial operation date (COD), asset life, land/roof rights and relevant permissions.
- Set generation assumptions: capacity units, resource/yield, losses, availability, degradation and curtailment. Prevent double-counting losses or availability adjustments.
- Set PPA/merchant assumptions, escalation, offtaker payment timing and contract expiry.
- Define capex components, contingency, construction interest, fees, initial working capital and debt-service reserve funding.
- Specify opex, maintenance/replacement spending, insurance, taxes and working capital.
- Propose equity contributions, drawdown order, floating benchmark plus margin, hedging assumptions, repayment tenor, grace period, reserve requirements and distribution controls.
- Establish hypothetical covenant thresholds with rationale. Do not describe them as DBS requirements or market standards without evidence.
- Choose a simple scheduled-amortisation baseline. Consider debt sculpting only as an explicit extension with a documented, reproducible solution to circularity.

**Gate:** Sources equal uses in the proposed funding structure; assumptions are internally consistent and sufficiently supported for a simulation. An unsupported funding gap remains visible.

### Phase 4 — Build the Excel model

Suggested workbook architecture:

| Sheet | Purpose |
| --- | --- |
| `ReadMe` | Scope, simulation disclosure, conventions, navigation and calculation instructions. |
| `Sources` | Public evidence register with source IDs and references. |
| `Assumptions` | Centralised inputs with units, status, rationale and source/assumption IDs. |
| `Sponsor_History` | Verified historical figures and formula-driven sponsor ratios. |
| `Timeline` | Period lengths, construction/COD flags, operating years and debt-service dates. |
| `Construction` | Capex timing, funding uses, equity/debt draws, fees and construction interest. |
| `Operations` | Generation, contracted/merchant revenue, operating costs and working capital. |
| `Tax` | Depreciation, taxable profit, losses and cash taxes under stated assumptions. |
| `Cash_Flow` | Project cash flow, CFADS, reserves, distributions and funding shortfalls. |
| `Debt` | Drawdowns, interest, scheduled repayments, optional sweeps and debt balances. |
| `Credit_Metrics` | Project and sponsor metrics, covenant tests and headroom. |
| `Scenarios` | Central scenario assumptions and comparable outcome tables. |
| `Sensitivity` | One-/two-variable sensitivities and break-even calculations. |
| `Dashboard` | Selected outputs and charts linked to calculation sheets. |
| `Checks` | Reconciliations, errors, missing evidence and completion status. |

Model rules:

- Hardcode only clearly identified input assumptions and verified source data; all calculated outputs use formulas. Avoid embedded numerical assumptions in formulas.
- Use consistent input/formula/reference styling, units, signs and dates. Do not rely on colour alone to identify input status.
- Separate construction from operation; link COD-dependent timing rather than merely changing one delay input.
- Define CFADS explicitly and reconcile it to project cash flow. Exclude financing inflows and prevent interest/principal being deducted twice.
- Reconcile beginning debt + drawings − principal = ending debt, including any explicitly capitalised interest consistently.
- Show reserves, funding shortfalls, unpaid debt service and covenant breaches explicitly. Never manufacture balancing equity or hide deficits with zero floors.
- Avoid external workbook dependencies, unnecessary macros and unexplained iterative calculation. Document any circularity treatment.
- Recalculate in a spreadsheet engine, save usable cached results and check the workbook in Excel where available. Workbook-writing libraries alone do not establish formula correctness.

**Gate:** A complete base case calculates from inputs to outputs; debt and funding schedules reconcile, with no unexplained errors or circular references.

### Phase 5 — Credit metrics, scenarios and sensitivities

Metric methodology to implement and document:

| Metric | Planned definition / limitation |
| --- | --- |
| DSCR | Period CFADS / scheduled cash interest and principal due. Report minimum, timing and clearly defined aggregate/average measure; flag periods without debt service as N/A. |
| Project leverage | Clearly specify debt / total funded project cost, measurement date and included cost components. Distinguish commitment from outstanding balance. |
| LTV | Use only with a defensible asset-valuation basis. If unavailable, report debt-to-cost instead and mark LTV unavailable. A modelled DCF is hypothetical and distinct from an independent valuation. |
| Sponsor leverage | Net debt / EBITDA or another justified measure, with explicit treatment of leases, restricted cash and material adjustments. |
| Interest coverage | Defined earnings measure / defined interest expense; explain accounting versus cash interest and construction-period limitations. |
| LLCR, optional | NPV of CFADS over remaining loan life / debt outstanding, with discount-rate and reserve treatment stated. |

- Build base, upside, downside and severe-but-plausible combined scenarios; select magnitudes only after evidence review.
- Stress electricity prices, interest rates, operating costs and construction delays individually and jointly.
- Link delays to capex timing/overruns where assumed, extra interest, lost or deferred generation, PPA dates, maturity and support funding. State whether maturity shifts or remains fixed.
- Apply interest-rate stresses only to exposed debt under the assumed hedge structure.
- Add generation/yield and capex-overrun tests because price alone does not capture solar cash-flow risk.
- Produce at least two decision-useful two-variable tables, such as exposed power price versus generation and interest rate versus opex.
- Identify break-even values for covenant breach and debt-service failure separately; report unsolved ranges honestly.
- Compare the requested S$100m facility with supportable debt under stated coverage and leverage constraints. If unsupported, quantify a lower loan, additional equity or other mitigation without overwriting the original request.

**Gate:** Scenario outputs respond correctly to inputs, stressed deficits remain visible, and each proposed mitigation has a modelled effect where quantifiable.

### Phase 6 — Form the credit view and write the memo

- Assess construction/completion, resource, offtaker, merchant, interest-rate, refinancing, operating, regulatory and security-enforcement risks relevant to the selected structure.
- Separate quantified findings, qualitative judgments and unverified limitations.
- Decide approval, rejection or conditional approval only after modelling and risk review.
- Propose a term sheet covering borrower, amount, purpose, tenor, pricing assumptions, repayment, security, sponsor commitments, reserve accounts, hedging, covenants, reporting, drawdown conditions and distribution restrictions.
- Distinguish conditions precedent from ongoing covenants and default triggers. Explain cure rights and consequences at a simulated level without claiming legal enforceability has been established.

Suggested five-page memo allocation:

1. Decision requested, recommendation, facility terms and main reasons.
2. Sponsor financial assessment and limits of sponsor support.
3. Project economics, financing structure and base-case debt-service capacity.
4. Downside results, key risks and mitigants.
5. Conditions, covenants, residual risks, limitations and compact source references.

**Gate:** Every numerical memo claim traces to a specific model output or source. The recommendation follows the evidence and distinguishes conditions from unresolved diligence.

### Phase 7 — Validate and package for a portfolio

- Reconcile source figures, funding, debt, reserves and cash movements; inspect all error flags.
- Independently hand-check representative revenue, interest, CFADS and DSCR periods.
- Test COD and maturity boundaries, zero debt, zero generation, a price/opex shock, rate changes and a delay extending beyond an assumed deadline.
- Confirm adverse shocks reduce headroom or document a structural reason for any exception; confirm all scenarios use the intended inputs.
- Check debt-service-period minimum DSCR directly against the schedule, not only a dashboard summary.
- Check workbook outputs against the memo after the final recalculation.
- Export the memo to PDF; inspect every page for readability, complete tables, citations and the 3–5-page limit.
- Document how to reproduce the analysis, change scenarios and run meaningful checks. Provide a concise limitations section and an honest statement of the author's contribution.
- Prepare GitHub-ready documentation and final files. Verify account, repository name and visibility before remote creation; confirm publication is within the user's execution instruction. The user subsequently requested Phase 7 execution. The user subsequently explicitly approved public visibility.
- Publish only material suitable for redistribution; link to public reports rather than automatically committing copyrighted source documents.

**Gate:** Final artifacts open correctly, checks pass or clearly identify substantive failures, the memo and workbook agree, and the repository can be understood without this conversation.

## 4. Proposed repository contents

| Path | Intended content |
| --- | --- |
| `README.md` | Case overview, simulation disclosure, deliverable links, key findings once completed and quick-start instructions. |
| `PROJECT_B_ROADMAP.md` | This execution plan and completion gates. |
| `docs/case_definition.md` | Asset, borrower, scope, cutoff and financing choices. |
| `docs/methodology.md` | Model mechanics, metric definitions, scenario design and limitations. |
| `docs/assumptions_register.csv` | Classified inputs, rationale, units and supporting evidence. |
| `docs/source_register.csv` | URLs, publication/access dates, financial periods and page/table references. |
| `docs/decision_log.md` | Material choices, unresolved questions and changes. |
| `docs/progress.md` | Phase status, validated artifacts and next action. |
| `data/processed/` | Traceable public-data extracts; no confidential or invented observations. |
| `model/renewable_project_finance.xlsx` | Final recalculated, auditable workbook. |
| `memo/credit_committee_memo.pdf` | Final 3–5-page memo. |
| `memo/credit_committee_memo_source.*` | Editable memo source. |
| `scripts/` | Reproducible generation/calculation helpers where useful. |
| `validation/` | Meaningful check scripts and concise validation results. |

Do not create empty final deliverables or insert placeholder conclusions simply to make this structure appear complete.

## 5. Effort and sequencing

Planning estimate, not a promised schedule: approximately **30–45 focused hours** for a polished first version, depending on source availability and spreadsheet tooling. Work in phase order; source collection and assumption research may overlap after the case is defined. Draft narrative only after the base case is coherent, and finalise the recommendation after stresses and checks.

Prioritise a credible, complete model and a concise credit decision. Advanced debt sculpting, elaborate dashboards and additional ratios are optional extensions after the core gates pass.

### Full-project milestone tracker

This roadmap covers the entire project through final delivery and GitHub publication when authorized. Each milestone produces something reviewable; completing the plan itself does not complete the case study.

| Milestone | Prerequisites | Concrete output | Estimated focused effort | Completion evidence |
| --- | --- | --- | --- | --- |
| M1 — Freeze the case | None | Case definition, folder structure, registers and decisions log | 2–3 hours | Borrower, asset, revenue structure, scope and cutoff are recorded. |
| M2 — Establish evidence | M1 | Three-year financial extracts and primary-source/project benchmark register | 5–7 hours | Material figures reconcile to reports; gaps and restatements are recorded. |
| M3 — Complete sponsor assessment | M2 | Historical financial analysis, ratio calculations and sponsor risk commentary | 3–4 hours | Every ratio has a definition and source reconciliation; support assumptions are explicit. |
| M4 — Freeze modelling assumptions | M1–M3 | Project assumption register, sources-and-uses structure and provisional loan terms | 3–4 hours | Inputs have evidence or hypothetical rationale; cost and funding scope agree. |
| M5 — Finish the base-case workbook | M4 | Linked construction, operating, tax, cash-flow and debt model | 7–10 hours | Core schedules calculate and reconcile; deficits and covenant failures remain visible. |
| M6 — Complete credit and downside analysis | M5 | Scenario comparison, sensitivities, covenant headroom and sustainable debt assessment | 4–6 hours | All required stresses work; the requested facility is tested without forcing viability. |
| M7 — Finish the committee memo | M3, M6 | Editable memo and 3–5-page PDF with a supported recommendation | 3–5 hours | Terms, risks, conditions and quantitative claims agree with the model. |
| M8 — Validate and release the portfolio | M7 | Validated workbook/PDF, final README, methodology and GitHub repository when authorized | 3–6 hours | Final completion checklist passes and downloadable artifacts match the reviewed versions. |

The milestone estimates total approximately 30–45 focused hours. Re-estimate if the chosen geography, data gaps, model mechanics or tooling materially increase the work.

### Final deliverable acceptance checklist

**Excel model**

- [x] Verified sponsor financial history and formula-based ratios are included.
- [x] Project revenue, opex, capex, taxes, working capital, free cash flow and CFADS are forecast over the selected horizon.
- [x] Drawdowns, construction interest, cash interest, principal, reserves and ending debt are linked and reconciled.
- [x] DSCR and applicable leverage/coverage metrics have explicit definitions; LTV is supported or clearly marked unavailable.
- [x] Price, interest, opex and delay stresses are implemented, with combined downside and decision-useful sensitivities.
- [x] Inputs, assumptions and derived outputs are distinguishable; no calculated result is hardcoded.
- [x] The workbook is recalculated in the calculation engine, exports with usable results, labelled units and no cached formula errors. Native Excel opening/recalculation is not independently verified.

**Credit committee memo**

- [x] The PDF is 3–5 pages, legible and professionally formatted.
- [x] It makes an explicit approval, rejection or conditional-approval recommendation based on completed analysis.
- [x] It covers sponsor strength, project repayment capacity, downside performance, key risks and residual limitations.
- [x] Proposed terms, conditions precedent, covenants and distribution restrictions are specific and consistent with the model.
- [x] Public facts, hypothetical assumptions and analytical judgments remain distinguishable.
- [x] All material numerical claims reconcile to the final workbook or cited sources.

**GitHub portfolio**

- [x] The README explains the credit question, simulation scope, methodology, completed findings and file navigation.
- [x] Source and assumption registers provide a usable audit trail.
- [x] Methodology explains CFADS, debt mechanics, ratios, scenarios and limitations.
- [x] Final Excel and PDF deliverables are included and linked using working relative paths.
- [x] Reproduction and validation instructions are sufficient for a reviewer to change assumptions and assess the results.
- [x] Confidential information, credentials, temporary files and source material unsuitable for redistribution are excluded.
- [x] Remote repository creation/publication follows the user's execution authorization; the repository URL and final commit are recorded after publication.

**Whole-project completion rule:** The project is complete only when all three deliverables meet their acceptance criteria and material analytical/calculation issues are resolved or explicitly limit the recommendation. A negative credit outcome is a valid completed result. A locally finished package awaiting authorized publication is labelled “analysis complete; publication pending,” not fully delivered.

### Final handoff

Provide links to the Excel model, PDF memo and repository; state the information cutoff and final recommendation; identify the assumptions that most affect the decision and any unresolved limitations. Include a short explanation of how to change a scenario and interpret the resulting covenant headroom. Draft a factual project description suitable for the portfolio; any resume bullet must describe completed work and actual outputs without implying employment by DBS or Sembcorp.

## 6. Instructions for resuming the work

1. Read this roadmap and any existing progress/decision logs. Preserve completed work and the frozen information cutoff unless an update is intentional.
2. Inspect current artifacts before changing them; identify the earliest unfinished gate.
3. Begin with Phase 0 and the case definition if no execution has occurred. Do not jump straight to Excel or a credit conclusion.
4. During execution, consult the applicable spreadsheet and PDF/document workflows before producing those artifacts.
5. At each handoff update phase status, evidence gaps, exact artifact paths and next tasks. Never mark a phase complete merely because its file exists.

### Current status

- [x] Project scope converted into an execution roadmap.
- [x] Phase 0 — Case definition and audit trail.
- [x] Phase 1 — Verified public evidence, with disclosed comparability/access limits.
- [x] Phase 2 — Sponsor analysis.
- [x] Phase 3 — Assumptions and financing structure for the simulation; real project conditions unverified.
- [x] Phase 4 — Linked Excel model, with calculation-engine and exported-file checks.
- [x] Phase 5 — Credit metrics, native sensitivities, scenarios and qualified sizing diagnostics.
- [x] Phase 6 — Evidence-led recommendation and five-page PDF memo.
- [x] Phase 7 — Validation, portfolio packaging and public GitHub publication; native Excel verification limits disclosed.

**Next action:** personally review the model and sources before using the case study in applications. Read `docs/viewing_guide.md` and `docs/contribution_statement.md`. Native Excel application recalculation remains outside the completed verification coverage. A revised lifecycle reserve structure would be a separate analytical iteration.
