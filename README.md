# Cards Club — International Export Command Center v2

A fast Streamlit dashboard and structured export study for **Cards Club**, focused on GCC + Africa.

## What changed in v2
- Corrected the market-scoring terminology from **Risk /15** to **Execution Readiness /15**.
- Added **Data Confidence** and **Recommended Wave** to every country.
- Added Wave 1 / Wave 2 / Discovery controls to the market dashboard.
- Added a **Commercial & Landed-Cost Calculator**.
- Added an interactive **Export Readiness Control Room**.
- Added explicit mirror-trade-data warnings.
- Strengthened the UAE / Saudi / South Africa evidence notes.
- Upgraded CI to validate the 50-country model, confidence flags, waves and study files.

## Dashboard modules
- Executive Dashboard
- 50-Country Market Intelligence
- Country Drill-down
- SWOT & Positioning
- Products & Offers
- Golden 1000 Account Model
- Commercial / Landed-Cost Calculator
- Export Readiness Control Room
- 90-Day GTM Roadmap
- Export Risk Register
- Customs & Trade Controls
- 7 Email Campaign Angles
- Sales Scenarios & KPI Tree
- Files & Sources

## Study files
- `study/MASTER_EXPORT_STUDY.md` — merged strategic study, corrected market evidence and operating model
- `study/EXPORT_READINESS_CHECKLIST.md` — operational gate before outreach, quote and shipment
- `study/OUTBOUND_EMAIL_PLAYBOOK.md` — seven campaign angles and sequence rules

## Runtime data
The app reads small sanitized CSV files from `data/` for speed and stability:
- `countries.csv`
- `products.csv`
- `risks.csv`
- `roadmap.csv`
- `golden1000.csv`
- `trade.csv`
- `sources.csv`

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud
- Repository: `mohamedabdelshafy4413-coder/CardsClub-Project`
- Branch: `main`
- Main file: `app.py`
- Recommended Python: `3.12`

## Security
The original internal workbook is intentionally **not published** because it contains sensitive operational / credential / banking-related information. This repository uses sanitized market and study data only.

## Research / decision rule
Research snapshot: **September 2026**. Market scores are decision-support heuristics, not guaranteed sales forecasts or sovereign-risk ratings. Country tariffs, Rules of Origin, conformity routes, buyer data, freight, tax treatment and payment risk must be re-validated before a live quotation or shipment.

Trade databases can contain importer/exporter mirror-data differences. Use those records as market evidence, not as audited Cards Club revenue or exact company market share.
