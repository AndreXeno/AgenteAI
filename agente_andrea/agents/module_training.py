# ======================================
# 🏋️ MODULE: TRAINING — Allenamenti manuali e statistiche
# ======================================

import os
import re
import datetime
import json
import pandas as pd
import logging
from config.settings import GEMINI_API_KEY
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
if not api_key:
    logging.error("Gemini API key not found in config.settings or .env")
genai.configure(api_key=api_key)

DATA_DIR = "data"


def parse_training_data(user_input: str):
    """Estrae automaticamente durata, distanza, battiti, pendenza e altre metriche dal testo."""
    data = {}
    text = user_input.lower()

    match = re.search(r"(\d+)\s*(min|minuti)", text)
    if match:
        data["durata_minuti"] = int(match.group(1))

    match = re.search(r"(\d+(?:\.\d+)?)\s*(km|chilometri)", text)
    if match:
        data["distanza_km"] = float(match.group(1))

    match = re.search(r"(\d+)\s*(bpm|battiti)", text)
    if match:
        data["bpm_medio"] = int(match.group(1))

    match = re.search(r"(\d+(?:\.\d+)?)\s*%(\s*pendenza)?", text)
    if match:
        data["pendenza_%"] = float(match.group(1))

    return data


def read_user_profile(username: str):
    """Legge il profilo utente da JSON se esiste, altrimenti ritorna dizionario vuoto."""
    profile_path = os.path.join(DATA_DIR, "users", username, "profilo_utente.json")
    if os.path.exists(profile_path):
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)
            return profile
        except Exception:
            return {}
    return {}


def read_recent_mood(username: str, days: int = 7):
    """
    Legge l'umore recente dal diario_utente.csv degli ultimi 'days' giorni.
    Restituisce la media o la descrizione più frequente o None se non disponibile.
    """
    diary_path = os.path.join(DATA_DIR, "users", username, "diario_utente.csv")
    if not os.path.exists(diary_path):
        return None
    try:
        df = pd.read_csv(diary_path, parse_dates=["data"])
        cutoff_date = pd.Timestamp(datetime.date.today() - datetime.timedelta(days=days))
        recent_entries = df[df["data"] >= cutoff_date]

        if recent_entries.empty or "umore" not in recent_entries.columns:
            return None

        # Se umore è numerico, calcoliamo media, altrimenti la modalità testo
        if pd.api.types.is_numeric_dtype(recent_entries["umore"]):
            return recent_entries["umore"].mean()
        else:
            mode = recent_entries["umore"].mode()
            if not mode.empty:
                return mode.iloc[0]
            return None
    except Exception:
        return None


def handle_training(user_input: str, username: str = "anonimo"):
    """
    Analizza un allenamento già registrato nel CSV e fornisce feedback o consigli.
    Non aggiunge mai nuovi allenamenti automaticamente.
    """
    user_dir = os.path.join(DATA_DIR, "users", username)
    file_path = os.path.join(user_dir, "allenamenti.csv")

    if not os.path.exists(file_path):
        return "Non ho trovato allenamenti registrati per te. Puoi aggiungerli nella sezione dedicata!"

    df = pd.read_csv(file_path)
    if df.empty:
        return "Non ho trovato allenamenti registrati. Inseriscine uno manualmente per poterne parlare insieme!"

    text = user_input.lower()
    matched = None

    # 🔍 Riconosce riferimenti temporali o tipo di allenamento
    for _, row in df.iterrows():
        tipo = str(row.get("tipo", "")).lower()
        data = str(row.get("data", ""))
        note = str(row.get("note", "")).lower()

        if any(k in text for k in [tipo, data[:10], "ieri", "ultimo", "scorso"]) or tipo in text or any(word in text for word in note.split()):
            matched = row
            break

    if matched is None:
        return "Parli pure del tuo allenamento, ma non trovo un record corrispondente. Se vuoi, specifica il tipo o il giorno."

    # 📊 Allenamento trovato → fornisci analisi e consiglio
    activity = matched.get("tipo", "allenamento")
    duration = matched.get("durata_min", "–")
    bpm = matched.get("bpm", "–")
    distance = matched.get("distanza_km", "–")
    slope = matched.get("pendenza", "–")

    profile = read_user_profile(username)
    mood = read_recent_mood(username)

    analysis_prompt = f"""
L'utente sta parlando del suo allenamento di tipo '{activity}'.

Dati registrati:
Durata: {duration} minuti
Distanza: {distance} km
Battiti medi: {bpm}
Pendenza: {slope}%

Profilo utente:
{json.dumps(profile, indent=2, ensure_ascii=False)}

Umore recente: {mood}

Fornisci:
1️⃣ Un feedback tecnico sull'allenamento (andamento, ritmo, performance).
2️⃣ Un consiglio personalizzato per migliorare nei prossimi allenamenti.
3️⃣ Un breve messaggio motivazionale coerente con l’umore e il tono dell’utente.
Non proporre mai di aggiungere o registrare nuovi dati.
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(analysis_prompt)
        feedback = response.text.strip() if hasattr(response, "text") else str(response)
    except Exception as e:
        logging.error(f"[AI] Errore nel feedback Gemini: {e}")
        feedback = "Posso darti qualche consiglio generale sul tuo allenamento, anche senza i dettagli tecnici."

    return f"📊 Riepilogo allenamento ({activity}) — Durata {duration} min, BPM {bpm}, Distanza {distance} km.\n\n{feedback}"