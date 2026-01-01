import streamlit as st

# Sivun asetukset
st.set_page_config(page_title="Lappis Foil Advaiser", page_icon="🏄‍♂️", layout="centered")

# --- TYYLITTELY ---
st.markdown("""
    <style>
    .stApp { background-color: #050508; }
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    .main-header { color: #38bdf8; font-size: 42px; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .result-box { 
        background-color: #1e293b; 
        padding: 25px; 
        border-radius: 15px; 
        border: 2px solid #38bdf8;
        color: #ffffff !important;
        font-size: 18px;
        line-height: 1.6;
    }
    .expert-card { 
        background-color: #0f172a; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 10px solid #38bdf8; 
        margin-top: 20px;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">Lappis Foil Advaiser</div>', unsafe_allow_html=True)

# --- SYÖTTEET ---
col1, col2 = st.columns(2)

with col1:
    laji = st.selectbox("Valitse Laji", ["Wingfoil", "Pumpfoil", "eFoil", "SUPfoil"])
    taso = st.select_slider("Taso", options=["Aloittelija", "Keskitaso", "Pro"])

with col2:
    paino = st.number_input("Paino (kg)", 30, 150, 85)
    pituus = st.number_input("Pituus (cm)", 100, 220, 180)

st.divider()

# --- TIETOKANTA JA LOGIIKKA ---

# Alustetaan muuttujat tyhjiksi
lauta_malli = ""
siivet = ""
masto = 0
volyymi = 0
wing_info = ""

if laji == "Pumpfoil":
    # Pakotetaan Pumpfoil-logiikka
    masto = 73 # Sabfoil Kraken standardi pumpulle
    if taso == "Aloittelija":
        lauta_malli = "Duotone Sky Style 4'11\" tai Sabfoil Torpedo"
        volyymi = 35
        siivet = "• Sabfoil LEVIATHAN 1550 (Suositus)<br>• Duotone Aero Glide 1595 / 1305<br>• Sabfoil SIREN 1350"
    elif taso == "Keskitaso":
        lauta_malli = "Duotone Sky Surf 4'2\" tai Sabfoil Torpedo 100"
        volyymi = 25
        siivet = "• Sabfoil LEVIATHAN 1350 / 1150<br>• Sabfoil SIREN 1350<br>• Duotone Aero Glide 1085"
    else: # Pro
        lauta_malli = "Duotone Sky Surf 3'9\" (Carbon)"
        volyymi = 15
        siivet = "• Sabfoil LEVIATHAN 950 / 1150<br>• Sabfoil BLADE 82<br>• Duotone Aero Glide 905"
    
    insight = "Pumpfoilissa laudan on oltava mahdollisimman pieni (15-35L). Sky Surf on täydellinen valinta heiluripainon minimoimiseksi."
    profiili = "Ultra-High Aspect"

elif laji == "Wingfoil":
    # Wingfoil-laudat ja -siivet
    if taso == "Aloittelija":
        lauta_malli = "Duotone Sky Free tai Sabfoil Medusa 110"
        volyymi = int(paino + 40)
        siivet = "• Sabfoil TORTUGA 1250 / 1100<br>• Duotone Aero Lift 2400 / Aero Free 2000"
        masto = 75
    elif taso == "Keskitaso":
        lauta_malli = "Duotone Sky Style tai Sabfoil Medusa 80"
        volyymi = int(paino + 5)
        siivet = "• Sabfoil MEDUSA PRO 869 / 969<br>• Duotone Aero Free 1250 / 1000"
        masto = 82
    else: # Pro
        lauta_malli = "Duotone Sky Style SLS tai Sabfoil Torpedo"
        volyymi = int(paino - 15)
        siivet = "• Sabfoil RAZOR 880 / 820<br>• Sabfoil MEDUSA PRO 769<br>• Duotone Aero Carve 2.0"
        masto = 93

    # Wingin koko laskenta
    wk = "4.0m" if paino < 65 else "5.0m" if paino < 85 else "6.0m"
    wing_info = f"<strong>SUOSITELTU WINGI:</strong> Duotone Unit / Slick {wk}<br><br>"
    insight = f"Wingfoilissa laudan ({lauta_malli}) volyymi on kriittinen vakaudelle ennen nousua."
    profiili = "Medium / High Aspect"

elif laji == "eFoil":
    lauta_malli = "Audi e-tron Foil by Aerofoils"
    volyymi = int(paino + 20)
    masto = 80
    siivet = "• Aero Lift 2400 (Standard)<br>• Aero Glide 1305 (Speed)"
    insight = "eFoilissa vakaus korostuu startissa. Moottori antaa jatkuvan työnnön."
    profiili = "Low Aspect"

# --- TULOSTUS ---
st.subheader(f"🎯 Suositus: {laji}")

st.markdown(f"""
<div class="result-box">
    <strong>LAUTAVAIHTOEHDOT:</strong><br>{lauta_malli}<br>
    <strong>LAUDAN TILAVUUS:</strong> {volyymi} Litraa<br><br>
    <strong>ETUSIIVET (Sabfoil & Duotone):</strong><br>{siivet}<br><br>
    <strong>MASTO:</strong> {masto} cm Carbon<br><br>
    {wing_info}
    <strong>SIIVEN TYYPPI:</strong> {profiili}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="expert-card">
    <strong style="color:#38bdf8;">LAPPIS EXPERT INSIGHT:</strong><br>
    <p style="color:white; margin-top:10px;">{insight}</p>
    <hr style="border:0.1px solid #1e293b;">
    <em style="color:#94a3b8;">Koneisto päivitetty: Sabfoil Kraken & Duotone SLS sarjat huomioitu.</em>
</div>
""", unsafe_allow_html=True)
