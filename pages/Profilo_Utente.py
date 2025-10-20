import streamlit as st
from datetime import datetime
import os
import pandas as pd

st.set_page_config(page_title="Profilo Utente", page_icon="👤", layout="centered")

st.title("👤 Profilo Utente")
st.caption("Gestisci i tuoi dati personali, fisici e sportivi. Ogni modifica viene salvata e archiviata nel tempo per tracciare i tuoi progressi.")

st.subheader("🔑 Identità utente")
username = st.text_input("Inserisci il tuo nome utente (usalo sempre uguale)", key="username")
if not username:
    st.warning("Inserisci un nome utente per continuare.")
    st.stop()

# Percorso CSV personale per utente
BASE_DIR = "data/users"
USER_DIR = os.path.join(BASE_DIR, username)
os.makedirs(USER_DIR, exist_ok=True)
PROFILE_PATH = os.path.join(USER_DIR, "profilo_utente.csv")

# Carica ultimo profilo se esiste
if os.path.exists(PROFILE_PATH) and os.path.getsize(PROFILE_PATH) > 0:
    df = pd.read_csv(PROFILE_PATH)
    df_user = df[df["username"] == username]
    latest = df_user.iloc[-1].to_dict() if not df_user.empty else {}
else:
    df = pd.DataFrame({
        "username": [],
        "data": [],
        "peso": [],
        "altezza": [],
        "eta": [],
        "sesso": [],
        "infortuni": [],
        "obiettivi": [],
        "circonferenza_vita": [],
        "circonferenza_fianchi": [],
        "circonferenza_torace": [],
        "circonferenza_braccio": [],
        "circonferenza_coscia": [],
        "bmi": [],
        "livello_attivita": [],
        "percentuale_grasso": [],
        "circonferenza_collo": [],
        "circonferenza_polso": [],
        "bmr": [],
        "fabbisogno_kcal": []
    })
    latest = {}

# Campi profilo
peso = st.number_input("Peso (kg)", min_value=30.0, step=0.1, value=float(latest.get("peso", 70)))
altezza = st.number_input("Altezza (cm)", min_value=100.0, step=0.1, value=float(latest.get("altezza", 170)))
eta = st.number_input("Età", min_value=10, max_value=100, step=1, value=int(latest.get("eta", 25)))
sesso = st.selectbox("Sesso", ["M", "F", "Altro"], index=0 if latest.get("sesso", "M") == "M" else 1)
infortuni = st.text_area("Infortuni o limitazioni fisiche", value=latest.get("infortuni", ""))
obiettivi = st.text_input("Obiettivi di allenamento", value=latest.get("obiettivi", "mantenimento"))

circonferenza_vita = st.number_input("Circonferenza Vita (cm)", min_value=40.0, max_value=200.0, step=0.1, value=float(latest.get("circonferenza_vita", 80)))
circonferenza_fianchi = st.number_input("Circonferenza Fianchi (cm)", min_value=40.0, max_value=200.0, step=0.1, value=float(latest.get("circonferenza_fianchi", 90)))
circonferenza_torace = st.number_input("Circonferenza Torace (cm)", min_value=40.0, max_value=200.0, step=0.1, value=float(latest.get("circonferenza_torace", 95)))
circonferenza_braccio = st.number_input("Circonferenza Braccio (cm)", min_value=15.0, max_value=60.0, step=0.1, value=float(latest.get("circonferenza_braccio", 30)))
circonferenza_coscia = st.number_input("Circonferenza Coscia (cm)", min_value=30.0, max_value=100.0, step=0.1, value=float(latest.get("circonferenza_coscia", 55)))

