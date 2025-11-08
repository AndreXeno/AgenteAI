# ======================================
# 🧠 MODULE: MIND — Stato mentale e consigli
# ======================================

import os
import datetime
import json
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
    Integra dati recenti dal diario, allenamenti e profilo utente,
    genera un prompt più sofisticato e profondo con Gemini,
    stima l'umore e salva tutto in mind_state.csv.
    """
    user_dir = os.path.join(DATA_DIR, "users", username)
    os.makedirs(user_dir, exist_ok=True)
    mind_path = os.path.join(user_dir, "mind_state.csv")

    # Carica dati recenti dal diario utente (ultimi 3 giorni)
    diario_path = os.path.join(user_dir, "diario_utente.csv")
    diario_recent = ""
    if os.path.exists(diario_path):
        try:
            diario_df = pd.read_csv(diario_path, parse_dates=["data"])
            cutoff_date = datetime.date.today() - datetime.timedelta(days=3)
            recent_entries = diario_df[diario_df["data"] >= pd.Timestamp(cutoff_date)]
            if not recent_entries.empty:
                diario_recent = "\n".join(
                    f"{row['data'].strftime('%Y-%m-%d')}: {row['testo']}" for _, row in recent_entries.iterrows()
                )
        except Exception as e:
            print(f"[WARN] Impossibile leggere diario utente: {e}")

    # Carica dati recenti dagli allenamenti (ultimi 3 giorni)
    allenamenti_path = os.path.join(DATA_DIR, "allenamenti.csv")
    allenamenti_recent = ""
    if os.path.exists(allenamenti_path):
        try:
            allen_df = pd.read_csv(allenamenti_path, parse_dates=["data"])
            cutoff_date = datetime.date.today() - datetime.timedelta(days=3)
            recent_allen = allen_df[(allen_df["data"] >= pd.Timestamp(cutoff_date)) & (allen_df["username"] == username)]
            if not recent_allen.empty:
                allenamenti_recent = "\n".join(
                    f"{row['data'].strftime('%Y-%m-%d')}: {row['tipo']} - Durata: {row['durata_minuti']} min" for _, row in recent_allen.iterrows()
                )
        except Exception as e:
            print(f"[WARN] Impossibile leggere allenamenti: {e}")

    # Carica profilo utente
    profilo_path = os.path.join(user_dir, "profilo_utente.json")
    profilo_utente = {}
    if os.path.exists(profilo_path):
        try:
            with open(profilo_path, "r", encoding="utf-8") as f:
                profilo_utente = json.load(f)
        except Exception as e:
            print(f"[WARN] Impossibile leggere profilo utente: {e}")

    # Recupera conoscenze pertinenti dai documenti
    relevant_docs = query_knowledge(user_input)
    knowledge_text = "\n".join(relevant_docs) if relevant_docs else "Nessuna conoscenza aggiuntiva trovata."

    # Costruisci contesto dettagliato per il prompt
    contesto = f"""Diario degli ultimi 3 giorni:
{diario_recent if diario_recent else 'Nessuna voce recente nel diario.'}

Allenamenti degli ultimi 3 giorni:
{allenamenti_recent if allenamenti_recent else 'Nessun allenamento recente registrato.'}

Profilo utente:
{json.dumps(profilo_utente, ensure_ascii=False, indent=2) if profilo_utente else 'Profilo utente non disponibile.'}

Conoscenze utili dai documenti:
{knowledge_text}
"""

    # Prompt unificato e potenziato
    prompt = f"""{BASE_PROMPT}
{MIND_PROMPT}

Usa il seguente contesto per rispondere con empatia, realismo e conoscenze psicologiche profonde:

{contesto}

Utente: {user_input}
Coach:"""

    # Genera risposta con Gemini
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    risposta_testo = response.text.strip()

    # Stima umore basata su input e risposta
    mood_prompt = f"""Determina l'umore complessivo (positivo, neutro, negativo) basandoti sul testo dell'utente e sulla risposta del coach.

Testo utente: {user_input}
Risposta coach: {risposta_testo}

Rispondi solo con una parola: positivo, neutro o negativo."""
    mood_response = model.generate_content(mood_prompt)
    umore_inferito = mood_response.text.strip().lower()
    if umore_inferito not in {"positivo", "neutro", "negativo"}:
        umore_inferito = "neutro"

    # Salva lo stato mentale in CSV personale
    today = datetime.date.today().strftime("%Y-%m-%d")
    entry = pd.DataFrame([[today, username, user_input, risposta_testo, umore_inferito]],
                         columns=["data", "username", "input", "risposta", "umore_inferito"])
    entry.to_csv(mind_path, mode="a", header=not os.path.exists(mind_path), index=False)

    print(f"[LOG] 💾 Stato mentale salvato in {mind_path} con umore inferito: {umore_inferito}")
    return f"🧠 {risposta_testo}"