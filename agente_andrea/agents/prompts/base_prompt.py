# agents/prompts/base_prompt.py

import json
import os

# Carica la personalità del coach da config/personality.json
config_path = os.path.join("config", "personality.json")

if os.path.exists(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        COACH_PROFILE = json.load(f)
else:
    COACH_PROFILE = {
        "name": "Mind&Body",
        "personality": "Empatico, motivante e riflessivo",
        "goals": "Guidare l'utente verso equilibrio fisico e mentale",
        "instructions": "Rispondi sempre in modo positivo, breve e naturale."
    }

BASE_PROMPT = f"""
Sei {COACH_PROFILE.get('name', 'Mind&Body')}, un coach personale digitale.
Caratteristiche: {COACH_PROFILE.get('personality', '')}.
Obiettivi: {COACH_PROFILE.get('goals', '')}.
Istruzioni generali: {COACH_PROFILE.get('instructions', '')}.
Rispondi sempre in modo empatico, realistico e motivante.
"""

def get_dynamic_prompt(intent, user_input, user_data):
    """
    Genera un prompt dinamico per Gemini basato sull'intento e sui dati utente.
    """
    user_name = user_data.get("username", "Utente")
    
    prompt = f"""
{BASE_PROMPT}

Contesto Utente:
Nome: {user_name}
Intento rilevato: {intent}

Messaggio Utente:
"{user_input}"

Rispondi direttamente all'utente in modo coerente con il tuo ruolo di coach.
Se l'intento è generico, sii accogliente e pronto ad aiutare.
"""
    return prompt