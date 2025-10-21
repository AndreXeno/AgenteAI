import json
from . import strava, myfitnesspal
from .base_utils import save_token, auto_sync_user_data

def auto_sync_user_data(username, provider, token_data):
    """
    Sincronizza automaticamente i dati utente in base al provider.
    """
    if provider == "strava":
        return strava.auto_sync(username, token_data)
    elif provider == "myfitnesspal":
        return myfitnesspal.connect(token_data["username"], token_data["password"])
    else:
        return {"error": "Provider non supportato"}

def handle_oauth_callback(username: str, provider: str, code: str):
    """
    Gestisce il callback OAuth dopo l'autorizzazione dell'utente.
    Scambia il codice per un token e sincronizza i dati utente.
    """
    try:
        if provider == "strava":
            from .strava import exchange_strava_token
            token_data = exchange_strava_token(code)
            if "access_token" in token_data:
                save_token(username, "strava", token_data)
                auto_sync_user_data(username, "strava", token_data)
                print(f"[SYNC] ✅ Strava connesso e sincronizzato per {username}")
                return {"status": "connected", "provider": "strava"}
            else:
                print(f"[SYNC] ❌ Errore token Strava: {json.dumps(token_data, indent=2)}")
                return {"status": "error", "message": "Token non ricevuto da Strava"}

        elif provider == "myfitnesspal":
            # MyFitnessPal non usa OAuth, ma credenziali dirette
            print("[SYNC] ⚠️ MyFitnessPal usa credenziali dirette, non OAuth.")
            return {"status": "manual"}

        else:
            print(f"[SYNC] ❌ Provider non riconosciuto: {provider}")
            return {"status": "unknown", "message": f"Provider '{provider}' non supportato."}

    except Exception as e:
        print(f"[SYNC] ⚠️ Errore durante la gestione del callback OAuth: {e}")
        return {"status": "error", "message": str(e)}