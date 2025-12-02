import json
from . import strava, myfitnesspal
from .base_utils import save_token

def auto_sync_user_data(username, provider, token_data):
    """
    🔄 Sincronizza automaticamente i dati utente in base al provider.
    Recupera e salva nel CSV le informazioni dell’utente e le attività.
    Include gestione token Strava con refresh automatico.
    """
    try:
        if provider == "strava":
            from .strava import get_valid_access_token

            print(f"[SYNC] 🚴 Avvio sincronizzazione Strava per {username}")

            # Verifica validità token
            access_token = get_valid_access_token(username, token_data)
            if not access_token:
                print(f"[SYNC] ❌ Nessun token Strava valido disponibile per {username}")
                return {"error": "Token Strava non valido o scaduto"}

            # Aggiorna token_data se rinnovato
            token_data["access_token"] = access_token
            save_token(username, "strava", token_data)

            # Avvia la sincronizzazione
            result = strava.auto_sync(username, token_data)
            if result and "error" not in result:
                print(f"[SYNC] ✅ Sincronizzazione Strava completata ({username})")
            else:
                print(f"[SYNC] ⚠️ Errore sincronizzazione Strava: {result}")
            return result

        elif provider == "myfitnesspal":
            print(f"[SYNC] 🍎 Avvio sincronizzazione MyFitnessPal per {username}")

            username_mfp = token_data.get("username")
            password_mfp = token_data.get("password")
            if not username_mfp or not password_mfp:
                print("[SYNC] ❌ Credenziali MyFitnessPal mancanti durante auto_sync_user_data.")
                return {"error": "Credenziali MyFitnessPal mancanti."}

            save_token(username, "myfitnesspal", token_data)

            result = myfitnesspal.auto_sync(username, token_data)
            if result and "error" not in result:
                print(f"[SYNC] ✅ Sincronizzazione MyFitnessPal completata per {username}")
                return result
            else:
                print(f"[SYNC] ⚠️ Errore MyFitnessPal: {result}")
                return result

        else:
            print(f"[SYNC] ❌ Provider non supportato: {provider}")
            return {"error": f"Provider '{provider}' non supportato."}

    except Exception as e:
        print(f"[SYNC] ⚠️ Errore generale durante auto_sync_user_data: {e}")
        return {"error": str(e)}


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
            print("[SYNC] ⚠️ MyFitnessPal usa credenziali dirette, non OAuth.")
            return {"status": "manual"}

        else:
            print(f"[SYNC] ❌ Provider non riconosciuto: {provider}")
            return {"status": "unknown", "message": f"Provider '{provider}' non supportato."}

    except Exception as e:
        print(f"[SYNC] ⚠️ Errore durante la gestione del callback OAuth: {e}")
        return {"status": "error", "message": str(e)}