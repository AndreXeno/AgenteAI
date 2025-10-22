import streamlit as st
from agents.fitness_connector import strava, myfitnesspal, sync_manager

st.set_page_config(page_title="Connessioni Fitness", page_icon="🔗", layout="centered")
st.title("🔗 Connessioni Fitness")

# ✅ Recupera nome utente dalla sessione
username = st.session_state.get("username", None)
if not username:
    st.warning("Effettua il login prima di gestire le connessioni.")
    st.stop()

# --- Gestione callback Strava ---
params = st.query_params
if "code" in params:
    code = params["code"][0]
    token_data = strava.exchange_strava_token(code)
    if "access_token" in token_data:
        strava.save_token(username, "strava", token_data)
        st.success("✅ Strava collegato con successo!")
        sync_manager.auto_sync_user_data(username, "strava", token_data)
        st.query_params.clear()
        st.rerun()
    else:
        st.error("❌ Errore nel collegamento a Strava.")

# --- Sezione STRAVA ---
st.subheader("🚴 Strava")

if strava.is_strava_connected(username):
    st.success("✅ Connesso a Strava")
    if st.button("Disconnetti Strava"):
        strava.disconnect_strava(username)
        st.rerun()
else:
    st.link_button("Connetti Strava", url=strava.connect_strava())

# --- Sezione MYFITNESSPAL ---
st.subheader("🍎 MyFitnessPal")

if myfitnesspal.is_myfitnesspal_connected(username):
    st.success("✅ MyFitnessPal connesso")
    if st.button("Disconnetti MyFitnessPal"):
        myfitnesspal.disconnect_myfitnesspal(username)
        st.rerun()
else:
    myfit_user = st.text_input("Username MyFitnessPal")
    myfit_pass = st.text_input("Password MyFitnessPal", type="password")
    if st.button("Connetti MyFitnessPal"):
        creds = {"username": myfit_user, "password": myfit_pass}
        myfitnesspal.save_token(username, "myfitnesspal", creds)
        sync_manager.auto_sync_user_data(username, "myfitnesspal", creds)
        st.success("✅ MyFitnessPal collegato e sincronizzato con successo!")
        st.rerun()