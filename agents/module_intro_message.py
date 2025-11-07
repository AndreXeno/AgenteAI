import os
import json

def generate_intro_message(memory, username="utente"):
    """
    Genera un messaggio introduttivo dinamico basato sul diario utente (ultimi 2 giorni)
    o, in mancanza, sull'ultima memoria conversazionale.
    """
    # Path del diario
    diary_path = os.path.join("data", "users", username, "diario_utente.json")

    # Liste base di parole chiave
    positive_words = ["bene", "felice", "motivato", "contento", "entusiasta", "ottimo", "positivo", "rilassato", "grato", "soddisfatto"]
    negative_words = ["male", "triste", "stanco", "stressato", "agitato", "demotivato", "ansia", "solitudine", "deluso", "preoccupato"]

    mood = "neutro"

    # 🔹 1. Se esiste il diario → leggi ultimi 2 giorni
    if os.path.exists(diary_path):
        try:
            with open(diary_path, "r", encoding="utf-8") as f:
                diary_entries = json.load(f)

            # Prendiamo le ultime due voci
            recent_entries = diary_entries[-2:] if len(diary_entries) >= 2 else diary_entries
            combined_text = " ".join(entry.get("contenuto", "") for entry in recent_entries)

            pos_count = sum(w in combined_text.lower() for w in positive_words)
            neg_count = sum(w in combined_text.lower() for w in negative_words)

            if pos_count > neg_count:
                mood = "positivo"
            elif neg_count > pos_count:
                mood = "negativo"

        except Exception as e:
            print(f"[WARN] Errore lettura diario per {username}: {e}")

    # 🔸 2. Fallback — usa la memoria conversazionale
    if mood == "neutro" and memory:
        recent_msgs = [m["content"] for m in memory[-6:] if m["role"] == "utente"]
        combined_text = " ".join(recent_msgs)
        pos_count = sum(w in combined_text.lower() for w in positive_words)
        neg_count = sum(w in combined_text.lower() for w in negative_words)
        if pos_count > neg_count:
            mood = "positivo"
        elif neg_count > pos_count:
            mood = "negativo"

    # 🔹 3. Genera messaggio coerente
    if mood == "positivo":
        return "🌞 Ieri avevi un’ottima energia! Ti senti ancora così motivato oggi?"
    elif mood == "negativo":
        return "🌧️ Ieri sembravi un po’ giù… Oggi vogliamo ripartire con calma e fiducia?"
    else:
        return "👋 Bentornato! Come ti senti oggi? Possiamo fissare insieme un piccolo obiettivo per la giornata?"