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

# --- KORJATTU LOGIIKKA ---

# 1. Lautavolyymi (Laji-kohtainen korjaus)
if laji == "Pumpfoil":
    # Pumpfoil-laudat ovat aina pieniä (15-35L)
    if taso == "Aloittelija": volyymi = 30
    elif taso == "Keskitaso": volyymi = 20
    else: volyymi = 15
elif laji == "eFoil":
    volyymi = int(paino + 20) if taso == "Aloittelija" else int(paino - 10)
else: # Wingfoil ja SUP
    volyymi = int(paino + (40 if taso == "Aloittelija" else 5 if taso == "Keskitaso" else -15))

if volyymi < 15: volyymi = 15 

# 2. Maston pituus
masto = 82 if pituus > 180 or taso != "Aloittelija" else 75
if laji == "Pumpfoil": masto = 73 # Sabfoil Kraken standardi pumpulle
if taso == "Pro": masto = 93

# 3. Varusteet ja Wingin koko
wing_koko = ""
if laji == "Wingfoil":
    if paino < 65: wing_koko = "4.0m - 4.5m"
    elif paino < 85: wing_koko = "5.0m"
    else: wing_koko = "5.5m - 6.5m"

# Lajikohtaiset tekstit
if laji == "Pumpfoil":
    siivet = "• Sabfoil LEVIATHAN 1550 (Paras nosto)<br>• Sabfoil LEVIATHAN 1350 (Vauhti/Glide)<br>• Sabfoil SIREN 1350"
    insight = "Pumpfoilissa lauta on vain 'alusta' josta ponnistetaan. 15-30L on optimaalinen, jotta lauta on mahdollisimman kevyt heiluri-ilmiön minimoimiseksi."
    profiili = "Ultra-High Aspect"
elif laji == "eFoil":
    siivet = "• Aero Lift 2400 (Vakaus)<br>• Integroitu moottorimasto"
    insight = "eFoilissa volyymi auttaa vakaudessa vedessä ollessa. Lennon aikana siipi hoitaa kaiken."
    profiili = "Low Aspect"
else: # Wingfoil
    if taso == "Aloittelija":
        siivet = "• Sabfoil TORTUGA 1250<br>• Duotone Aero Lift 2400"
        insight = f"Aloittelijana tarvitset kelluttavan laudan ({volyymi}L). Suositeltu siipi: {wing_koko}."
    else:
        siivet = "• Sabfoil MEDUSA PRO 869<br>• Sabfoil RAZOR 880"
        insight = f"Kokeneempana voit käyttää pienempää lautaa. Suositeltu wingi: {wing_koko}."
    profiili = "Medium Aspect"

# --- TULOSTUS ---
st.subheader("🎯 Suositeltu kokoonpano")

st.markdown(f"""
<div class="result-box">
    <strong>ETUSIIPI:</strong><br>{siivet}<br><br>
    <strong>LAUDAN TILAVUUS:</strong> {volyymi} Litraa<br>
    <strong>MASTON PITUUS:</strong> {masto} cm<br>
    {"<strong>SUOSITELTU WINGI:</strong> " + wing_koko + "<br><br>" if wing_koko else ""}
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

raportti = f"LAPPIS FOIL ADVAISER\nLaji: {laji}\nPaino: {paino}kg\nLauta: {volyymi}L\nMasto: {masto}cm"
st.download_button("📥 Tallenna suositus", raportti, file_name=f"lappis_foili_{laji}.txt")
