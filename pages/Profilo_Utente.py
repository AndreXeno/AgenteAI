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

# Percorso CSV
DATA_DIR = "data"
PROFILE_PATH = os.path.join(DATA_DIR, "profilo_utente.csv")

os.makedirs(DATA_DIR, exist_ok=True)

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