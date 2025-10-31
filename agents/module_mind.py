# ======================================
# 🧠 MODULE: MIND — Stato mentale e consigli
# ======================================

import os
import datetime
import pandas as pd
import google.generativeai as genai

from config.settings import GEMINI_API_KEY
from agents.knowledge_loader import query_knowledge
from agents.prompts.base_prompt import BASE_PROMPT
from agents.prompts.modules.mind_prompt import MIND_PROMPT

# Inizializza Gemini
genai.configure(api_key=GEMINI_API_KEY)

DATA_DIR = "data"

def handle_mind_state(user_input: str, username: str = "anonimo"):
    """
    Risponde al messaggio dell'utente in modo empatico e naturale,
    usando il sistema di prompt unificati (BASE_PROMPT + MIND_PROMPT).
    """
    user_dir = os.path.join(DATA_DIR, "users", username)
    os.makedirs(user_dir, exist_ok=True)
    mind_path = os.path.join(user_dir, "mind_state.csv")

    # Recupera conoscenze pertinenti dai documenti
    relevant_docs = query_knowledge(user_input)
    num_docs = len(relevant_docs) if relevant_docs else 0
    print(f"[LOG] 🧠 handle_mind_state: trovate {num_docs} fonti rilevanti per '{user_input}'")

    knowledge_text = "\n".join(relevant_docs) if relevant_docs else "Nessuna conoscenza aggiuntiva trovata."

    # Prompt unificato
    prompt = f"""{BASE_PROMPT}
{MIND_PROMPT}

📘 Conoscenze utili dai documenti (se pertinenti):
{knowledge_text}

Utente: {user_input}
Coach:"""

    # Genera risposta con Gemini
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    # Salva lo stato mentale in CSV personale
    today = datetime.date.today().strftime("%Y-%m-%d")
    entry = pd.DataFrame([[today, username, user_input, response.text]],
                         columns=["data", "username", "input", "risposta"])
    entry.to_csv(mind_path, mode="a", header=not os.path.exists(mind_path), index=False)

    print(f"[LOG] 💾 Stato mentale salvato in {mind_path}")
    return f"🧠 {response.text}"