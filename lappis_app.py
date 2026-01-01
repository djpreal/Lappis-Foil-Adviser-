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

# --- TÄYSIN ERIYTETTY LOGIIKKA PUMPFOILILLE ---

if laji == "Pumpfoil":
    # Pumpfoil-lautasuositukset (Sky Surf / Sky Style)
    if taso == "Aloittelija":
        lauta_malli = "Duotone Sky Style (tai Sky Free)"
        volyymi = 35
        masto = 73
        siivet = "• Sabfoil LEVIATHAN 1550<br>• Duotone Aero Glide 1595"
    elif taso == "Keskitaso":
        lauta_malli = "Duotone Sky Surf"
        volyymi = 25
        masto = 73
        siivet = "• Sabfoil LEVIATHAN 1350<br>• Sabfoil SIREN 1350"
    else: # Pro
        lauta_malli = "Duotone Sky Surf (Carbon)"
        volyymi = 15
        masto = 73
        siivet = "• Sabfoil LEVIATHAN 1150<br>• Sabfoil BLADE 82"
    
    insight = f"Pumpfoilissa käytetään pieniä lautoja ({volyymi}L). Sky Surf on suunniteltu minimoimaan heiluripaino, jotta pumppaaminen on tehokasta."
    profiili = "Ultra-High Aspect (Pumppaukseen)"
    wing_info = "" # Ei wingiä pumppauksessa

elif laji == "eFoil":
    lauta_malli = "Audi e-tron Foil (L-koko)" if taso == "Aloittelija" else "Audi e-tron Foil (Performance)"
    volyymi = int(paino + 20)
    masto = 80
    siivet = "• Aero Lift 2400"
    insight = "eFoilissa moottori hoitaa noston, lauta antaa vakauden startissa."
    profiili = "Low Aspect"
    wing_info = ""

else: # Wingfoil
    if taso == "Aloittelija":
        lauta_malli = "Duotone Sky Free"
        volyymi = int(paino + 40)
        siivet = "• Sabfoil TORTUGA 1250"
    elif taso == "Keskitaso":
        lauta_malli = "Duotone Sky Style"
        volyymi = int(paino + 5)
        siivet = "• Sabfoil MEDUSA PRO 869"
    else: # Pro
        lauta_malli = "Duotone Sky Surf / Style"
        volyymi = int(paino - 15)
        siivet = "• Sabfoil RAZOR 880"
    
    masto = 82 if pituus > 180 else 75
    profiili = "Medium Aspect"
    
    # Wingin koko painon mukaan
    if paino < 65: wk = "4.0m"
    elif paino < 85: wk = "5.0m"
    else: wk = "6.0m"
    wing_info = f"<strong>SUOSITELTU WINGI:</strong> Duotone Unit {wk}<br><br>"
    insight = f"Wingfoilissa laudan ({lauta_malli}) volyymi auttaa kelluttavuudessa ennen nousua."

# --- TULOSTUS ---
st.subheader(f"🎯 Suositus: {laji}")

st.markdown(f"""
<div class="result-box">
    <strong>LAUTA:</strong> {lauta_malli}<br>
    <strong>LAUDAN TILAVUUS:</strong> {volyymi} Litraa<br><br>
    <strong>ETUSIIVI:</strong><br>{siivet}<br><br>
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
    <em style="color:#94a3b8;">Kuski: {paino}kg | {pituus}cm | {taso}</em>
</div>
""", unsafe_allow_html=True)

raportti = f"LAPPIS FOIL ADVAISER\nLaji: {laji}\nLauta: {lauta_malli} ({volyymi}L)\nSiivet: {siivet.replace('<br>', ', ')}"
st.download_button("📥 Tallenna suositus", raportti, file_name=f"lappis_{laji}.txt")
