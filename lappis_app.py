import streamlit as st

# Sivun asetukset - Moderni tumma teema
st.set_page_config(page_title="Lappis Foil Advaiser Pro", page_icon="🏄‍♂️", layout="wide")

# --- AMMATTIMAINEN TYYLITTELY (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; }
    
    /* Pääotsikko */
    .main-header { 
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 52px; font-weight: 800; text-align: center; margin-bottom: 0px;
    }
    
    /* Kortit */
    .stat-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.3s;
    }
    .stat-card:hover { border-color: #58a6ff; transform: translateY(-5px); }
    
    .category-label { color: #8b949e; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .value-label { color: #ffffff; font-size: 20px; font-weight: 700; margin-top: 5px; }
    .product-list { color: #38bdf8; font-size: 16px; font-weight: 500; margin-top: 10px; line-height: 1.4; }

    /* Expert Insight Box */
    .insight-box {
        background: rgba(56, 189, 248, 0.1);
        border-radius: 12px;
        padding: 25px;
        border-left: 6px solid #38bdf8;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- YLÄOSA ---
st.markdown('<div class="main-header">Lappis Foil Advaiser</div>', unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #8b949e;'>Premium Gear Configurator v4.0</p>", unsafe_allow_html=True)

# --- SYÖTTEET (Sivupalkissa tai ylhäällä) ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1: laji = st.selectbox("Laji", ["Wingfoil", "Pumpfoil", "eFoil", "SUPfoil"])
    with c2: taso = st.select_slider("Taso", options=["Aloittelija", "Keskitaso", "Pro"])
    with c3: paino = st.number_input("Paino (kg)", 30, 150, 85)
    with c4: pituus = st.number_input("Pituus (cm)", 100, 220, 180)

st.markdown("<br>", unsafe_allow_html=True)

# --- LOGIIKKA (Sama korjattu logiikka) ---
if laji == "Pumpfoil":
    vol = 30 if taso == "Aloittelija" else 20 if taso == "Keskitaso" else 15
    lauta = "Duotone Sky Surf" if taso != "Aloittelija" else "Duotone Sky Style"
    siivet = "Sabfoil Leviathan 1550 / 1350<br>Duotone Aero Glide 1595"
    masto = "73cm Kraken Carbon"
    profiili = "Ultra-High Aspect"
    wing_koko = "N/A"
else:
    vol = int(paino + (40 if taso == "Aloittelija" else 5))
    lauta = "Duotone Sky Free" if taso == "Aloittelija" else "Duotone Sky Style SLS"
    siivet = "Sabfoil Medusa Pro / Razor<br>Duotone Aero Free / Carve"
    masto = "82cm Carbon" if pituus > 180 else "75cm Carbon"
    profiili = "High / Medium Aspect"
    wing_koko = "5.0m" if paino < 85 else "6.0m"

# --- TULOSTUS (Dashboard-näkymä) ---
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">🌊 Lautasuositus</div>
        <div class="value-label">{lauta}</div>
        <div class="product-list">Tilavuus: {vol}L</div>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">🦅 Foil-setti</div>
        <div class="value-label">{profiili}</div>
        <div class="product-list">{siivet}</div>
    </div>""", unsafe_allow_html=True)

with col_c:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">📏 Tekniset tiedot</div>
        <div class="value-label">Masto: {masto}</div>
        <div class="product-list">Wing-koko: {wing_koko}</div>
    </div>""", unsafe_allow_html=True)

# --- EXPERT INSIGHT ---
st.markdown(f"""
<div class="insight-box">
    <h3 style="margin-top:0; color:#38bdf8;">Lappis Expert Insight</h3>
    <p style="font-size:16px;">Paino-pituussuhteesi perusteella ({paino}kg / {pituus}cm) suosittelemme painottamaan 
    <b>{profiili}</b> profiilia, joka tarjoaa optimaalisen nosteen ja hallinnan tässä taitotasossa. 
    Lauta <b>{lauta}</b> antaa tarvittavan vakauden startteihin.</p>
</div>
""", unsafe_allow_html=True)
