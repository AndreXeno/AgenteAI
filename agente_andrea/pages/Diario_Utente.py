# pages/Diario_Utente.py
import os
import json
import datetime
import pandas as pd
import streamlit as st
from collections import defaultdict

PAGE_TITLE = "📔 Diario Giornaliero — Mind&Body"

# ---------- Utilità filesystem ----------
def _user_dir(username: str) -> str:
    p = os.path.join("data", "users", username)
    os.makedirs(p, exist_ok=True)
    return p

def _load_json(path: str, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _save_json(path: str, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

# ---------- Heuristics “stato mentale” ----------
POS_KW = ["felice", "content", "sollev", "motivato", "gasat", "ottimist", "carico", "bene", "orgoglioso"]
NEG_KW = ["triste", "stanco", "stress", "ansia", "ansioso", "agitato", "preoccupato", "solo", "demoral", "arrabbi", "male"]
NEU_KW = ["ok", "normale", "così così", "neutro"]

def _score_text(s: str) -> int:
    t = s.lower()
    score = 0
    score += sum(1 for k in POS_KW if k in t)
    score -= sum(1 for k in NEG_KW if k in t)
    # neutro non cambia score, ma aiuta label
    return score

def _label_from_score(score: int, sample_texts: list[str]) -> str:
    if score >= 2:
        return "positivo"
    if score <= -2:
        return "negativo"
    # lieve: guarda presenza parole neutre
    joined = " ".join(sample_texts).lower()
    if any(k in joined for k in NEU_KW):
        return "neutro"
    return "misto"

# ---------- Raccolta eventi per giorno ----------
def _group_chat_by_day(chat_messages: list[dict]) -> dict[str, list[dict]]:
    per_day = defaultdict(list)
    # non tutti i messaggi hanno timestamp ⇒ salviamo per “oggi” come fallback
    today = datetime.date.today().isoformat()
    for m in chat_messages:
        # proviamo a leggere un timestamp opzionale
        ts = m.get("ts") or m.get("timestamp")
        if ts:
            try:
                d = datetime.datetime.fromisoformat(str(ts)).date().isoformat()
            except Exception:
                d = today
        else:
            d = today
        per_day[d].append(m)
    return per_day

def _load_all(user):
    udir = _user_dir(user)
    chat = _load_json(os.path.join(udir, "chat_history.json"), [])
    diario = _load_json(os.path.join(udir, "diario.json"), [])
    # allenamenti
    allenamenti_path = os.path.join(udir, "allenamenti.csv")
    wkt = []
    if os.path.exists(allenamenti_path):
        try:
            df = pd.read_csv(allenamenti_path)
            for _, r in df.iterrows():
                # normalizza data
                d = str(r.get("data") or r.get("date") or "")
                try:
                    d = datetime.date.fromisoformat(d).isoformat()
                except Exception:
                    d = d[:10] if len(d) >= 10 else d
                wkt.append({
                    "data": d,
                    "tipo": r.get("tipo", ""),
                    "durata_min": r.get("durata_min", None),
                    "note": r.get("note", "")
                })
        except Exception:
            pass
    return chat, diario, wkt

def _workouts_by_day(allenamenti: list[dict]) -> dict[str, list[dict]]:
    per_day = defaultdict(list)
    for a in allenamenti:
        d = str(a.get("data") or "")
        if not d:
            continue
        d = d[:10]
        per_day[d].append(a)
    return per_day

# ---------- Sintesi discorsiva per giorno ----------
def _compose_summary(day: str, chat_msgs: list[dict], workouts: list[dict], manual_notes: list[str]) -> dict:
    # prendi solo messaggi utente per “stato mentale”
    user_texts = [m.get("content", "") for m in chat_msgs if m.get("role") in ("user", "utente")]
    coach_texts = [m.get("content", "") for m in chat_msgs if m.get("role") in ("bot", "coach", "assistant")]

    mood_score = sum(_score_text(t) for t in user_texts)
    mood_label = _label_from_score(mood_score, user_texts)

    # mini riassunto workout
    w_count = len(workouts)
    w_line = ""
    if w_count > 0:
        types = {}
        for w in workouts:
            t = str(w.get("tipo", "allenamento")).lower() or "allenamento"
            types[t] = types.get(t, 0) + 1
        parts = [f"{cnt}× {k}" for k, cnt in types.items()]
        w_line = f"Hai registrato {w_count} allenamento/i: " + ", ".join(parts) + "."

    # frase discorsiva
    # punta a “note da coach” brevi e umane
    feeling = {
        "positivo": "sensazioni complessivamente buone e orientate al progresso",
        "negativo": "fatica emotiva: serve gentilezza verso te stesso e ritmi sostenibili",
        "neutro": "equilibrio stabile: puoi investire su tecnica e recupero",
        "misto": "giornata mista: normalizza gli alti e bassi, resta costante"
    }.get(mood_label, "stato da monitorare con costanza")

    manual_tail = f" Annotazione personale: {manual_notes[-1]}" if manual_notes else ""

    # prendi ultimo tema emerso dalla chat
    last_user = user_texts[-1] if user_texts else ""
    topic_hint = ""
    if last_user:
        if any(k in last_user.lower() for k in ["laurea", "esame", "studio", "università"]):
            topic_hint = " Sul fronte studio/laurea, mantieni micro-obiettivi chiari."
        elif any(k in last_user.lower() for k in ["palestra", "corsa", "allenamento", "workout"]):
            topic_hint = " Sul piano fisico, consolida la routine e cura il recupero."
        elif any(k in last_user.lower() for k in ["arbitro", "partita", "gara", "match"]):
            topic_hint = " Come arbitro/atleta, prepara i dettagli: sonno, idratazione, warm-up."
        elif any(k in last_user.lower() for k in ["solo", "solitudine", "triste", "ansia", "stress"]):
            topic_hint = " Ricorda: chiedere supporto e programmare piccole interazioni aiuta molto."

    text = (
        f"Oggi il quadro emotivo sembra **{mood_label}**: {feeling}.{(' ' + w_line) if w_line else ''}"
        f"{topic_hint}{manual_tail}"
    ).strip()

    return {
        "data": day,
        "mood": mood_label,
        "score": mood_score,
        "workouts": w_count,
        "nota": text
    }

def _merge_manual_notes(diario_json: list[dict]) -> dict[str, list[str]]:
    per_day = defaultdict(list)
    for e in diario_json:
        d = str(e.get("data") or e.get("giorno") or "")[:10]
        t = str(e.get("testo") or e.get("nota") or "").strip()
        if d and t:
            per_day[d].append(t)
    return per_day

# ---------- UI ----------
def _inject_css():
    css_path = os.path.join("static", "diario.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def _day_card(entry: dict):
    color_map = {"positivo": "ok", "neutro": "neutral", "misto": "warn", "negativo": "bad"}
    badge = color_map.get(entry["mood"], "neutral")
    st.markdown(
        f"""
        <div class="day-card">
            <div class="day-head">
                <div class="day-date">🗓️ {entry['data']}</div>
                <div class="day-badges">
                    <span class="badge {badge}">{entry['mood'].capitalize()}</span>
                    <span class="badge">{entry['workouts']} allen.</span>
                    <span class="badge score">score {entry['score']:+d}</span>
                </div>
            </div>
            <div class="day-body">
                {entry['nota']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- Pagina principale ----------
def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon="📔", layout="centered")
    _inject_css()

    # auth semplice basata su sessione (già presente nell'app)
    username = st.session_state.get("username")
    if not username:
        st.warning("Devi effettuare l’accesso per vedere il diario.")
        st.stop()

    st.title(PAGE_TITLE)

    # carica dati
    chat, diario_json, allenamenti = _load_all(username)
    per_day_chat = _group_chat_by_day(chat)
    per_day_workouts = _workouts_by_day(allenamenti)
    manual_notes = _merge_manual_notes(diario_json)

    # intervallo date (default 30 giorni)
    today = datetime.date.today()
    start_default = (today - datetime.timedelta(days=30)).isoformat()
    col1, col2 = st.columns(2)
    with col1:
        d_from = st.date_input("Dal", value=datetime.date.fromisoformat(start_default))
    with col2:
        d_to = st.date_input("Al", value=today)

    # genera entries
    days = []
    cursor = d_from
    while cursor <= d_to:
        day_str = cursor.isoformat()
        c_msgs = per_day_chat.get(day_str, [])
        w_list = per_day_workouts.get(day_str, [])
        m_notes = manual_notes.get(day_str, [])

        # se non c'è nulla quel giorno, salta
        if not (c_msgs or w_list or m_notes):
            cursor += datetime.timedelta(days=1)
            continue

        entry = _compose_summary(day_str, c_msgs, w_list, m_notes)
        days.append(entry)
        cursor += datetime.timedelta(days=1)

    # ordine: più recenti in alto
    days.sort(key=lambda x: x["data"], reverse=True)

    # azioni top
    st.markdown("### ✍️ Aggiungi una nota al diario di oggi")
    with st.form("add_note"):
        nota = st.text_area("Scrivi una breve annotazione (stato d’animo, cosa è successo, riflessioni)...", height=120)
        submitted = st.form_submit_button("Aggiungi al diario")
    if submitted and nota.strip():
        # append su diario.json
        udir = _user_dir(username)
        path = os.path.join(udir, "diario.json")
        cur = _load_json(path, [])
        cur.append({
            "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "testo": nota.strip()
        })
        _save_json(path, cur)
        st.success("Nota aggiunta! Aggiorno la pagina…")
        st.rerun()

    st.markdown("---")

    if not days:
        st.info("Nessuna voce trovata nell’intervallo selezionato. Scrivi la tua prima nota qui sopra! 🙂")
    else:
        for e in days:
            _day_card(e)

    # esportazioni
    st.markdown("---")
    st.markdown("### ⬇️ Esporta")
    if st.button("Scarica diario in CSV"):
        if days:
            df = pd.DataFrame(days)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, file_name=f"diario_{username}.csv", mime="text/csv")
        else:
            st.warning("Niente da esportare nell’intervallo selezionato.")
    if st.button("Scarica diario in JSON"):
        if days:
            b = json.dumps(days, ensure_ascii=False, indent=2).encode("utf-8")
            st.download_button("Download JSON", b, file_name=f"diario_{username}.json", mime="application/json")
        else:
            st.warning("Niente da esportare nell’intervallo selezionato.")

if __name__ == "__main__":
    main()