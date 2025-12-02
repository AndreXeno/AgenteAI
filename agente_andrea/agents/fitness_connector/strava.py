import os
import json
import requests
import pandas as pd
from pandas.errors import EmptyDataError
from .base_utils import ensure_user_dir, save_token
import streamlit as st

# === Configurazione OAuth Strava ===
STRAVA_CLIENT_ID = st.secrets["STRAVA_CLIENT_ID"]
STRAVA_CLIENT_SECRET = st.secrets["STRAVA_CLIENT_SECRET"]
STRAVA_REDIRECT_URI = st.secrets["STRAVA_REDIRECT_URI"]

STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"

DATA_DIR = "data/users"


# =====================================
# 🔗 CONNESSIONE E AUTORIZZAZIONE
# =====================================
def connect_strava(username=None):
    """
    Genera l'URL di autorizzazione Strava per collegare l'account dell'utente.
    Include un parametro di stato sicuro e log utile per il debug.
    """
    if not username:
        st.error("⚠️ Nessun utente in sessione. Effettua l’accesso prima di collegare Strava.")
        return None

    redirect_uri = f"{STRAVA_REDIRECT_URI}?user={username}"
    auth_url = (
        f"{STRAVA_AUTH_URL}?client_id={STRAVA_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&approval_prompt=auto"
        f"&scope=read,activity:read_all"
        f"&state={username}"
    )
    print(f"[STRAVA] 🔗 URL generato per {username}: {auth_url}")
    return auth_url


def refresh_strava_token(username: str, refresh_token: str):
    """Aggiorna il token Strava scaduto e lo salva su file."""
    try:
        payload = {
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        res = requests.post(STRAVA_TOKEN_URL, data=payload)
        data = res.json()

        if "access_token" in data:
            save_token(username, "strava", data)
            print(f"[STRAVA] ♻️ Token aggiornato correttamente per {username}")
            return data
        else:
            print(f"[STRAVA] ⚠️ Errore aggiornamento token: {data}")
            return None
    except Exception as e:
        print(f"[STRAVA] ❌ Errore refresh token per {username}: {e}")
        return None


def get_valid_access_token(username: str, token_data: dict):
    """
    Verifica la validità del token Strava e lo rinnova se scaduto.
    Restituisce un token valido o None.
    """
    import time
    access_token = token_data.get("access_token")
    expires_at = token_data.get("expires_at")
    refresh_token = token_data.get("refresh_token")

    if not access_token or not expires_at:
        print("[STRAVA] ❌ Nessun token access valido trovato.")
        return None

    # Se scaduto → refresh
    if time.time() > expires_at:
        print(f"[STRAVA] 🔄 Token scaduto per l’utente, rigenero...")
        new_data = refresh_strava_token(username, refresh_token)
        return new_data.get("access_token") if new_data else None

    return access_token


def exchange_strava_token(code):
    """Scambia il codice OAuth per un token d’accesso"""
    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    res = requests.post(STRAVA_TOKEN_URL, data=payload)
    return res.json()


def is_strava_connected(username: str):
    """Controlla se l'utente ha già collegato Strava"""
    user_dir = ensure_user_dir(username)
    token_path = os.path.join(user_dir, "tokens.json")
    if not os.path.exists(token_path):
        return False
    with open(token_path, "r") as f:
        tokens = json.load(f)
    return "strava" in tokens and "access_token" in tokens["strava"]


def disconnect_strava(username: str):
    """Disconnette Strava rimuovendo il token"""
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


# =====================================
# 📊 SCARICA DATI STRAVA
# =====================================
def get_strava_activities(access_token, per_page=50):
    """Recupera le ultime attività Strava"""
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(f"{STRAVA_API_BASE}/athlete/activities", headers=headers, params={"per_page": per_page})
    return res.json()


def get_strava_profile(access_token):
    """Recupera le info del profilo Strava"""
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(f"{STRAVA_API_BASE}/athlete", headers=headers)
    return res.json() if res.status_code == 200 else {"error": res.text}


# =====================================
# 💾 SALVATAGGIO AUTOMATICO
# =====================================
def auto_sync(username: str, token_data: dict):
    """
    Sincronizza automaticamente profilo e attività Strava nel CSV dell’utente.
    """
    try:
        access_token = get_valid_access_token(username, token_data)
        if not access_token:
            st.error("⚠️ Token Strava non valido o scaduto. Ricollega il tuo account Strava.")
            return {"error": "Token Strava non valido"}

        user_dir = ensure_user_dir(username)
        profile_path = os.path.join(user_dir, "profilo_utente.csv")
        fitness_path = os.path.join(user_dir, "dati_fitness.csv")

        # --- Profilo Strava ---
        profile = get_strava_profile(access_token)
        if "error" not in profile:
            df_profile = pd.DataFrame([{
                "username": username,
                "id_strava": profile.get("id"),
                "firstname": profile.get("firstname"),
                "lastname": profile.get("lastname"),
                "city": profile.get("city"),
                "country": profile.get("country"),
                "sex": profile.get("sex"),
                "weight": profile.get("weight"),
                "created_at": profile.get("created_at"),
                "updated_at": profile.get("updated_at")
            }])
            if os.path.exists(profile_path):
                try:
                    df_old = pd.read_csv(profile_path)
                except EmptyDataError:
                    df_old = pd.DataFrame()
            else:
                df_old = pd.DataFrame()
            df_final = pd.concat([df_old, df_profile], ignore_index=True)
            df_final.to_csv(profile_path, index=False)
            print(f"[SYNC] ✅ Profilo Strava salvato per {username}")

        # --- Attività Strava ---
        activities = get_strava_activities(access_token)
        if isinstance(activities, list) and activities:
            df_activities = pd.DataFrame([{
                "activity_id": a.get("id"),
                "name": a.get("name"),
                "distance": a.get("distance"),
                "type": a.get("type"),
                "start_date": a.get("start_date"),
                "elapsed_time": a.get("elapsed_time"),
                "average_speed": a.get("average_speed"),
                "total_elevation_gain": a.get("total_elevation_gain"),
                "calories": a.get("calories", None)
            } for a in activities])
            if os.path.exists(fitness_path):
                try:
                    df_old = pd.read_csv(fitness_path)
                except EmptyDataError:
                    df_old = pd.DataFrame()
            else:
                df_old = pd.DataFrame()
            df_final = pd.concat([df_old, df_activities], ignore_index=True)
            df_final.to_csv(fitness_path, index=False)
            print(f"[SYNC] ✅ {len(df_activities)} attività Strava salvate per {username}")
            return {"status": "ok", "rows": len(df_activities)}

        return {"status": "ok", "message": "Profilo sincronizzato"}

    except Exception as e:
        print(f"[SYNC] ❌ Errore sincronizzazione Strava: {e}")
        return {"error": str(e)}