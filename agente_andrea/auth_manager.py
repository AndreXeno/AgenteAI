# auth_manager.py
import os
import pandas as pd
import streamlit as st

USERS_FILE = "data/users.csv"
os.makedirs("data", exist_ok=True)

def _load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    else:
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USERS_FILE, index=False)
        return df

def login_page():
    """Mostra la pagina di login o registrazione."""
    st.title("🔐 Accesso Mind&Body Coach AI")

    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    users_df = _load_users()
    rerun_needed = False  # 👈 flag che useremo in app.py

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Accedi"):
            if username in users_df["username"].values:
                if users_df.loc[users_df["username"] == username, "password"].iloc[0] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success("✅ Accesso effettuato!")
                    rerun_needed = True
                else:
                    st.error("❌ Password errata.")
            else:
                st.error("❌ Utente non trovato.")

    with tab2:
        new_user = st.text_input("Nuovo username", key="new_user")
        new_pass = st.text_input("Crea password", type="password", key="new_pass")
        if st.button("Crea account"):
            if new_user.strip() == "" or new_pass.strip() == "":
                st.warning("Inserisci username e password validi.")
            elif new_user in users_df["username"].values:
                st.warning("Questo username esiste già.")
            else:
                new_row = pd.DataFrame({"username": [new_user], "password": [new_pass]})
                users_df = pd.concat([users_df, new_row], ignore_index=True)
                users_df.to_csv(USERS_FILE, index=False)
                st.success("🎉 Registrazione completata! Ora effettua l'accesso.")

    return rerun_needed  # 👈 restituiamo il flag invece di rerun diretto


def logout_user():
    """Esegue il logout e resetta la sessione."""
    if st.sidebar.button("🔓 Logout"):
        import shutil
        session_file = "session.json"
        if os.path.exists(session_file):
            os.remove(session_file)
        st.session_state.clear()
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.success("✅ Logout completato!")
        st.rerun()