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

def load_user_data(username):
    user_data = {}
    base_path = os.path.join("data", "users", username)
    if os.path.exists(base_path):
        allenamenti_path = os.path.join(base_path, "allenamenti.csv")
        profilo_path = os.path.join(base_path, "profilo_utente.csv")
        fitness_path = os.path.join(base_path, "dati_fitness.csv")

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
        if os.path.exists(fitness_path):
            try:
                df_fitness = pd.read_csv(fitness_path)
                user_data["dati_fitness"] = df_fitness.to_dict(orient="records")
            except Exception as e:
                user_data["dati_fitness"] = f"Errore caricamento dati fitness: {e}"
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
        text = user_input.lower().strip()
        print("\n==============================")
        print(f"💬 Nuovo input utente: {user_input}")

        user_data = load_user_data(username)
        print(f"📂 Dati utente caricati per contesto: {list(user_data.keys())}")

        self.update_memory("utente", user_input)

        # 🏋️ Caso 1 — Comando esplicito per aggiungere allenamento
        if text.startswith("/allenamento") or text.startswith("/aggiungi allenamento"):
            print("🏋️ Attivo modulo: TRAINING (aggiunta manuale).")
            clean_input = user_input.replace("/allenamento", "").replace("/aggiungi allenamento", "").strip()
            response = handle_training(clean_input, username)
            self.update_memory("coach", response)
            print("✅ Allenamento processato e registrato.")
            return type("Response", (), {"text": response})()

        # 💬 Caso 2 — Riflessioni o emozioni legate a giornata o allenamento
        if any(word in text for word in ["corsa", "palestra", "allenamento", "allenato", "fatica", "giornata", "gara", "workout", "stanco", "demotivato", "solo", "svuotato", "stressato", "ansioso", "rassegnato", "felice"]):
            print("💭 Attivo modulo: TRAINING_REFLECTION.")
            context = f"{BASE_PROMPT}\n\n📚 Conoscenze disponibili:\n{GLOBAL_KNOWLEDGE[:3000]}\n\n" + self.get_context()
            context = f"📊 Dati aggiornati dell'utente:\n{json.dumps(user_data, indent=2, ensure_ascii=False)}\n\n" + context
            print("🧠 Context inviato a Gemini (anteprima):")
            print(context[:500] + "...")
            response = handle_training_reflection(f"Contesto conversazione:\n{context}\n\nNuovo messaggio:\n{user_input}", username)
            self.update_memory("coach", response)
            print("✅ Risposta generata da modulo TRAINING_REFLECTION.")
            return type("Response", (), {"text": response})()

        # 🧘 Caso 3 — Stato mentale puro
        if any(word in text for word in ["stress", "ansia", "rilassat", "felice", "motivato", "triste", "agitato", "scarico", "rassegnato", "isolato", "invidioso", "geloso"]):
            print("🧘 Attivo modulo: MIND_STATE.")
            context = f"{BASE_PROMPT}\n\n📚 Conoscenze disponibili:\n{GLOBAL_KNOWLEDGE[:3000]}\n\n" + self.get_context()
            context = f"📊 Dati aggiornati dell'utente:\n{json.dumps(user_data, indent=2, ensure_ascii=False)}\n\n" + context
            print("🧠 Context inviato a Gemini (anteprima):")
            print(context[:500] + "...")
            response = handle_mind_state(f"Contesto conversazione:\n{context}\n\nNuovo messaggio:\n{user_input}", username)
            self.update_memory("coach", response)
            print("✅ Risposta generata da modulo MIND_STATE.")
            return type("Response", (), {"text": response})()

        # 📊 Caso 4 — Richiesta di analisi settimanale
        if any(word in text for word in ["settimana", "report", "analisi", "riepilogo"]):
            print("📊 Attivo modulo: WEEKLY_ANALYSIS.")
            # In questo caso non c'è un context testuale, ma possiamo comunque fornire i dati utente se necessario
            # Per coerenza, passiamo i dati utente in qualche modo se il modulo lo supporta, altrimenti solo response
            # Qui si assume che handle_weekly_analysis accetti solo username
            response = handle_weekly_analysis(username)
            self.update_memory("coach", response)
            print("✅ Report settimanale generato.")
            return type("Response", (), {"text": response})()

        # ❓ Default — Non classificato
        print("❓ Input non riconosciuto, rispondo in fallback.")
        response = "Non ho capito bene, puoi spiegarmi meglio o dirmi come ti senti?"
        self.update_memory("coach", response)
        return type("Response", (), {"text": response})()