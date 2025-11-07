# chat_input_manager.py — form + invio + risposta AI, nessun rendering HTML qui
import os
import json
import datetime
import streamlit as st

# Usa il tuo agente reale
try:
    from agents.mindbody_agent import MindBodyAgent
    _HAS_AGENT = True
except Exception as e:
    print("[WARN] MindBodyAgent non disponibile:", e)
    _HAS_AGENT = False

def _now_ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def render_chat_input(form_key="chat_form_main", input_key="chat_text_main",
                      button_key="chat_send_main", placeholder="Scrivi un messaggio…"):
    with st.form(form_key, clear_on_submit=True):
        txt = st.text_input("", key=input_key, placeholder=placeholder)
        btn = st.form_submit_button("📤 Invia")
    return txt, btn

def _ensure_agent():
    if "agent" not in st.session_state:
        try:
            print("[LOG] Inizializzo MindBodyAgent")
            st.session_state.agent = MindBodyAgent() if _HAS_AGENT else None
        except Exception as e:
            print("[ERROR] Errore inizializzando MindBodyAgent:", e)
            st.session_state.agent = None

def _append_message(role, content):
    st.session_state.messages.append({
        "role": role, "content": content, "ts": _now_ts()
    })

def process_user_message(user_input, send_btn):
    # evita doppie renderizzazioni: questo file NON visualizza messaggi, solo muta lo stato
    if not (send_btn and isinstance(user_input, str) and user_input.strip()):
        return

    user_input = user_input.strip()
    _append_message("user", user_input)

    # prepara agente
    _ensure_agent()
    username = st.session_state.get("username", "anonimo")

    # genera risposta
    reply = None
    if st.session_state.get("agent") is not None:
        try:
            res = st.session_state.agent.run(user_input, username=username)
            if isinstance(res, str):
                reply = res
            elif hasattr(res, "text"):
                reply = res.text
            elif isinstance(res, dict) and "text" in res:
                reply = res["text"]
            else:
                reply = str(res)
        except Exception as e:
            print("[ERROR] agent.run:", e)
            reply = "Ops, ho avuto un piccolo problema tecnico. Riproviamo."

    else:
        # fallback se l'agente non è importabile
        reply = "Ciao! Per ora sono offline, ma ho ricevuto il tuo messaggio. 😊"

    _append_message("bot", reply)

    # persistenza minima (opzionale)
    try:
        user_dir = os.path.join("data", "users", username)
        os.makedirs(user_dir, exist_ok=True)
        with open(os.path.join(user_dir, "chat_history.json"), "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[WARN] salvataggio chat_history.json:", e)

    st.rerun()