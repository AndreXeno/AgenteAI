import os
import pandas as pd
import datetime


# Ottieni il percorso assoluto della directory base del progetto (agente_andrea)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def log_workout(activity: str, duration: int, intensity:str):
    """
       Salva un allenamento nel file log_fitness.csv
       """
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path=os.path.join(DATA_DIR,"log_fitness.csv")
    today=datetime.date.today().strftime("%d-%m-%Y")

    try:
        df= pd.DataFrame([[today,activity,duration,intensity]],
                         columns=["data","attività", "durata_minuti","intensità"])
        df.to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False)
        print(f"[LOG] 🏋️ Allenamento salvato in {file_path}")
    except Exception as e:
        print(f"[ERROR] ❌ Errore durante il salvataggio dell'allenamento: {e}")

def log_mind_state(username: str, mood: str, emotions: list, note: str = ""):
    """
    Salva lo stato mentale nel file log_mentale.csv specifico dell'utente.
    """
    user_dir = os.path.join(DATA_DIR, "users", username)
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, "log_mentale.csv")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    emotions_str = ",".join(emotions) if emotions else ""

    try:
        df = pd.DataFrame([[timestamp, mood, emotions_str, note]],
                          columns=["timestamp", "mood", "emotions", "note"])
        # Append to CSV, write header only if file doesn't exist
        df.to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False)
        print(f"[LOG] 🧘 Stato mentale salvato per {username} in {file_path}")
        return True
    except Exception as e:
        print(f"[ERROR] ❌ Errore durante il salvataggio dello stato mentale: {e}")
        return False

def get_recent_logs(username: str, limit: int = 7):
    """
    Recupera gli ultimi log mentali dell'utente.
    """
    file_path = os.path.join(DATA_DIR, "users", username, "log_mentale.csv")
    if not os.path.exists(file_path):
        return []
    
    try:
        df = pd.read_csv(file_path)
        # Sort by timestamp descending
        df = df.sort_values(by="timestamp", ascending=False)
        return df.head(limit).to_dict(orient="records")
    except Exception as e:
        print(f"[ERROR] ❌ Errore durante la lettura dei log mentali: {e}")
        return []
