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