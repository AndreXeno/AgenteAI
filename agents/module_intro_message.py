import os
import json

def generate_intro_message(memory, username="utente"):
    """
    Genera un messaggio introduttivo dinamico:
    - Legge l'umore dell'utente negli ultimi 2 giorni per definire il tono
    - Legge le attività svolte e formula una domanda personalizzata
    """
    diary_path = os.path.join("data", "users", username, "diario_utente.json")

    positive_words = ["bene", "felice", "motivato", "contento", "entusiasta", "ottimo", "positivo", "rilassato", "grato", "soddisfatto"]
    negative_words = ["male", "triste", "stanco", "stressato", "agitato", "demotivato", "ansia", "solitudine", "deluso", "preoccupato"]
    activity_keywords = ["palestra", "allenamento", "uscita", "amici", "compito", "studio", "lezione", "scuola", "gara", "viaggio", "cinema", "lavoro"]

    mood = "neutro"
    recent_entries = []

    # 🔹 Leggi ultimi 2 giorni di diario
    if os.path.exists(diary_path):
        try:
            with open(diary_path, "r", encoding="utf-8") as f:
                diary_entries = json.load(f)

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

    # 🔸 Se non c'è diario, analizza la memoria
    if mood == "neutro" and memory:
        recent_msgs = [m["content"] for m in memory[-6:] if m["role"] == "utente"]
        combined_text = " ".join(recent_msgs)
        pos_count = sum(w in combined_text.lower() for w in positive_words)
        neg_count = sum(w in combined_text.lower() for w in negative_words)
        if pos_count > neg_count:
            mood = "positivo"
        elif neg_count > pos_count:
            mood = "negativo"

    # 🔹 Estrai attività menzionata
    chosen_activity = None
    if recent_entries:
        all_text = " ".join(entry.get("contenuto", "").lower() for entry in recent_entries)
        for act in activity_keywords:
            if act in all_text:
                chosen_activity = act
                break

    # 🔸 Genera messaggio personalizzato
    if mood == "positivo":
        if chosen_activity:
            return f"🌞 Hai scritto di {chosen_activity} e sembravi di ottimo umore! Mi racconti com'è andata?"
        else:
            return "🌞 Hai avuto giornate molto positive ultimamente! C’è qualcosa di particolare che ti ha reso felice?"
    elif mood == "negativo":
        if chosen_activity:
            return f"🌧️ Hai accennato a {chosen_activity}, ma sembravi un po’ giù. È andata meglio da allora?"
        else:
            return "🌧️ Ultimamente sembri un po’ stressato. Hai avuto modo di riposarti o fare qualcosa per stare meglio?"
    else:
        if chosen_activity:
            return f"👋 Bentornato! Vedo che hai parlato di {chosen_activity}. Com’è andata quell’esperienza?"
        else:
            return "👋 Bentornato! Cosa hai fatto negli ultimi giorni? Mi piacerebbe sapere com’è andata."