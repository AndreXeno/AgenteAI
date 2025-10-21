import os, json, pandas as pd
from pandas.errors import EmptyDataError

DATA_DIR = "data/users"

def ensure_user_dir(username: str):
    path = os.path.join(DATA_DIR, username)
    os.makedirs(path, exist_ok=True)
    return path

def save_token(username: str, provider: str, token_data: dict):
    user_dir = ensure_user_dir(username)
    token_path = os.path.join(user_dir, "tokens.json")
    tokens = {}
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            tokens = json.load(f)
    tokens[provider] = token_data
    with open(token_path, "w") as f:
        json.dump(tokens, f, indent=2)

def append_fitness_data(username: str, provider: str, data_list: list):
    user_dir = ensure_user_dir(username)
    csv_path = os.path.join(user_dir, "dati_fitness.csv")
    if os.path.exists(csv_path):
        try:
            df_existing = pd.read_csv(csv_path)
        except EmptyDataError:
            df_existing = pd.DataFrame()
    else:
        df_existing = pd.DataFrame()
    df_new = pd.DataFrame(data_list)
    for col in df_new.columns:
        if col not in df_existing.columns:
            df_existing[col] = None
    for col in df_existing.columns:
        if col not in df_new.columns:
            df_new[col] = None
    df_new["provider"] = provider
    df_new["data_importazione"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    df_final = pd.concat([df_existing, df_new], ignore_index=True)
    df_final.to_csv(csv_path, index=False)
    print(f"[LOG] ✅ Dati fitness salvati per {username} ({len(df_new)} da {provider})")
    return {"rows_added": len(df_new), "file": csv_path}


# --- Nuova funzione per sincronizzazione automatica dei dati utente (Strava/MyFitnessPal) ---
def auto_sync_user_data(username: str, provider: str, token_data: dict):
    """
    Sincronizza automaticamente i dati dell'utente nel CSV.
    Supporta Strava e MyFitnessPal.
    """
    try:
        if provider == "strava":
            from agents.fitness_connector import get_strava_activities
            access_token = token_data.get("access_token")
            if not access_token:
                print(f"[LOG] ⚠️ Nessun token trovato per Strava di {username}")
                return {"error": "Token mancante"}
            activities = get_strava_activities(access_token, per_page=50)
            if isinstance(activities, list):
                append_fitness_data(username, "strava", activities)
                print(f"[LOG] ✅ Dati Strava sincronizzati per {username}")
                return {"status": "ok", "provider": "strava", "rows": len(activities)}
            else:
                print(f"[LOG] ⚠️ Errore nel recupero attività Strava per {username}")
                return {"error": "Errore nel recupero attività"}

        elif provider == "myfitnesspal":
            from agents.fitness_connector import get_myfitnesspal_data
            creds_user = token_data.get("username")
            creds_pass = token_data.get("password")
            if not creds_user or not creds_pass:
                print(f"[LOG] ⚠️ Credenziali MyFitnessPal mancanti per {username}")
                return {"error": "Credenziali mancanti"}
            data = get_myfitnesspal_data(creds_user, creds_pass)
            if "error" not in data:
                append_fitness_data(username, "myfitnesspal", [data])
                print(f"[LOG] ✅ Dati MyFitnessPal sincronizzati per {username}")
                return {"status": "ok", "provider": "myfitnesspal", "rows": 1}
            else:
                print(f"[LOG] ⚠️ Errore MyFitnessPal: {data['error']}")
                return {"error": data["error"]}

        else:
            print(f"[LOG] ⚠️ Provider non supportato: {provider}")
            return {"error": "Provider non supportato"}

    except Exception as e:
        print(f"[LOG] ❌ Errore in auto_sync_user_data per {username}: {e}")
        return {"error": str(e)}