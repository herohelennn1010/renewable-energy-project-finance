# Portfolio website verification

17 November 2026. This report concerns the website presentation, not new assurance of the financial analysis.

- HTML links and section anchors resolve locally; IDs are unique.
- JavaScript passes syntax checking.
- All four embedded scenario outputs match the published model JSON exactly.
- Scenario input shocks are read from the original workbook formula map.
- Base, Upside, Downside and Severe were switched in the browser and the displayed values inspected.
- Severe outputs retain the completion qualification and do not present conditional zero arrears as a healthier credit.
- Desktop layout and 390 px mobile layout were visually reviewed.
- Mobile page width equals its 390 px viewport, with no horizontal overflow; dashboard image loads.
- Download section and scenario results are readable on mobile.

The live website returns HTTP 200. All 7 internal page/asset/download URLs return HTTP 200 and match repository bytes by SHA-256, including the PDF and Excel file. The published downside selector and contribution accordion were checked in the browser. GitHub Pages deployment succeeded for source commit `f417e68c0b662717ed26ee633ae8887dce50814f`. See `site_validation.json` for file-level evidence. The financial model and PDF are unchanged from the verified project release.
