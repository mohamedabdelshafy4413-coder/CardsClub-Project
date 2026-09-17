# Cards Club — International Export Command Center v3

A fast Streamlit dashboard and structured export study for **Cards Club**, focused on GCC + Africa.

## What changed in v3
- Added a dedicated **Top 50 Importer Markets** operating file and dashboard page.
- Added **Importer Category** for every market.
- Added **Primary Buyer Roles** and recommended outreach language.
- Added **Export Success Index %** and a separate Success Rank.
- Added success bands: Priority A / B / C / Test-Research.
- Assigned a recommended **Email Campaign**, subject line and CTA to every country.
- Added country-level campaign drill-down inside Streamlit.
- Added a direct CSV download for the Top 50 importer-market file.
- Kept the Export Success Index explicitly labeled as an internal planning index, not a statistical probability or guaranteed forecast.

## Dashboard modules
- Executive Dashboard
- **Top 50 Importer Markets**
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
- `study/MASTER_EXPORT_STUDY.md` — merged strategic study and operating model
- `study/TOP_50_IMPORTER_MARKETS.md` — importer targeting, success-index methodology and campaign mapping
- `study/EXPORT_READINESS_CHECKLIST.md` — operating gate before outreach, quote and shipment
- `study/OUTBOUND_EMAIL_PLAYBOOK.md` — seven campaign angles and sequence rules
- `study/DATA_QUALITY_AND_ASSUMPTIONS.md` — assumptions / evidence-quality register

## Runtime data
The app reads small sanitized CSV files from `data/` for speed and stability:
- `countries.csv`
- `top50_importer_markets.csv`
- `products.csv`
- `risks.csv`
- `roadmap.csv`
- `golden1000.csv`
- `trade.csv`
- `sources.csv`

## Top 50 importer-market logic
The new file ranks the existing GCC + Africa market universe by both:
1. **Market Rank** — the strategic market-attractiveness score.
2. **Success Rank** — the Export Success Index after applying a data-confidence adjustment.

The Export Success Index is an internal planning score only. It is **not** the probability that Cards Club will win an order.

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
Research snapshot: **September 2026**. Market scores and the Export Success Index are decision-support heuristics, not guaranteed sales forecasts or sovereign-risk ratings. Country tariffs, Rules of Origin, conformity routes, buyer data, freight, tax treatment and payment risk must be re-validated before a live quotation or shipment.

Trade databases can contain importer/exporter mirror-data differences. Use those records as market evidence, not as audited Cards Club revenue or exact company market share.
