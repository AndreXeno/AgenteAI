import os, json

SESSION_FILE = "data/active_sessions.json"

def save_session(username: str):
    os.makedirs("data", exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("username")
    return None
# ======================================
# 🔐 MODULE: SESSION MANAGER — Gestione sessione utente attiva
# ======================================

import os
import json

SESSION_FILE = "data/active_sessions.json"


def save_session(username: str):
    """Salva la sessione utente corrente in modo persistente."""
    os.makedirs("data", exist_ok=True)
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump({"username": username}, f, ensure_ascii=False, indent=2)
        print(f"[LOG] 💾 Sessione salvata per utente: {username}")
    except Exception as e:
        print(f"[ERROR] ❌ Errore durante il salvataggio della sessione: {e}")


def load_session() -> str:
    """Carica la sessione utente se esiste, altrimenti restituisce None."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                username = data.get("username")
                print(f"[LOG] 🔄 Sessione caricata: {username}")
                return username
        except Exception as e:
            print(f"[WARN] ⚠️ Errore nel caricamento della sessione: {e}")
            return None
    else:
        print("[LOG] ℹ️ Nessuna sessione attiva trovata.")
        return None


def clear_session():
    """Cancella la sessione attiva (logout)."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print("[LOG] 🚪 Sessione terminata e file rimosso.")
    else:
        print("[LOG] ℹ️ Nessuna sessione da cancellare.")