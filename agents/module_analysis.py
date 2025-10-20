# ======================================
# 📊 MODULE: ANALYSIS — Report settimanale mente + corpo
# ======================================

import os
import pandas as pd
import datetime
import google.generativeai as genai
from config.settings import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)


DATA_DIR = "data"

def handle_weekly_analysis(username: str = "anonimo"):
    """
    Combina i dati mentali e fisici e genera un report motivante settimanale.
    Non si blocca mai se i nomi delle colonne non corrispondono perfettamente.
    Chiede conferma all’utente in caso di ambiguità.
    """
    # Crea la cartella utente e i percorsi dei file personali
    user_dir = os.path.join("data", "users", username)
    os.makedirs(user_dir, exist_ok=True)
    mental_path = os.path.join(user_dir, "mind_state.csv")
    train_path = os.path.join(user_dir, "allenamenti.csv")

    if not os.path.exists(mental_path) and not os.path.exists(train_path):
        return "Non ho ancora abbastanza dati per analizzare la tua settimana 😅"

    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    summary = {"allenamenti": 0, "durata_tot": 0, "stress_medio": None}

    # ⚙️ Allenamenti
    try:
        df_train = pd.read_csv(train_path)
    except Exception:
        df_train = pd.DataFrame()
    if not df_train.empty:
        if "data" in df_train.columns:
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
    try:
        df_mind = pd.read_csv(mental_path)
    except Exception:
        df_mind = pd.DataFrame()
    if not df_mind.empty:
        if "data" in df_mind.columns:
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

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(analysis_prompt)

    # ✅ Restituisci il report finale
    return f"📅 Report settimanale corpo-mente per **{username}** 🧘‍♂️\n\n{response.text}"