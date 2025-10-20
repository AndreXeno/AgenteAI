

import os
import json
import requests

# ======================================
# 🌐 FITNESS CONNECTOR
# Supporto per Strava, Google Fit e Fitbit
# ======================================

DATA_DIR = "data/users"

def ensure_user_dir(username: str):
    user_dir = os.path.join(DATA_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def save_token(username: str, provider: str, token_data: dict):
    user_dir = ensure_user_dir(username)
    token_path = os.path.join(user_dir, "tokens.json")
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            tokens = json.load(f)
    else:
        tokens = {}
    tokens[provider] = token_data
    with open(token_path, "w") as f:
        json.dump(tokens, f, indent=2)

# =========================
# 🔗 STRAVA
# =========================
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"

def connect_strava(client_id, redirect_uri):
    return f"{STRAVA_AUTH_URL}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=auto&scope=activity:read_all"

def exchange_strava_token(client_id, client_secret, code):
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code"
    }
    return requests.post(STRAVA_TOKEN_URL, data=payload).json()

def get_strava_activities(access_token, per_page=10):
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(f"{STRAVA_API_BASE}/athlete/activities", headers=headers, params={"per_page": per_page})
    return res.json()

# =========================
# 🔗 GOOGLE FIT
# =========================
GOOGLE_FIT_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_FIT_TOKEN_URL = "https://oauth2.googleapis.com/token"

def connect_google_fit(client_id, redirect_uri):
    scope = "https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/fitness.body.read"
    return f"{GOOGLE_FIT_AUTH_URL}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

def exchange_google_fit_token(client_id, client_secret, code, redirect_uri):
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    return requests.post(GOOGLE_FIT_TOKEN_URL, data=payload).json()

# =========================
# 🔗 FITBIT
# =========================
FITBIT_AUTH_URL = "https://www.fitbit.com/oauth2/authorize"
FITBIT_TOKEN_URL = "https://api.fitbit.com/oauth2/token"
FITBIT_API_BASE = "https://api.fitbit.com/1/user/-"

def connect_fitbit(client_id, redirect_uri):
    scope = "activity heartrate nutrition sleep"
    return f"{FITBIT_AUTH_URL}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

def exchange_fitbit_token(client_id, client_secret, code, redirect_uri):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "client_id": client_id,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code": code
    }
    auth = (client_id, client_secret)
    return requests.post(FITBIT_TOKEN_URL, headers=headers, data=payload, auth=auth).json()

def get_fitbit_profile(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(f"{FITBIT_API_BASE}/profile.json", headers=headers)
    return res.json()

# =========================
# 🔗 MYFITNESSPAL
# =========================
# Libreria non ufficiale: pip install myfitnesspal
try:
    import myfitnesspal
except ImportError:
    myfitnesspal = None

def get_myfitnesspal_data(username, password):
    if not myfitnesspal:
        return {"error": "Libreria myfitnesspal non installata."}
    try:
        client = myfitnesspal.Client(username, password)
        today = client.get_date()
        return {
            "calories_consumed": today.totals.get("calories"),
            "protein": today.totals.get("protein"),
            "carbs": today.totals.get("carbohydrates"),
            "fat": today.totals.get("fat")
        }
    except Exception as e:
        return {"error": str(e)}

# =========================
# 🔗 MAPMYRUN
# =========================
MAPMYRUN_AUTH_URL = "https://www.mapmyfitness.com/v7.1/oauth2/authorize/"
MAPMYRUN_TOKEN_URL = "https://api.ua.com/v7.1/oauth2/uacf/access_token/"
MAPMYRUN_API_BASE = "https://api.ua.com/v7.1/workout/"

def connect_mapmyrun(client_id, redirect_uri):
    scope = "read"
    return f"{MAPMYRUN_AUTH_URL}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

def exchange_mapmyrun_token(client_id, client_secret, code, redirect_uri):
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }
    return requests.post(MAPMYRUN_TOKEN_URL, data=payload).json()

def get_mapmyrun_workouts(access_token, limit=10):
    headers = {"Authorization": f"Bearer {access_token}", "Api-Key": "your_mapmyrun_api_key"}
    res = requests.get(f"{MAPMYRUN_API_BASE}?limit={limit}", headers=headers)
    return res.json()

