import os
import json
import requests
import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError
import xml.etree.ElementTree as ET

# ======================================
# 🌐 FITNESS CONNECTOR
# Supporto per Strava, Google Fit, Fitbit, MapMyRun, MyFitnessPal, ecc.
# ======================================

DATA_DIR = "data/users"

def ensure_user_dir(username: str):
    user_dir = os.path.join(DATA_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

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
    auto_sync_user_data(username, provider, token_data)

# =========================
# 🔗 STRAVA
# =========================
STRAVA_CLIENT_ID = st.secrets["STRAVA_CLIENT_ID"]
STRAVA_CLIENT_SECRET = st.secrets["STRAVA_CLIENT_SECRET"]
STRAVA_REDIRECT_URI = st.secrets["STRAVA_REDIRECT_URI"]

STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"

def is_strava_connected(username: str):
    user_dir = ensure_user_dir(username)
    token_path = os.path.join(user_dir, "tokens.json")
    if not os.path.exists(token_path):
        return False
    with open(token_path, "r") as f:
        tokens = json.load(f)
    return "strava" in tokens and "access_token" in tokens["strava"]

def disconnect_strava(username: str):
    user_dir = ensure_user_dir(username)
    token_path = os.path.join(user_dir, "tokens.json")
    if not os.path.exists(token_path):
        return False
    with open(token_path, "r") as f:
        tokens = json.load(f)
    if "strava" in tokens:
        del tokens["strava"]
        with open(token_path, "w") as f:
            json.dump(tokens, f, indent=2)
        print(f"[LOG] 🔌 Strava disconnesso per {username}")
        return True
    return False

def connect_strava(username: str = None):
    if username and is_strava_connected(username):
        print(f"[LOG] ✅ Strava già connesso per {username}")
        return None
    return (
        f"{STRAVA_AUTH_URL}?client_id={STRAVA_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={STRAVA_REDIRECT_URI}"
        f"&approval_prompt=auto"
        f"&scope=activity:read_all"
    )

def exchange_strava_token(code):
    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
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

# =========================
# 🔗 MAPMYRUN / MYFITNESSPAL / ALTRI
# =========================
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

MAPMYRUN_AUTH_URL = "https://www.mapmyfitness.com/v7.1/oauth2/authorize/"
MAPMYRUN_TOKEN_URL = "https://api.ua.com/v7.1/oauth2/uacf/access_token/"
MAPMYRUN_API_BASE = "https://api.ua.com/v7.1/workout/"

def connect_mapmyrun(client_id, redirect_uri):
    return f"{MAPMYRUN_AUTH_URL}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=read"

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
# 📂 GPX IMPORT & UNIVERSAL DATA HANDLER
# =========================

def auto_sync_user_data(username, provider, token_data):
    user_dir = ensure_user_dir(username)
    profile_path = os.path.join(user_dir, "profilo_utente.csv")
    fitness_data_path = os.path.join(user_dir, "dati_fitness.csv")

    if provider == "strava":
        access_token = token_data.get("access_token")
        if not access_token:
            print("[LOG] ⚠️ Access token Strava mancante, impossibile sincronizzare.")
            return
        # Get athlete profile
        headers = {"Authorization": f"Bearer {access_token}"}
        res_profile = requests.get(f"{STRAVA_API_BASE}/athlete", headers=headers)
        if res_profile.status_code == 200:
            profile = res_profile.json()
            df_profile = pd.DataFrame([{
                "id": profile.get("id"),
                "username": username,
                "firstname": profile.get("firstname"),
                "lastname": profile.get("lastname"),
                "city": profile.get("city"),
                "state": profile.get("state"),
                "country": profile.get("country"),
                "sex": profile.get("sex"),
                "profile": profile.get("profile"),
                "created_at": profile.get("created_at"),
                "updated_at": profile.get("updated_at")
            }])
            if os.path.exists(profile_path):
                try:
                    df_existing = pd.read_csv(profile_path)
                except EmptyDataError:
                    df_existing = pd.DataFrame()
            else:
                df_existing = pd.DataFrame()
            df_existing = df_existing[df_existing["id"] != profile.get("id")]
            df_final = pd.concat([df_existing, df_profile], ignore_index=True)
            df_final.to_csv(profile_path, index=False)
            print(f"[LOG] ✅ Profilo Strava sincronizzato per {username}")
        else:
            print(f"[LOG] ⚠️ Errore nel recupero profilo Strava: {res_profile.status_code}")

        # Get activities
        activities = get_strava_activities(access_token, per_page=50)
        if isinstance(activities, list):
            data_list = []
            for act in activities:
                data_list.append({
                    "activity_id": act.get("id"),
                    "name": act.get("name"),
                    "distance": act.get("distance"),
                    "moving_time": act.get("moving_time"),
                    "elapsed_time": act.get("elapsed_time"),
                    "total_elevation_gain": act.get("total_elevation_gain"),
                    "type": act.get("type"),
                    "start_date": act.get("start_date"),
                    "average_speed": act.get("average_speed"),
                    "max_speed": act.get("max_speed"),
                    "calories": act.get("calories"),
                })
            append_fitness_data(username, provider, data_list)
        else:
            print(f"[LOG] ⚠️ Errore nel recupero attività Strava: {activities}")

    elif provider == "google_fit":
        # Google Fit sync requires more complex API calls; here we just log the event.
        print(f"[LOG] ℹ️ Sincronizzazione Google Fit non ancora implementata per {username}")

    elif provider == "fitbit":
        # Fitbit sync placeholder
        print(f"[LOG] ℹ️ Sincronizzazione Fitbit non ancora implementata per {username}")

    elif provider == "myfitnesspal":
        # For MyFitnessPal, token_data should contain username and password for simplicity
        mfp_username = token_data.get("username")
        mfp_password = token_data.get("password")
        if not mfp_username or not mfp_password:
            print("[LOG] ⚠️ Credenziali MyFitnessPal mancanti, impossibile sincronizzare.")
            return
        data = get_myfitnesspal_data(mfp_username, mfp_password)
        if "error" not in data:
            df_data = pd.DataFrame([data])
            append_fitness_data(username, provider, [data])
            print(f"[LOG] ✅ Dati MyFitnessPal sincronizzati per {username}")
        else:
            print(f"[LOG] ⚠️ Errore sincronizzazione MyFitnessPal: {data['error']}")

# =========================
# 💾 SAVE MERGE SYSTEM (AUTOCREATE COLUMNS)
# =========================
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
    print(f"[LOG] ✅ Dati fitness salvati per {username} ({len(df_new)} righe da {provider})")
    return {"status": "ok", "rows_added": len(df_new), "file": csv_path}