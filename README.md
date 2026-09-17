# Cards Club — International Export Command Center v3

A fast Streamlit dashboard and structured export study for **Cards Club**, focused on GCC + Africa.

## What changed in v3
- Added a dedicated **Smart Search** page under `pages/01_Smart_Search.py`.
- Added multilingual search support across Arabic, English, French and Portuguese market terms.
- Added smart/fuzzy relevance scoring, exact-phrase mode and all-words mode.
- Added fast filters for region, wave, confidence, importer category and minimum opportunity score.
- Added quick-intent filters for distributors, corporate gifting/private label, tourism/hospitality, Arabic/French markets and research-first markets.
- Added sorting by relevance, export-opportunity score, import value and market rank.
- Added pagination so the UI does not render unnecessary rows.
- Added market drill-down with importer type, buyer roles, language, product focus, search queries, recommended research channels, campaign, subject and CTA.
- Added ready-to-personalize email output for each market.
- Added one-click download for filtered search results.
- Added **Knowledge Search** across products, risks, roadmap, customs/trade and sources.
- Enriched `data/top50_importer_markets.csv` with search keywords, local-language buyer queries, recommended research channels and research priority.
- Renamed the duplicated probability-style metric internally as **Opportunity Score /100** while keeping the original field for backwards compatibility; it is an internal planning score, not a probability of sale.
- Reduced Streamlit runtime watcher overhead with `fileWatcherType="none"`.
- Extended GitHub Actions validation to compile and validate the Smart Search page and enriched importer dataset.

## Dashboard modules
- Executive Dashboard
- 50-Country Market Intelligence
- Top 50 Importer Markets
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

## Smart Search
The Streamlit multipage navigation now includes **Smart Search**.

It searches and filters:
- country and country aliases in Arabic / English
- importer category
- buyer roles
- language
- product focus
- campaign angle
- wave / priority / evidence confidence
- local-language buyer-search phrases
- recommended discovery channels

It also includes a project-wide knowledge search for product, risk, roadmap, trade and source data.

## Study files
- `study/MASTER_EXPORT_STUDY.md` — merged strategic study, corrected market evidence and operating model
- `study/EXPORT_READINESS_CHECKLIST.md` — operational gate before outreach, quote and shipment
- `study/OUTBOUND_EMAIL_PLAYBOOK.md` — seven campaign angles and sequence rules
- `study/TOP_50_IMPORTER_MARKETS.md` — 50-market importer targeting layer and opportunity-ranking logic
- `study/DATA_QUALITY_AND_ASSUMPTIONS.md` — assumptions, evidence-quality rules and fields requiring validation

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

## Performance design
- standard-library CSV parsing for the main app/search layer
- Streamlit cache for data and normalized search indexes
- search filters applied before relevance scoring
- pagination before result rendering
- no Pandas or Plotly runtime dependency
- file watcher disabled in deployed runtime
- compact sanitized datasets instead of the raw internal workbook

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
