
import { useMemo, useState } from "react";
import "../styles/pages/diary.css";
import Navbar from '../components/Navbar';

const MOOD_LEVELS = ["Terribile", "Male", "Ok", "Bene", "Benissimo"];
const TAGS = ["Stress", "Ansia", "Felicità", "Calma", "Tristezza", "Stanchezza", "Produttività"];


function Segmented({ value, onChange }) {
    return (
        <div className="d-seg" role="radiogroup" aria-label="Umore generale">
            {MOOD_LEVELS.map((label) => {
                const active = value === label;
                return (
                    <button
                        key={label}
                        type="button"
                        className={`d - segBtn ${active ? "is-active" : ""} `}
                        role="radio"
                        aria-checked={active}
                        onClick={() => onChange(label)}
                    >
                        {label}
                    </button>
                );
            })}
        </div>
    );
}

function Chip({ label, selected, onToggle }) {
    return (
        <button
            type="button"
            className={`d - chip ${selected ? "is-selected" : ""} `}
            onClick={onToggle}
            aria-pressed={selected}
        >
            {label}
        </button>
    );
}

export default function DiaryPage() {
    const [mood, setMood] = useState("Ok");
    const [selectedTags, setSelectedTags] = useState(new Set(["Calma", "Stanchezza"]));
    const [text, setText] = useState("");

    const tagList = useMemo(() => TAGS, []);

    function toggleTag(t) {
        setSelectedTags((prev) => {
            const next = new Set(prev);
            if (next.has(t)) next.delete(t);
            else next.add(t);
            return next;
        });
    }

    function handleSave(e) {
        e.preventDefault();
        // demo: qui collegherai API/DB
        const payload = {
            mood,
            tags: Array.from(selectedTags),
            text,
            createdAt: new Date().toISOString(),
        };
        console.log("SAVE_DIARY_ENTRY", payload);
        alert("Voce salvata (demo). Controlla la console.");
    }

    return (
        <div className="d-page">
            <Navbar />

            <main className="d-main">
                <h1 className="d-title">Registra il tuo Stato Mentale</h1>

                <form className="d-card" onSubmit={handleSave}>
                    <h2 className="d-h2">Come ti senti in generale?</h2>
                    <Segmented value={mood} onChange={setMood} />

                    <h2 className="d-h2 d-mt">Cosa contribuisce a questo stato?</h2>
                    <div className="d-chipGrid">
                        {tagList.map((t) => (
                            <Chip
                                key={t}
                                label={t}
                                selected={selectedTags.has(t)}
                                onToggle={() => toggleTag(t)}
                            />
                        ))}
                    </div>

                    <h2 className="d-h2 d-mt">Scrivi della tua giornata...</h2>
                    <textarea
                        className="d-textarea"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Vuoi aggiungere altri dettagli? I tuoi dati sono privati e sicuri."
                    />

                    <button className="d-saveBtn" type="submit">
                        Salva Diario
                    </button>
                </form>
            </main>
        </div>
    );
}
