import streamlit as st
from agents.mindbody_agent import MindBodyAgent
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
import tempfile

# ==============================
# 🎨 CONFIGURAZIONE BASE
# ==============================
st.set_page_config(page_title="Mind&Body Coach AI", page_icon="🧘‍♂️", layout="centered")

st.sidebar.header("👤 Profilo Utente")
if st.sidebar.button("Modifica Profilo"):
    st.switch_page("pages/Profilo_Utente.py")

st.markdown("""
<style>
.chat-message {
    padding: 1rem;
    margin-bottom: 0.7rem;
    border-radius: 1rem;
    width: 90%;
    color: black !important;
}
.user-msg {
    background-color: #DCF8C6;
    align-self: flex-end;
    margin-left: auto;
}
.bot-msg {
    background-color: #F1F0F0;
    align-self: flex-start;
    margin-right: auto;
}
.chat-container {
    display: flex;
    flex-direction: column;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🧠 INIZIALIZZAZIONE AGENTE
# ==============================
if "agent" not in st.session_state:
    st.session_state.agent = MindBodyAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Sono Mind&Body il tuo coach personale ")
st.caption("Scrivi o parla liberamente con me")

# ==============================
# 💬 AREA CHAT
# ==============================
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        role_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        st.markdown(f"<div class='chat-message {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# ==============================
# 🎙️ INPUT UTENTE (Testo o Voce)
# ==============================
st.divider()
st.subheader("💬 Invia un messaggio o parla")

col1, col2, col3 = st.columns([8, 1, 1])

with col1:
    user_input = st.text_input("Scrivi qui...", key="input", placeholder="Come ti senti oggi?")
with col2:
    send_btn = st.button("📤")
with col3:
    add_btn = st.button("➕")
    if add_btn:
        st.switch_page("pages/Allenamenti_Manuali.py")

# 🎤 Registrazione vocale
audio = mic_recorder(
    start_prompt="🎙️ Premi per parlare",
    stop_prompt="⏹️ Ferma la registrazione",
    just_once=True,
    use_container_width=True
)

# ==============================
# 🔄 GESTIONE INPUT
# ==============================
if send_btn and user_input:
    user_text = user_input.strip()
elif audio:
    st.info("🎧 Elaboro la tua voce con Gemini...")
    from google import genai
    import base64
    client = genai.Client()
    # Codifica audio in base64 per l'invio
    encoded_audio = base64.b64encode(audio["bytes"]).decode("utf-8")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "inline_data": {
                    "mime_type": "audio/webm",
                    "data": encoded_audio
                }
            }
        ]
    )
    user_text = response.text
else:
    user_text = None

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.spinner("🤖 Il coach sta riflettendo..."):
        response = st.session_state.agent.run(user_text)
        reply_text = response.text


    st.session_state.messages.append({
        "role": "bot",
        "content": reply_text
    })
    st.rerun()

# ==============================
# 🏋️ Aggiungi Allenamento Manuale
# ==============================
import os
import pandas as pd
from datetime import datetime

st.divider()
st.subheader("🏋️ Aggiungi Allenamento Manuale")

sports = [
    "Corsa",
    "Nuoto",
    "Palestra",
    "Ciclismo",
    "Calcio",
    "Basket",
    "Yoga"
]

sport = st.selectbox("Scegli lo sport", sports)

# Inizializza i campi
durata = distanza = bpm = pendenza = gruppo_muscolare = n_esercizi = intensita = vasche = stile = ruolo = stress_pre = stress_post = note = None

if sport in ["Corsa", "Ciclismo"]:
    durata = st.number_input("Durata (minuti)", min_value=1, step=1, key="durata")
    distanza = st.number_input("Distanza (km)", min_value=0.0, step=0.1, key="distanza")
    bpm = st.number_input("BPM medio", min_value=0, step=1, key="bpm")
    pendenza = st.number_input("Pendenza (%)", min_value=0.0, step=0.1, key="pendenza")
    note = st.text_input("Note", key="note_corsa_ciclismo")
elif sport == "Palestra":
    durata = st.number_input("Durata (minuti)", min_value=1, step=1, key="durata_palestra")
    gruppo_muscolare = st.text_input("Gruppo muscolare", key="gruppo_muscolare")
    n_esercizi = st.number_input("Numero esercizi", min_value=1, step=1, key="n_esercizi")
    intensita = st.slider("Intensità percepita (1–10)", 1, 10, key="intensita")
    note = st.text_input("Note", key="note_palestra")
elif sport == "Nuoto":
    durata = st.number_input("Durata (minuti)", min_value=1, step=1, key="durata_nuoto")
    vasche = st.number_input("Numero vasche", min_value=1, step=1, key="vasche")
    stile = st.text_input("Stile", key="stile")
    bpm = st.number_input("BPM medio", min_value=0, step=1, key="bpm_nuoto")
    note = st.text_input("Note", key="note_nuoto")
elif sport in ["Calcio", "Basket"]:
    durata = st.number_input("Durata (minuti)", min_value=1, step=1, key="durata_calcio_basket")
    ruolo = st.text_input("Ruolo", key="ruolo")
    intensita = st.slider("Intensità percepita (1–10)", 1, 10, key="intensita_calcio_basket")
    note = st.text_input("Note", key="note_calcio_basket")
elif sport == "Yoga":
    durata = st.number_input("Durata (minuti)", min_value=1, step=1, key="durata_yoga")
    stress_pre = st.slider("Livello stress prima (1–10)", 1, 10, key="stress_pre")
    stress_post = st.slider("Livello stress dopo (1–10)", 1, 10, key="stress_post")
    note = st.text_input("Note", key="note_yoga")

save_btn = st.button("💾 Salva Allenamento")

if save_btn:
    # Prepara i dati per il salvataggio
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "data": now,
        "sport": sport,
        "durata_min": durata,
        "distanza_km": None,
        "bpm": None,
        "pendenza": None,
        "note": ""
    }
    # Inserisci i campi specifici dove rilevanti
    if sport in ["Corsa", "Ciclismo"]:
        row["distanza_km"] = distanza
        row["bpm"] = bpm
        row["pendenza"] = pendenza
        row["note"] = note
    elif sport == "Palestra":
        row["note"] = f"Gruppo: {gruppo_muscolare}, Esercizi: {n_esercizi}, Intensità: {intensita}. {note}"
    elif sport == "Nuoto":
        row["note"] = f"Vasche: {vasche}, Stile: {stile}. {note}"
        row["bpm"] = bpm
    elif sport in ["Calcio", "Basket"]:
        row["note"] = f"Ruolo: {ruolo}, Intensità: {intensita}. {note}"
    elif sport == "Yoga":
        row["note"] = f"Stress prima: {stress_pre}, dopo: {stress_post}. {note}"

    # Crea la cartella se non esiste
    os.makedirs("data", exist_ok=True)
    csv_path = "data/allenamenti_manual.csv"
    # Controlla se il file esiste già
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(csv_path, index=False)
    st.success("Allenamento salvato con successo!")