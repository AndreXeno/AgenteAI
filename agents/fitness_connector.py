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