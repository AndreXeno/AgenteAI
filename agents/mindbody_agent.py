# ======================================
# 🤖 MIND-BODY AGENT — Orchestratore centrale con memoria conversazionale
# ======================================

# ======================================
# Import standard e datetime
# ======================================
from agents.module_mind import handle_mind_state
from agents.module_training import handle_training
from agents.module_analysis import handle_weekly_analysis
from agents.mindbody_reflection import handle_training_reflection
from agents.knowledge_loader import load_all_knowledge
import google.generativeai as genai
import json
import os
import pandas as pd
import datetime
# Fitness sync helper: try to fetch fresh data if Strava is connected
from agents.fitness_connector.sync_manager import auto_sync_user_data

# ======= Import modulo messaggio introduttivo dinamico =======
from agents.module_intro_message import generate_intro_message

# ======================================
# 🧩 CLASSIFICAZIONE DELL'INTENTO
# Importa il classificatore semantico (Gemini 2.5 Flash) dal modulo dedicato.
# In futuro si potrà estendere per supportare modelli alternativi (es. GPT, Gemini Pro).
# ======================================
from agents.intent_classifier import classify_intent

def load_user_data(username):
    user_data = {}
    user_data["username"] = username
    base_path = os.path.join("data", "users", username)
    if os.path.exists(base_path):
        allenamenti_path = os.path.join(base_path, "allenamenti.csv")
        profilo_path = os.path.join(base_path, "profilo_utente.css.csv")
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
                user_data["profilo_utente.css"] = df_profilo.to_dict(orient="records")
            except Exception as e:
                user_data["profilo_utente.css"] = f"Errore caricamento profilo: {e}"
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

    def save_memory(self, username: str):
        """Salva la memoria conversazionale su file JSON per l'utente."""
        user_dir = os.path.join("data", "users", username)
        os.makedirs(user_dir, exist_ok=True)
        memory_path = os.path.join(user_dir, "memory.json")
        try:
            with open(memory_path, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
            print(f"💾 Memoria salvata su file per {username} ({len(self.memory)} messaggi).")
        except Exception as e:
            print(f"[WARN] Errore durante il salvataggio della memoria per {username}: {e}")

    def load_memory(self, username: str):
        """Carica la memoria conversazionale da file, se esiste."""
        memory_path = os.path.join("data", "users", username, "memory.json")
        if os.path.exists(memory_path):
            try:
                with open(memory_path, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
                print(f"🧠 Memoria caricata per {username} ({len(self.memory)} messaggi).")
            except Exception as e:
                print(f"[WARN] Errore durante il caricamento della memoria per {username}: {e}")
                self.memory = []
        else:
            self.memory = []

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
        user_input = str(user_input).strip()
        if not user_input:
            return type("Response", (), {"text": "Non ho ricevuto alcun messaggio, puoi riprovare?"})()

        print("\n==============================")
        print(f"💬 Nuovo input utente: {user_input}")

        # Carica la memoria pregressa per l'utente
        self.load_memory(username)

        # RIMOSSA LA LOGICA DEL MESSAGGIO INTRODUTTIVO DINAMICO QUI

        # Normalizza testo
        text = user_input.lower().strip()

        # Carica i dati dell’utente (profilo, allenamenti, token, ecc.)
        user_data = load_user_data(username)
        print(f"📂 Dati utente caricati per contesto: {list(user_data.keys())}")

        # Costruisci un riassunto sintetico del profilo
        if isinstance(user_data.get("profilo_utente.css"), list) and len(user_data["profilo_utente.css"]) > 0:
            prof = user_data["profilo_utente.css"][-1]
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

        # Classifica l'intento tramite modello Gemini
        intent = classify_intent(user_input)
        print(f"🔍 Intent rilevato: {intent}")

        # 🔁 SISTEMA IBRIDO DI CLASSIFICAZIONE (fallback locale)
        text = user_input.lower()

        keywords_mind = ["felice", "triste", "stanco", "stressato", "agitato", "ansia", "motivato", "rilassato", "demotivato", "solo"]
        keywords_train = ["allenamento", "palestra", "workout", "gambe", "petto", "corsa", "cardio"]
        keywords_reflect = ["imparato", "giornata", "lezione", "riflettendo", "migliorare"]
        keywords_analysis = ["report", "statistiche", "settimana", "grafico", "progressi", "analisi"]

        if intent in ["generico", ""]:
            if any(k in text for k in keywords_mind):
                intent = "mente"
            elif any(k in text for k in keywords_train):
                intent = "allenamento"
            elif any(k in text for k in keywords_reflect):
                intent = "riflessione"
            elif any(k in text for k in keywords_analysis):
                intent = "analisi"

        print(f"🧩 Intent finale (ibrido): {intent}")

        # 🏋️ Caso 1 — Aggiunta manuale di un allenamento (manteniamo la vecchia logica per i comandi espliciti)
        if text.startswith("/allenamento") or text.startswith("/aggiungi allenamento"):
            print("🏋️ Attivo modulo: TRAINING (aggiunta manuale).")
            clean_input = user_input.replace("/allenamento", "").replace("/aggiungi allenamento", "").strip()
            response = handle_training(clean_input, username)
            self.update_memory("coach", response)
            self.save_memory(username)
            print("✅ Allenamento processato e registrato.")
            return type("Response", (), {"text": response})()

        # Gestione moduli in base all'intento classificato
        elif intent == "allenamento":
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                intent_check_prompt = f"""
L'utente ha scritto: "{user_input}".
Classifica questo messaggio in UNA delle seguenti tre categorie:
1️⃣ "descrittivo" → se l'utente parla di esperienze o giornate (es: "sono andato in palestra oggi", "oggi ho fatto attività fisica");
2️⃣ "allenamento" → se fornisce un allenamento strutturato da registrare (es: "corsa 40 minuti", "ho fatto 5 km in bici", "nuoto 30 vasche");
3️⃣ "conversazione" → se l'utente vuole solo parlare o riflettere, senza registrare nulla (es: "voglio solo parlarne", "mi va di chiacchierare", "niente registrazione").

Rispondi SOLO con una delle tre parole: "descrittivo", "allenamento" oppure "conversazione".

Tieni sempre in priorità ciò che l’utente ha detto in questo messaggio. 
Puoi collegarti a conversazioni passate solo se sono rilevanti o coerenti con quanto espresso ora.
"""
                result = model.generate_content(intent_check_prompt)
                mode = result.text.strip().lower() if hasattr(result, "text") else "descrittivo"

                if "descrittivo" in mode:
                    response = (
                        "Hai fatto bene a muoverti 💪 Vuoi che lo registri come allenamento o lo segni solo come attività?"
                    )
                    self.update_memory("coach", response)
                    self.save_memory(username)
                    print("🤖 Gemini ha classificato l'input come descrittivo.")
                    return type("Response", (), {"text": response})()
                elif "conversazione" in mode:
                    response = "Va bene 😊 raccontami pure, sono qui per ascoltare."
                    self.update_memory("coach", response)
                    self.save_memory(username)
                    print("🤖 Gemini ha classificato l'input come conversazione.")
                    return type("Response", (), {"text": response})()
                else:
                    # Solo registra se l'utente chiede esplicitamente
                    reg_keywords = ["registra", "aggiungi", "salva", "inserisci", "metti nel diario"]
                    if any(kw in user_input.lower() for kw in reg_keywords):
                        print("🏋️ Gemini ha classificato l'input come allenamento strutturato e l'utente ha chiesto la registrazione esplicita.")
                        response = handle_training(user_input, username)
                        self.update_memory("coach", response)
                        self.save_memory(username)
                        return type("Response", (), {"text": response})()
                    else:
                        # Comportati come descrittivo: chiedi conferma
                        response = (
                            "Hai fatto bene a muoverti 💪 Vuoi che lo registri come allenamento o lo segni solo come attività?"
                        )
                        self.update_memory("coach", response)
                        self.save_memory(username)
                        print("🤖 Allenamento NON registrato: attendo conferma esplicita.")
                        return type("Response", (), {"text": response})()

            except Exception as e:
                print(f"[AI CHECK ERROR] {e}")
                # fallback classico: NON registra, chiede conferma
                response = (
                    "Hai fatto bene a muoverti 💪 Vuoi che lo registri come allenamento o lo segni solo come attività?"
                )
                self.update_memory("coach", response)
                self.save_memory(username)
                return type("Response", (), {"text": response})()

        elif intent == "riflessione":
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
            self.save_memory(username)
            print("✅ Risposta generata da modulo TRAINING_REFLECTION.")
            return type("Response", (), {"text": response})()

        elif intent == "mente":
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
            self.save_memory(username)
            print("✅ Risposta generata da modulo MIND_STATE.")
            return type("Response", (), {"text": response})()

        elif intent == "analisi":
            print("📊 Attivo modulo: WEEKLY_ANALYSIS.")
            response = handle_weekly_analysis(username)
            self.update_memory("coach", response)
            self.save_memory(username)
            print("✅ Report settimanale generato.")
            return type("Response", (), {"text": response})()

        # ==============================
        # 🤖 FALLBACK INTELLIGENTE CON PROMPT DINAMICO
        # ==============================
        else:
            print("🧠 Nessun modulo specifico attivato — uso sistema di prompt dinamico.")
            try:
                from agents.prompts.base_prompt import get_dynamic_prompt
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = get_dynamic_prompt(intent, user_input, user_data or {})
                print(f"[PROMPT DINAMICO USATO] → {intent.upper()}")
                gemini_response = model.generate_content(prompt)
                response_text = gemini_response.text.strip() if hasattr(gemini_response, "text") else str(gemini_response)
                if not response_text:
                    response_text = "Posso aiutarti a capire meglio come ti senti o su cosa vuoi concentrarti oggi?"
                self.update_memory("coach", response_text)
                self.save_memory(username)
                print("✅ Risposta generata da Gemini con prompt dinamico.")
                return type("Response", (), {"text": response_text})()
            except Exception as e:
                print(f"[ERROR] ❌ Errore durante l'elaborazione del prompt dinamico: {e}")
                response = "Mi dispiace, ho avuto un piccolo problema tecnico."
                self.update_memory("coach", response)
                self.save_memory(username)
                return type("Response", (), {"text": response})()