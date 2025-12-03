# agents/prompts/intent_prompt.py

INTENT_PROMPT = """
Analizza il messaggio e decidi in quale categoria rientra:
- 'allenamento'
- 'mente'
- 'riflessione'
- 'analisi'
- 'generico'

Sii molto sensibile al tono emotivo implicito: se percepisci uno stato d’animo,
scegli 'mente'. Rispondi solo con la categoria.
"""