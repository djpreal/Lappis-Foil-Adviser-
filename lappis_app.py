import streamlit as st

# Sivun asetukset ja selaimen välilehden nimi
st.set_page_config(page_title="Lappis Foil Advaiser", page_icon="🏄‍♂️", layout="centered")

# --- TYYLITTELY ---
st.markdown("""
    <style>
    .stApp { background-color: #050508; }
    .main-header { color: #38bdf8; font-size: 36px; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .sub-header { color: #94a3b8; font-size: 14px; text-align: center; margin-bottom: 30px; }
    .expert-card { background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #38bdf8; margin-top: 20px; }
    .result-text { font-family: 'Courier New', Courier, monospace; color: #f8fafc; font-size: 16px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">Lappis Foil Advaiser</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Asiantuntijan työkalu oikean kaluston valintaan</div>', unsafe_allow_html=True)

# --- SYÖTTEET ---
col1, col2 = st.columns(2)

with col1:
    laji = st.selectbox("Laji", ["Wingfoil", "Pumpfoil", "eFoil", "SUPfoil"])
    taso = st.select_slider("Taso", options=["Aloittelija", "Keskitaso", "Pro"])

with col2:
    paino = st.number_input("Paino (kg)", 30, 150, 85)
    pituus = st.number_input("Pituus (cm)", 100, 220, 180)

st.divider()

# --- ANALYYSI JA LOGIIKKA ---
# Tilavuuslaskenta
volyymi = int(paino + (40 if taso == "Aloittelija" else 5 if taso == "Keskitaso" else -15))
if volyymi < 20: volyymi = 20 

# Mastolaskenta
masto = 82 if pituus > 180 or taso != "Aloittelija" else 75
if taso == "Pro": masto = 93

# Varuste- ja infologiikka
if laji == "Pumpfoil":
    siivet = "• Sabfoil LEVIATHAN 1550 (Paras liito)\n• Sabfoil LEVIATHAN 1350 (All-round)\n• Duotone Aero Glide 1595"
    insight = f"Pumppauksessa pituutesi ({pituus}cm) on etu vipuvarren kannalta. Mitä suurempi siiven kärkiväli (High Aspect), sitä vähemmän työtä joudut tekemään lennon ylläpitämiseksi."
    profiili = "High Aspect (Kapea & Pitkä)"
elif laji == "eFoil":
    siivet = f"• Aero Lift 2400 (Vakaa nousu {paino}kg kuskille)\n• Sähköjärjestelmä: 5kW Brushless / 2.8kWh akku"
    insight = "eFoilissa painopisteen hallinta on tärkeämpää kuin voima. Aloita 'Eco'-asetuksella, kunnes hallitset nousun."
    profiili = "Low Aspect (Paksu & Nostava)"
else: # Wingfoil / SUP
    if taso == "Aloittelija":
        siivet = "• Sabfoil TORTUGA 1250 / 1100\n• Duotone Aero Lift 2400"
        insight = "Aloittelijana tarvitset pituussuuntaista vakautta. Tortuga-sarja antaa anteeksi virheitä sijoittumisessa."
        profiili = "Low Aspect (Vakaa & Hidas)"
    else:
        siivet = "• Sabfoil MEDUSA PRO 869 (Vauhti)\n• Sabfoil RAZOR 880 (Aaltosurffi)\n• Duotone Aero Carve 2.0"
        insight = f"Painosi ({paino}kg) huomioiden Medusa Pro tarjoaa parhaan vasteen hypyissä ja tiukoissa käännöksissä."
        profiili = "Medium/High Aspect (Nopea)"

# --- TULOSTUS ---
st.subheader("🎯 Suositeltu kokoonpano")

res_col, viz_col = st.columns([2, 1])

with res_col:
    st.markdown(f"""
    <div class="result-text">
    <strong>ETUSIIVET:</strong><br>{siivet}<br><br>
    <strong>LAUTA:</strong> {volyymi} Litraa<br>
    <strong>MASTO:</strong> {masto} cm Carbon<br>
    <strong>PROFIILI:</strong> {profiili}
    </div>
    """, unsafe_allow_html=True)

with viz_col:
    st.write("Siiven muoto:")
    if "High" in profiili:
        st.caption("Kapea / Liitävä")
        st.progress(0.9)
    elif "Low" in profiili:
        st.caption("Leveä / Vakaa")
        st.progress(0.3)
    else:
        st.caption("Hybrid / All-round")
        st.progress(0.6)

st.markdown(f"""
<div class="expert-card">
    <strong>LAPPIS EXPERT INSIGHT:</strong><br>
    {insight}<br><br>
    <em>Analyysi generoitu Lappis Foil Advaiserilla.</em>
</div>
""", unsafe_allow_html=True)

# LATAUSNAPPULA
raportti = f"LAPPIS FOIL ADVAISER - RAPORTTI\n---------------------------\nLaji: {laji}\nTaso: {taso}\nKuski: {paino}kg / {pituus}cm\n\nSUOSITUS:\n{siivet}\nLauta: {volyymi}L\nMasto: {masto}cm"
st.download_button("Tallenna analyysi (.txt)", raportti, file_name="lappis_analyysi.txt")
