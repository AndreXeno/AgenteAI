# ======================================
# 🏋️ MODULE: TRAINING — Allenamenti manuali e statistiche
# ======================================

import os
import re
import datetime
import pandas as pd
import google.generativeai as genai
from config.settings import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

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


def handle_training(user_input: str, username: str = "anonimo"):
    """
    Analizza un allenamento manuale, lo registra in CSV,
    confronta con gli allenamenti passati e genera feedback tecnico + motivazione.
    - Se lo chiede o lo fa intendere dai una comparazione rispetto allo stesso allenamento delle volte precedenti.
    - Fai notare se c'é stato un miglioramento o peggioramento, dai consigli e spiega il motivo di questo andamento
    - Dai consigli pratici su come migliorare sull'allenamento in questione.
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

    from agents.prompts.base_prompt import BASE_PROMPT
    from agents.prompts.modules.training_prompt import TRAINING_PROMPT

    # 🔹 Prompt unificato per feedback tecnico + motivazione
    analysis_prompt = f"""{BASE_PROMPT}
{TRAINING_PROMPT}

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
1️⃣ Un feedback tecnico (prestazione, ritmo, andamento)
2️⃣ Un consiglio pratico e motivante per migliorare
3️⃣ Mantieni un tono realistico e positivo, come un coach empatico Mind&Body.
"""

    # ✅ Generazione del feedback tramite Gemini
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(analysis_prompt)
    print(f"[LOG] 💬 Feedback generato con prompt unificato per {username}")

    # 🔹 Messaggio finale
    info_parts = [
        f"🏋️ Allenamento registrato ✅ ({activity})",
        f"Durata: {duration} min | Distanza: {distance or '–'} km | BPM: {bpm or '–'} | Pendenza: {slope or '–'}%",
        f"Media precedente: {avg_duration:.1f} min → {trend_text}",
        "",
        response.text
    ]

    return "\n".join(info_parts)