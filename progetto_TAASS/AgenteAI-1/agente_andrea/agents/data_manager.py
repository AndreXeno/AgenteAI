import os
import pandas as pd
import datetime


DATA_DIR="data"

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

def log_mind_state(mood:str,stress:int, note: str=""):
    """
      Salva lo stato mentale nel file log_mentale.csv
      """
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path=os.path.join(DATA_DIR, "log_mentale.csv")
    today=datetime.date.today().strftime("%d-%m-%Y")

    try:
        df = pd.DataFrame([[today, mood, stress, note]],
                          columns=["data", "umore", "stress", "note"])
        df.to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False)
        print(f"[LOG] 🧘 Stato mentale salvato in {file_path}")
    except Exception as e:
        print(f"[ERROR] ❌ Errore durante il salvataggio dello stato mentale: {e}")
