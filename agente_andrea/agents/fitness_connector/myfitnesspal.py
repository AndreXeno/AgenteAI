import os
import json
import pandas as pd
from pandas.errors import EmptyDataError

# ✅ Import compatibili da qualsiasi contesto (anche Streamlit Cloud)
from agents.fitness_connector.base_utils import ensure_user_dir, save_token, load_token

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
            "fat": today.totals.get("fat", 0),
            "data_importazione": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
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
            print(f"[SYNC] ⚠️ Errore MyFitnessPal per {username}: {data['error']}")
            return {"error": f"Impossibile sincronizzare MyFitnessPal: {data['error']}"}

        if not os.path.exists(user_dir):
            os.makedirs(user_dir, exist_ok=True)

        if not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0:
            df_existing = pd.DataFrame(columns=data.keys())
        else:
            try:
                df_existing = pd.read_csv(csv_path)
            except EmptyDataError:
                df_existing = pd.DataFrame(columns=data.keys())

        df_new = pd.DataFrame([data])
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        df_final.to_csv(csv_path, index=False)

        save_token(username, "myfitnesspal", token_data)
        print(f"[SYNC] ✅ Dati MyFitnessPal salvati correttamente per {username}")
        return {"status": "ok", "rows_added": len(df_new)}

    except Exception as e:
        print(f"[SYNC] ❌ Errore sincronizzazione MyFitnessPal: {e}")
        return {"error": str(e)}


# Recupera le credenziali MyFitnessPal salvate per l'utente specificato
def get_saved_credentials(username: str):
    """
    Recupera le credenziali MyFitnessPal salvate (username e password)
    dal file tokens.json per l'utente specificato.
    """
    try:
        user_dir = ensure_user_dir(username)
        token_path = os.path.join(user_dir, "tokens.json")

        if not os.path.exists(token_path):
            print(f"[CRED] ⚠️ Nessun file token trovato per {username}")
            return None

        with open(token_path, "r") as f:
            tokens = json.load(f)

        creds = tokens.get("myfitnesspal")
        if creds and "username" in creds and "password" in creds:
            print(f"[CRED] 🔑 Credenziali MyFitnessPal recuperate per {username}")
            return creds
        else:
            print(f"[CRED] ⚠️ Nessuna credenziale valida trovata per {username}")
            return None

    except Exception as e:
        print(f"[CRED] ❌ Errore nel recupero delle credenziali MyFitnessPal: {e}")
        return None