import streamlit as st
from groq import Groq

# --- SIVUN ASETUKSET ---
st.set_page_config(page_title="Lappis Foil Advaiser Pro", page_icon="🏄‍♂️", layout="wide")

# --- GROQ API ALUSTUS ---
# Käytetään ensisijaisesti Secretsiä, mutta jos sitä ei ole, käytetään antamaasi avainta
api_key = st.secrets.get("GROQ_API_KEY", "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")
client = Groq(api_key=api_key)

# --- AMMATTIMAINEN TYYLITTELY ---
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
    .category-label { color: #8b949e; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
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

st.markdown("<br>", unsafe_allow_html=True)

# --- LAAJENNETTU LOGIIKKA ---
lauta_malli = ""; vol = 0; siivet = ""; masto = ""; extra_label = ""; extra_val = ""; insight = ""

if laji == "Pumpfoil":
    vol = 35 if taso == "Aloittelija" else 25 if taso == "Keskitaso" else 15
    lauta_malli = "Duotone Sky Surf / Style"
    siivet = "Sabfoil Leviathan 1550 / 1350<br>Duotone Aero Glide 1595"
    masto = "73cm Kraken Carbon"
    extra_label = "Lajispesifit"; extra_val = "Pump-optimized"
    insight = "Pumpfoilissa pieni tilavuus on välttämätön heiluripainon minimoimiseksi."
elif laji == "eFoil":
    vol = int(paino + 25); lauta_malli = "Audi e-tron Foil"; siivet = "Aero Lift 2400"
    masto = "80cm Integrated"; extra_label = "Sähköjärjestelmä"; extra_val = "5kW / 2.8kWh Akku"
    insight = "eFoil-järjestelmä antaa 120min ajoaikaa ja on markkinoiden hiljaisin."
elif laji == "SUPfoil":
    vol = int(paino + 55); lauta_malli = "Duotone Sky Brid"; siivet = "Sabfoil Leviathan 1550"
    masto = "75-82cm Carbon"; extra_label = "Mela"; extra_val = "Full Carbon Fixed"
    insight = "SUP-foilaus vaatii suuren tilavuuden seisten tapahtuvaan melontaan."
else: # Wingfoil
    vol = int(paino + (45 if taso == "Aloittelija" else 5 if taso == "Keskitaso" else -15))
    lauta_malli = "Duotone Sky Free / Style"
    siivet = "Sabfoil Medusa Pro / Tortuga<br>Duotone Aero Free"
    masto = "82cm Carbon"
    wk = "4.5m" if paino < 70 else "5.5m"
    extra_label = "Wing-koko"; extra_val = f"Duotone Unit {wk}"
    insight = f"Wingfoilissa suosittelemme {wk} siipeä painoosi nähden."

# --- DASHBOARD ---
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.markdown(f'<div class="stat-card"><div class="category-label">🌊 Lauta</div><div class="value-label">{lauta_malli}</div><div class="product-list">Tilavuus: {vol}L</div></div>', unsafe_allow_html=True)
with col_b:
    st.markdown(f'<div class="stat-card"><div class="category-label">🦅 Etusiipi</div><div class="value-label">Sabfoil / Duotone</div><div class="product-list">{siivet}</div></div>', unsafe_allow_html=True)
with col_c:
    st.markdown(f'<div class="stat-card"><div class="category-label">🪁 {extra_label}</div><div class="value-label">{extra_val}</div><div class="product-list">Suositeltu varuste</div></div>', unsafe_allow_html=True)
with col_d:
    st.markdown(f'<div class="stat-card"><div class="category-label">📏 Masto</div><div class="value-label">{masto}</div><div class="product-list">Käyttäjä: {paino}kg</div></div>', unsafe_allow_html=True)

# --- 🤖 LAPPIS AI CHATBOT (GROQ) ---
st.divider()
st.subheader("🤖 Lappis AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": f"Olet Lappis-kaupan asiantuntija. Autat asiakasta lajissa {laji}. Paino {paino}kg. Suosittele Sabfoil ja Duotone tuotteita. Vastaa suomeksi."}]

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Kysy foilaamisesta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        response_stream = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True
        )
        response = st.write_stream(response_stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
