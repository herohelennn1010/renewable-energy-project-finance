# How to view this project

**Release note:** the complete project is available in the [public GitHub repository](https://github.com/herohelennn1010/renewable-energy-project-finance). Read the memo in your browser, download the workbook to use it in Excel, or choose Code → Download ZIP for the complete package. Publication checks are recorded in `validation/publication_receipt.json`.

## Read in this order

For the visual presentation, start at the [portfolio website](https://herohelennn1010.github.io/renewable-energy-project-finance/). It provides a scenario explorer, credit summary and direct downloads. The GitHub repository retains the detailed audit trail.

1. **README.md** gives the credit question, simulation disclosure, headline results and deliverable links. On GitHub it appears below the file list.
2. **memo/credit_committee_memo.pdf** is the five-page banking deliverable. Read this first for the recommendation and risk reasoning. Preview it in the browser or download and open it in Preview.
3. **model/renewable_project_finance.xlsx** is the working model. Download the raw file from GitHub and open it in Microsoft Excel. The GitHub file page is a download location, not a working spreadsheet.
4. **docs/source_register.csv**, **docs/assumptions_register.csv** and **docs/model_implementation.md** show the evidence, hypothetical assumptions and calculation design.
5. **validation/model_validation.md** and **validation/release_validation.md** document the checks and remaining limits.

No Python, Node or code execution is required to read the memo or use the workbook. The code and snapshots are included for audit and reconstruction.

## A five-minute workbook demonstration

Save a separate working copy before editing. Use automatic calculation. On **Assumptions**, go to **E4** (Excel's Name Box can jump to an address). Enter **1** for Base, **2** for Upside, **3** for Downside or **4** for Severe.

Start at **Dashboard**. Compare actual drawn debt with the S$100m commitment, then review minimum DSCR, covenant breaches, unpaid debt service and construction funding gaps. The base case has about S$90.15m drawn debt and minimum ordinary-quarter DSCR of 1.54x. Its full minimum DSCR is -2.89x because the year-12 replacement is deducted from CFADS. Retained cash meets scheduled debt service, but does not cure that covenant calculation.

Change E4 to **3**. The ordinary-quarter minimum falls to 1.12x and peak unpaid debt service is about S$0.22m. Change it to **4** to see the construction funding gap and missed longstop. Severe operating coverage is conditional on completion and cannot demonstrate bankability.

Trace the calculations through **Operations → Debt → Cash_Flow**, with **Construction** and **Tax** supporting the forecast. Review the **Checks** tab. These reconciliation checks do not mean credit approval.

On **Sensitivity**, E4:E7 hold merchant-price multiplier, yield multiplier, additional benchmark rate and opex multiplier. Neutral settings are **1, 1, 0, 1**. Enter rates as decimals (0.01 means +100 basis points). The two native tables show minimum DSCR excluding replacement, explicitly a diagnostic. They do not remove the full-covenant breach.

Restore **Assumptions!E4 = 1** and **Sensitivity!E4:E7 = 1, 1, 0, 1** when finished. If the application does not support Excel What-If tables, retain that limitation and use the main scenario schedules. Native Excel recalculation coverage is stated in the release validation report.

## What to share on a resume

Link the project title to the **portfolio website** for a visual introduction. The reviewer can open the memo, download Excel and explore the four scenarios. The website links to GitHub for the detailed source, assumptions and validation. The memo remains the fastest substantive read.

Suggested title: **Renewable Energy Project Finance & Credit Assessment — Independent Case Study**.

Describe only work you have personally reviewed and can explain. This project was developed with substantial AI assistance; see [contribution statement](contribution_statement.md). Do not imply employment by DBS or Sembcorp, an actual mandate, or independent manual authorship of all calculations.
