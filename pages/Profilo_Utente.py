

import streamlit as st
from datetime import datetime
import os
import pandas as pd

st.set_page_config(page_title="Profilo Utente", page_icon="👤", layout="centered")

st.title("👤 Profilo Utente")
st.caption("Gestisci i tuoi dati personali, fisici e sportivi. Ogni modifica viene salvata e archiviata nel tempo per tracciare i tuoi progressi.")

# Percorso CSV
DATA_DIR = "data"
PROFILE_PATH = os.path.join(DATA_DIR, "profilo_utente.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# Carica ultimo profilo se esiste
if os.path.exists(PROFILE_PATH):
    df = pd.read_csv(PROFILE_PATH)
    latest = df.iloc[-1].to_dict()
else:
    latest = {}

# Campi profilo
peso = st.number_input("Peso (kg)", min_value=30.0, step=0.1, value=float(latest.get("peso", 70)))
altezza = st.number_input("Altezza (cm)", min_value=100.0, step=0.1, value=float(latest.get("altezza", 170)))
eta = st.number_input("Età", min_value=10, max_value=100, step=1, value=int(latest.get("eta", 25)))
sesso = st.selectbox("Sesso", ["M", "F", "Altro"], index=0 if latest.get("sesso", "M") == "M" else 1)
infortuni = st.text_area("Infortuni o limitazioni fisiche", value=latest.get("infortuni", ""))
obiettivi = st.text_input("Obiettivi di allenamento", value=latest.get("obiettivi", "mantenimento"))

if st.button("💾 Salva Profilo"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "data": now,
        "peso": peso,
        "altezza": altezza,
        "eta": eta,
        "sesso": sesso,
        "infortuni": infortuni,
        "obiettivi": obiettivi
    }

    if os.path.exists(PROFILE_PATH):
        df = pd.read_csv(PROFILE_PATH)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(PROFILE_PATH, index=False)
    st.success("✅ Profilo aggiornato con successo!")

    st.subheader("📜 Cronologia Modifiche")
    st.dataframe(df.tail(5))

# Mostra ultimo profilo
st.divider()
st.subheader("📋 Ultimo Profilo Salvato")
if latest:
    st.write(pd.DataFrame([latest]))
else:
    st.info("Nessun profilo ancora registrato.")