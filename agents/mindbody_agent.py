# ======================================
# 🤖 MIND-BODY AGENT — Orchestratore centrale con memoria conversazionale
# ======================================

from agents.module_mind import handle_mind_state
from agents.module_training import handle_training
from agents.module_analysis import handle_weekly_analysis
from agents.mindbody_reflection import handle_training_reflection
from agents.knowledge_loader import load_all_knowledge
import json
import os
import pandas as pd
# Fitness sync helper: try to fetch fresh data if Strava is connected
from agents.fitness_connector.sync_manager import auto_sync_user_data

def load_user_data(username):
    user_data = {}
    user_data["username"] = username
    base_path = os.path.join("data", "users", username)
    if os.path.exists(base_path):
        allenamenti_path = os.path.join(base_path, "allenamenti.csv")
        profilo_path = os.path.join(base_path, "profilo_utente.csv")
        # fitness_path = os.path.join(base_path, "dati_fitness.csv")

        # --- Carica token e (se necessario) sincronizza Strava automaticamente ---
        tokens_path = os.path.join(base_path, "tokens.json")
        user_data["tokens"] = {}
        if os.path.exists(tokens_path):
            try:
                with open(tokens_path, "r", encoding="utf-8") as tf:
                    tokens = json.load(tf)
                    user_data["tokens"] = tokens
            except Exception as e:
                print(f"[WARN] Impossibile leggere tokens.json per {username}: {e}")

            # Se è presente un token Strava e non esistono dati allenamenti, proviamo una sincronizzazione rapida
            try:
                if "strava" in user_data["tokens"]:
                    token_info = user_data["tokens"]["strava"]
                    if (not os.path.exists(allenamenti_path)) or (os.path.exists(allenamenti_path) and os.stat(allenamenti_path).st_size == 0):
                        print(f"[SYNC] Dati allenamenti mancanti per {username}, avvio sync Strava...")
                        try:
                            auto_sync_user_data(username, "strava", token_info)
                            print(f"[SYNC] Sync Strava completata per {username}.")
                        except Exception as sync_e:
                            print(f"[SYNC] Errore durante auto_sync Strava per {username}: {sync_e}")
            except Exception as e:
                print(f"[WARN] Errore controllo sync Strava per {username}: {e}")

        if os.path.exists(allenamenti_path):
            try:
                df_allenamenti = pd.read_csv(allenamenti_path)
                user_data["allenamenti"] = df_allenamenti.to_dict(orient="records")
            except Exception as e:
                user_data["allenamenti"] = f"Errore caricamento allenamenti: {e}"
        if os.path.exists(profilo_path):
            try:
                df_profilo = pd.read_csv(profilo_path)
                user_data["profilo_utente"] = df_profilo.to_dict(orient="records")
            except Exception as e:
                user_data["profilo_utente"] = f"Errore caricamento profilo: {e}"
        # if os.path.exists(fitness_path):
        #     try:
        #         df_fitness = pd.read_csv(fitness_path)
        #         user_data["dati_fitness"] = df_fitness.to_dict(orient="records")
        #     except Exception as e:
        #         user_data["dati_fitness"] = f"Errore caricamento dati fitness: {e}"
    print(f"[LOAD] user_data keys for {username}: {list(user_data.keys())}")
    return user_data

# ======================================
# ⚙️ CONFIGURAZIONE E LOG AVVIO
# ======================================

config_path = os.path.join("config", "personality.json")

if not os.path.exists(config_path):
    print("⚠️ [ATTENZIONE] personality.json non trovato in /config")
else:
    print(f"🧩 Carico profilo coach da: {config_path}")

with open(config_path, "r", encoding="utf-8") as f:
    COACH_PROFILE = json.load(f)

print(f"✅ Profilo Coach caricato: {COACH_PROFILE.get('name', 'Coach')}")

BASE_PROMPT = (
    f"Sei un coach con le seguenti caratteristiche:\n"
    f"Nome: {COACH_PROFILE.get('name', 'Coach')}\n"
    f"Personalità: {COACH_PROFILE.get('personality', '')}\n"
    f"Obiettivi: {COACH_PROFILE.get('goals', '')}\n"
    f"Istruzioni: {COACH_PROFILE.get('instructions', '')}\n"
    f"Rispondi sempre in modo empatico e motivante.\n"
)

# ======================================
# 📚 KNOWLEDGE LOADER
# ======================================

print("🔍 Caricamento knowledge base...")
GLOBAL_KNOWLEDGE = load_all_knowledge()
print(f"📚 Knowledge caricata ({len(GLOBAL_KNOWLEDGE)} caratteri).")

# ======================================
# 🧠 CLASSE AGENTE
# ======================================

