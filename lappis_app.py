import streamlit as st

# Sivun asetukset
st.set_page_config(page_title="Lappis Foil Advaiser Pro", page_icon="🏄‍♂️", layout="wide")

# --- TYYLITTELY ---
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
st.write("<p style='text-align: center; color: #8b949e; margin-bottom: 30px;'>Premium Gear Configurator</p>", unsafe_allow_html=True)

# --- SYÖTTEET ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1: laji = st.selectbox("Valitse Laji", ["Wingfoil", "Pumpfoil", "eFoil", "SUPfoil"])
    with c2: taso = st.select_slider("Taitotaso", options=["Aloittelija", "Keskitaso", "Pro"])
    with c3: paino = st.number_input("Paino (kg)", 30, 150, 85)
    with c4: pituus = st.number_input("Pituus (cm)", 100, 220, 180)

st.divider()

# --- LAAJENNETTU LOGIIKKA LAJEITTAIN ---

# Alustus oletusarvoilla
lauta_malli = ""; vol = 0; siivet = ""; masto = ""; extra_info_label = ""; extra_info_val = ""; insight = ""

# 1. WINGFOIL
if laji == "Wingfoil":
    extra_info_label = "🪁 Wing-siipi"
    if taso == "Aloittelija":
        lauta_malli = "Duotone Sky Free / Sabfoil Medusa 110"
        vol = int(paino + 45)
        siivet = "• Sabfoil Tortuga 1250<br>• Duotone Aero Lift 2400"
        masto = "75cm Aluminum/Carbon"
    else:
        lauta_malli = "Duotone Sky Style SLS / Sabfoil Torpedo"
        vol = int(paino + 5) if taso == "Keskitaso" else int(paino - 15)
        siivet = "• Sabfoil Medusa Pro 869 / 969<br>• Duotone Aero Carve 2.0"
        masto = "82cm - 90cm Carbon"
    
    wk = "4.0m" if paino < 65 else "5.0m" if paino < 85 else "6.0m"
    extra_info_val = f"Unit / Slick {wk}"
    insight = "Wingfoilissa tilavuus takaa helpon startin. Mitä kokeneempi olet, sitä pienemmän laudan voit valita."

# 2. PUMPFOIL
elif laji == "Pumpfoil":
    extra_info_label = "⏱️ Arvioitu Lentoaika"
    masto = "73cm Sabfoil Kraken"
    if taso == "Aloittelija":
        lauta_malli = "Duotone Sky Style 4'11\""
        vol = 35
        siivet = "• Sabfoil Leviathan 1550<br>• Duotone Aero Glide 1595"
        extra_info_val = "10-30 sekuntia"
    else:
        lauta_malli = "Duotone Sky Surf 4'2\" / 3'9\""
        vol = 25 if taso == "Keskitaso" else 15
        siivet = "• Sabfoil Leviathan 1350 / 1150<br>• Sabfoil Blade 82"
        extra_info_val = "60+ sekuntia"
    insight = "Pumpfoilissa lauta on kevyt heiluri. Pieni litramäärä (15-35L) on välttämätön pumppaustehon säilyttämiseksi."

# 3. EFOIL
elif laji == "eFoil":
    extra_info_label = "⚡ Sähköjärjestelmä"
    lauta_malli = "Audi e-tron Foil by Aerofoils"
    vol = int(paino + 25)
    masto = "80cm Integrated"
    siivet = "• Aero Lift 2400 (Vakaa)<br>• Aero Glide 1305 (Nopea)"
    extra_info_val = "5kW Brushless / 2.8kWh Akku"
    insight = "Audi e-tron järjestelmä on markkinoiden hiljaisin. 2.8kWh akku tarjoaa jopa 120min ajoaikaa."

# 4. SUPFOIL
elif laji == "SUPfoil":
    extra_info_label = "🛶 Melasuositus"
    # SUP-foilaus vaatii suuren tilavuuden jotta laudalla voi seistä ja meloa vauhtia
    if taso == "Aloittelija":
        lauta_malli = "Duotone Sky Brid / Sky Free"
        vol = int(paino + 55)
        siivet = "• Sabfoil Leviathan 1750 / 1550"
    else:
        lauta_malli = "Duotone Sky Style (Large sizes)"
        vol = int(paino + 30)
        siivet = "• Sabfoil Leviathan 1350<br>• Duotone Aero Glide 1595"
    masto = "75cm - 82cm Carbon"
    extra_info_val = "Full Carbon Fixed Paddle"
    insight = "SUP-foilaus vaatii huomattavasti enemmän litroja kuin Wingfoil, koska melonta tapahtuu seisten ilman wingin antamaa tukea."

# --- NELJÄN KORTIN DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">🌊 Lauta</div>
        <div class="value-label">{lauta_malli}</div>
        <div class="product-list">Suositeltu tilavuus: {vol}L</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">🦅 Foili (Etusiipi)</div>
        <div class="value-label">Sabfoil / Duotone</div>
        <div class="product-list">{siivet}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">{extra_info_label}</div>
        <div class="value-label">{extra_info_val}</div>
        <div class="product-list">Lajikohtainen varuste</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class="stat-card">
        <div class="category-label">📏 Tekniset tiedot</div>
        <div class="value-label">{masto}</div>
        <div class="product-list">Masto & Rikiarvio<br>Käyttäjä: {paino}kg</div>
    </div>""", unsafe_allow_html=True)

# --- INSIGHT BOX ---
st.markdown(f"""
<div class="insight-box">
    <h4 style="margin-top:0; color:#38bdf8; font-size:16px;">Lappis Expert Insight</h4>
    <p style="color:white; font-size:14px; margin-bottom:0;">{insight}</p>
</div>
""", unsafe_allow_html=True)

# Latausnappi
raportti = f"LAPPIS FOIL ADVAISER - RAPORTTI\nLaji: {laji}\nLauta: {lauta_malli} ({vol}L)\nFoili: {siivet.replace('<br>', ' ')}\nInfo: {extra_info_val}\nMasto: {masto}"
st.download_button("📥 Lataa analyysi", raportti, file_name=f"lappis_advisor_{laji}.txt")
