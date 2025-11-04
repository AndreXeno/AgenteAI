# ======================================
# 🧩 MODULE: INTENT CLASSIFIER — Riconoscimento dell'intento utente
# ======================================

import google.generativeai as genai
from config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


def classify_intent(user_input: str, context: str = "", profile_summary: str = "") -> str:
    """
    Classifica l’intento dell’utente in:
    'allenamento', 'mente', 'analisi', 'riflessione', 'info_utente' o 'generico'.
    Usa Gemini 2.5 Flash con contesto emotivo e profilo utente.
    """

    prompt = f"""
    Sei parte del sistema Mind&Body, un coach digitale empatico che integra benessere fisico e mentale.
    Analizza il messaggio dell’utente considerando anche il contesto delle conversazioni precedenti
    e il suo profilo personale.

    Devi classificare il messaggio in UNA sola delle seguenti categorie:
    - 'allenamento' → esercizi, obiettivi fisici, allenarsi, progressi, performance.
    - 'mente' → emozioni, stress, felicità, ansia, riflessioni interiori, motivazione, malessere implicito.
    - 'riflessione' → analisi personale o lezioni apprese da esperienze passate.
    - 'analisi' → dati, statistiche, progressi numerici, report settimanali.
    - 'info_utente' → richieste dirette sull’utente, come “cosa pensi di me”, “come sto andando”, “qual è il mio ultimo allenamento”, “quali dati hai salvato su di me”, o domande sui suoi progressi o sul suo stato personale.
    - 'generico' → saluti, messaggi neutri o non classificabili.

    🔹 Se percepisci un tono emotivo o mentale, anche implicito, scegli 'mente'.
    🔹 Se il messaggio riguarda numeri, analisi o performance → 'analisi'.
    🔹 Se è auto-riflessivo → 'riflessione'.
    🔹 Se parla di attività fisica o allenamenti → 'allenamento'.
    🔹 Se chiede informazioni su se stesso, le sue prestazioni, o cosa pensa il coach di lui, oppure sui dati personali salvati → 'info_utente'.

    Esempi:
    - “oggi non mi sento molto bene” → mente
    - “ieri ho corso 5 km” → allenamento
    - “sto riflettendo su come migliorare la costanza” → riflessione
    - “fammi vedere i progressi della settimana” → analisi
    - “cosa pensi di me?” → info_utente
    - “qual è stato il mio ultimo allenamento?” → info_utente
    - “quali dati personali hai su di me?” → info_utente
    - “mostrami le informazioni che hai salvato su di me” → info_utente
    - “ciao” → generico

    Contesto recente della conversazione:
    {context if context else 'Nessun contesto recente disponibile.'}

    Profilo utente sintetizzato:
    {profile_summary if profile_summary else 'Profilo non disponibile.'}

    Messaggio utente: {user_input}
    Rispondi solo con la categoria scelta.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        intent = response.text.strip().lower() if response and response.text else "generico"
        print(f"🤖 Intent Gemini 2.5 Flash (contestuale): {intent}")
    except Exception as e:
        print(f"[WARN] ⚠️ Errore classificazione Gemini: {e}")
        intent = "generico"

    return intent
