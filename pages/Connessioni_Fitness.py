import streamlit as st
from agents.fitness_connector import strava, myfitnesspal, sync_manager
st.set_page_config(page_title="Connessioni Fitness", page_icon="🔗", layout="centered")
st.title("🔗 Connessioni Fitness")

username = st.session_state.get("username", None)
if not username:
    st.warning("Effettua il login prima di gestire le connessioni.")
    st.stop()

# --- Gestione callback Strava ---
params = st.experimental_get_query_params()
if "code" in params:
    code = params["code"][0]
    token_data = strava.exchange_strava_token(code)
    if "access_token" in token_data:
        strava.save_token(username, "strava", token_data)
        st.success("✅ Strava collegato con successo!")
        st.experimental_set_query_params()
        st.experimental_rerun()
    else:
        st.error("❌ Errore nel collegamento a Strava.")

st.subheader("🚴 Strava")
if strava.is_connected(username):
    st.success("✅ Connesso a Strava")
    if st.button("Disconnetti Strava"):
        strava.disconnect(username)
        st.experimental_rerun()
else:
    st.link_button("Connetti Strava", url=strava.connect_strava())

st.subheader("🍎 MyFitnessPal")
myfit_user = st.text_input("Username MyFitnessPal")
myfit_pass = st.text_input("Password MyFitnessPal", type="password")
if st.button("Connetti MyFitnessPal"):
    result = myfitnesspal.connect(myfit_user, myfit_pass)
    if "error" in result:
        st.error(result["error"])
    else:
        st.success("✅ Dati importati da MyFitnessPal!")