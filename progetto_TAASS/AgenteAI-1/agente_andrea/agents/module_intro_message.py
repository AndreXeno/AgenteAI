import os
import json

def generate_intro_message(memory, username="utente"):
    """
    Genera un messaggio introduttivo dinamico e naturale utilizzando Gemini:
    - Legge il diario e i messaggi recenti dell’utente
    - Crea un prompt per Gemini con queste informazioni
    - Genera un messaggio empatico, coerente con l’umore e le attività menzionate
    - Gestisce errori con un messaggio di fallback naturale
    """
    diary_path = os.path.join("data", "users", username, "diario_utente.json")

    recent_entries = []
    if os.path.exists(diary_path):
        try:
            with open(diary_path, "r", encoding="utf-8") as f:
                diary_entries = json.load(f)
            recent_entries = diary_entries[-2:] if len(diary_entries) >= 2 else diary_entries
        except Exception as e:
            print(f"[WARN] Errore lettura diario per {username}: {e}")

    recent_memory_msgs = []
    if memory:
        recent_memory_msgs = [m["content"] for m in memory[-6:] if m["role"] == "utente"]

    # Prepara i dati per il prompt
    diary_text = " ".join(entry.get("contenuto", "") for entry in recent_entries).strip()
    memory_text = " ".join(recent_memory_msgs).strip()

    prompt_parts = [
        "Sei un assistente empatico che genera un messaggio introduttivo naturale e personalizzato per un utente.",
        "Usa le seguenti informazioni dal diario e dai messaggi recenti dell'utente per creare un messaggio coerente con il suo umore e le attività menzionate.",
        "",
        f"Diario: {diary_text if diary_text else 'Nessun contenuto disponibile.'}",
        f"Messaggi recenti: {memory_text if memory_text else 'Nessun messaggio recente disponibile.'}",
        "",
        "Genera un messaggio introduttivo empatico, fluido e senza frasi predefinite."
    ]
    prompt = "\n".join(prompt_parts)

    try:
        # Import Gemini client (assumed available)
        from gemini import GeminiClient
        client = GeminiClient()

        response = client.generate_text(prompt=prompt, max_tokens=200)
        message = response.text.strip()
        if not message:
            raise ValueError("Risposta vuota da Gemini")
        return message

    except Exception as e:
        print(f"[WARN] Errore generazione messaggio con Gemini: {e}")
        # Fallback naturale
        fallback = (
            "Ciao! Non ho molte informazioni al momento, ma sono qui per ascoltarti e supportarti. "
            "Raccontami pure come ti senti o cosa hai fatto di recente."
        )
        return fallback.strip()