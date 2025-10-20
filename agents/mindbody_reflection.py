# ======================================
# 💬 MODULE: MIND-BODY REFLECTION — Riflessioni empatiche su allenamento o giornata
# ======================================

import os
import pandas as pd
import datetime
import google.generativeai as genai
from config.settings import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

DATA_DIR = "data"


def handle_training_reflection(user_input: str):
    """
    Analizza una riflessione sull'allenamento o sulla giornata e risponde in modo empatico,
    usando i dati già registrati (senza analisi tecniche).
    """

    # 1️⃣ Recupera contesto recente dagli allenamenti
    train_path = os.path.join(DATA_DIR, "allenamenti_manual.csv")

    summary = ""
    if os.path.exists(train_path):
        df = pd.read_csv(train_path)
        df["data"] = pd.to_datetime(df["data"])
        last_week = datetime.date.today() - datetime.timedelta(days=7)
        recent = df[df["data"].dt.date >= last_week]

        if not recent.empty:
            tot = len(recent)
            media = recent["durata_min"].mean() if "durata_min" in recent.columns else 0
            ultima = df.iloc[-1]
            summary = (
                f"Negli ultimi 7 giorni hai fatto {tot} allenamenti "
                f"con una durata media di {media:.0f} minuti. "
                f"L'ultimo è stato il {ultima['data']} ({ultima['tipo']}, {ultima['durata_min']} min)."
            )
        else:
            summary = "Negli ultimi giorni non ci sono stati allenamenti registrati."
    else:
        summary = "Non ho ancora dati sui tuoi allenamenti."

    # 2️⃣ Genera risposta empatica con Gemini
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
    L'utente ha detto: "{user_input}"

    Contesto sui suoi allenamenti:
    {summary}

    Rispondi come un coach di vita e motivatore sportivo empatico:
    - Ascolta e riconosci le emozioni (felicità, stanchezza, stress, demotivazione, orgoglio, ecc.)
    - Riconosci i suoi sforzi fisici e mentali senza dare dati numerici diretti
    - Offri una riflessione e un consiglio umano e incoraggiante
    - Evita schemi o elenchi, scrivi come se parlassi direttamente con lui.
    """

    response = model.generate_content(prompt)

    return response.text