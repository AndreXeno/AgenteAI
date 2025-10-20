import os
import pandas as pd
import datetime


DATA_DIR="data"

def log_workout(activity: str, duration: int, intensity:str):
    """
       Salva un allenamento nel file log_fitness.csv
       """
    os.makedirs(DATA_DIR, exist_o=True)
    file_path=os.path.join(DATA_DIR,"log_fitness.csv")
    today=datetime.date.today().strftime("%d-%m-%Y")

    df= pd.DataFrame([[today,activity,duration,intensity]],
                     columns=["data","attività", "durata_minuti","intensità"])
    df.to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False)
def log_mind_state(mood:str,stress:int, note: str=""):
    """
      Salva lo stato mentale nel file log_mentale.csv
      """
    os.makedirs(DATA_DIR,exist_ok=True)
    file_path=os.path.join(DATA_DIR, "log_mentale.csv")
    today=datetime.date.today().strftime("%d-%m-%Y")

    df=pd.dataFrame([[today, mood, stress, note]],
                    columns=["data", "umore", "stress", "note"])
    df.to_csv(file_path, mode="a", header=not os.path.exists(file_path, index=False))
