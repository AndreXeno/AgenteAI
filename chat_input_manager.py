# chat_input_manager.py
import os
import json
import streamlit as st
from agents.mindbody_agent import MindBodyAgent

def render_chat_input():
    """Mostra l’input di chat e ritorna testo + pulsante di invio."""
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Scrivi un messaggio...", placeholder="Come ti senti oggi?")
        send_btn = st.form_submit_button("📤 Invia")
    return user_input, send_btn

def process_user_message(user_input, send_btn):
    """Processa il messaggio e aggiorna la conversazione."""
    if not (send_btn and user_input and user_input.strip()):
        return

    # salva messaggio utente
    st.session_state.messages.append({"role": "user", "content": user_input})

    if "agent" not in st.session_state:
        st.session_state.agent = MindBodyAgent()

    username = st.session_state.get("username", "anonimo")

    try:
        response = st.session_state.agent.run(user_input, username=username)
        ai_reply = response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        ai_reply = "Mi dispiace, ho avuto un problema tecnico."
        print(f"[ERROR] process_user_message: {e}")

    st.session_state.messages.append({"role": "bot", "content": ai_reply})
    save_chat_history(username)
    st.rerun()

def save_chat_history(username):
    """Salva la chat dell’utente su file JSON."""
    user_dir = os.path.join("data", "users", username)
    os.makedirs(user_dir, exist_ok=True)
    chat_file = os.path.join(user_dir, "chat_history.json")
    try:
        with open(chat_file, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] ❌ Impossibile salvare chat: {e}")