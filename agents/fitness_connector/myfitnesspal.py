import os
import json
import pandas as pd
from pandas.errors import EmptyDataError
from .base_utils import ensure_user_dir, save_token

try:
    import myfitnesspal
except ImportError:
    myfitnesspal = None


def is_myfitnesspal_connected(username: str):
    """Controlla se l'utente ha collegato MyFitnessPal"""
    user_dir = ensure_user_dir(username)
    token_path = os.path.join(user_dir, "tokens.json")
    if not os.path.exists(token_path):
        return False
    with open(token_path, "r") as f:
        tokens = json.load(f)
    return "myfitnesspal" in tokens


def disconnect_myfitnesspal(username: str):
    """Disconnette MyFitnessPal rimuovendo le credenziali"""
    user_dir = ensure_user_dir(username)
    token_path = os.path.join(user_dir, "tokens.json")
    if not os.path.exists(token_path):
        return False
    with open(token_path, "r") as f:
        tokens = json.load(f)
    if "myfitnesspal" in tokens:
        del tokens["myfitnesspal"]
        with open(token_path, "w") as f:
            json.dump(tokens, f, indent=2)
        print(f"[LOG] 🔌 MyFitnessPal disconnesso per {username}")
        return True
    return False


def connect(username_mfp, password_mfp):
    """Connette MyFitnessPal e scarica i dati giornalieri"""
    if not myfitnesspal:
        return {"error": "Libreria myfitnesspal non installata."}
    try:
        client = myfitnesspal.Client(username_mfp, password_mfp)
        today = client.get_date()
        data = {
            "calories_consumed": today.totals.get("calories", 0),
            "protein": today.totals.get("protein", 0),
            "carbs": today.totals.get("carbohydrates", 0),
            "fat": today.totals.get("fat", 0)
        }
        return data
    except Exception as e:
        return {"error": str(e)}


def auto_sync(username: str, token_data: dict):
    """Sincronizza automaticamente i dati da MyFitnessPal"""
    try:
        user_dir = ensure_user_dir(username)
        csv_path = os.path.join(user_dir, "dati_fitness.csv")

        username_mfp = token_data.get("username")
        password_mfp = token_data.get("password")

        if not username_mfp or not password_mfp:
            return {"error": "Credenziali MyFitnessPal mancanti."}

        data = connect(username_mfp, password_mfp)
        if "error" in data:
            return data

        df_new = pd.DataFrame([data])
        if os.path.exists(csv_path):
            try:
                df_existing = pd.read_csv(csv_path)
            except EmptyDataError:
                df_existing = pd.DataFrame()
        else:
            df_existing = pd.DataFrame()

        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        df_final.to_csv(csv_path, index=False)

        save_token(username, "myfitnesspal", token_data)
        print(f"[SYNC] ✅ Dati MyFitnessPal sincronizzati per {username}")
        return {"status": "ok", "rows_added": 1}

    except Exception as e:
        print(f"[SYNC] ❌ Errore sincronizzazione MyFitnessPal: {e}")
        return {"error": str(e)}