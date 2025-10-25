import streamlit as st
import json
from agents.fitness_connector import strava, myfitnesspal
from agents.session_manager import load_session, save_session
from agents.fitness_connector.sync_manager import auto_sync_user_data

# ==============================
# ⚙️ CONFIGURAZIONE BASE
# ==============================
st.set_page_config(page_title="Connessioni Fitness", page_icon="🔗", layout="centered")
st.title("🔗 Connessioni Fitness")

# ==============================
# 🔐 GESTIONE SESSIONE UTENTE
# ==============================
if "username" not in st.session_state:
    st.session_state["username"] = None
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

saved_user = load_session()
if saved_user and not st.session_state["username"]:
    st.session_state["username"] = saved_user
    st.session_state["logged_in"] = True
    print(f"[SESSION RESTORE] Ripristinato utente: {saved_user}")

qp = st.query_params

if not st.session_state["username"]:
    if "user" in qp and qp["user"]:
        st.session_state["username"] = qp["user"]
        st.session_state["logged_in"] = True
        save_session(st.session_state["username"])
        print(f"[SESSION RESTORE] Username ripristinato da URL (user): {st.session_state['username']}")
    elif "state" in qp and qp["state"]:
        st.session_state["username"] = qp["state"]
        st.session_state["logged_in"] = True
        save_session(st.session_state["username"])
        print(f"[SESSION RESTORE] Username ripristinato da URL (state): {st.session_state['username']}")

username = st.session_state.get("username", None)
if not username:
    st.warning("Effettua il login prima di gestire le connessioni.")
    st.stop()
# ==============================
# 🔁 CALLBACK STRAVA
# ==============================
if "code" in qp and qp["code"]:
    code = qp["code"]
    st.info("⏳ Autorizzazione Strava in corso...")
    token_data = strava.exchange_strava_token(code)

    if token_data and "access_token" in token_data:
        # Salva token e sincronizza subito i dati
        strava.save_token(username, "strava", token_data)
        auto_sync_user_data(username, "strava", token_data)
        st.success("✅ Strava collegato! Dati sincronizzati.")

        # Pulisci i parametri di query e ricarica la pagina
        st.query_params.clear()
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
    connect_url = strava.connect_strava(username)
    st.link_button("🔗 Collega Strava", url=connect_url)
st.divider()

# ==============================
# 🍎 SEZIONE MYFITNESSPAL
# ==============================
st.subheader("🍎 Connessione a MyFitnessPal")

if myfitnesspal.is_myfitnesspal_connected(username):
    st.success("✅ MyFitnessPal connesso")
    if st.button("Disconnetti MyFitnessPal"):
        result = myfitnesspal.disconnect_myfitnesspal(username)
        if result:
            st.success("🔌 Disconnesso con successo da MyFitnessPal")
        else:
            st.warning("⚠️ Nessuna connessione trovata da disconnettere.")
        st.rerun()
else:
    st.info("⚙️ MyFitnessPal non ancora connesso")

    # Prova a caricare token salvato per mantenere la connessione tra le sessioni
    saved_creds = myfitnesspal.load_token(username, "myfitnesspal")
    if saved_creds:
        myfit_user = saved_creds.get("username", "")
        myfit_pass = saved_creds.get("password", "")
    else:
        myfit_user = ""
        myfit_pass = ""

    with st.expander("Connetti a MyFitnessPal"):
        myfit_user = st.text_input("Username MyFitnessPal", value=myfit_user)
        myfit_pass = st.text_input("Password MyFitnessPal", type="password", value=myfit_pass)

        if st.button("Conferma Connessione MyFitnessPal"):
            creds = {"username": myfit_user, "password": myfit_pass}
            result = myfitnesspal.auto_sync(username, creds)
            if "error" not in result:
                myfitnesspal.save_token(username, "myfitnesspal", creds)
                st.success("✅ Connessione completata e dati importati da MyFitnessPal!")
                st.rerun()
            else:
                st.warning(f"⚠️ Errore durante la sincronizzazione: {result['error']}")