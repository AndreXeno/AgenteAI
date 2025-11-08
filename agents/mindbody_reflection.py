# ======================================
# 💬 MODULE: MIND-BODY REFLECTION — Riflessioni empatiche su allenamento o giornata
# ======================================

import os
import pandas as pd
import datetime
import json

try:
    import google.generativeai as genai
    from config.settings import GEMINI_API_KEY
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    genai = None

DATA_DIR = "data"


def handle_training_reflection(user_input: str, username: str = "anonimo"):
    """
    Analizza una riflessione sull'allenamento o sulla giornata e risponde in modo empatico,
    usando i dati già registrati (senza analisi tecniche).
    """

    user_dir = os.path.join(DATA_DIR, "users", username)
    os.makedirs(user_dir, exist_ok=True)

    diario_path = os.path.join(user_dir, "diario_utente.csv")
    allenamenti_path = os.path.join(user_dir, "allenamenti.csv")
    profilo_path = os.path.join(user_dir, "profilo_utente.json")
    riflessioni_path = os.path.join(user_dir, "riflessioni.csv")

    context_parts = []

    # 1️⃣ Leggi diario degli ultimi 3 giorni e estrai emozioni e riflessioni
    try:
        if os.path.exists(diario_path):
            df_diario = pd.read_csv(diario_path)
            if not df_diario.empty and "data" in df_diario.columns and "riflessione" in df_diario.columns:
                df_diario["data"] = pd.to_datetime(df_diario["data"], errors="coerce")
                df_diario = df_diario.dropna(subset=["data"])
                three_days_ago = datetime.date.today() - datetime.timedelta(days=3)
                recent_diario = df_diario[df_diario["data"].dt.date >= three_days_ago]
                if not recent_diario.empty:
                    diario_texts = []
                    for _, row in recent_diario.iterrows():
                        date_str = row["data"].strftime("%d %B %Y")
                        rifl = row["riflessione"]
                        diario_texts.append(f"{date_str}: {rifl}")
                    context_parts.append("Riflessioni ed emozioni degli ultimi 3 giorni dal diario personale:\n- " + "\n- ".join(diario_texts))
                else:
                    context_parts.append("Nessuna riflessione recente (ultimi 3 giorni) disponibile dal diario personale.")
            else:
                context_parts.append("Il diario personale non contiene dati sufficienti per l'analisi.")
        else:
            context_parts.append("Nessun diario personale trovato.")
    except Exception as e:
        context_parts.append(f"Errore nella lettura del diario personale: {e}")

    # 2️⃣ Leggi allenamenti recenti (ultimi 7 giorni)
    try:
        if os.path.exists(allenamenti_path):
            df_allen = pd.read_csv(allenamenti_path)
            if not df_allen.empty and "data" in df_allen.columns and "durata_min" in df_allen.columns:
                df_allen["data"] = pd.to_datetime(df_allen["data"], errors="coerce")
                df_allen = df_allen.dropna(subset=["data"])
                seven_days_ago = datetime.date.today() - datetime.timedelta(days=7)
                recent_allen = df_allen[df_allen["data"].dt.date >= seven_days_ago]
                if not recent_allen.empty:
                    tot = len(recent_allen)
                    media = recent_allen["durata_min"].mean()
                    ultima = recent_allen.iloc[-1]
                    allenamento_descr = (
                        f"Hai completato {tot} sessioni negli ultimi 7 giorni, "
                        f"con una durata media di circa {media:.0f} minuti. "
                        f"L'ultima sessione è stata il {ultima['data'].strftime('%d %B %Y')} "
                        f"({ultima.get('tipo', 'allenamento')}, {int(ultima.get('durata_min', 0))} minuti)."
                    )
                    context_parts.append("Riepilogo allenamenti recenti:\n" + allenamento_descr)
                else:
                    context_parts.append("Non risultano allenamenti registrati negli ultimi 7 giorni.")
            else:
                context_parts.append("Il file degli allenamenti non contiene dati sufficienti per l'analisi.")
        else:
            context_parts.append("Nessun file di allenamenti trovato.")
    except Exception as e:
        context_parts.append(f"Errore nella lettura degli allenamenti: {e}")

    # 3️⃣ Leggi profilo utente per eventuali informazioni contestuali
    profilo_info = {}
    try:
        if os.path.exists(profilo_path):
            with open(profilo_path, "r", encoding="utf-8") as f:
                profilo_info = json.load(f)
            context_parts.append("Informazioni sul profilo utente disponibili.")
        else:
            context_parts.append("Nessun profilo utente trovato.")
    except Exception as e:
        context_parts.append(f"Errore nella lettura del profilo utente: {e}")

    # Costruisci contesto completo
    context = "\n\n".join(context_parts)

    # 4️⃣ Genera prompt profondo e realistico per Gemini
    prompt = f"""
L'utente ha detto: "{user_input}"

Contesto raccolto dai suoi dati personali:
{context}

Informazioni aggiuntive sul profilo utente: {json.dumps(profilo_info) if profilo_info else "Nessuna"}

Come coach empatico, riflessivo e umano, analizza lo stato emotivo dell'utente basandoti sulle sue parole e sul contesto fornito. 
Rispondi con una riflessione sincera e profonda, riconoscendo emozioni, sfide e progressi. Offri consigli motivanti e supporto psicologico, 
con un tono caldo, umano e non tecnico. Evita schemi o elenchi, parla come se fossi un amico che ascolta con attenzione e cuore.
Includi nell'analisi uno stato emotivo inferito (es. gioia, stress, determinazione, ecc.) e integralo nella riflessione.
"""

    # 5️⃣ Genera risposta con Gemini e gestisci errori/fallback
    try:
        if genai is None:
            raise ImportError("Modulo Gemini non disponibile")

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        riflessione = response.text.strip()

        # Prova a inferire umore dall'inizio della riflessione (semplice estrazione)
        umore_inferito = "Non specificato"
        lower_text = riflessione.lower()
        if "gioia" in lower_text or "felicità" in lower_text:
            umore_inferito = "Gioia"
        elif "stress" in lower_text or "ansia" in lower_text:
            umore_inferito = "Stress"
        elif "determinazione" in lower_text or "forza" in lower_text:
            umore_inferito = "Determinazione"
        elif "tristezza" in lower_text or "delusione" in lower_text:
            umore_inferito = "Tristezza"
        elif "orgoglio" in lower_text:
            umore_inferito = "Orgoglio"
        elif "calma" in lower_text or "serenità" in lower_text:
            umore_inferito = "Calma"

        # 6️⃣ Salva la riflessione in riflessioni.csv
        try:
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_entry = pd.DataFrame([{
                "data": now_str,
                "input": user_input,
                "riflessione": riflessione,
                "umore_inferito": umore_inferito
            }])
            if os.path.exists(riflessioni_path):
                df_riflessioni = pd.read_csv(riflessioni_path)
                df_riflessioni = pd.concat([df_riflessioni, new_entry], ignore_index=True)
            else:
                df_riflessioni = new_entry
            df_riflessioni.to_csv(riflessioni_path, index=False)
        except Exception as e:
            print(f"[Reflection WARN] Errore nel salvataggio della riflessione: {e}")

        return riflessione

    except Exception as e:
        print(f"[Reflection ERROR] ❌ Errore durante la generazione riflessione: {e}")
        return (
            "Non riesco a elaborare la riflessione con Gemini al momento. "
            "Ti dico comunque che apprezzo il tuo impegno e che ogni passo, anche piccolo, "
            "ti avvicina ai tuoi obiettivi. Continua così!"
        )