# Dati aggiuntivi per calcolo kcal e schede di allenamento
livello_attivita = st.selectbox("Livello di attività fisica", ["Sedentario", "Leggero", "Moderato", "Intenso"], index=1)
percentuale_grasso = st.number_input("Percentuale di massa grassa (%)", min_value=3.0, max_value=60.0, step=0.1, value=float(latest.get("percentuale_grasso", 20.0)))
circonferenza_collo = st.number_input("Circonferenza Collo (cm)", min_value=20.0, max_value=60.0, step=0.1, value=float(latest.get("circonferenza_collo", 35.0)))
circonferenza_polso = st.number_input("Circonferenza Polso (cm)", min_value=10.0, max_value=30.0, step=0.1, value=float(latest.get("circonferenza_polso", 16.0)))
metabolismo_basal = None

bmi = peso / ((altezza / 100) ** 2)
st.metric("💪 BMI (Indice di Massa Corporea)", f"{bmi:.2f}")

if sesso == "M":
    metabolismo_basal = 88.36 + (13.4 * peso) + (4.8 * altezza) - (5.7 * eta)
elif sesso == "F":
    metabolismo_basal = 447.6 + (9.2 * peso) + (3.1 * altezza) - (4.3 * eta)
else:
    metabolismo_basal = (88.36 + 447.6) / 2 + (11.3 * peso) + (4.0 * altezza) - (5.0 * eta)

# Fattore di attività
fattori = {"Sedentario": 1.2, "Leggero": 1.375, "Moderato": 1.55, "Intenso": 1.725}
fabbisogno_kcal = metabolismo_basal * fattori[livello_attivita]

st.metric("🔥 Metabolismo Basale (BMR)", f"{metabolismo_basal:.0f} kcal/giorno")
st.metric("⚡ Fabbisogno Calorico Totale", f"{fabbisogno_kcal:.0f} kcal/giorno")

if st.button("💾 Salva Profilo"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "username": username,
        "data": now,
        "peso": peso,
        "altezza": altezza,
        "eta": eta,
        "sesso": sesso,
        "infortuni": infortuni,
        "obiettivi": obiettivi,
        "circonferenza_vita": circonferenza_vita,
        "circonferenza_fianchi": circonferenza_fianchi,
        "circonferenza_torace": circonferenza_torace,
        "circonferenza_braccio": circonferenza_braccio,
        "circonferenza_coscia": circonferenza_coscia,
        "bmi": round(bmi, 2),
        "livello_attivita": livello_attivita,
        "percentuale_grasso": percentuale_grasso,
        "circonferenza_collo": circonferenza_collo,
        "circonferenza_polso": circonferenza_polso,
        "bmr": round(metabolismo_basal, 2),
        "fabbisogno_kcal": round(fabbisogno_kcal, 2)
    }

    if os.path.exists(PROFILE_PATH):
        df = pd.read_csv(PROFILE_PATH)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(PROFILE_PATH, index=False)
    st.success("✅ Profilo aggiornato con successo!")

    st.subheader("📜 Cronologia Modifiche")
    df_user = df[df["username"] == username]
    st.dataframe(df_user.tail(5))

# Mostra ultimo profilo
st.divider()
st.subheader("📋 Ultimo Profilo Salvato")
if latest:
    st.write(pd.DataFrame([latest]))
else:
    st.info("Nessun profilo ancora registrato.")

# --- Integrazione con connettore fitness ---
from agents.fitness_connector import (
    connect_strava, connect_fitbit, connect_mapmyrun, connect_google_fit,
    import_gpx_file, import_and_save
)

st.divider()
st.subheader("🔗 Connessioni Fitness")

col1, col2 = st.columns(2)

with col1:
    if st.button("Connetti Strava"):
        st.markdown(f"[Apri Strava Login]({connect_strava('TUO_CLIENT_ID', 'http://localhost:8501')})")

    if st.button("Connetti Fitbit"):
        st.markdown(f"[Apri Fitbit Login]({connect_fitbit('TUO_CLIENT_ID', 'http://localhost:8501')})")

    if st.button("Connetti MapMyRun"):
        st.markdown(f"[Apri MapMyRun Login]({connect_mapmyrun('TUO_CLIENT_ID', 'http://localhost:8501')})")

    if st.button("Connetti Google Fit"):
        st.markdown(f"[Apri Google Fit Login]({connect_google_fit('TUO_CLIENT_ID', 'http://localhost:8501')})")

    st.write(" ")

