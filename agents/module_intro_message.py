import datetime

def generate_intro_message(memory):
    """
    Genera un messaggio introduttivo dinamico ogni volta che l'app viene aperta.
    Analizza la memoria recente per dedurre l'umore dell'utente.
    """
    today = datetime.date.today()

    # Estrai ultimi messaggi utente
    recent_msgs = [m["content"] for m in memory[-6:] if m["role"] == "utente"]

    # Liste base di parole chiave
    positive_words = ["bene", "felice", "motivato", "contento", "entusiasta", "ottimo", "positivo", "rilassato", "grato", "soddisfatto"]
    negative_words = ["male", "triste", "stanco", "stressato", "agitato", "demotivato", "ansia", "solitudine", "deluso", "preoccupato"]

    pos_count = sum(any(w in m.lower() for w in positive_words) for m in recent_msgs)
    neg_count = sum(any(w in m.lower() for w in negative_words) for m in recent_msgs)

    if pos_count > neg_count:
        mood = "positivo"
    elif neg_count > pos_count:
        mood = "negativo"
    else:
        mood = "neutro"

    # Messaggio finale basato sull'umore
    if mood == "positivo":
        return f"🌞 Bentornato! Oggi ({today.strftime('%Y-%m-%d')}) sento un'ottima energia da parte tua! Continua così e affronta la giornata con il sorriso. Hai nuovi obiettivi o sfide da condividere?"
    elif mood == "negativo":
        return f"🌧️ Ciao! Oggi ({today.strftime('%Y-%m-%d')}) potresti aver bisogno di un po’ di motivazione. Ricorda che anche un piccolo passo è progresso. Vuoi raccontarmi come ti senti?"
    else:
        return f"👋 Bentornato! Oggi è il {today.strftime('%Y-%m-%d')}. Come ti senti? Possiamo fissare insieme un piccolo obiettivo per la giornata?"