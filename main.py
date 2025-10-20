# ======================================
# 🌿 MAIN — Mind&Body Coach AI
# ======================================

from agents.mindbody_agent import MindBodyAgent

def main():
    print("\n🧘‍♂️ Benvenuto in Mind&Body Coach AI — versione Gemini 🌿")
    print("Scrivi 'esci' per chiudere.\n")

    mindbody_agent = MindBodyAgent()  # inizializzazione

    while True:
        user_input = input("Tu ➜ ").strip()

        if user_input.lower() in ["esci", "exit", "quit"]:
            print("\n👋 Alla prossima! Continua a prenderti cura del tuo corpo e della tua mente ❤️\n")
            break

        try:
            # L’agente ora restituisce direttamente una stringa (testo)
            response = mindbody_agent.run(user_input)
            print(f"\nCoach 🤖 ➜ {response.text if hasattr(response, 'text') else response}\n")
        except Exception as e:
            print(f"⚠️ Errore: {e}\n")

if __name__ == "__main__":
    main()