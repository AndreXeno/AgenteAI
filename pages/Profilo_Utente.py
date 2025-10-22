import streamlit as st
import os, json, pandas as pd
from datetime import datetime
from agents.fitness_connector.strava import connect_strava, is_strava_connected, disconnect_strava
from agents.fitness_connector.myfitnesspal import is_myfitnesspal_connected, disconnect_myfitnesspal
from agents.fitness_connector.sync_manager import auto_sync_user_data

st.set_page_config(page_title="Profilo Utente", page_icon="👤", layout="centered")
st.title("👤 Profilo Utente")

# ==========================
# 🔐 Verifica login utente
# ==========================
if "username" not in st.session_state or not st.session_state["username"]:
    st.warning("Effettua il login per accedere al profilo utente.")
    st.stop()

username = st.session_state["username"]
USER_DIR = f"data/users/{username}"
PROFILE_PATH = f"{USER_DIR}/profilo_utente.csv"
os.makedirs(USER_DIR, exist_ok=True)

# ==========================
# 📄 Caricamento ultimo profilo
# ==========================
if os.path.exists(PROFILE_PATH):
    df = pd.read_csv(PROFILE_PATH)
    latest = df.iloc[-1].to_dict() if not df.empty else {}
else:
    df = pd.DataFrame()
    latest = {}

st.subheader("📋 Dati fisici e personali")
peso = st.number_input("Peso (kg)", min_value=30.0, value=float(latest.get("peso", 70)))
altezza = st.number_input("Altezza (cm)", min_value=100.0, value=float(latest.get("altezza", 170)))
eta = st.number_input("Età", min_value=10, value=int(latest.get("eta", 25)))
sesso = st.selectbox("Sesso", ["M", "F", "Altro"], index=["M", "F", "Altro"].index(latest.get("sesso", "M")))
obiettivi = st.text_input("Obiettivi di allenamento", latest.get("obiettivi", ""))

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