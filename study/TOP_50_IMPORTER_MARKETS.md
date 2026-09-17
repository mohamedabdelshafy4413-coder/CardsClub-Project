# Cards Club — Top 50 Importer Markets Playbook

**Scope:** GCC + Africa  
**Product family:** HS 950440 — Playing Cards  
**Research snapshot:** September 2026

## Purpose
This file converts the 50-country market-intelligence model into an importer-outreach operating layer. For every market it defines:

- overall market rank
- export-success index rank
- importer category
- primary buyer roles
- recommended outreach language
- product focus
- recommended wave
- email campaign angle
- subject line and CTA

The runtime dataset is `data/top50_importer_markets.csv`.

## Export Success Index
`Export Success Index %` is **not a statistical probability of winning an order** and must never be presented to a buyer as one.

It is an internal planning index calculated from the existing market-attractiveness score and the quality of supporting market data:

- High data confidence: Market Score × 1.00
- Medium data confidence: Market Score × 0.92
- Low data confidence: Market Score × 0.82

The result is rounded to the nearest whole number.

### Bands
- **Priority A:** 85–100
- **Priority B:** 70–84
- **Priority C:** 55–69
- **Test / Research:** below 55

This structure deliberately penalizes attractive markets where import evidence is incomplete or older.

## Importer categories

### Playing Cards / Games Importer & General Distributor
Primary roles:
- Owner / CEO
- Import Manager
- Category Buyer

Best offer:
- Cards Club Core
- Bridge range
- distributor pricing
- trial MOQ

Primary campaign: **Distributor Acquisition**.

### Private-Label / Corporate Gifting Importer
Primary roles:
- Owner
- Import Manager
- Marketing Director
- Procurement

Best offer:
- Cards Club BrandLab
- private-label deck
- campaign merchandise
- corporate gifting

Primary campaign: **Corporate BrandLab**.

### Tourism / Souvenir Importer & Hospitality Supplier
Primary roles:
- Import Manager
- Merchandise Buyer
- Hotel Procurement
- Guest Experience / Marketing

Best offer:
- destination decks
- hotel/resort editions
- souvenir collections
- local cultural decks

Primary campaign: **Tourism / Souvenir** or hospitality-specific variation.

### Premium Games / Gift Distributor
Primary roles:
- Owner
- Category Buyer
- Import Manager

Best offer:
- premium Core
- Heritage
- collector / gift bundles

## Priority execution

### Wave 1
- Saudi Arabia
- United Arab Emirates
- Kuwait
- Morocco
- Qatar
- South Africa

Objective: buyer validation, RFQs, sample requests, landed-price feedback and first pilot POs.

### Wave 2
- Oman
- Kenya
- Bahrain
- Mauritius
- Tanzania
- Uganda
- Algeria
- Ghana

Objective: expand only after Wave 1 reveals winning segment × offer × message combinations.

### Discovery
The remaining markets should receive controlled tests rather than scaled outreach. Markets with Low data confidence must pass a research gate before significant spend.

## Campaign operating rule
Each market receives a primary campaign angle, but the final email must still be customized to the target company.

Default cadence:
1. Email 1 — value proposition and low-friction CTA
2. Day 3–4 — proof / product / relevant range
3. Day 7–10 — final low-pressure follow-up

Do not send the seven campaign angles to the same buyer. Choose one angle based on importer category, market and product focus.

## KPI layer
Track by country and campaign:
- delivered rate
- bounce rate
- reply rate
- positive reply rate
- qualified buyer rate
- RFQ rate
- sample request rate
- sample → PO conversion
- average PO value
- gross margin
- sales cycle
- reorder rate

## Data-control rule
Import values are market evidence, not Cards Club sales. Export Success Index is an internal decision-support score, not a forecast guarantee. Tariffs, Rules of Origin, conformity, freight, taxes, payment terms and importer legitimacy must be re-validated before live quotation or shipment.
