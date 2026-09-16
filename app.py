from pathlib import Path
import csv
import math
from html import escape
import streamlit as st

st.set_page_config(
    page_title="Cards Club Export Command Center",
    page_icon="🂡",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
DATA = ROOT / "data"
LOGO = ROOT / "assets" / "cards-club-logo.svg"

st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"]{background:#fbfdfb;color:#101410}
[data-testid="stSidebar"]{background:#0b0e0c;border-right:1px solid #d9e4dc}
[data-testid="stSidebar"] *{color:#f6fff8}
.block-container{max-width:1680px;padding-top:1rem;padding-bottom:2rem}
.hero{background:linear-gradient(135deg,#080b09 0%,#111713 68%,#a6f3b5 180%);border:1px solid #27352b;border-radius:24px;padding:30px 32px;margin-bottom:18px;box-shadow:0 14px 40px rgba(0,0,0,.12)}
.hero h1{color:#fff;margin:7px 0 0;font-size:2.25rem}.hero p{color:#dce8df;line-height:1.8;margin:.7rem 0 0}.tag{display:inline-block;background:#c9ffd5;color:#07150b;border-radius:999px;padding:5px 11px;margin-right:6px;font-size:.76rem;font-weight:850}
.kpi{background:#fff;border:1px solid #dce7df;border-radius:16px;padding:16px 18px;min-height:128px;box-shadow:0 6px 18px rgba(10,30,18,.05)}
.kpi .label{font-size:.82rem;color:#58675e}.kpi .value{font-size:1.46rem;font-weight:850;color:#0c1710;margin:.3rem 0}.kpi .note{font-size:.78rem;color:#6b786f;line-height:1.55}
.panel{background:#fff;border:1px solid #dce7df;border-radius:16px;padding:18px 20px;margin:.55rem 0 1rem}.good{border-left:5px solid #61d881;background:#f3fff6}.warn{border-left:5px solid #e5b34f;background:#fffaf0}.risk{border-left:5px solid #db6a6a;background:#fff5f5}.info{border-left:5px solid #8fd9ff;background:#f4fbff}.titleline{font-weight:900;font-size:1.05rem;color:#0b1710;margin-bottom:.3rem}
.barrow{display:grid;grid-template-columns:190px 1fr 60px;gap:10px;align-items:center;margin:8px 0}.track{height:11px;background:#edf2ee;border-radius:99px;overflow:hidden}.fill{height:11px;background:#a6f3b5;border-radius:99px}.rank{font-weight:850;color:#0b1710}
.mono{direction:ltr;text-align:left;font-family:monospace;white-space:pre-wrap;background:#0c120e;color:#dfffea;border-radius:12px;padding:14px}
.pill{display:inline-block;padding:4px 9px;border:1px solid #cfe5d4;background:#f6fff8;border-radius:999px;margin:2px;font-size:.78rem}.muted{color:#68756c;font-size:.84rem}
div[data-testid="stDataFrame"]{border:1px solid #e0e8e2;border-radius:14px;overflow:hidden}
</style>
""",
    unsafe_allow_html=True,
)

@st.cache_data(show_spinner=False, ttl=3600)
def load_csv(name: str):
    path = DATA / name
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def num(v, default=0.0):
    try:
        if v in (None, "", "nan", "NaN"):
            return default
        return float(v)
    except Exception:
        return default


def money(v):
    x = num(v, math.nan)
    return "Not verified" if math.isnan(x) else f"${x:,.0f}"


def kpi(label, value, note):
    st.markdown(
        f'<div class="kpi"><div class="label">{escape(str(label))}</div><div class="value">{escape(str(value))}</div><div class="note">{escape(str(note))}</div></div>',
        unsafe_allow_html=True,
    )


def panel(title, body, kind="good", allow_html=False):
    safe_title = escape(str(title))
    safe_body = body if allow_html else escape(str(body))
    st.markdown(
        f'<div class="panel {kind}"><div class="titleline">{safe_title}</div>{safe_body}</div>',
        unsafe_allow_html=True,
    )


def bars(rows, limit=10):
    if not rows:
        return
    top = sorted(rows, key=lambda r: num(r.get("Score /100")), reverse=True)[:limit]
    html = []
    for r in top:
        score = int(num(r.get("Score /100")))
        html.append(
            '<div class="barrow">'
            f'<div><span class="rank">#{escape(str(r.get("Rank", "")))}</span> {escape(str(r.get("Country", "")))}</div>'
            f'<div class="track"><div class="fill" style="width:{max(0,min(score,100))}%"></div></div>'
            f'<div>{score}/100</div></div>'
        )
    st.markdown("".join(html), unsafe_allow_html=True)


def count_by(rows, field):
    out = {}
    for r in rows:
        key = r.get(field) or "Unknown"
        out[key] = out.get(key, 0) + 1
    return out


def calc_margin_sell(cost, margin_pct):
    margin = max(0.0, min(float(margin_pct), 95.0)) / 100.0
    return cost / (1.0 - margin) if cost > 0 else 0.0


SWOT = {
    "Strengths": [
        "Made-in-Egypt manufacturing base close to GCC and Africa.",
        "Standard + heritage + tourism + seasonal + custom portfolio.",
        "Customization reduces dependence on commodity-only price competition.",
        "Egyptian cultural storytelling creates differentiated creative IP.",
        "Potential regional trade preferences, subject to Rules of Origin.",
    ],
    "Weaknesses": [
        "International export proof is still limited versus established suppliers.",
        "Master-data inconsistencies must be eliminated before buyer-facing use.",
        "Pricing still needs complete EXW / FOB / CIF governance.",
        "B2B case studies and verified distributor references are limited.",
        "Some operational claims and SKU data require verification.",
    ],
    "Opportunities": [
        "Cards Club BrandLab for corporate and private-label orders.",
        "Hotels, resorts, museums, duty-free and tourism souvenir decks.",
        "UAE as a documented GCC trading hub for HS 950440.",
        "Localized Ramadan, wildlife, national-occasion and destination decks.",
        "Importers, gifting agencies, hospitality and direct strategic brands.",
    ],
    "Threats": [
        "China and other scale suppliers dominate pure price competition.",
        "Origin/compliance errors can block shipments or remove tariff benefits.",
        "FX, freight and payment risk can erase margin.",
        "Weak exclusivity contracts can lock a market behind a weak distributor.",
        "IP, cultural sensitivity and gambling perception can create friction.",
    ],
}

EMAILS = {
    "Distributor Acquisition": (
        "Playing cards for {{Country}}",
        "Standard, cultural and private-label decks manufactured in Egypt.",
        "Hi {{FirstName}},\n\nCards Club manufactures premium playing cards in Egypt for retail, distribution and private-label programs.\n\nWe offer standard Bridge decks, cultural collections and fully customized editions. We're opening selected distribution partnerships in {{Country}}, and {{Company}} looks relevant.\n\nWould it be useful if I sent our distributor range, MOQ and export pricing?\n\nBest,\nCards Club Export Team",
    ),
    "Regional Supplier Alternative": (
        "A closer deck supplier",
        "Regional production instead of another long Asian supply chain.",
        "Hi {{FirstName}},\n\nIf your playing-card range currently comes from Asia or Europe, Cards Club offers a manufacturing alternative from Egypt. We produce standard and custom decks with flexible branding, packaging and regional export support.\n\nIf you share the product you currently buy, I can prepare a like-for-like commercial comparison.\n\nBest,\nCards Club Export Team",
    ),
    "Corporate BrandLab": (
        "52 branded touchpoints",
        "Not another promotional giveaway.",
        "Hi {{FirstName}},\n\nA custom playing-card deck puts {{Company}} across 52 usable, collectible brand touchpoints — from the cards to the packaging. Cards Club handles concept, design and manufacturing in Egypt.\n\nWould you like us to create one sample concept for {{Company}}?\n\nBest,\nCards Club BrandLab",
    ),
    "Hotels & Resorts": (
        "Your hotel as a collectible deck",
        "Guest entertainment, souvenir and branded gift in one product.",
        "Hi {{FirstName}},\n\nWe manufacture custom playing-card decks for hospitality and tourism brands. A {{Hotel}} edition can feature the property, destination and local landmarks for guest rooms, VIP gifts and retail.\n\nWould you like to see three creative directions?\n\nBest,\nCards Club Export Team",
    ),
    "Tourism / Souvenir": (
        "Put {{City}} in their pocket",
        "A souvenir travelers can actually use.",
        "Hi {{FirstName}},\n\nCards Club creates destination decks inspired by local culture, landmarks and stories. We'd like to explore a {{Destination}} edition with {{Company}}.\n\nShould I send a sample concept?\n\nBest,\nCards Club Export Team",
    ),
    "Seasonal / Ramadan": (
        "52 moments for Ramadan",
        "A limited branded edition built for gifting.",
        "Hi {{FirstName}},\n\nCards Club creates premium seasonal playing-card editions for corporate gifting and brand campaigns. We can build a Ramadan edition around {{Company}} — artwork, packaging and production.\n\nWould you like a visual direction?\n\nBest,\nCards Club BrandLab",
    ),
    "Breakup / Re-engagement": (
        "Close {{Country}}?",
        "Last note from me.",
        "Hi {{FirstName}},\n\nI haven't heard back, so I'll close the conversation. We're selecting distribution and custom-deck partners in {{Country}}, and {{Company}} was still on our shortlist.\n\nIf relevant, reply CATALOG and I'll send everything over.\n\nBest,\nCards Club Export Team",
    ),
}

READINESS = {
    "Product master data": [
        "Final SKU names/codes approved",
        "Country of origin consistent across labels/listings",
        "Unit + master-carton dimensions/weights/CBM verified",
        "Paper/coating/finish specification locked",
        "Lead time and peak-season lead time verified",
    ],
    "Customs & origin": [
        "Destination HS classification checked",
        "Rules of Origin checked for priority routes",
        "BOM / Egyptian value-added evidence prepared",
        "Certificate of Origin route confirmed",
        "Destination conformity/marking route checked",
    ],
    "Commercial": [
        "EXW and FOB price matrices approved",
        "CIF workflow and quote-validity policy approved",
        "Trial / Standard / Strategic MOQ ladder approved",
        "Sample policy and design/setup fees approved",
        "Payment terms matrix approved by risk level",
    ],
    "Quality & shipment": [
        "Golden Sample approved",
        "Batch QC tolerances documented",
        "Moisture-control requirement assessed by route",
        "Packing list / invoice / COO document SOP ready",
        "Insurance / freight / release gate defined",
    ],
    "Sales operations": [
        "Golden 1000 account universe built",
        "Contacts verified and buyer roles assigned",
        "Country × segment × offer campaigns prepared",
        "CRM stages / objection tags defined",
        "Weekly KPI review cadence scheduled",
    ],
}

left, right = st.columns([1, 5])
with left:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
with right:
    st.markdown(
        '<div class="hero"><span class="tag">GCC + AFRICA</span><span class="tag">HS 950440</span><span class="tag">90-DAY GTM</span><span class="tag">DATA CONFIDENCE</span><h1>Cards Club Export Command Center</h1><p><b>From Concept to Deck.</b> Market intelligence, commercial economics, export risk control, buyer targeting and execution.</p></div>',
        unsafe_allow_html=True,
    )

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Dashboard",
        "Market Intelligence",
        "SWOT & Positioning",
        "Products & Offers",
        "Golden 1000",
        "Commercial Calculator",
        "Export Readiness",
        "90-Day Roadmap",
        "Risk Register",
        "Customs & Trade",
        "Email Campaigns",
        "Sales Scenarios",
        "Files & Sources",
    ],
)
st.sidebar.caption("Research snapshot: Sep 2026. Re-validate tariffs, origin, conformity, freight and buyer data before live quotation or shipment.")

if page == "Executive Dashboard":
    countries = load_csv("countries.csv")
    wave1 = [r for r in countries if r.get("Recommended Wave") == "Wave 1"]
    high_conf = [r for r in countries if r.get("Data Confidence") == "High"]
    verified_2024 = [r for r in countries if str(r.get("Data Year", "")).startswith("2024")]
    c = st.columns(5)
    items = [
        ("Priority markets", len(countries) or 50, "GCC + Africa intelligence universe"),
        ("Wave 1", len(wave1) or 6, "Immediate pilot markets"),
        ("High-confidence markets", len(high_conf), "Evidence strength flag"),
        ("2024 import observations", len(verified_2024), "Latest-year records in model"),
        ("Core HS", "950440", "Playing cards"),
    ]
    for col, item in zip(c, items):
        with col:
            kpi(*item)
    panel("Execution rule", "The 50 markets are an intelligence universe, not a simultaneous rollout. Wave 1 is the controlled commercial pilot; Wave 2 follows only after message, offer and buyer-quality validation.", "warn")
    if countries:
        st.markdown("### Top market-attractiveness scores")
        bars(countries, 12)
        cols = ["Rank","Tier","Country","Score /100","Data Confidence","Recommended Wave","Product Focus","Country Positioning"]
        st.dataframe([{k:r.get(k) for k in cols} for r in countries[:12]], use_container_width=True, hide_index=True)
    a, b, c = st.columns(3)
    with a: panel("Avoid the commodity trap", "Core opens doors; BrandLab, destination and heritage lines are the margin engine.")
    with b: panel("Use evidence quality", "A high score with low data confidence is a research lead, not a launch instruction.", "info")
    with c: panel("Build export proof", "Qualified buyer → RFQ → sample → pilot PO → reorder → case study.")

elif page == "Market Intelligence":
    countries = load_csv("countries.csv")
    st.subheader("50-country market intelligence")
    if not countries:
        st.error("Country dataset is missing.")
    else:
        f1, f2, f3, f4 = st.columns(4)
        tiers = f1.multiselect("Tier", ["A", "B", "C", "D"], default=["A", "B", "C", "D"])
        regions_all = sorted({r.get("Region", "") for r in countries if r.get("Region")})
        regions = f2.multiselect("Region", regions_all, default=regions_all)
        waves_all = ["Wave 1", "Wave 2", "Discovery"]
        waves = f3.multiselect("Recommended wave", waves_all, default=waves_all)
        conf_all = ["High", "Medium", "Low"]
        confidence = f4.multiselect("Data confidence", conf_all, default=conf_all)
        query = st.text_input("Search market / product / positioning").strip().lower()
        view = [r for r in countries if r.get("Tier") in tiers and r.get("Region") in regions and r.get("Recommended Wave") in waves and r.get("Data Confidence") in confidence]
        if query:
            view = [r for r in view if query in " ".join(str(v) for v in r.values()).lower()]
        cols = ["Rank","Tier","Country","Region","HS950440 Import USD","Data Year","Score /100","Execution Readiness /15","Outreach Priority","Data Confidence","Recommended Wave","Product Focus","Country Positioning"]
        st.dataframe([{k:r.get(k) for k in cols} for r in view], use_container_width=True, hide_index=True)
        options = [r["Country"] for r in view] or [r["Country"] for r in countries]
        market = st.selectbox("Country drill-down", options)
        r = next(x for x in countries if x["Country"] == market)
        a, b, c, d, e = st.columns(5)
        a.metric("Rank", r.get("Rank")); b.metric("Tier", r.get("Tier")); c.metric("Import signal", money(r.get("HS950440 Import USD"))); d.metric("Score", f"{int(num(r.get('Score /100')))}/100"); e.metric("Wave", r.get("Recommended Wave"))
        panel("Country positioning", r.get("Country Positioning", ""))
        x, y = st.columns(2)
        with x:
            st.write("**Product focus:**", r.get("Product Focus"))
            st.write("**Trade route:**", r.get("Potential Trade Route"))
            st.write("**Outreach priority:**", r.get("Outreach Priority"))
            st.write("**Data confidence:**", r.get("Data Confidence"))
            st.write("**Data status:**", r.get("Data Status"))
        with y:
            for label, field, maxv in [
                ("Demand", "Demand /30", 30),
                ("Trade access", "Trade /20", 20),
                ("Product fit", "Fit /20", 20),
                ("Logistics", "Logistics /15", 15),
                ("Execution readiness", "Execution Readiness /15", 15),
            ]:
                val = num(r.get(field)); st.caption(f"{label}: {val:.0f}/{maxv}"); st.progress(min(max(val / maxv, 0), 1.0))
        if r.get("Data Confidence") == "Low":
            panel("Research gate", "This market has low data confidence. Verify import demand, tariff treatment, buyer universe and payment conditions before allocating meaningful outbound volume.", "warn")
        st.caption("Score = internal decision-support heuristic. It is not a sovereign-risk rating, a sales forecast or a guarantee of tariff preference.")

elif page == "SWOT & Positioning":
    panel("Master positioning", "<b>Cards Club — a regional design-to-deck manufacturing partner for brands, distributors, retailers, hotels and destinations across the Middle East and Africa.</b>", allow_html=True)
    st.write("**Architecture:** Core · Heritage · Destinations · Seasons · BrandLab · Collector")
    a, b = st.columns(2)
    for idx, key in enumerate(["Strengths", "Weaknesses", "Opportunities", "Threats"]):
        target = a if idx % 2 == 0 else b
        kind = "good" if key in ["Strengths", "Opportunities"] else "risk"
        with target:
            items = "<ul>" + "".join(f"<li>{escape(x)}</li>" for x in SWOT[key]) + "</ul>"
            panel(key, items, kind, allow_html=True)
    panel("Competitive frame", "Do not compete as the cheapest deck. Position Cards Club between anonymous commodity supply and expensive imported premium brands: closer, flexible, customizable, culturally relevant and export-oriented.", "warn")

elif page == "Products & Offers":
    products = load_csv("products.csv")
    st.subheader("Product & offer architecture")
    st.dataframe(products, use_container_width=True, hide_index=True)
    a, b = st.columns(2)
    with a: panel("Margin priority", "BrandLab → Destination → Heritage → Core")
    with b: panel("Volume priority", "Core → Private Label → Tourism/Destination → Heritage")
    panel("Commercial ladder", "Trial MOQ → Standard MOQ → Strategic Distributor MOQ. Quote EXW → FOB → CIF with freight separated and short validity when FX/freight are volatile.", "warn")
    panel("Pricing control", "Any internal working price marked unverified must not be sent to a buyer until COGS, pack configuration, Incoterm, MOQ and validity are approved.", "risk")

elif page == "Golden 1000":
    golden = load_csv("golden1000.csv")
    st.subheader("Golden 1000 account model")
    st.dataframe(golden, use_container_width=True, hide_index=True)
    total = sum(int(num(r.get("Target Accounts"))) for r in golden)
    st.metric("Planned accounts", f"{total:,}")
    wave = [
        {"Market":"UAE","Accounts":100,"Primary angle":"Distributor + BrandLab + Hospitality"},
        {"Market":"Saudi Arabia","Accounts":100,"Primary angle":"Distributor + BrandLab + Ramadan"},
        {"Market":"South Africa","Accounts":70,"Primary angle":"Distributor + Retail + Private Label"},
        {"Market":"Kuwait","Accounts":50,"Primary angle":"Premium retail + corporate gifting"},
        {"Market":"Morocco","Accounts":50,"Primary angle":"Tourism + distributor"},
        {"Market":"Qatar","Accounts":40,"Primary angle":"Hospitality + corporate"},
    ]
    st.markdown("### Wave 1 allocation")
    st.dataframe(wave, hide_index=True, use_container_width=True)
    panel("Outbound operating rule", "No 1,000-contact blast. Split by country × segment × offer. Start with 1–2 decision makers per company and optimize positive reply, RFQ and sample rates.", "warn")

elif page == "Commercial Calculator":
    st.subheader("Commercial & landed-cost scenario calculator")
    panel("Use", "This is a scenario tool for internal decision-making. Customs duty, import VAT/tax treatment, recoverability, destination fees and Incoterms must be verified before buyer quotation.", "warn")
    a, b, c = st.columns(3)
    qty = a.number_input("Units", min_value=1, value=1000, step=100)
    exw_unit = b.number_input("EXW unit price (USD)", min_value=0.0, value=2.35, step=0.05, format="%.2f")
    freight = c.number_input("Freight (USD)", min_value=0.0, value=450.0, step=50.0)
    a2, b2, c2 = st.columns(3)
    insurance = a2.number_input("Insurance (USD)", min_value=0.0, value=25.0, step=5.0)
    duty_pct = b2.number_input("Customs duty %", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
    import_tax_pct = c2.number_input("Import VAT/tax %", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
    a3, b3, c3 = st.columns(3)
    fixed_fees = a3.number_input("Clearance / destination fixed fees (USD)", min_value=0.0, value=150.0, step=25.0)
    distributor_margin = b3.number_input("Distributor gross margin %", min_value=0.0, max_value=90.0, value=25.0, step=1.0)
    retailer_margin = c3.number_input("Retailer gross margin %", min_value=0.0, max_value=90.0, value=35.0, step=1.0)
    goods = qty * exw_unit
    customs_base = goods + freight + insurance
    duty = customs_base * duty_pct / 100.0
    tax_base = customs_base + duty
    import_tax = tax_base * import_tax_pct / 100.0
    landed_total = goods + freight + insurance + duty + import_tax + fixed_fees
    landed_unit = landed_total / qty if qty else 0
    distributor_sell = calc_margin_sell(landed_unit, distributor_margin)
    retail_sell = calc_margin_sell(distributor_sell, retailer_margin)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Goods value", f"${goods:,.2f}")
    c2.metric("Estimated landed total", f"${landed_total:,.2f}")
    c3.metric("Estimated landed / unit", f"${landed_unit:,.2f}")
    c4.metric("Indicative retail / unit", f"${retail_sell:,.2f}")
    st.dataframe([
        {"Layer":"EXW goods","Total USD":round(goods,2),"Per unit USD":round(exw_unit,2)},
        {"Layer":"Freight + insurance","Total USD":round(freight+insurance,2),"Per unit USD":round((freight+insurance)/qty,2)},
        {"Layer":"Customs duty","Total USD":round(duty,2),"Per unit USD":round(duty/qty,2)},
        {"Layer":"Import VAT/tax","Total USD":round(import_tax,2),"Per unit USD":round(import_tax/qty,2)},
        {"Layer":"Fixed destination fees","Total USD":round(fixed_fees,2),"Per unit USD":round(fixed_fees/qty,2)},
        {"Layer":"Landed cost","Total USD":round(landed_total,2),"Per unit USD":round(landed_unit,2)},
        {"Layer":"Distributor sell-out target","Total USD":"—","Per unit USD":round(distributor_sell,2)},
        {"Layer":"Indicative retail target","Total USD":"—","Per unit USD":round(retail_sell,2)},
    ], use_container_width=True, hide_index=True)
    st.caption("Margin calculation assumes gross margin on selling price, not markup on cost. Import VAT may be recoverable in some jurisdictions; this calculator does not treat recoverability as a fact.")

elif page == "Export Readiness":
    st.subheader("Export readiness control room")
    total_items = sum(len(v) for v in READINESS.values())
    completed = 0
    for category, items in READINESS.items():
        st.markdown(f"### {category}")
        for idx, item in enumerate(items):
            if st.checkbox(item, key=f"ready-{category}-{idx}"):
                completed += 1
    pct = completed / total_items if total_items else 0
    st.progress(pct)
    st.metric("Readiness completion", f"{completed}/{total_items} · {pct*100:.0f}%")
    if pct < .6:
        panel("Status", "Do not scale outbound yet. Close master-data, origin, pricing, payment and QC gaps first.", "risk")
    elif pct < .85:
        panel("Status", "Pilot outreach is possible, but shipment commitments should remain gated by unresolved compliance/quality controls.", "warn")
    else:
        panel("Status", "Operational readiness is strong enough for controlled scaling, subject to country-specific customs and buyer due diligence.", "good")
    st.caption("This checklist is session-based and does not replace signed operating records or document-control systems.")

elif page == "90-Day Roadmap":
    roadmap = load_csv("roadmap.csv")
    st.subheader("90-day export execution")
    st.dataframe(roadmap, use_container_width=True, hide_index=True)
    for r in roadmap:
        with st.expander(f"Phase {r.get('Phase')} · {r.get('Timing')} · {r.get('Workstream')}"):
            st.write("**Actions:**", r.get("Actions")); st.write("**Deliverable:**", r.get("Deliverable")); st.write("**Success metric:**", r.get("Success Metric"))
    panel("Gate 1", "No mass outbound before data, security and compliance cleanup.", "risk")
    panel("Gate 2", "No final landed-price promise before origin, freight and destination-customs validation.", "warn")
    panel("Gate 3", "No shipment before payment security, conformity and QC approval.", "risk")

elif page == "Risk Register":
    risks = load_csv("risks.csv")
    st.subheader("Export risk register")
    order = ["Critical", "High", "Medium", "Low"]
    selected = st.multiselect("Severity", order, default=order)
    view = [r for r in risks if r.get("Severity") in selected]
    st.dataframe(view, use_container_width=True, hide_index=True)
    counts = count_by(view, "Severity")
    cols = st.columns(4)
    for col, level in zip(cols, order):
        col.metric(level, counts.get(level,0))
    st.markdown("### Critical + high-risk controls")
    for r in risks:
        if r.get("Severity") in ["Critical", "High"]:
            with st.expander(f"{r.get('ID')} · {r.get('Risk')} — {r.get('Severity')}"):
                st.write("**Impact:**", r.get("Impact")); st.write("**Mitigation:**", r.get("Mitigation")); st.write(f"**Owner:** {r.get('Owner')} · **Gate:** {r.get('Deadline / Gate')}")

elif page == "Customs & Trade":
    trade = load_csv("trade.csv")
    panel("Non-negotiable", "Never market ‘zero customs guaranteed’. Preferential treatment depends on HS classification, current agreement implementation, Rules of Origin, documentary evidence and destination-customs acceptance.", "risk")
    st.dataframe(trade, use_container_width=True, hide_index=True)
    panel("Mirror-data warning", "Trade databases can show exporter-side and importer-side differences. Use them as market evidence, not as audited Cards Club sales or exact company market share.", "warn")
    st.markdown("### Pre-shipment gate")
    checks = ["Confirm destination HS classification", "Confirm applicable agreement + Rules of Origin", "Confirm label / marking / conformity route", "Approve commercial invoice + packing list + COO route", "Confirm payment security + Incoterm", "Approve Golden Sample / batch QC", "Validate freight, insurance, transit time and quote validity"]
    for i, text in enumerate(checks, 1):
        st.checkbox(f"{i}. {text}", key=f"gate-{i}")

elif page == "Email Campaigns":
    st.subheader("7 outbound campaign angles")
    name = st.selectbox("Campaign", list(EMAILS))
    subject, preview, body = EMAILS[name]
    a, b = st.columns(2)
    with a: panel("Subject", subject)
    with b: panel("Preview", preview)
    st.markdown(f'<div class="mono">{escape(body)}</div>', unsafe_allow_html=True)
    st.caption("Treat these as controlled templates. Personalize account context, verify contact data, and keep the first CTA low-friction.")

elif page == "Sales Scenarios":
    st.subheader("90-day sales scenarios")
    st.caption("Operating scenarios, not guaranteed forecasts.")
    scenarios = [
        {"Scenario":"Conservative","Target companies":"1,000","Replies":"15–25","Qualified buyers":"2–5","Pilot POs":"0–1"},
        {"Scenario":"Base","Target companies":"1,000","Replies":"30–50","Qualified buyers":"6–15","Pilot POs":"2–4"},
        {"Scenario":"Strong","Target companies":"1,000","Replies":"50–80+","Qualified buyers":"12–25","Pilot POs":"5–8"},
    ]
    st.dataframe(scenarios, hide_index=True, use_container_width=True)
    panel("KPI tree", "Deliverability → Reply → Positive reply → Qualified buyer → RFQ → Sample → PO → Gross margin → Reorder.")
    panel("72-hour goal", "Buyer interest, catalog/RFQ/sample intent — not assuming closed orders from cold email.", "warn")

elif page == "Files & Sources":
    sources = load_csv("sources.csv")
    st.subheader("Runtime files & source index")
    panel("Deployment architecture", "The dashboard uses small sanitized CSV files for fast startup. The original raw workbook is intentionally not published because it contains sensitive operational / credential / banking-related information.", "warn")
    st.markdown("### Download sanitized runtime data")
    names = ["countries.csv", "products.csv", "risks.csv", "roadmap.csv", "golden1000.csv", "trade.csv", "sources.csv"]
    cols = st.columns(3)
    for i, name in enumerate(names):
        path = DATA / name
        if path.exists():
            with cols[i % 3]:
                st.download_button(f"Download {name}", path.read_bytes(), file_name=name, mime="text/csv", use_container_width=True, key=f"download-{name}")
    st.markdown("### Research & source register")
    st.dataframe(sources, use_container_width=True, hide_index=True)
