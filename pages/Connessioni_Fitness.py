import os
import json
import streamlit as st

# ================================
# ⚙️ GESTIONE TOKEN UTENTE
# ================================

def ensure_user_dir(username: str):
    """Assicura che la directory dell'utente esista"""
    if not username:
        st.error("⚠️ Nome utente non specificato. Effettua nuovamente il login.")
        raise ValueError("Username non valido o non presente in sessione.")
    user_dir = os.path.join("data", "users", username)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir


def save_token(username: str, provider: str, token_data: dict):
    """Salva un token per un determinato provider"""
    try:
        user_dir = ensure_user_dir(username)
        token_path = os.path.join(user_dir, "tokens.json")
        tokens = {}
        if os.path.exists(token_path):
            with open(token_path, "r") as f:
                tokens = json.load(f)
        tokens[provider] = token_data
        with open(token_path, "w") as f:
            json.dump(tokens, f, indent=2)
        print(f"[SAVE] ✅ Token salvato per {provider} (utente: {username})")
    except Exception as e:
        print(f"[ERROR] ❌ Impossibile salvare token per {provider}: {e}")
        st.error(f"Errore nel salvataggio token: {e}")


def load_token(username: str, provider: str):
    """Carica un token salvato per un determinato provider"""
    try:
        user_dir = ensure_user_dir(username)
        token_path = os.path.join(user_dir, "tokens.json")
        if not os.path.exists(token_path):
            return None
        with open(token_path, "r") as f:
            tokens = json.load(f)
        token = tokens.get(provider)
        if token:
            print(f"[LOAD] 🔑 Token caricato per {provider} (utente: {username})")
        return token
    except Exception as e:
        print(f"[ERROR] ❌ Impossibile caricare token per {provider}: {e}")
        return None