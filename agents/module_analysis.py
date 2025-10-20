# ======================================
# 📊 MODULE: ANALYSIS — Report settimanale mente + corpo
# ======================================

import os
import pandas as pd
import datetime
from google import genai

# Inizializza il client Gemini (usa GEMINI_API_KEY se impostata)
from config.settings import GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)


DATA_DIR = "data"

def handle_weekly_analysis():
    """
    Combina i dati mentali e fisici e genera un report motivante settimanale.
    Non si blocca mai se i nomi delle colonne non corrispondono perfettamente.
    Chiede conferma all’utente in caso di ambiguità.
    """

    mental_path = os.path.join(DATA_DIR, "log_mentale.csv")
    train_path = os.path.join(DATA_DIR, "allenamenti_manual.csv")

    if not os.path.exists(mental_path) and not os.path.exists(train_path):
        return "Non ho ancora abbastanza dati per analizzare la tua settimana 😅"

    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    summary = {"allenamenti": 0, "durata_tot": 0, "stress_medio": None}

    # ⚙️ Allenamenti
    if os.path.exists(train_path):
        df_train = pd.read_csv(train_path)
        df_train["data"] = pd.to_datetime(df_train["data"], errors="coerce")
        df_train = df_train[df_train["data"].dt.date >= week_ago]

        if not df_train.empty:
            summary["allenamenti"] = len(df_train)

            # Controlla colonne possibili
            possible_dur_cols = [c for c in df_train.columns if "durata" in c.lower()]
            if possible_dur_cols:
                durata_col = possible_dur_cols[0]
                print(f"✅ Colonna durata rilevata: '{durata_col}'")
                summary["durata_tot"] = df_train[durata_col].sum()
            else:
                return (
                    "Non riesco a trovare la colonna durata nel file allenamenti. "
                    f"Le colonne disponibili sono: {list(df_train.columns)}. "
                    "Potresti dirmi come si chiama quella con la durata in minuti?"
                )

    # 🧠 Mente
    if os.path.exists(mental_path):
        df_mind = pd.read_csv(mental_path)
        df_mind["data"] = pd.to_datetime(df_mind["data"], errors="coerce")
        df_mind = df_mind[df_mind["data"].dt.date >= week_ago]

        if not df_mind.empty:
            possible_stress_cols = [c for c in df_mind.columns if "stress" in c.lower()]
            if possible_stress_cols:
                stress_col = possible_stress_cols[0]
                print(f"✅ Colonna stress rilevata: '{stress_col}'")
                summary["stress_medio"] = round(df_mind[stress_col].mean(), 1)
            else:
                return (
                    "Non riesco a trovare la colonna stress nel file mentale. "
                    f"Le colonne disponibili sono: {list(df_mind.columns)}. "
                    "Potresti dirmi come si chiama quella con il livello di stress?"
                )

    # 📊 Prompt per Gemini
    analysis_prompt = f"""
    Crea un resoconto motivante settimanale per l'utente basandoti su questi dati:

    - Allenamenti totali: {summary['allenamenti']}
    - Durata totale: {summary['durata_tot']} minuti
    - Stress medio: {summary['stress_medio'] if summary['stress_medio'] else 'non disponibile'}

    Fornisci:
    1. Un breve riepilogo numerico
    2. Una riflessione mente-corpo
    3. Una frase motivante finale
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=analysis_prompt
    )

    # ✅ Restituisci il report finale
    return f"📅 Report settimanale corpo-mente ️\n\n{response.text}"