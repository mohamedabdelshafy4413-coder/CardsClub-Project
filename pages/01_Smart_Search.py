from pathlib import Path
import csv
import io
import math
import re
import unicodedata
from difflib import SequenceMatcher
from html import escape
import streamlit as st

st.set_page_config(page_title="Cards Club Smart Search", page_icon="🔎", layout="wide")
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

st.markdown("""
<style>
html,body,[data-testid="stAppViewContainer"]{background:#fbfdfb;color:#101410}
[data-testid="stSidebar"]{background:#0b0e0c;border-right:1px solid #d9e4dc}
[data-testid="stSidebar"] *{color:#f6fff8}
.block-container{max-width:1700px;padding-top:1rem;padding-bottom:2rem}
.hero{background:linear-gradient(135deg,#080b09,#111713 70%,#a6f3b5 180%);border:1px solid #27352b;border-radius:22px;padding:24px 28px;color:white;margin-bottom:16px}
.hero h1{margin:4px 0;color:#fff}.hero p{margin:6px 0 0;color:#dce8df}.tag{display:inline-block;background:#c9ffd5;color:#07150b;border-radius:999px;padding:5px 10px;margin-right:5px;font-size:.75rem;font-weight:800}
.card{background:#fff;border:1px solid #dce7df;border-radius:15px;padding:15px 17px;box-shadow:0 5px 16px rgba(10,30,18,.045);margin:.45rem 0}.muted{font-size:.82rem;color:#69766d}.score{font-size:1.35rem;font-weight:900;color:#102016}.bar{height:9px;background:#edf2ee;border-radius:99px;overflow:hidden}.fill{height:9px;background:#a6f3b5;border-radius:99px}.code{direction:ltr;text-align:left;font-family:monospace;white-space:pre-wrap;background:#0c120e;color:#dfffea;border-radius:11px;padding:12px}
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_csv(name):
    p = DATA / name
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

ARABIC_DIACRITICS = re.compile(r"[\u0617-\u061A\u064B-\u0652\u0670\u06D6-\u06ED]")

def normalize(value):
    s = str(value or "").strip().lower()
    s = ARABIC_DIACRITICS.sub("", s).replace("ـ", "")
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي").replace("ة", "ه")
    s = "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))
    s = re.sub(r"[^\w\u0600-\u06FF]+", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()

@st.cache_data(show_spinner=False)
def market_index():
    rows = load_csv("top50_importer_markets.csv")
    fields = ["Country","Region","Tier","Importer Category","Primary Buyer Roles","Language","Product Focus","Success Band","Data Confidence","Wave","Email Campaign","Email Subject","CTA","Search Keywords","Buyer Search Query EN","Buyer Search Query Local","Recommended Channels","Research Priority"]
    for r in rows:
        r["_search"] = normalize(" | ".join(str(r.get(f, "")) for f in fields))
        r["_country"] = normalize(r.get("Country"))
        r["_category"] = normalize(r.get("Importer Category"))
        r["_product"] = normalize(r.get("Product Focus"))
    return rows

@st.cache_data(show_spinner=False)
def knowledge_index():
    specs = [
        ("Products", "products.csv"),
        ("Risks", "risks.csv"),
        ("Roadmap", "roadmap.csv"),
        ("Trade", "trade.csv"),
        ("Sources", "sources.csv"),
    ]
    out=[]
    for kind,name in specs:
        for row in load_csv(name):
            row=dict(row); row["_type"]=kind; row["_search"]=normalize(" | ".join(str(v) for v in row.values())); out.append(row)
    return out

def n(v, default=0.0):
    try:
        if v in (None, "", "nan", "NaN"): return default
        return float(v)
    except Exception:
        return default

def relevance(row, query, mode="Smart"):
    q=normalize(query)
    if not q: return 0.0
    text=row.get("_search","")
    tokens=[t for t in q.split() if len(t)>1]
    if mode=="Exact phrase":
        return 100.0 if q in text else 0.0
    if mode=="All words":
        return 100.0 if tokens and all(t in text for t in tokens) else 0.0
    exact=55 if q in text else 0
    token_ratio=(sum(1 for t in tokens if t in text)/len(tokens)*30) if tokens else 0
    country=SequenceMatcher(None,q,row.get("_country","")).ratio()*15
    category=SequenceMatcher(None,q,row.get("_category","")).ratio()*8
    product=SequenceMatcher(None,q,row.get("_product","")).ratio()*8
    return min(100.0, exact+token_ratio+max(country,category,product))

def table_csv(rows, fields):
    sio=io.StringIO(); w=csv.DictWriter(sio,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows); return sio.getvalue().encode("utf-8-sig")

def email_for(r):
    country=r.get("Country","{{Country}}")
    company="{{Company}}"; first="{{FirstName}}"
    camp=r.get("Email Campaign","")
    if camp=="Seasonal / Ramadan":
        return f"Hi {first},\n\nCards Club manufactures premium playing-card editions in Egypt for branded gifting and campaigns. We would like to explore a Ramadan edition for {company} in {country}, covering artwork, packaging and production.\n\nWould you like us to send a visual direction and indicative MOQ?\n\nBest,\nCards Club BrandLab"
    if camp=="Corporate BrandLab":
        return f"Hi {first},\n\nCards Club manufactures custom playing-card decks in Egypt for brands and corporate gifting. A deck gives {company} 52 usable branded touchpoints plus custom packaging.\n\nWould you like a visual concept for {country}?\n\nBest,\nCards Club BrandLab"
    if camp=="Tourism / Souvenir":
        return f"Hi {first},\n\nCards Club creates destination playing-card decks around landmarks, culture and local stories. We would like to explore a {country} edition with {company} for tourism, hospitality or souvenir retail.\n\nShould I send a sample concept?\n\nBest,\nCards Club Export Team"
    if camp=="Regional Supplier Alternative":
        return f"Hi {first},\n\nCards Club manufactures standard and custom playing cards in Egypt. If {company} currently sources from Asia or Europe, we can prepare a like-for-like regional supply comparison for {country}.\n\nIf you share your current specification, I can prepare the comparison.\n\nBest,\nCards Club Export Team"
    return f"Hi {first},\n\nCards Club manufactures premium playing cards in Egypt for retail, distribution and private-label programs. We are opening selected partner conversations in {country}, and {company} looks relevant.\n\nWould it be useful if I sent our range, MOQ and export-pricing structure?\n\nBest,\nCards Club Export Team"

st.markdown('<div class="hero"><span class="tag">SMART SEARCH</span><span class="tag">AR / EN / FR / PT</span><span class="tag">TOP 50</span><h1>Cards Club Market Search Engine</h1><p>Search countries, importer types, buyer roles, products, languages and campaign angles — with evidence filters and export-opportunity scoring.</p></div>',unsafe_allow_html=True)

tab1,tab2=st.tabs(["Importer-market search","Knowledge search"])

with tab1:
    rows=market_index()
    qcol,modecol=st.columns([3,1])
    query=qcol.text_input("Search",placeholder="Examples: السعودية · UAE hotels · French distributors · private label · tourism · Ramadan")
    mode=modecol.selectbox("Search mode",["Smart","All words","Exact phrase"])

    quick=st.selectbox("Quick intent",["All markets","Wave 1 only","Distributors","Corporate gifting / private label","Tourism / hotels / souvenirs","French-speaking markets","Arabic-speaking markets","High-confidence only","Research-first markets"])
    f1,f2,f3,f4=st.columns(4)
    regions=f1.multiselect("Region",["GCC","Africa"],default=["GCC","Africa"])
    waves=f2.multiselect("Wave",["Wave 1","Wave 2","Discovery"],default=["Wave 1","Wave 2","Discovery"])
    conf=f3.multiselect("Data confidence",["High","Medium","Low"],default=["High","Medium","Low"])
    min_score=f4.slider("Min opportunity score",0,100,0,5)
    f5,f6,f7=st.columns(3)
    categories=sorted({r.get("Importer Category","") for r in rows if r.get("Importer Category")})
    selected_categories=f5.multiselect("Importer category",categories,default=categories)
    sort_by=f6.selectbox("Sort by",["Relevance","Opportunity score","Import value","Market rank"])
    page_size=f7.selectbox("Rows per page",[10,20,50],index=1)

    results=[]
    for r in rows:
        if r.get("Region") not in regions or r.get("Wave") not in waves or r.get("Data Confidence") not in conf: continue
        if r.get("Importer Category") not in selected_categories: continue
        if n(r.get("Opportunity Score /100",r.get("Export Success Index %"))) < min_score: continue
        text=r.get("_search","")
        if quick=="Wave 1 only" and r.get("Wave")!="Wave 1": continue
        if quick=="Distributors" and "distributor" not in text: continue
        if quick=="Corporate gifting / private label" and not any(x in text for x in ["private label","corporate gifting","promotional"]): continue
        if quick=="Tourism / hotels / souvenirs" and not any(x in text for x in ["tourism","hotel","souvenir","hospitality"]): continue
        if quick=="French-speaking markets" and "french" not in text: continue
        if quick=="Arabic-speaking markets" and "arabic" not in text: continue
        if quick=="High-confidence only" and r.get("Data Confidence")!="High": continue
        if quick=="Research-first markets" and r.get("Research Priority")!="Research-first": continue
        rel=relevance(r,query,mode) if query else 0.0
        if query and rel<=0: continue
        x=dict(r); x["Relevance %"]=round(rel,1); results.append(x)

    if sort_by=="Relevance" and query: results.sort(key=lambda r:(n(r.get("Relevance %")),n(r.get("Opportunity Score /100"))),reverse=True)
    elif sort_by=="Opportunity score" or (sort_by=="Relevance" and not query): results.sort(key=lambda r:n(r.get("Opportunity Score /100")),reverse=True)
    elif sort_by=="Import value": results.sort(key=lambda r:n(r.get("HS950440 Import USD"),-1),reverse=True)
    else: results.sort(key=lambda r:n(r.get("Market Rank"),999))

    m1,m2,m3,m4=st.columns(4)
    m1.metric("Matches",len(results)); m2.metric("Wave 1",sum(r.get("Wave")=="Wave 1" for r in results)); m3.metric("High confidence",sum(r.get("Data Confidence")=="High" for r in results)); m4.metric("Avg opportunity score",f"{sum(n(r.get('Opportunity Score /100')) for r in results)/len(results):.0f}/100" if results else "—")

    if results:
        max_page=max(1,math.ceil(len(results)/page_size)); page=st.number_input("Page",1,max_page,1,1)
        shown=results[(page-1)*page_size:page*page_size]
        fields=["Success Rank","Market Rank","Country","Region","Importer Category","Primary Buyer Roles","Language","Product Focus","Opportunity Score /100","Data Confidence","Wave","Research Priority","Email Campaign","Relevance %"]
        st.dataframe([{k:r.get(k,"") for k in fields} for r in shown],use_container_width=True,hide_index=True)
        st.download_button("Download filtered market results",table_csv(results,[c for c in rows[0].keys() if not c.startswith("_")]),file_name="cardsclub_market_search_results.csv",mime="text/csv",use_container_width=True)

        st.markdown("### Market drill-down")
        country=st.selectbox("Select market",[r.get("Country") for r in results])
        r=next(x for x in results if x.get("Country")==country)
        c1,c2,c3,c4,c5=st.columns(5)
        c1.metric("Opportunity",f"{int(n(r.get('Opportunity Score /100')))} / 100")
        c2.metric("Success rank",r.get("Success Rank")); c3.metric("Market rank",r.get("Market Rank")); c4.metric("Wave",r.get("Wave")); c5.metric("Confidence",r.get("Data Confidence"))
        score=int(n(r.get("Opportunity Score /100"))); st.markdown(f'<div class="bar"><div class="fill" style="width:{max(0,min(score,100))}%"></div></div>',unsafe_allow_html=True)
        a,b=st.columns(2)
        with a:
            st.write("**Importer category:**",r.get("Importer Category")); st.write("**Buyer roles:**",r.get("Primary Buyer Roles")); st.write("**Language:**",r.get("Language")); st.write("**Product focus:**",r.get("Product Focus")); st.write("**Recommended channels:**",r.get("Recommended Channels")); st.write("**Research priority:**",r.get("Research Priority"))
        with b:
            st.write("**Campaign:**",r.get("Email Campaign")); st.write("**Subject:**",r.get("Email Subject")); st.write("**CTA:**",r.get("CTA")); st.write("**Buyer search query — EN:**"); st.code(r.get("Buyer Search Query EN",""),language=None); st.write("**Buyer search query — local:**"); st.code(r.get("Buyer Search Query Local",""),language=None)
        st.caption(r.get("Metric Note","Internal opportunity score; not a probability of sale."))
        st.markdown("#### Ready-to-personalize email")
        st.markdown(f'<div class="code">{escape(email_for(r))}</div>',unsafe_allow_html=True)
    else:
        st.info("No matches. Broaden filters or use Smart search mode.")

with tab2:
    knowledge=knowledge_index()
    q=st.text_input("Search the project knowledge base",placeholder="Examples: MOQ, customs, humidity, BrandLab, Saber, payment, Morocco")
    types=st.multiselect("Search in",["Products","Risks","Roadmap","Trade","Sources"],default=["Products","Risks","Roadmap","Trade","Sources"])
    if q:
        out=[]
        qn=normalize(q); tokens=qn.split()
        for r in knowledge:
            if r.get("_type") not in types: continue
            text=r.get("_search","")
            matches=sum(1 for t in tokens if t in text)
            if qn in text or matches:
                score=(60 if qn in text else 0)+(matches/max(1,len(tokens))*40)
                x={k:v for k,v in r.items() if not k.startswith("_")}; x["Type"]=r.get("_type"); x["Relevance %"]=round(score,1); out.append(x)
        out.sort(key=lambda x:x.get("Relevance %",0),reverse=True)
        st.metric("Knowledge matches",len(out)); st.dataframe(out[:50],use_container_width=True,hide_index=True)
    else:
        st.info("Search across Products, Risks, 90-Day Roadmap, Customs/Trade and Sources from one box.")

st.caption("Performance design: cached CSV loading, cached normalized search index, no Pandas/Plotly dependency, pagination before rendering, and query scoring only after filters are applied.")