with col2:
    st.write("📂 Importazione file GPX (Nike, Adidas, Decathlon...)")
    uploaded_file = st.file_uploader("Carica GPX", type=["gpx"])
    if uploaded_file is not None:
        file_path = os.path.join(USER_DIR, "upload.gpx")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        result = import_gpx_file(username, file_path)
        st.success(f"✅ {result.get('rows', 0)} punti GPX importati con successo!")

# Importazione MyFitnessPal
st.subheader("🍎 Sincronizza MyFitnessPal")
myfit_user = st.text_input("Username MyFitnessPal")
myfit_pass = st.text_input("Password MyFitnessPal", type="password")
if st.button("Importa dati MyFitnessPal"):
    creds = {"username": myfit_user, "password": myfit_pass}
    result = import_and_save(username, "myfitnesspal", creds)
    st.success(f"✅ Importati {result.get('rows_added', 0)} record da MyFitnessPal!")

# Anteprima dati fitness
st.divider()
st.subheader("📊 Dati Fitness Recenti")

fitness_path = os.path.join(USER_DIR, "dati_fitness.csv")
if os.path.exists(fitness_path):
    df_fit = pd.read_csv(fitness_path)
    st.dataframe(df_fit.tail(10))
else:
    st.info("Nessun dato fitness ancora importato.")

# ==============================
# 🏋️ GESTIONE ALLENAMENTI SALVATI
# ==============================
st.divider()
st.subheader("🏋️ I tuoi allenamenti salvati")

allenamenti_path = os.path.join(USER_DIR, "allenamenti_manual.csv")

if os.path.exists(allenamenti_path) and os.path.getsize(allenamenti_path) > 0:
    df_allen = pd.read_csv(allenamenti_path)

    # Mostra tutta la cronologia o solo gli ultimi 20
    show_all = st.checkbox("📜 Mostra tutta la cronologia allenamenti", value=False)
    if show_all:
        st.dataframe(df_allen)
    else:
        st.dataframe(df_allen.tail(20))

    # Selezione e cancellazione
    st.write("Seleziona gli allenamenti da eliminare:")
    if not df_allen.empty:
        selected_rows = st.multiselect(
            "Seleziona le righe da eliminare (in base all’indice):",
            df_allen.index.tolist()
        )

        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("🗑️ Elimina allenamenti selezionati"):
                df_allen = df_allen.drop(index=selected_rows)
                df_allen.to_csv(allenamenti_path, index=False)
                st.success(f"✅ Eliminati {len(selected_rows)} allenamenti selezionati.")
                st.rerun()

        with col_b:
            # Pulsante download CSV
            csv_allen = df_allen.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Scarica cronologia allenamenti",
                data=csv_allen,
                file_name=f"{username}_allenamenti.csv",
                mime="text/csv"
            )
else:
    st.info("Nessun allenamento ancora registrato.")

# ==============================
# 📈 VISUALIZZAZIONE DATI FITNESS IMPORTATI
# ==============================
st.divider()
st.subheader("📈 Dati importati da app di fitness")

if os.path.exists(fitness_path) and os.path.getsize(fitness_path) > 0:
    df_fit = pd.read_csv(fitness_path)

    show_all_fit = st.checkbox("📜 Mostra tutta la cronologia fitness", value=False)
    if show_all_fit:
        st.dataframe(df_fit)
    else:
        st.dataframe(df_fit.tail(20))

    # Pulsante download CSV fitness
    csv_fit = df_fit.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Scarica dati fitness",
        data=csv_fit,
        file_name=f"{username}_dati_fitness.csv",
        mime="text/csv"
    )
else:
    st.info("Nessun dato fitness ancora importato.")