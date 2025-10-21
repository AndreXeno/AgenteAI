import os, json

DATA_DIR = "data/users"

def is_strava_connected(username: str):
    """Controlla se l'utente ha già collegato Strava"""
    user_dir = os.path.join(DATA_DIR, username)
    token_path = os.path.join(user_dir, "tokens.json")
    if not os.path.exists(token_path):
        return False
    with open(token_path, "r") as f:
        tokens = json.load(f)
    return "strava" in tokens and "access_token" in tokens["strava"]

def disconnect_strava(username: str):
    """Disconnette l'account Strava rimuovendo il token"""
    user_dir = os.path.join(DATA_DIR, username)
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

import streamlit as st
import requests

STRAVA_CLIENT_ID = st.secrets["STRAVA_CLIENT_ID"]
STRAVA_CLIENT_SECRET = st.secrets["STRAVA_CLIENT_SECRET"]
STRAVA_REDIRECT_URI = st.secrets["STRAVA_REDIRECT_URI"]

STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"

def connect_strava(username: str = None):
    """Genera il link per connettere l’account Strava"""
    return (
        f"{STRAVA_AUTH_URL}?client_id={STRAVA_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={STRAVA_REDIRECT_URI}"
        f"&approval_prompt=auto"
        f"&scope=activity:read_all"
    )

def exchange_strava_token(code):
    """Scambia il codice di autorizzazione per ottenere il token Strava"""
    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(STRAVA_TOKEN_URL, data=payload)
    return response.json()

def get_strava_activities(access_token, per_page=10):
    """Recupera le attività Strava dell'utente autenticato"""
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(f"{STRAVA_API_BASE}/athlete/activities", headers=headers, params={"per_page": per_page})
    return res.json()