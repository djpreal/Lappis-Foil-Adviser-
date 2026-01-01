import streamlit as st

# Sivun asetukset
st.set_page_config(page_title="Lappis Foil Advaiser", page_icon="🏄‍♂️", layout="centered")

# --- TYYLITTELY (Valkoinen teksti ja selkeys) ---
st.markdown("""
    <style>
    /* Tausta mustaksi */
    .stApp { background-color: #050508; }
    
    /* Otsikot valkoiseksi/syaaniksi */
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    
    /* Pääotsikko */
    .main-header { color: #38bdf8; font-size: 42px; font-weight: bold; text-align: center; margin-bottom: 5px; }
    
    /* Tulokset selkeään valkoiseen laatikkoon */
    .result-box { 
        background-color: #1e293b; 
        padding: 25px; 
        border-radius: 15px; 
        border: 2px solid #38bdf8;
        color: #ffffff !important;
        font-size: 18px;
        line-height: 1.6;
    }
    
    /* Expert Card */
    .expert-card { 
        background-color: #0f172a; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 10px solid #38bdf8; 
        margin-top: 20px;
        color: #ffffff !important;
    }

    /* Input-kenttien tekstin väri */
    .stNumberInput input, .stSelectbox div { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">Lappis Foil Advaiser</div>', unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Tiedot päivittyvät automaattisesti syötteen mukaan.</p>", unsafe_allow_html=True)

# --- SYÖTTEET ---
col1, col2 = st.columns(2)

with col1:
    laji = st.selectbox("Valitse Laji", ["Wingfoil", "Pumpfoil", "eFoil", "SUPfoil"])
    taso = st.select_slider("Taitotaso", options=["Aloittelija", "Keskitaso", "Pro"])

with col2:
    paino = st.number_input("Paino (kg)", 30, 150, 85)
    pituus = st.number_input("Pituus (cm)", 100, 220, 180)

st.divider()

# --- LOGIIKKA ---
volyymi = int(paino + (40 if taso == "Aloittelija" else 5 if taso == "Keskitaso" else -15))
if volyymi < 20: volyymi = 20 

masto = 82 if pituus > 180 or taso != "Aloittelija" else 75
if taso == "Pro": masto = 93

if laji == "Pumpfoil":
    siivet = "• Sabfoil LEVIATHAN 1550 (Paras liito)<br>• Sabfoil LEVIATHAN 1350 (All-round)<br>• Duotone Aero Glide 1595"
    insight = "Pumppauksessa pituutesi on etu vipuvarren kannalta. Mitä suurempi siiven kärkiväli (High Aspect), sitä helpompi lento on ylläpitää."
    profiili = "High Aspect (Kapea & Pitkä)"
elif laji == "eFoil":
    siivet = "• Aero Lift 2400 (Vakaa nousu)<br>• 5kW Brushless Moottori<br>• 2.8kWh Tehoakku"
    insight = "eFoilissa vakaus on tärkeintä. Aero Lift nousee hitaassa vauhdissa, mikä tekee oppimisesta turvallista."
    profiili = "Low Aspect (Paksu & Nostava)"
else:
    if taso == "Aloittelija":
        siivet = "• Sabfoil TORTUGA 1250 / 1100<br>• Duotone Aero Lift 2400"
        insight = "Aloittelijana tarvitset pituussuuntaista vakautta (Pitch stability). Tortuga antaa anteeksi virheitä sijoittumisessa."
        profiili = "Low Aspect (Vakaa)"
    else:
        siivet = "• Sabfoil MEDUSA PRO 869 (Vauhti)<br>• Sabfoil RAZOR 880 (Surffi)<br>• Duotone Aero Carve 2.0"
        insight = f"Painollesi ({paino}kg) Medusa Pro tarjoaa parhaan vasteen kovemmassa vauhdissa ja hypyissä."
        profiili = "Medium/High Aspect"

# --- TULOSTUS ---
st.subheader("🎯 Analyysin tulos")

# Tuloslaatikko valkoisella tekstillä
st.markdown(f"""
<div class="result-box">
    <strong>SUOSITELTU ETUSIIPI:</strong><br>{siivet}<br><br>
    <strong>LAUDAN TILAVUUS:</strong> {volyymi} Litraa<br>
    <strong>MASTON PITUUS:</strong> {masto} cm Carbon<br>
    <strong>SIIVEN PROFIILI:</strong> {profiili}
</div>
""", unsafe_allow_html=True)



st.markdown(f"""
<div class="expert-card">
    <strong style="color:#38bdf8;">LAPPIS EXPERT INSIGHT:</strong><br>
    <p style="color:white; margin-top:10px;">{insight}</p>
    <hr style="border:0.1px solid #1e293b;">
    <em style="color:#94a3b8;">Analysoitu profiilille: {paino}kg / {pituus}cm</em>
</div>
""", unsafe_allow_html=True)

# Tallenna nappi
raportti = f"LAPPIS FOIL ADVAISER\nLaji: {laji}\nPaino: {paino}kg\nLauta: {volyymi}L\nMasto: {masto}cm\nSiivet: {siivet.replace('<br>', ', ')}"
st.download_button("📥 Tallenna suositus asiakkaalle", raportti, file_name=f"lappis_suositus_{paino}kg.txt")