# =========================
# 📂 UNIVERSAL GPX IMPORT
# =========================
import xml.etree.ElementTree as ET
import pandas as pd

def import_gpx_file(username, gpx_path):
    """
    Legge un file GPX (es. esportato da Nike Run Club, Adidas Running, Decathlon, ecc.)
    e salva i dati in CSV dentro la cartella dell'utente.
    """
    user_dir = ensure_user_dir(username)
    csv_path = os.path.join(user_dir, "allenamenti_importati.csv")

    try:
        tree = ET.parse(gpx_path)
        root = tree.getroot()
        ns = {'default': 'http://www.topografix.com/GPX/1/1'}

        points = []
        for trkpt in root.findall(".//default:trkpt", ns):
            lat = trkpt.attrib.get('lat')
            lon = trkpt.attrib.get('lon')
            ele = trkpt.find('default:ele', ns)
            time = trkpt.find('default:time', ns)
            points.append({
                "lat": float(lat),
                "lon": float(lon),
                "elevazione": float(ele.text) if ele is not None else None,
                "tempo": time.text if time is not None else None
            })

        df = pd.DataFrame(points)
        df.to_csv(csv_path, mode="a", index=False, header=not os.path.exists(csv_path))
        return {"status": "ok", "rows": len(df), "file": csv_path}

    except Exception as e:
        return {"error": str(e)}

# =========================
# 🔁 Importazione unificata
# =========================
def import_from_provider(username, provider, token_data):
    if provider == "strava":
        return get_strava_activities(token_data["access_token"])
    elif provider == "fitbit":
        return get_fitbit_profile(token_data["access_token"])
    elif provider == "google_fit":
        return {"message": "Integrazione Google Fit base completata, endpoint avanzati da aggiungere."}
    elif provider == "mapmyrun":
        return get_mapmyrun_workouts(token_data["access_token"])
    elif provider == "myfitnesspal":
        return get_myfitnesspal_data(token_data.get("username"), token_data.get("password"))
    else:
        return {"error": "Provider non supportato."}

# =========================
# 💾 SALVATAGGIO DATI FLESSIBILE
# =========================
import pandas as pd

def append_fitness_data(username: str, provider: str, data_list: list):
    """
    Aggiunge dinamicamente nuovi dati fitness al CSV dell'utente.
    Se arrivano campi nuovi, aggiunge automaticamente nuove colonne.
    """
    user_dir = ensure_user_dir(username)
    csv_path = os.path.join(user_dir, "dati_fitness.csv")

    # Se il file esiste, leggilo. Altrimenti crea un DataFrame vuoto
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
    else:
        df_existing = pd.DataFrame()

    # Normalizza i dati nuovi in DataFrame
    df_new = pd.DataFrame(data_list)

    # Se serve, aggiungi colonne mancanti
    for col in df_new.columns:
        if col not in df_existing.columns:
            df_existing[col] = None

    # Stessa cosa al contrario (vecchie colonne nei nuovi dati)
    for col in df_existing.columns:
        if col not in df_new.columns:
            df_new[col] = None

    # Aggiungi colonna "provider" e "data_importazione"
    df_new["provider"] = provider
    df_new["data_importazione"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    # Combina tutto e salva
    df_final = pd.concat([df_existing, df_new], ignore_index=True)
    df_final.to_csv(csv_path, index=False)

    print(f"[LOG] ✅ Dati fitness aggiunti per {username}: {len(df_new)} righe da {provider}")
    return {"status": "ok", "rows_added": len(df_new), "file": csv_path}

# =========================
# ⚙️ IMPORTAZIONE + SALVATAGGIO AUTOMATICO
# =========================
def import_and_save(username, provider, token_data):
    """
    Importa i dati dal provider e li salva automaticamente nel CSV dell'utente.
    """
    data = import_from_provider(username, provider, token_data)
    if isinstance(data, dict):
        # singolo record
        data_list = [data]
    elif isinstance(data, list):
        data_list = data
    else:
        return {"error": "Formato dati non riconosciuto"}

    result = append_fitness_data(username, provider, data_list)
    return result