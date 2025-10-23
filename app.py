import streamlit as st
from agents.mindbody_agent import MindBodyAgent
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
import tempfile

from agents.session_manager import load_session, save_session

# Inizializza chiavi di sessione
if "username" not in st.session_state:
    st.session_state["username"] = None
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ==============================
# 🔐 GESTIONE SESSIONE UTENTE
# ==============================
saved_user = load_session()
if saved_user and not st.session_state["username"]:
    st.session_state["username"] = saved_user
    print(f"[SESSION RESTORE] Ripristinato utente: {saved_user}")

if st.session_state.get("username"):
    save_session(st.session_state["username"])
    print(f"[SESSION SAVE] Sessione salvata per {st.session_state['username']}")
else:
    print("[SESSION] Nessun utente loggato al momento.")
# ==============================
# 🎨 CONFIGURAZIONE BASE
# ==============================
st.set_page_config(page_title="Mind&Body Coach AI", page_icon="🧘‍♂️", layout="centered")

# ==============================
# 🔐 LOGIN / REGISTRAZIONE UTENTE
# ==============================
# ==============================
# 🔐 LOGIN / REGISTRAZIONE UTENTE
# ==============================
import pandas as pd, os
users_file = "data/users.csv"
os.makedirs("data", exist_ok=True)



# Carica o crea file utenti
if os.path.exists(users_file):
    users_df = pd.read_csv(users_file)
else:
    users_df = pd.DataFrame(columns=["username", "password"])
    users_df.to_csv(users_file, index=False)

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.sidebar.title("🔑 Accesso")
    auth_mode = st.sidebar.radio("Seleziona modalità:", ["Login", "Registrati"])
    if auth_mode == "Registrati":
        new_user = st.sidebar.text_input("Crea username")
        new_pass = st.sidebar.text_input("Crea password", type="password")
        if st.sidebar.button("Registrati"):
            if new_user and new_pass:
                if new_user in users_df["username"].values:
                    st.sidebar.error("⚠️ Nome utente già esistente.")
                else:
                    users_df.loc[len(users_df)] = [new_user, new_pass]
                    users_df.to_csv(users_file, index=False)
                    st.sidebar.success("✅ Registrazione completata! Ora effettua il login.")
            else:
                st.sidebar.warning("Compila entrambi i campi.")
    else:
        login_user = st.sidebar.text_input("Username")
        login_pass = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Accedi"):
            if ((users_df["username"] == login_user) & (users_df["password"] == login_pass)).any():
                st.session_state["logged_in"] = True
                st.session_state["username"] = login_user
                st.sidebar.success(f"👋 Bentornato, {login_user}!")
            else:
                st.sidebar.error("❌ Credenziali errate.")
    st.warning("🔒 Effettua l’accesso o registrati per continuare.")
    st.stop()
else:
    # Only show logout and profile modification after login
    st.sidebar.header("👤 Profilo Utente")
    if st.sidebar.button("Modifica Profilo"):
        st.switch_page("pages/Profilo_Utente.py")
    # Simple logout button
    if st.sidebar.button("🔓 Logout"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

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
    user_input = st.text_input("", key="input", placeholder="Come ti senti oggi?")
with col2:
    send_btn = st.button("📤")
with col3:
    add_btn = st.button("➕")
    if add_btn:
        # Go to Fitness Connector page for third-party fitness accounts
        st.switch_page("pages/Fitness_Connector.py")

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
    import google.generativeai as genai
    from config.settings import GEMINI_API_KEY
    genai.configure(api_key=GEMINI_API_KEY)

    encoded_audio = base64.b64encode(audio["bytes"]).decode("utf-8")

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        [
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

    username = st.session_state.get("username", "anonimo")
    with st.spinner("🤖 Il coach sta riflettendo..."):
        response = st.session_state.agent.run(user_text, username=username)
        reply_text = response.text


    st.session_state.messages.append({
        "role": "bot",
        "content": reply_text
    })
    st.rerun()