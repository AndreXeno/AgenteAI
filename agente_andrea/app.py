# app.py — chat con bolle stile chat, senza CSS esterni
import os
import json
import streamlit as st

# ============ CONFIG ============
st.set_page_config(page_title="Mind&Body Coach AI", page_icon="🧘‍♂️", layout="centered")


# ============ SESSIONE ============
if "username" not in st.session_state:
    st.session_state["username"] = "a"  # metti il tuo meccanismo reale di login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True
if "messages" not in st.session_state:
    st.session_state["messages"] = []   # [{role:"user"|"bot", content:"...", ts: "..."}]

# ============ MESSAGGIO INTRODUTTIVO DINAMICO ============
from agents.module_intro_message import generate_intro_message

if not st.session_state.get("intro_message_shown", False):
    try:
        from agents.mindbody_agent import MindBodyAgent
        if "agent" not in st.session_state:
            st.session_state.agent = MindBodyAgent()
        intro_msg = generate_intro_message(st.session_state.agent.memory)
        st.session_state.messages.append({
            "role": "bot",
            "content": intro_msg,
            "ts": st.session_state.get("last_intro_ts", "")
        })
        st.session_state.intro_message_shown = True
    except Exception as e:
        print(f"[WARN] Errore nel messaggio introduttivo: {e}")

# ============ STILE INLINE (niente CSS esterno) ============
def inject_inline_chat_css():
    st.markdown("""
    <style>
      .chat-wrap { max-width: 800px; margin: 0 auto; }
      .msg { display: inline-block; padding: 10px 14px; border-radius: 16px; margin: 6px 0; line-height: 1.35; }
      .row { display: flex; margin: 0.25rem 0; }
      .row.user { justify-content: flex-end; }
      .row.bot  { justify-content: flex-start; }
      .msg.user {
        background: #e8f0fe; color: #0b132b; border: 1px solid #d1e3ff;
        border-top-right-radius: 6px;
        max-width: 75%;
      }
      .msg.bot {
        background: #f6f7f9; color: #111; border: 1px solid #e6e6e6;
        border-top-left-radius: 6px;
        max-width: 75%;
      }
      .ts { font-size: 0.75rem; opacity: 0.6; margin-top: 2px; }
      .bubble { display:flex; flex-direction:column; }
    </style>
    """, unsafe_allow_html=True)

inject_inline_chat_css()

# ============ TITOLO ============
st.title("Sono Mind&Body, il tuo coach personale")

# ============ RENDER MESSAGGI ============
st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for m in st.session_state.messages:
    role = m.get("role", "bot")
    content = m.get("content", "")
    ts = m.get("ts", "")
    row_cls = "user" if role == "user" else "bot"
    bubble_cls = "msg user" if role == "user" else "msg bot"
    st.markdown(
        f'''
        <div class="row {row_cls}">
          <div class="bubble">
            <div class="{bubble_cls}">{content}</div>
            <div class="ts">{ts}</div>
          </div>
        </div>
        ''',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# ============ INPUT / INVIO ============
from chat_input_manager import render_chat_input, process_user_message

user_input, send_btn = render_chat_input(
    form_key="chat_form_main",
    input_key="chat_text_main",
    button_key="chat_send_main",
    placeholder="Scrivi un messaggio…"
)

process_user_message(user_input, send_btn)