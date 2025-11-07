import streamlit as st
from auth_manager import login_page, logout_user
from chat_input_manager import render_chat_input, process_user_message
from agents.mindbody_agent import MindBodyAgent

# ==============================
# SESSIONE
# ==============================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ==============================
# LOGIN / REGISTRAZIONE
# ==============================
if not st.session_state["logged_in"]:
    rerun_needed = login_page()
    # Rendering chat messages with modern chat bubble style
    if rerun_needed:
        # niente st.experimental_rerun()
        st.session_state["logged_in"] = True
    st.stop()

# ==============================
# INTERFACCIA PRINCIPALE
# ==============================
st.set_page_config(page_title="Mind&Body Coach AI", page_icon="🧘‍♂️", layout="centered")
st.sidebar.title(f"Benvenuto, {st.session_state['username']} 👋")
logout_user()

st.title("🧠 Mind&Body Coach AI")
st.subheader("Parla con il tuo coach personale")

# ==============================
# MESSAGGI CHAT
# ==============================
for msg in st.session_state.messages:
    role_class = "🧍 Utente" if msg["role"] == "user" else "🤖 Coach"
    st.markdown(f"**{role_class}:** {msg['content']}")

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'''
            <div class="chat-message user-message">
                <div class="user-bubble">{msg["content"]}</div>
                <div class="avatar user-avatar">🧍</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'''
            <div class="chat-message bot-message">
                <div class="avatar bot-avatar">🤖</div>
                <div class="bot-bubble">{msg["content"]}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# INPUT CHAT
# ==============================
user_input, send_btn = render_chat_input()
process_user_message(user_input, send_btn)