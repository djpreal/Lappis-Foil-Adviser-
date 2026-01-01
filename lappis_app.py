import streamlit as st

# Sivun asetukset
st.set_page_config(page_title="Lappis Foil Advaiser Pro", page_icon="🏄‍♂️", layout="wide")

# --- AMMATTIMAINEN TYYLITTELY ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; }
    .main-header { 
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 52px; font-weight: 800; text-align: center; margin-bottom: 0px;
    }
    .stat-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        transition: transform 0.2s;
    }
    .stat-card:hover { border-color: #58a6ff; }
    .category-label { color: #8b949e; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; }
    .value-label { color: #ffffff; font-size: 19px; font-weight: 700; margin-top: 5px; margin-bottom: 10px; }
    .product-list { color: #38bdf8; font-size: 14px; font-weight: 500; line-height: 1.4; }
    .insight-box {
        background: rgba(56, 189, 248, 0.05);
        border-radius: 12px;
        padding: 20px;
        border: 1px dashed #38bdf8;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">Lappis Foil Advaiser</div>', unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #8b949e; margin-bottom: 30px;'>Asiantuntijan konfiguraattori</p>", unsafe_allow_html=True)

# --- SYÖTTEET ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1: laji = st.selectbox("Laji", ["Wingfoil", "Pumpfoil", "eFoil", "SUPfoil"])
    with c2: taso = st.select_slider("Taso", options=["Aloittelija", "Keskitaso", "Pro"])
    with c3: paino = st.number_input("Paino (kg)", 30, 150, 85)
    with c4: pituus = st.number_input("Pituus (cm)", 100, 220, 180)

st.markdown("<br>", unsafe_allow_html=True)

# --- LOGIIKKA ---
# Alustus
lauta_malli = ""; vol = 0; siivet = ""; masto = ""; wing_koko = ""; wing_malli = ""; insight = ""

if laji == "Pumpfoil":
    vol = 35 if taso == "Aloittelija" else 25 if taso == "Keskitaso" else 15
    lauta_malli = "Duotone Sky Surf" if taso != "Aloittelija" else "Duotone Sky Style"
    siivet = "• Sabfoil Leviathan 1550/1350<br>• Duotone Aero Glide 1595"
    masto = "73cm Kraken Carbon"
    wing_koko = "N/A"
    wing_malli = "Ei käytössä"
    insight = "Pumpfoilissa painotus on mahdollisimman pienessä laudassa ja suuressa High Aspect -etusiivessä."

elif laji == "Wingfoil":
    # Lauta
    if taso == "Aloittelija":
        lauta_malli = "Duotone Sky Free / Sabfoil Medusa"
        vol = int(paino + 40)
        siivet = "• Sabfoil Tortuga 1250<br>• Duotone Aero Lift 2400"
    else:
        lauta_malli = "Duotone Sky Style SLS"
        vol = int(paino + 5) if taso == "Keskitaso" else int(paino - 15)
        siivet = "• Sabfoil Medusa Pro 869<br>• Duotone Aero Carve 2.0"
    
    # Masto
    masto = "82cm Carbon" if pituus > 180 or taso != "Aloittelija" else "75cm Aluminum/Carbon"
    
    # Wing-purje
    wing_malli = "Duotone Unit / Slick"
    if paino < 65: wing_koko = "4.0m"
    elif paino < 85: wing_koko = "5.0m"
    else: wing_koko = "6.0m"
    
    insight = f"Wingfoilissa {paino}kg kuskille {wing_koko} siipi on optimaalinen yleiskoko Suomen olosuhteisiin."

# --- NELJÄN KORTIN DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">🌊 Lauta</div>
        <div class="value-label">{lauta_malli}</div>
        <div class="product-list">Tilavuus: {vol}L</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">🦅 Foili (Etusiipi)</div>
        <div class="value-label">Sabfoil / Duotone</div>
        <div class="product-list">{siivet}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">🪁 Wing-siipi (Purje)</div>
        <div class="value-label">{wing_koko}</div>
        <div class="product-list">{wing_malli}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">📏 Tekniikka</div>
        <div class="value-label">Masto & Riki</div>
        <div class="product-list">Pituus: {masto}<br>Painoarvio: {paino}kg</div>
    </div>""", unsafe_allow_html=True)

# --- ALAOIKEIN INSIGHT ---
st.markdown(f"""
<div class="insight-box">
    <h4 style="margin-top:0; color:#38bdf8; font-size:16px;">Lappis Expert Insight</h4>
    <p style="color:white; font-size:14px; margin-bottom:0;">{insight} Suosittelemme tarkistamaan saatavuuden myymälästä tälle kokoonpanolle.</p>
</div>
""", unsafe_allow_html=True)

# Latausnappi
raportti = f"LAPPIS FOIL ADVAISER\nLaji: {laji}\nLauta: {lauta_malli} ({vol}L)\nFoili: {siivet.replace('<br>', ' ')}\nWing: {wing_malli} {wing_koko}\nMasto: {masto}"
st.download_button("📥 Lataa kokoonpano (.txt)", raportti, file_name=f"lappis_config_{laji}.txt")
