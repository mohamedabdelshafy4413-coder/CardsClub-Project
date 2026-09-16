# Cards Club — Data Quality & Assumptions Register

This file documents the assumptions and evidence-quality controls behind the dashboard.

## 1) Market data
- Core trade family: **HS 950440 — Playing Cards**.
- Import values are market-demand signals, not Cards Club sales.
- Latest available year differs by market; the dashboard shows `Data Year` explicitly.
- Where an importer total was not sufficiently verified, the market remains in the model with a lower `Data Confidence` flag and a Discovery recommendation.

## 2) Mirror-data discrepancies
Exporter-side and importer-side trade values can differ because of timing, valuation, re-export, partner-country attribution and reporting practices.

Example used in the study:
- Saudi import-side data for 2024 reports approximately **USD 208.8K** of HS 950440 from Egypt.
- Exporter-side mirror data for Egypt → Saudi records a different value.

Therefore the dashboard uses the bilateral flow as proof that trade exists, not as audited market share or a Cards Club transaction.

## 3) UAE hub evidence
UAE 2023 import and export values are used because the validated 2023 dataset provides both sides of the category flow:
- Imports: approximately **USD 12.259M**.
- Exports: approximately **USD 5.629M**.

This supports UAE as a category trading node in the GCC. It does not prove that any specific UAE distributor will be appropriate for Cards Club.

## 4) South Africa correction
South Africa has a strong 2024 import signal (approximately **USD 6.395M**). The dashboard treats South Africa as a major African demand market.

A Southern Africa hub strategy is a **commercial hypothesis** to validate through:
- distributor footprint
- neighboring-market coverage
- freight economics
- channel rights
- payment terms
- landed price

It must not be assumed only from import volume.

## 5) Scoring model
Country score =
- Demand /30
- Trade Access /20
- Product Fit /20
- Logistics /15
- Execution Readiness /15

`Execution Readiness` replaces the earlier ambiguous label `Risk quality`.

The total is a prioritization heuristic, not a sovereign-risk score.

## 6) Data Confidence
- **High:** recent reported import observation and reasonably clear route context.
- **Medium:** older year, mirror-data issue or material route uncertainty.
- **Low:** importer total / route not sufficiently verified for confident budget allocation.

## 7) Recommended Wave
- **Wave 1:** controlled 90-day pilot.
- **Wave 2:** launch after Wave 1 message / offer validation.
- **Discovery:** research and small tests only until evidence improves.

## 8) Product / pricing assumptions
Internal working prices are not buyer-ready until the following are validated:
- COGS
- unit and carton configuration
- MOQ
- payment terms
- Incoterm
- freight validity
- gross margin target
- design/setup scope

The Commercial Calculator is a scenario tool and does not establish actual customs duty, VAT recoverability or destination fees.

## 9) Customs assumptions
Trade agreements in the dashboard are potential routes only. Never promise duty-free treatment before confirming:
- destination HS classification
- current tariff schedule
- Rules of Origin
- valid Certificate of Origin
- destination customs acceptance

## 10) Public portfolio / client-proof rule
Logos or brand concepts shown in a portfolio must not be described as verified clients unless a separate source confirms that the work was actually commissioned/completed.

## 11) Update discipline
Before a new campaign wave, refresh:
1. import data year / value
2. destination trade route
3. conformity requirement
4. freight assumptions
5. buyer universe
6. data confidence
7. recommended wave

This keeps the dashboard usable as a decision system rather than a static presentation.
