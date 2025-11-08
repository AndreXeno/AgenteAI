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
    Analizza un allenamento manuale, lo registra in CSV,
    confronta con gli allenamenti passati e genera feedback tecnico + motivazione.
    - Se lo chiede o lo fa intendere dai una comparazione rispetto allo stesso allenamento delle volte precedenti.
    - Fai notare se c'é stato un miglioramento o peggioramento, dai consigli e spiega il motivo di questo andamento
    - Dai consigli pratici su come migliorare sull'allenamento in questione.
    - Personalizza feedback basandoti sul profilo utente e umore recente.
    """
    user_dir = os.path.join("data", "users", username)
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, "allenamenti.csv")

    text = user_input.lower()

    emotional_words = ["triste", "felice", "solo", "stress", "ansia", "agitato", "demotivato", "arrabbiato", "rassegnato", "stanco", "isolato", "paura", "insicuro", "invidioso", "geloso"]
    if any(word in text for word in emotional_words):
        # Se ci sono emozioni, registra solo i dati ma non genera feedback tecnico
        parsed = parse_training_data(text)
        duration = parsed.get("durata_minuti", 0)
        distance = parsed.get("distanza_km", None)
        bpm = parsed.get("bpm_medio", None)
        slope = parsed.get("pendenza_%", None)
        notes = user_input

        today = datetime.date.today().strftime("%Y-%m-%d")

        df = pd.DataFrame([[username, today, "non specificato", duration, distance, bpm, slope, notes]],
                          columns=["username", "data", "tipo", "durata_min", "distanza_km", "bpm", "pendenza", "note"])
        df.to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False)

        return "🏋️ Ho registrato il tuo allenamento. Sembra che oggi ci sia anche molto di cui parlare... vuoi raccontarmi come ti senti?"

    # 🔹 Estrai tipo di allenamento
    activity_match = re.search(r"(corsa outdoor|corsa indoor|palestra|nuoto|cyclette|calcio|basket|pallavolo)", text)
    if not activity_match:
        return "Non ho riconosciuto il tipo di allenamento (es. 'corsa 40 minuti')."
    activity = activity_match.group(1)

    # 🔹 Estrai tutti i dati rilevanti
    parsed = parse_training_data(text)
    duration = parsed.get("durata_minuti", 0)
    distance = parsed.get("distanza_km", None)
    bpm = parsed.get("bpm_medio", None)
    slope = parsed.get("pendenza_%", None)
    notes = user_input

    # 🔹 Salvataggio CSV con colonne aggiuntive
    today = datetime.date.today().strftime("%Y-%m-%d")

    df = pd.DataFrame([[username, today, activity, duration, distance, bpm, slope, notes]],
                      columns=["username", "data", "tipo", "durata_min", "distanza_km", "bpm", "pendenza", "note"])
    df.to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False)

    # 🔹 Analisi statistica (solo su durata per ora)
    prev_df = pd.read_csv(file_path)
    same_user = prev_df[prev_df["username"] == username]
    same_type = same_user[same_user["tipo"] == activity]
    avg_duration = same_type["durata_min"].mean() if not same_type.empty else duration
    diff = duration - avg_duration
    trend = "🔺" if diff > 0 else "🔻" if diff < 0 else "➖"
    trend_text = f"{'+' if diff > 0 else ''}{int(diff)} min {trend}"

    # 🔹 Lettura profilo utente e umore recente
    profile = read_user_profile(username)
    mood = read_recent_mood(username)

    # Prepara stringhe di personalizzazione
    profile_info = ""
    if profile:
        age = profile.get("età") or profile.get("eta") or profile.get("age")
        level = profile.get("livello") or profile.get("level")
        goals = profile.get("obiettivi") or profile.get("goals")
        if age:
            profile_info += f"Età utente: {age}\n"
        if level:
            profile_info += f"Livello di allenamento: {level}\n"
        if goals:
            profile_info += f"Obiettivi: {goals}\n"

    mood_info = ""
    if mood is not None:
        mood_info = f"Umore recente: {mood}\n"

    from agents.prompts.base_prompt import BASE_PROMPT
    from agents.prompts.modules.training_prompt import TRAINING_PROMPT

    # 🔹 Prompt unificato per feedback tecnico + motivazione con personalizzazione
    analysis_prompt = f"""{BASE_PROMPT}
{TRAINING_PROMPT}

Profilo utente:
{profile_info}{mood_info}
Dati dell'allenamento:
🏃 Tipo: {activity}
⏱️ Durata: {duration or 'non indicata'} minuti
📏 Distanza: {distance or 'non indicata'} km
❤️ BPM medio: {bpm or 'non disponibile'}
↗️ Pendenza: {slope or 'non indicata'} %
📝 Descrizione: "{notes}"

📊 Statistiche precedenti:
- Media durata {activity}: {avg_duration:.1f} minuti
- Differenza rispetto alla media: {trend_text}

Fornisci:
1️⃣ Un feedback tecnico (prestazione, ritmo, andamento) personalizzato in base al profilo e umore utente
2️⃣ Un consiglio pratico e motivante per migliorare, tenendo conto degli obiettivi e livello
3️⃣ Mantieni un tono realistico e positivo, come un coach empatico Mind&Body.
"""

    # ✅ Generazione del feedback tramite Gemini con gestione errori e fallback
    try:
        if not api_key:
            raise ValueError("API key for Gemini not configured.")
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(analysis_prompt)
        feedback_text = response.text.strip() if response and hasattr(response, "text") and response.text else None
        if not feedback_text:
            logging.error(f"[LOG] 💬 Feedback generato vuoto per {username}, uso fallback.")
            feedback_text = "Non sono riuscito a generare un feedback dettagliato al momento, ma il tuo allenamento è stato registrato con successo. Continua così!"
    except Exception as e:
        logging.error(f"[LOG] Errore durante generazione feedback Gemini per {username}: {e}")
        feedback_text = "Non sono riuscito a generare un feedback dettagliato al momento, ma il tuo allenamento è stato registrato con successo. Continua così!"

    # 🔹 Messaggio finale
    info_parts = [
        f"🏋️ Allenamento registrato ✅ ({activity})",
        f"Durata: {duration} min | Distanza: {distance or '–'} km | BPM: {bpm or '–'} | Pendenza: {slope or '–'}%",
        f"Media precedente: {avg_duration:.1f} min → {trend_text}",
        "",
        feedback_text
    ]

    return "\n".join(info_parts)