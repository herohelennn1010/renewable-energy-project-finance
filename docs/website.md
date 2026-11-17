# Portfolio website

Public address: https://herohelennn1010.github.io/renewable-energy-project-finance/

The website is an additional presentation of the completed case study. It does not change the workbook, credit recommendation or public source facts.

## Content and controls

- Credit decision and the three principal risk findings.
- Four pre-calculated scenarios, with input shocks, full/diagnostic DSCR, debt, completion support, arrears and construction funding gap.
- Ordinary-quarter coverage comparison labelled as a diagnostic, not the contractual covenant.
- Severe operating results explicitly conditional on completion.
- Dashboard preview, memo and Excel downloads, source register, methodology and contribution statement.
- Responsive desktop/mobile layouts, keyboard-accessible scenario buttons and reduced-motion support.

## Rebuild

Run `python3 scripts/build_site.py` from the repository. This reads `model/scenario_results.json` and `model/formula_map.json`, then embeds the data in `site/index.template.html` to write `index.html`. The calculation engine is not required to rebuild the website. Rebuild the financial model separately when assumptions change. The narrative credit findings must also be reviewed if the model is changed.

GitHub Pages publishes the root of the `main` branch. `.nojekyll` makes it a static HTML site. No third-party tracking, external fonts, server, login or database is used. Commit and push approved changes to publish updates.

The published workbook and PDF remain the primary analytical deliverables. Native Microsoft Excel application recalculation is still unverified, and the website preserves that limitation. Website checks are reported separately in `validation/site_validation.md`.
