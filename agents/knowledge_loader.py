# ======================================
# 📚 KNOWLEDGE LOADER — Importa e gestisce conoscenze permanenti
# ======================================

import os
from PyPDF2 import PdfReader
from docx import Document

KNOWLEDGE_DIR = "knowledge"

def extract_text_from_file(file_path):
    """Estrae testo da PDF, DOCX o TXT."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"

    elif ext == ".docx":
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    return text.strip()


def load_all_knowledge():
    """
    Legge tutti i file nella cartella 'knowledge/'
    e restituisce un unico blocco di testo da usare come base nei prompt.
    """
    if not os.path.exists(KNOWLEDGE_DIR):
        os.makedirs(KNOWLEDGE_DIR)
        return "Nessuna conoscenza caricata (cartella creata)."

    all_text = []
    for filename in os.listdir(KNOWLEDGE_DIR):
        path = os.path.join(KNOWLEDGE_DIR, filename)
        if os.path.isfile(path) and os.path.splitext(filename)[1].lower() in [".pdf", ".docx", ".txt"]:
            text = extract_text_from_file(path)
            all_text.append(f"\n📘 {filename}\n{text}")

    if not all_text:
        return "Nessun documento trovato nella cartella 'knowledge/'."

    return "\n".join(all_text)

def query_knowledge(user_query: str, k: int = 3):
    """
    Cerca nei documenti caricati nella cartella 'knowledge' i paragrafi più pertinenti rispetto alla query dell’utente.
    Restituisce un elenco dei frammenti più rilevanti.
    """
    import re

    if not os.path.exists(KNOWLEDGE_DIR):
        print("Cartella 'knowledge' non trovata.")
        return []

    fragments = []

    # Carica tutti i testi dai file
    for filename in os.listdir(KNOWLEDGE_DIR):
        path = os.path.join(KNOWLEDGE_DIR, filename)
        if os.path.isfile(path) and os.path.splitext(filename)[1].lower() in [".pdf", ".docx", ".txt"]:
            text = extract_text_from_file(path)
            # Suddividi in paragrafi (separati da righe vuote)
            paragraphs = re.split(r'\n\s*\n', text)
            for para in paragraphs:
                if para.strip():
                    fragments.append((filename, para.strip()))

    # Calcola la pertinenza semplice basata su quante parole della query sono presenti nel paragrafo
    query_words = set(user_query.lower().split())
    scored_fragments = []
    for filename, para in fragments:
        para_words = set(para.lower().split())
        common_words = query_words.intersection(para_words)
        score = len(common_words)
        if score > 0:
            scored_fragments.append((score, filename, para))

    # Ordina per punteggio decrescente e prendi i primi k
    scored_fragments.sort(key=lambda x: x[0], reverse=True)
    top_fragments = scored_fragments[:k]

    print(f"Trovati {len(top_fragments)} frammenti rilevanti per la query.")

    # Restituisci solo i paragrafi con il nome del file
    return [f"📘 {filename}:\n{para}" for _, filename, para in top_fragments]