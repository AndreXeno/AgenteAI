# ======================================
# ⚙️ CONFIG — settings.py
# ======================================

import os
from dotenv import load_dotenv

# Carica eventuali variabili da file .env
load_dotenv()

# Se trovi una chiave nel file .env, usa quella; altrimenti usa quella di fallback
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC1j7K8pYwRCgvHGD4fQpWu0VSny6IosWE")