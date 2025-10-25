import os
import json
import pandas as pd
from pandas.errors import EmptyDataError

DATA_DIR = "data/users"


# ======================
# 📁 Gestione directory
# ======================
def ensure_user_dir(username: str):
    """Crea la directory utente se non esiste"""
    path = os.path.join(DATA_DIR, username)
    os.makedirs(path, exist_ok=True)
    return path


# ======================
# 🔐 Gestione token OAuth
# ======================
def save_token(username: str, provider: str, token_data: dict):
    """Salva o aggiorna i token nel file tokens.json"""
    user_dir = ensure_user_dir(username)
    token_path = os.path.join(user_dir, "tokens.json")
    tokens = {}
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            tokens = json.load(f)
    tokens[provider] = token_data
    with open(token_path, "w") as f:
        json.dump(tokens, f, indent=2)
    print(f"[LOG] 🔒 Token aggiornato per {username} ({provider})")


# ======================
# 💾 Gestione dati CSV
# ======================
def append_fitness_data(username: str, provider: str, data_list: list):
    """Aggiunge o aggiorna i dati fitness nel CSV utente"""
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
    # Allinea le colonne
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


# ======================
# 🔄 Sincronizzazione automatica
# ======================
def auto_sync_user_data(username: str, provider: str, token_data: dict):
    """
    Sincronizza automaticamente i dati utente da Strava o MyFitnessPal.
    Chiama le funzioni auto_sync dei moduli dedicati.
    """
    try:
        if provider == "strava":
            from agents.fitness_connector import strava
            print(f"[SYNC] 🚴 Avvio sincronizzazione Strava per {username}")
            return strava.auto_sync(username, token_data)

        elif provider == "myfitnesspal":
            from agents.fitness_connector import myfitnesspal
            print(f"[SYNC] 🍎 Avvio sincronizzazione MyFitnessPal per {username}")
            return myfitnesspal.auto_sync(username, token_data)

        else:
            print(f"[LOG] ⚠️ Provider non supportato: {provider}")
            return {"error": "Provider non supportato"}

    except Exception as e:
        print(f"[LOG] ❌ Errore in auto_sync_user_data per {username}: {e}")
        return {"error": str(e)}


def load_token(username: str, provider: str):
    """
    Carica il token salvato per un provider (Strava, MyFitnessPal, ecc.).
    Restituisce un dizionario con i dati del token oppure {} se non trovato.
    """
    import os, json

    user_dir = ensure_user_dir(username)
    token_path = os.path.join(user_dir, "tokens.json")

    if not os.path.exists(token_path):
        print(f"[TOKEN] Nessun token trovato per {username}")
        return {}

    try:
        with open(token_path, "r") as f:
            tokens = json.load(f)
        return tokens.get(provider, {})
    except Exception as e:
        print(f"[TOKEN] Errore durante il caricamento token per {username}: {e}")
        return {}