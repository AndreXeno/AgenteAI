import streamlit as st
import os, json, pandas as pd
from datetime import datetime
from agents.fitness_connector.strava import connect_strava, is_strava_connected, disconnect_strava
from agents.fitness_connector.myfitnesspal import is_myfitnesspal_connected, disconnect_myfitnesspal
from agents.fitness_connector.sync_manager import auto_sync_user_data

from agents.session_manager import load_session, save_session

# ==============================
# 🔐 GESTIONE SESSIONE UTENTE
# ==============================
# Assicura che la chiave esista sempre
if "username" not in st.session_state:
    st.session_state["username"] = None

# Carica la sessione precedente se esiste, in modo sicuro
try:
    saved_user = load_session()
    if (
        saved_user
        and isinstance(saved_user, str)
        and saved_user.strip()
        and not st.session_state.get("username")
    ):
        st.session_state["username"] = saved_user.strip()
        print(f"[SESSION RESTORE] Ripristinato utente: {saved_user.strip()}")
    else:
        print(f"[SESSION RESTORE] Nessun utente valido da ripristinare (saved_user={repr(saved_user)})")
except Exception as e:
    print(f"[SESSION RESTORE] Errore durante il ripristino della sessione: {e}")
    if "username" not in st.session_state:
        st.session_state["username"] = None

# Salva la sessione solo se l'utente è loggato
if st.session_state.get("username"):
    save_session(st.session_state["username"])
    print(f"[SESSION SAVE] Sessione salvata per {st.session_state['username']}")
else:
    print("[SESSION] Nessun utente loggato al momento")
st.set_page_config(page_title="Profilo Utente", page_icon="👤", layout="centered")
st.title("👤 Profilo Utente")

# ==========================
# 🔐 Verifica login utente
# ==========================
if "username" not in st.session_state or not st.session_state["username"]:
    st.warning("Effettua il login per accedere al profilo utente.")
    st.stop()

username = st.session_state["username"]
USER_DIR = os.path.join("data", "users", username)
PROFILE_PATH = os.path.join(USER_DIR, "profilo_utente.csv")
os.makedirs(USER_DIR, exist_ok=True)

# ==========================
# 📄 Caricamento ultimo profilo
# ==========================
if os.path.exists(PROFILE_PATH):
    try:
        if os.path.getsize(PROFILE_PATH) == 0:
            st.warning("Il file del profilo utente è vuoto. Viene creato un nuovo profilo vuoto.")
            df = pd.DataFrame(columns=["username", "data", "peso", "altezza", "eta", "sesso", "obiettivi"])
            latest = {}
        else:
            df = pd.read_csv(PROFILE_PATH)
            latest = df.iloc[-1].to_dict() if not df.empty else {}
    except Exception as e:
        st.warning(f"Errore nel caricamento del profilo utente: {e}. Viene creato un nuovo profilo vuoto.")
        df = pd.DataFrame(columns=["username", "data", "peso", "altezza", "eta", "sesso", "obiettivi"])
        latest = {}
else:
    df = pd.DataFrame(columns=["username", "data", "peso", "altezza", "eta", "sesso", "obiettivi"])
    latest = {}

st.subheader("📋 Dati fisici e personali")
try:
    peso = st.number_input("Peso (kg)", min_value=30.0, value=float(latest.get("peso", 70)))
    altezza = st.number_input("Altezza (cm)", min_value=100.0, value=float(latest.get("altezza", 170)))
    eta = st.number_input("Età", min_value=10, value=int(latest.get("eta", 25)))
    sesso = st.selectbox("Sesso", ["M", "F", "Altro"], index=["M", "F", "Altro"].index(latest.get("sesso", "M")))
    obiettivi = st.text_input("Obiettivi di allenamento", latest.get("obiettivi", ""))
except (ValueError, TypeError):
    st.warning("⚠️ Alcuni dati salvati non sono validi. Controlla e correggi i campi evidenziati.")
    peso = st.number_input("Peso (kg)", min_value=30.0, value=70.0)
    altezza = st.number_input("Altezza (cm)", min_value=100.0, value=170.0)
    eta = st.number_input("Età", min_value=10, value=25)
    sesso = st.selectbox("Sesso", ["M", "F", "Altro"], index=0)
    obiettivi = st.text_input("Obiettivi di allenamento", "mantenimento")

# ==========================
# 💾 Salvataggio profilo
# ==========================
if st.button("💾 Salva Profilo"):
    row = {
        "username": username,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "peso": peso,
        "altezza": altezza,
        "eta": eta,
        "sesso": sesso,
        "obiettivi": obiettivi
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(PROFILE_PATH, index=False)
    st.success("✅ Profilo aggiornato con successo!")

    # ==========================
    # 🔄 Sincronizzazione automatica
    # ==========================
    token_path = os.path.join(USER_DIR, "tokens.json")
    if os.path.exists(token_path):
        try:
            with open(token_path, "r") as f:
                tokens = json.load(f)
            for provider, token_data in tokens.items():
                st.info(f"🔁 Sincronizzazione automatica con {provider.capitalize()} in corso...")
                result = auto_sync_user_data(username, provider, token_data)
                if isinstance(result, dict) and "error" not in result:
                    st.success(f"✅ Dati da {provider.capitalize()} sincronizzati automaticamente!")
                else:
                    st.warning(f"⚠️ Errore sincronizzando {provider.capitalize()}: {result.get('error', 'Errore sconosciuto')}")
        except Exception as e:
            st.error(f"Errore durante la sincronizzazione automatica: {e}")

# ==========================
# 🔗 Gestione connessioni fitness
# ==========================
st.divider()
st.subheader("🔗 Connessioni Fitness")

col1, col2 = st.columns(2)

# --- STRAVA ---
with col1:
    if is_strava_connected(username):
        st.success("✅ Strava connesso")
        if st.button("Disconnetti Strava"):
            disconnect_strava(username)
            st.rerun()
    else:
        st.info("⚙️ Strava non connesso")
        if st.button("Connetti Strava"):
            st.markdown(f"[🔗 Autorizza Strava]({connect_strava(username)})")

# --- MYFITNESSPAL ---
with col2:
    if is_myfitnesspal_connected(username):
        st.success("✅ MyFitnessPal connesso")
        if st.button("Disconnetti MyFitnessPal"):
            disconnect_myfitnesspal(username)
            st.rerun()
    else:
        st.info("⚙️ MyFitnessPal non connesso")
        with st.expander("Connetti a MyFitnessPal"):
            myfit_user = st.text_input("Username MyFitnessPal")
            myfit_pass = st.text_input("Password MyFitnessPal", type="password")
            if st.button("Conferma Connessione MyFitnessPal"):
                creds = {"username": myfit_user, "password": myfit_pass}
                result = auto_sync_user_data(username, "myfitnesspal", creds)
                if isinstance(result, dict) and "error" not in result:
                    st.success("✅ Connessione completata e dati importati!")
                    st.rerun()
                else:
                    st.error(f"❌ Errore: {result.get('error', 'Connessione fallita')}")

# ==========================
# 📄 Link alle altre sezioni
# ==========================
st.divider()
st.page_link("pages/Connessioni_Fitness.py", label="🔗 Gestisci Connessioni Fitness")
st.page_link("pages/Allenamenti_Manuali.py", label="🏋️ Gestisci Allenamenti")