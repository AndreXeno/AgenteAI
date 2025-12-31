# ======================================
# 🧠 MODULE: MIND — Stato mentale e consigli
# ======================================

import os
import datetime
import json
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import time
import random

from config.settings import GEMINI_API_KEY
from agents.knowledge_loader import query_knowledge
from agents.prompts.base_prompt import BASE_PROMPT
from agents.prompts.modules.mind_prompt import MIND_PROMPT

# Inizializza Gemini con fallback robusto
def initialize_gemini():
    api_key = GEMINI_API_KEY
    if not api_key:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    else:
        print("[WARN] Chiave API Gemini non trovata. Il modulo Mind funzionerà in modalità ridotta.")
        return False

gemini_initialized = initialize_gemini()

DATA_DIR = "data"

def handle_mind_state(user_input: str, username: str = "anonimo"):
    """
    Risponde al messaggio dell'utente usando un'unica chiamata a Gemini,
    ma FILTRATA da keyword per evitare di consumare quota su messaggi generici.
    """
    user_dir = os.path.join(DATA_DIR, "users", username)
    os.makedirs(user_dir, exist_ok=True)
    mind_path = os.path.join(user_dir, "mind_state.csv")

    # 1. FILTRO KEYWORD (Stabilità/Quota)
    emotive_keywords = [
        "mi sento", "sono stressato", "ansia", "felice", "triste", "arrabbiato", "depress*", "preoccupat*",
        "agitato", "ansioso", "stress", "paura", "disperato", "emozion*", "nervoso", "sereno", "contento",
        "rabbia", "gioia", "solitudine", "angoscia", "malinconia", "stanco", "affaticato", "frustrato",
        "suicid*", "mort*", "uccider*", "farla finita", "non voglio vivere", "non ce la faccio", "disperazion",
        "dolore", "sofferenza", "aiuto", "morire", "grigio", "buio", "inutile", "fallito", "finito"
    ]
    neutral_keywords = [
        "allenamento", "scuola", "amici", "giochi", "sport", "studio", "lavoro", "tempo libero",
        "film", "libro", "cibo", "viaggio", "camminata", "passeggiata", "progetto", "ciao", "buongiorno", "sera"
    ]

    user_input_lower = user_input.lower()
    is_emotive = any(kw in user_input_lower for kw in emotive_keywords)
    is_neutral = any(kw in user_input_lower for kw in neutral_keywords) and not is_emotive

    # 2. SE NEUTRO O FALLBACK (Risparmio API)
    if not is_emotive and not is_neutral:
        # Fallback statico gratutito
        fallback_response = "Ciao! Come posso aiutarti oggi?"
        today_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = pd.DataFrame([[today_ts, username, user_input, fallback_response, "neutro"]],
                             columns=["timestamp", "username", "input", "risposta", "umore_inferito"])
        try:
             header_exists = os.path.exists(mind_path)
             entry.to_csv(mind_path, mode="a", header=not header_exists, index=False)
        except Exception:
            pass
        return f"🧠 {fallback_response}"

    if is_neutral:
        # Chiamata semplice (Economy)
        if not gemini_initialized:
             return "🧠 Ciao! Purtroppo sono offline."
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(f"Rispondi brevemente a: {user_input}")
            return f"🧠 {response.text.strip()}"
        except Exception:
            return "🧠 Ciao! Tutto bene?"

    # 3. SE EMOTIVO -> CHIAMATA COMPLETA (Single Pass)
    
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

    # Recupera conoscenze pertinenti dai documenti (se initialized)
    knowledge_text = "Nessuna conoscenza aggiuntiva trovata."
    try:
        relevant_docs = query_knowledge(user_input)
        if relevant_docs:
            knowledge_text = "\n".join(relevant_docs)
    except Exception:
        pass

    if not gemini_initialized:
        return "🧠 [FALLBACK] Mi dispiace, sono offline al momento. Riprova più tardi."

    # --- COSTUZIONE PROMPT UNIFICATO ---
    contesto = f"""DATI UTENTE:
Diario (ultimi 3gg): {diario_recent if diario_recent else 'Nessuno'}
Allenamenti (ultimi 3gg): {allenamenti_recent if allenamenti_recent else 'Nessuno'}
Profilo: {json.dumps(profilo_utente, ensure_ascii=False) if profilo_utente else 'N/A'}

CONOSCENZE UTILI:
{knowledge_text}
"""

    unified_prompt = f"""{BASE_PROMPT}

CONTESTO AGGIUNTIVO:
{contesto}

MESSAGGIO UTENTE: "{user_input}"

COMPITI (Esegui in ordine):
1. ANALISI SEMANTICA:
   - Identifica il tono (es. sad, happy, neutral, angry, hopeless, anxious).
   - Valuta il RISCHIO (none, low, medium, high, critical) per suicidio, autolesionismo, o pericolo grave.
   
2. GENERAZIONE RISPOSTA:
   - Se Rischio > low OPPURE Tono emotivo: Usa empatia profonda, accogli il sentimento.
   - Se Rischio = none E Tono neutro/positivo: Rispondi in modo conversazionale, breve e amichevole.
   - REGOLA SICUREZZA: Se rilevi alto rischio (suicidio/autolesionismo), devi suggerire aiuto professionale o numeri emergenza.
   - NON dare consigli non richiesti (tranne nel caso di sicurezza).

OUTPUT RICHIESTO (JSON ESCLUSIVAMENTE):
{{
  "analysis": {{
    "tone": "valore",
    "risk_level": "valore (none/low/medium/high/critical)",
    "risk_type": "valore (nessuno/suicidio/depressione_grave/etc)",
    "description": "breve analisi"
  }},
  "response_text": "Il testo della risposta per l'utente"
}}
"""

    max_retries = 5
    base_delay = 4

    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            # Generazione unica
            response = model.generate_content(unified_prompt, generation_config={"response_mime_type": "application/json"})
            
            result = json.loads(response.text)
            
            analysis = result.get("analysis", {})
            risposta_testo = result.get("response_text", "Mi dispiace, non ho capito.")
            
            tone = analysis.get("tone", "neutral").lower()
            risk_level = analysis.get("risk_level", "none").lower()
            risk_type = analysis.get("risk_type", "nessuno").lower()
            risk_desc = analysis.get("description", "")
            
            # --- LOGICA DI SALVATAGGIO ---
            
            # 1. Salva log generale in mind_state.csv
            today_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = pd.DataFrame([[today_ts, username, user_input, risposta_testo, tone]],
                                 columns=["timestamp", "username", "input", "risposta", "umore_inferito"])
            
            try:
                 header_exists = os.path.exists(mind_path)
                 entry.to_csv(mind_path, mode="a", header=not header_exists, index=False)
            except Exception as e:
                print(f"[WARN] Errore salvataggio mind_state: {e}")

            # 2. Salva log PERICOLO se necessario
            if risk_level in ["medium", "high", "critical", "suicidal_intent", "severe_depression", "danger", "self_harm"]:
                danger_path = os.path.join(user_dir, "dangerous_behaviors.csv")
                danger_entry = pd.DataFrame([[today_ts, username, user_input, risk_level, risk_type, risk_desc]],
                                          columns=["timestamp", "username", "input", "risk_level", "risk_type", "description"])
                danger_entry.to_csv(danger_path, mode="a", header=not os.path.exists(danger_path), index=False)
                print(f"[ALERT] ⚠️ COMPORTAMENTO PERICOLOSO RILEVATO: {risk_level} ({risk_type})")

            print(f"[LOG] 💾 Transazione completata. Tono: {tone}, Rischio: {risk_level}")
            
            # DEBUG: Aggiungi info di debug alla risposta visibile
            # debug_info = f"\n\n[DEBUG: Tono={tone}, Rischio={risk_level}, Tipo={risk_type}]"
            return f"🧠 {risposta_testo}"

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "ResourceExhausted" in error_msg or "Quota exceeded" in error_msg:
                # Calcola delay con backoff esponenziale + jitter
                delay = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                print(f"[WARN] Quota Gemini superata. Riprovo tra {delay:.2f}s (Tentativo {attempt+1}/{max_retries})...")
                time.sleep(delay)
            else:
                print(f"[ERROR] Errore API/JSON non recuperabile: {e}")
                return "🧠 Mi dispiace, si è verificato un errore tecnico momentaneo. Riprova tra poco."

    return "🧠 Il servizio è momentaneamente molto occupato. Per favore attendi 30 secondi e riprova."