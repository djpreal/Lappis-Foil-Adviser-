import streamlit as st
from groq import Groq

# --- SIVUN ASETUKSET ---
st.set_page_config(page_title="Lappis Foil Advaiser Pro", page_icon="🏄‍♂️", layout="wide")

# --- TURVALLINEN API-ALUSTUS ---
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ API-avain puuttuu!")
    st.info("Lisää 'GROQ_API_KEY' Streamlit Cloudin Secrets-asetuksiin.")
    st.stop()

client = Groq(api_key=api_key)

# --- TYYLITTELY ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; }
    .main-header { 
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 52px; font-weight: 800; text-align: center; margin-bottom: 30px;
    }
    .stat-card {
        background-color: #161b22; border: 1px solid #30363d;
        border-radius: 12px; padding: 20px; height: 100%; transition: 0.3s;
    }
    .stat-card:hover { border-color: #38bdf8; }
    .category-label { color: #8b949e; font-size: 11px; font-weight: 600; text-transform: uppercase; }
    .value-label { color: #ffffff; font-size: 20px; font-weight: 700; margin-top: 5px; }
    .product-list { color: #38bdf8; font-size: 14px; font-weight: 500; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">Lappis Foil Advaiser</div>', unsafe_allow_html=True)

# --- SYÖTTEET ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1: laji = st.selectbox("Valitse Laji", ["Wingfoil", "Pumpfoil", "eFoil", "SUPfoil"])
    with c2: taso = st.select_slider("Taitotaso", options=["Aloittelija", "Keskitaso", "Pro"])
    with c3: paino = st.number_input("Paino (kg)", 30, 150, 85)
    with c4: pituus = st.number_input("Pituus (cm)", 100, 220, 180)

# --- LASKENTALOGIIKKA ---
lauta_malli = ""; vol = 0; siivet = ""; masto = ""; extra_label = ""; extra_val = ""

if laji == "Pumpfoil":
    vol = 35 if taso == "Aloittelija" else 15
    lauta_malli = "Duotone Sky Surf"
    siivet = "Sabfoil Leviathan 1550 / 1350"
    masto = "73cm Kraken Carbon"
    extra_label = "Tyyppi"; extra_val = "Pump-Specialist"
elif laji == "eFoil":
    vol = int(paino + 25); lauta_malli = "Audi e-tron Foil"; siivet = "Aero Lift 2400"
    masto = "80cm Integrated"; extra_label = "Akku"; extra_val = "2.8kWh (120min)"
elif laji == "SUPfoil":
    vol = int(paino + 55); lauta_malli = "Duotone Sky Brid"; siivet = "Sabfoil Leviathan 1750"
    masto = "75-82cm Carbon"; extra_label = "Mela"; extra_val = "Full Carbon"
else: # Wingfoil
    vol = int(paino + (45 if taso == "Aloittelija" else 5 if taso == "Keskitaso" else -15))
    lauta_malli = "Duotone Sky Free / Style"
    siivet = "Sabfoil Medusa Pro / Tortuga"; masto = "82cm Carbon"
    wk = "4.5m" if paino < 70 else "5.5m"
    extra_label = "Wing-koko"; extra_val = f"Duotone Unit {wk}"

# --- DASHBOARD ---
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.markdown(f'<div class="stat-card"><div class="category-label">🌊 Lauta</div><div class="value-label">{lauta_malli}</div><div class="product-list">Tilavuus: {vol}L</div></div>', unsafe_allow_html=True)
with col_b:
    st.markdown(f'<div class="stat-card"><div class="category-label">🦅 Etusiipi</div><div class="value-label">Sabfoil / Duotone</div><div class="product-list">{siivet}</div></div>', unsafe_allow_html=True)
with col_c:
    st.markdown(f'<div class="stat-card"><div class="category-label">🪁 {extra_label}</div><div class="value-label">{extra_val}</div><div class="product-list">Suositus</div></div>', unsafe_allow_html=True)
with col_d:
    st.markdown(f'<div class="stat-card"><div class="category-label">📏 Masto</div><div class="value-label">{masto}</div><div class="product-list">Käyttäjä: {paino}kg</div></div>', unsafe_allow_html=True)

# --- 🤖 LAPPIS AI ASSISTANT (GROQ) ---
st.divider()
st.subheader("🤖 Lappis AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Näytetään vanhat viestit
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Kysy foilaamisesta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # --- RAJOITETTU SYSTEEMIOHJE ---
            api_messages = [
                {
                    "role": "system", 
                    "content": (
                        f"Olet Lappis-kaupan foilaus-asiantuntija. Käyttäjä harrastaa lajia {laji}. "
                        "VASTAA VAIN foilaamiseen, vesiurheiluun sekä Sabfoil- ja Duotone-tuotteisiin liittyviin kysymyksiin. "
                        "Jos käyttäjä kysyy jotain, mikä ei liity foilaamiseen (esim. politiikka, ruokaohjeet, koodaus), "
                        "kieltäydy kohteliaasti vastaamasta ja sano, että osaat auttaa vain foilausasioissa. "
                        "Puhu suomea, ole ystävällinen ja asiantunteva."
                    )
                }
            ]
            for m in st.session_state.messages:
                api_messages.append({"role": m["role"], "content": m["content"]})

            # Tehdään kutsu
            response_stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                stream=True
            )
            
            # Puretaan vastaus tekstiksi (poistaa JSON-koodit)
            full_response = ""
            placeholder = st.empty()
            
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    text = chunk.choices[0].delta.content
                    full_response += text
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("Yhteysvirhe. Botti on hetken veden alla. Kokeile hetken päästä uudelleen.")
