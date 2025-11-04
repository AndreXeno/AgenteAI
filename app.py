import streamlit as st
from agents.mindbody_agent import MindBodyAgent

from agents.session_manager import load_session, save_session

# ==============================
# 🔐 GESTIONE SESSIONE UTENTE (robusta)
# ==============================
# Inizializza chiavi principali di sessione
if "username" not in st.session_state:
    st.session_state["username"] = None
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Tenta di ripristinare la sessione salvata localmente
try:
    saved_user = load_session()
    if saved_user and not st.session_state["username"]:
        st.session_state["username"] = saved_user
        st.session_state["logged_in"] = True
        print(f"[SESSION RESTORE] ✅ Utente ripristinato da sessione salvata: {saved_user}")
except Exception as e:
    print(f"[SESSION ERROR] ❌ Errore nel ripristino sessione: {e}")

# Salva la sessione solo se un utente è loggato
if st.session_state.get("username"):
    try:
        save_session(st.session_state["username"])
        print(f"[SESSION SAVE] 💾 Sessione salvata per {st.session_state['username']}")
    except Exception as e:
        print(f"[SESSION ERROR] ⚠️ Errore durante il salvataggio della sessione: {e}")
else:
    print("[SESSION INFO] Nessun utente loggato al momento.")
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

# ==============================
# 🎨 STILE CHAT (CSS ESTERNO)
# ==============================
css_path = os.path.join("static", "chat_styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
# 💬 INPUT UTENTE (Solo Testo)
# ==============================
# ==============================
# 💬 INPUT UTENTE (Solo Testo)
# ==============================
st.divider()
st.subheader("💬 Invia un messaggio")

# 🔹 Form per invio con ENTER
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([9, 1])
    with col1:
        user_input = st.text_input(
            "Scrivi un messaggio al tuo coach:",
            key="input",
            placeholder="Come ti senti oggi?",
            label_visibility="collapsed"
        )
    with col2:
        send_btn = st.form_submit_button("📤")

# ➕ Pulsante per la pagina Fitness Connector
col_plus = st.columns([10, 1])[1]
with col_plus:
    if st.button("➕"):
        st.switch_page("pages/Fitness_Connector.py")

# ==============================
# 🔄 GESTIONE INPUT
# ==============================
user_text = user_input.strip() if send_btn and user_input else None
# ==============================
# 🔄 ELABORAZIONE INPUT UTENTE
# ==============================
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})

    # Carica dati utente aggiornati da CSV
    username = st.session_state.get("username", "anonimo")
    user_dir = f"data/users/{username}"
    profilo_path = f"{user_dir}/profilo_utente.css.csv"
    allenamenti_path = f"{user_dir}/allenamenti.csv"
    fitness_path = f"{user_dir}/dati_fitness.csv"

    user_data = {}
    import pandas as pd, os
    try:
        if os.path.exists(profilo_path):
            df = pd.read_csv(profilo_path)
            user_data["profilo"] = df.iloc[-1].to_dict() if not df.empty else {}
        if os.path.exists(allenamenti_path):
            df = pd.read_csv(allenamenti_path)
            user_data["allenamenti"] = df.to_dict("records")[-5:]  # ultimi 5
        if os.path.exists(fitness_path):
            df = pd.read_csv(fitness_path)
            user_data["fitness"] = df.to_dict("records")[-5:]
    except Exception as e:
        st.warning(f"⚠️ Dati non accessibili: {e}")

    # Passa i dati a MindBodyAgent per migliorare le risposte
    with st.spinner("🤖 Il coach sta riflettendo sui tuoi dati..."):
        try:
            # Nuova firma con user_data
            response = st.session_state.agent.run(user_text, username=username, user_data=user_data)
        except TypeError:
            # Retrocompatibilità: firma senza user_data
            response = st.session_state.agent.run(user_text, username=username)
        reply_text = getattr(response, "text", str(response))

    st.session_state.messages.append({
        "role": "bot",
        "content": reply_text
    })
    st.rerun()