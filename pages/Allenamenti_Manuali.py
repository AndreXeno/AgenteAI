

import streamlit as st
import os
import pandas as pd
from datetime import datetime

from agents.session_manager import load_session, save_session

# ==============================
# 🔐 GESTIONE SESSIONE UTENTE
# ==============================
# Assicura che la chiave esista sempre
if "username" not in st.session_state:
    st.session_state["username"] = None

# Carica la sessione precedente se esiste
saved_user = load_session()
if saved_user and not st.session_state["username"]:
    st.session_state["username"] = saved_user
    print(f"[SESSION RESTORE] Ripristinato utente: {saved_user}")

# Salva la sessione solo se l'utente è loggato
if st.session_state.get("username"):
    save_session(st.session_state["username"])
    print(f"[SESSION SAVE] Sessione salvata per {st.session_state['username']}")
else:
    print("[SESSION] Nessun utente loggato al momento")
st.set_page_config(page_title="Allenamenti Manuali", page_icon="🏋️", layout="centered")

st.title("🏋️ Aggiungi Allenamento Manuale")
st.caption("Inserisci i dati del tuo allenamento per registrarlo e monitorare i progressi.")

# Lista sport supportati
sports = [
    "Corsa",
    "Ciclismo",
    "Palestra",
    "Nuoto",
    "Calcio",
    "Basket",
    "Yoga",
    "Pilates"
]

sport = st.selectbox("Scegli lo sport", sports)

# Campi dinamici in base allo sport
durata = distanza = bpm = pendenza = gruppo_muscolare = n_esercizi = intensita = vasche = stile = ruolo = stress_pre = stress_post = note = None

if sport in ["Corsa", "Ciclismo"]:
    durata = st.number_input("Durata (minuti)", min_value=1, step=1)
    distanza = st.number_input("Distanza (km)", min_value=0.0, step=0.1)
    bpm = st.number_input("Frequenza cardiaca media (BPM)", min_value=0, step=1)
    pendenza = st.number_input("Pendenza (%)", min_value=0.0, step=0.1)
    note = st.text_area("Note aggiuntive")

elif sport == "Palestra":
    durata = st.number_input("Durata (minuti)", min_value=1, step=1)
    gruppo_muscolare = st.text_input("Gruppo muscolare principale")
    n_esercizi = st.number_input("Numero esercizi", min_value=1, step=1)
    intensita = st.slider("Intensità percepita (1–10)", 1, 10)
    note = st.text_area("Note aggiuntive")

elif sport == "Nuoto":
    durata = st.number_input("Durata (minuti)", min_value=1, step=1)
    vasche = st.number_input("Numero di vasche", min_value=1, step=1)
    stile = st.text_input("Stile principale (es. rana, stile libero...)")
    bpm = st.number_input("Frequenza cardiaca media (BPM)", min_value=0, step=1)
    note = st.text_area("Note aggiuntive")

elif sport in ["Calcio", "Basket"]:
    durata = st.number_input("Durata (minuti)", min_value=1, step=1)
    ruolo = st.text_input("Ruolo o posizione")
    intensita = st.slider("Intensità percepita (1–10)", 1, 10)
    note = st.text_area("Note aggiuntive")

elif sport in ["Yoga", "Pilates"]:
    durata = st.number_input("Durata (minuti)", min_value=1, step=1)
    stress_pre = st.slider("Livello di stress prima (1–10)", 1, 10)
    stress_post = st.slider("Livello di stress dopo (1–10)", 1, 10)
    note = st.text_area("Note aggiuntive")

# Pulsante di salvataggio
if st.button("💾 Salva Allenamento"):
    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("data", "allenamenti_manual.csv")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = {
        "data": now,
        "sport": sport,
        "durata_min": durata,
        "distanza_km": distanza,
        "bpm": bpm,
        "pendenza": pendenza,
        "note": ""
    }

    if sport in ["Corsa", "Ciclismo"]:
        row["note"] = note
    elif sport == "Palestra":
        row["note"] = f"Gruppo: {gruppo_muscolare}, Esercizi: {n_esercizi}, Intensità: {intensita}. {note}"
    elif sport == "Nuoto":
        row["note"] = f"Vasche: {vasche}, Stile: {stile}. {note}"
        row["bpm"] = bpm
    elif sport in ["Calcio", "Basket"]:
        row["note"] = f"Ruolo: {ruolo}, Intensità: {intensita}. {note}"
    elif sport in ["Yoga", "Pilates"]:
        row["note"] = f"Stress prima: {stress_pre}, dopo: {stress_post}. {note}"

    # Salvataggio nel CSV
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(csv_path, index=False)
    st.success("✅ Allenamento salvato con successo!")

    # Mostra riepilogo
    st.subheader("📋 Riepilogo Allenamento")
    st.write(pd.DataFrame([row]))