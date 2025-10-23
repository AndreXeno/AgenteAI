import streamlit as st
import json
from agents.fitness_connector import strava, myfitnesspal, sync_manager
from agents.session_manager import load_session, save_session

# ==============================
# ⚙️ CONFIGURAZIONE BASE
# ==============================
st.set_page_config(page_title="Connessioni Fitness", page_icon="🔗", layout="centered")
st.title("🔗 Connessioni Fitness")

# ==============================
# 🔐 GESTIONE SESSIONE UTENTE
# ==============================
# Assicura che la chiave esista sempre
if "username" not in st.session_state:
    st.session_state["username"] = None
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Prova a ripristinare la sessione da file
saved_user = load_session()
if saved_user and not st.session_state["username"]:
    st.session_state["username"] = saved_user
    st.session_state["logged_in"] = True
    print(f"[SESSION RESTORE] Ripristinato utente: {saved_user}")

# ==============================
# 🔁 CALLBACK STRAVA (dopo autorizzazione)
# ==============================
params = st.experimental_get_query_params()

# Se la sessione è vuota ma arriva un parametro 'user' o 'state', ricreala
if not st.session_state["username"]:
    if "user" in params:
        st.session_state["username"] = params["user"][0]
        st.session_state["logged_in"] = True
        save_session(st.session_state["username"])
        print(f"[SESSION RESTORE] Username ripristinato da URL (user): {st.session_state['username']}")
    elif "state" in params:
        st.session_state["username"] = params["state"][0]
        st.session_state["logged_in"] = True
        save_session(st.session_state["username"])
        print(f"[SESSION RESTORE] Username ripristinato da URL (state): {st.session_state['username']}")

username = st.session_state.get("username", None)
if not username:
    st.warning("Effettua il login prima di gestire le connessioni.")
    st.stop()

# Dopo il redirect da Strava, gestisci il token di accesso
if "code" in params:
    code = params["code"][0]
    st.info("⏳ Autorizzazione Strava in corso...")
    token_data = strava.exchange_strava_token(code)
    if "access_token" in token_data:
        strava.save_token(username, "strava", token_data)
        st.success("✅ Strava collegato con successo!")
        # Sincronizzazione automatica immediata
        sync_manager.auto_sync_user_data(username, "strava", token_data)
        st.experimental_set_query_params()  # Rimuove il codice dalla URL
        st.rerun()
    else:
        st.error(f"❌ Errore nel collegamento a Strava: {token_data}")

# ==============================
# 🚴 SEZIONE STRAVA
# ==============================
st.subheader("🚴 Connessione a Strava")

if strava.is_strava_connected(username):
    st.success("✅ Strava attualmente connesso")
    if st.button("Disconnetti Strava"):
        strava.disconnect(username)
        st.experimental_rerun()
else:
    st.info("⚙️ Strava non ancora connesso")
    # Aggiungiamo il parametro “user” all’URL di redirect
    connect_url = strava.connect_strava(username)
    st.link_button("🔗 Collega Strava", url=f"{connect_url}&state={username}")

st.divider()

# ==============================
# 🍎 SEZIONE MYFITNESSPAL
# ==============================
st.subheader("🍎 Connessione a MyFitnessPal")

if myfitnesspal.is_connected(username):
    st.success("✅ MyFitnessPal connesso")
    if st.button("Disconnetti MyFitnessPal"):
        myfitnesspal.disconnect(username)
        st.experimental_rerun()
else:
    myfit_user = st.text_input("Username MyFitnessPal")
    myfit_pass = st.text_input("Password MyFitnessPal", type="password")
    if st.button("Connetti a MyFitnessPal"):
        creds = {"username": myfit_user, "password": myfit_pass}
        result = sync_manager.auto_sync_user_data(username, "myfitnesspal", creds)
        if "error" not in result:
            st.success("✅ Collegato e dati importati da MyFitnessPal!")
            st.experimental_rerun()
        else:
            st.error(f"❌ Errore: {result['error']}")