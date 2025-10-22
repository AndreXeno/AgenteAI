import streamlit as st
import json
from agents.fitness_connector import strava, myfitnesspal, sync_manager

st.set_page_config(page_title="Connessioni Fitness", page_icon="🔗", layout="centered")
st.title("🔗 Connessioni Fitness")

username = st.session_state.get("username", None)
if not username:
    st.warning("Effettua il login prima di gestire le connessioni.")
    st.stop()

# --- CALLBACK STRAVA (dopo autorizzazione) ---
params = st.experimental_get_query_params()
if "code" in params:
    code = params["code"][0]
    st.info("⏳ Autorizzazione Strava in corso...")
    token_data = strava.exchange_strava_token(code)
    if "access_token" in token_data:
        strava.save_token(username, "strava", token_data)
        st.success("✅ Strava collegato con successo!")
        # Sincronizzazione automatica immediata
        sync_manager.auto_sync_user_data(username, "strava", token_data)
        st.experimental_set_query_params()
        st.rerun()
    else:
        st.error(f"❌ Errore nel collegamento a Strava: {token_data}")

# --- Sezione Strava ---
st.subheader("🚴 Connessione a Strava")

if strava.is_connected(username):
    st.success("✅ Strava attualmente connesso")
    if st.button("Disconnetti Strava"):
        strava.disconnect(username)
        st.experimental_rerun()
else:
    st.info("⚙️ Strava non ancora connesso")
    st.link_button("🔗 Collega Strava", url=strava.connect_strava(username))

st.divider()

# --- Sezione MyFitnessPal ---
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