class MindBodyAgent:
    """
    Orchestratore centrale che decide quale modulo attivare
    (mente, allenamento, riflessione o analisi settimanale)
    e mantiene memoria conversazionale temporanea (RAM).
    """

    def __init__(self):
        # Memoria dei turni conversazionali recenti
        self.memory = []
        print("🚀 MindBodyAgent inizializzato con memoria vuota.")

    def update_memory(self, role: str, content: str):
        """Aggiunge un messaggio alla memoria e limita a 10 scambi recenti."""
        self.memory.append({"role": role, "content": content})
        if len(self.memory) > 10:
            self.memory.pop(0)
        print(f"💾 Memoria aggiornata ({len(self.memory)} messaggi totali).")

    def get_context(self):
        """Costruisce un contesto utile per Gemini, sintetizzando emozioni e azioni."""
        if not self.memory:
            return ""

        recent = self.memory[-8:]
        summary = []
        for m in recent:
            if m["role"] == "utente":
                text = m["content"].lower()
                if any(word in text for word in ["palestra", "allenamento", "corsa", "workout", "esercizi"]):
                    summary.append(f"L'utente ha menzionato attività fisica: {m['content']}")
                elif any(word in text for word in ["stanco", "felice", "triste", "stressato", "solo", "demotivato", "agitato", "entusiasta", "rilassato"]):
                    summary.append(f"L'utente ha espresso un'emozione: {m['content']}")
                else:
                    summary.append(f"L'utente ha detto: {m['content']}")
            else:
                summary.append(f"Coach ha risposto: {m['content']}")

        context = "\n".join(summary)
        print(f"🧩 Contesto generato ({len(context)} caratteri).")
        return context

    def run(self, user_input: str, username: str = "anonimo"):
        print("\n==============================")
        print(f"💬 Nuovo input utente: {user_input}")

        # Normalizza testo
        text = user_input.lower().strip()

        # Carica i dati dell’utente (profilo, allenamenti, token, ecc.)
        user_data = load_user_data(username)
        print(f"📂 Dati utente caricati per contesto: {list(user_data.keys())}")

        # Costruisci un riassunto sintetico del profilo
        if isinstance(user_data.get("profilo_utente"), list) and len(user_data["profilo_utente"]) > 0:
            prof = user_data["profilo_utente"][-1]
            profile_summary = (
                f"L'utente si chiama {username}, ha {prof.get('eta', 'un’età non specificata')} anni, "
                f"pesa {prof.get('peso', 'un peso non indicato')} kg, è alto {prof.get('altezza', 'un’altezza non indicata')} cm "
                f"e il suo obiettivo è {prof.get('obiettivi', 'non specificato')}."
            )
        else:
            profile_summary = f"L'utente si chiama {username}, ma non ha ancora completato il profilo personale."

        print(f"🧠 Profilo utente sintetizzato: {profile_summary}")

        # Aggiorna la memoria conversazionale
        self.update_memory("utente", user_input)

        # 🏋️ Caso 1 — Aggiunta manuale di un allenamento
        if text.startswith("/allenamento") or text.startswith("/aggiungi allenamento"):
            print("🏋️ Attivo modulo: TRAINING (aggiunta manuale).")
            clean_input = user_input.replace("/allenamento", "").replace("/aggiungi allenamento", "").strip()
            response = handle_training(clean_input, username)
            self.update_memory("coach", response)
            print("✅ Allenamento processato e registrato.")
            return type("Response", (), {"text": response})()

        # 💭 Caso 2 — Riflessioni o emozioni legate all’allenamento o alla giornata
        if any(word in text for word in ["corsa", "palestra", "allenamento", "allenato", "fatica", "giornata", "gara", "workout", "stanco", "demotivato", "solo", "stressato", "felice"]):
            print("💭 Attivo modulo: TRAINING_REFLECTION.")
            context = (
                f"👤 Identità utente:\n{profile_summary}\n\n"
                f"📊 Dati aggiornati dell'utente:\n{json.dumps(user_data, indent=2, ensure_ascii=False)}\n\n"
                f"{BASE_PROMPT}\n\n"
                f"📚 Conoscenze disponibili:\n{GLOBAL_KNOWLEDGE[:3000]}\n\n"
                f"{self.get_context()}"
            )
            print("🧠 Context inviato a Gemini (anteprima):")
            print(context[:500] + "...")
            response = handle_training_reflection(f"Contesto conversazione:\n{context}\n\nNuovo messaggio:\n{user_input}", username)
            self.update_memory("coach", response)
            print("✅ Risposta generata da modulo TRAINING_REFLECTION.")
            return type("Response", (), {"text": response})()

        # 🧘 Caso 3 — Stato mentale o emozioni
        if any(word in text for word in ["stress", "ansia", "rilassat", "motivato", "triste", "agitato", "scarico", "felice", "rassegnato"]):
            print("🧘 Attivo modulo: MIND_STATE.")
            context = (
                f"👤 Identità utente:\n{profile_summary}\n\n"
                f"📊 Dati aggiornati dell'utente:\n{json.dumps(user_data, indent=2, ensure_ascii=False)}\n\n"
                f"{BASE_PROMPT}\n\n"
                f"📚 Conoscenze disponibili:\n{GLOBAL_KNOWLEDGE[:3000]}\n\n"
                f"{self.get_context()}"
            )
            print("🧠 Context inviato a Gemini (anteprima):")
            print(context[:500] + "...")
            response = handle_mind_state(f"Contesto conversazione:\n{context}\n\nNuovo messaggio:\n{user_input}", username)
            self.update_memory("coach", response)
            print("✅ Risposta generata da modulo MIND_STATE.")
            return type("Response", (), {"text": response})()

        # 📊 Caso 4 — Analisi settimanale
        if any(word in text for word in ["settimana", "report", "analisi", "riepilogo"]):
            print("📊 Attivo modulo: WEEKLY_ANALYSIS.")
            response = handle_weekly_analysis(username)
            self.update_memory("coach", response)
            print("✅ Report settimanale generato.")
            return type("Response", (), {"text": response})()

        # ❓ Default — Fallback
        print("❓ Input non riconosciuto, rispondo in fallback.")
        response = "Non ho capito bene, puoi spiegarmi meglio o dirmi come ti senti?"
        self.update_memory("coach", response)
        return type("Response", (), {"text": response})()