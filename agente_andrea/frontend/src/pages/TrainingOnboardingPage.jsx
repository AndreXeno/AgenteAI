import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import "../styles/shared.css";

/**
 * Mind&Body - Training Onboarding (IT)
 * - Navbar condivisa (usata anche in altre pagine)
 * - Accessibile SOLO la prima volta che l'utente entra in "Allenamento"
 *
 * Come funziona il gate "prima volta":
 * - Usa localStorage key: "mb_training_onboarding_done"
 * - Se già presente => renderizza <TrainingHomePlaceholder />
 * - Se non presente => renderizza onboarding
 *
 * Nota: in produzione, meglio salvarlo su DB (es. Supabase) per utente.
 */

const LS_KEY = "mb_training_onboarding_done";

function cn(...classes) {
    return classes.filter(Boolean).join(" ");
}

function MaterialIcon({ name, className = "" }) {
    return (
        <span className={cn("material-symbols-outlined", className)} aria-hidden="true">
            {name}
        </span>
    );
}

function ChipToggle({ label, checked, onChange, tone = "primary" }) {
    const base =
        "inline-flex items-center gap-2 px-4 py-2 rounded-full border text-sm font-medium cursor-pointer select-none transition";
    const styles =
        tone === "danger"
            ? checked
                ? "border-red-500 bg-red-50 text-red-700"
                : "border-gray-200 bg-white text-gray-700 hover:border-red-300"
            : checked
                ? "border-emerald-500 bg-emerald-50 text-emerald-800"
                : "border-gray-200 bg-white text-gray-700 hover:border-emerald-300";
    return (
        <label className={cn(base, styles)}>
            <input
                type="checkbox"
                className="sr-only"
                checked={checked}
                onChange={(e) => onChange(e.target.checked)}
            />
            {label}
        </label>
    );
}

function RadioCard({ name, value, selected, onChange, icon, title, subtitle }) {
    return (
        <label
            className={cn(
                "group relative cursor-pointer rounded-2xl border-2 p-4 transition",
                selected ? "border-emerald-500 bg-emerald-50/40" : "border-transparent bg-gray-50 hover:border-emerald-200"
            )}
        >
            <input
                className="sr-only"
                type="radio"
                name={name}
                value={value}
                checked={selected}
                onChange={() => onChange(value)}
            />
            <div className="flex items-center gap-4">
                <MaterialIcon
                    name={icon}
                    className={cn("text-3xl", selected ? "text-emerald-500" : "text-gray-400")}
                />
                <div className="min-w-0">
                    <p className="font-extrabold">{title}</p>
                    <p className="text-sm text-gray-500">{subtitle}</p>
                </div>
            </div>

            <div className={cn("absolute top-4 right-4 transition", selected ? "opacity-100" : "opacity-0")}>
                <MaterialIcon name="check_circle" className="text-emerald-500" />
            </div>
        </label>
    );
}

function SelectPillRadio({ name, value, selected, onChange, children }) {
    return (
        <label
            className={cn(
                "px-5 py-2.5 rounded-xl border cursor-pointer font-semibold transition inline-flex items-center justify-center",
                selected ? "bg-emerald-400 text-[#102216] border-emerald-500" : "border-gray-200 hover:border-emerald-300"
            )}
        >
            <input
                className="sr-only"
                type="radio"
                name={name}
                value={value}
                checked={selected}
                onChange={() => onChange(value)}
            />
            {children}
        </label>
    );
}

function DayPill({ label, checked, onChange }) {
    return (
        <label
            className={cn(
                "size-11 md:size-12 rounded-full border-2 flex items-center justify-center cursor-pointer font-extrabold transition",
                checked ? "bg-emerald-400 text-[#102216] border-emerald-500" : "border-gray-200 hover:border-emerald-300"
            )}
        >
            <input className="sr-only" type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} />
            {label}
        </label>
    );
}

function TagInput({ placeholder, tags, setTags, tone = "green" }) {
    const [value, setValue] = useState("");

    const add = () => {
        const v = value.trim();
        if (!v) return;
        if (tags.some((t) => t.toLowerCase() === v.toLowerCase())) return;
        setTags([...tags, v]);
        setValue("");
    };

    const remove = (idx) => setTags(tags.filter((_, i) => i !== idx));

    const tagClass =
        tone === "red"
            ? "bg-red-100 text-red-800"
            : "bg-green-100 text-green-800";

    return (
        <div className="space-y-2">
            <div className="relative">
                <input
                    className="w-full rounded-xl border border-gray-200 bg-white py-2.5 pl-3 pr-12 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-200 outline-none"
                    placeholder={placeholder}
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            e.preventDefault();
                            add();
                        }
                    }}
                />
                <button
                    type="button"
                    onClick={add}
                    className="absolute right-2 top-2 rounded-lg px-2 py-1 text-emerald-600 hover:text-emerald-700"
                    aria-label="Aggiungi"
                >
                    <MaterialIcon name="add" />
                </button>
            </div>
            <div className="flex flex-wrap gap-2">
                {tags.map((t, idx) => (
                    <span
                        key={t + idx}
                        className={cn("inline-flex items-center gap-2 px-2 py-1 rounded-lg text-sm font-semibold", tagClass)}
                    >
                        {t}
                        <button type="button" className="hover:text-red-600" onClick={() => remove(idx)} aria-label="Rimuovi tag">
                            ×
                        </button>
                    </span>
                ))}
            </div>
        </div>
    );
}

function Section({ id, icon, title, subtitle, children, iconTone = "primary" }) {
    const iconWrap =
        iconTone === "danger"
            ? "bg-red-100 text-red-600"
            : "bg-emerald-100 text-emerald-700";
    return (
        <section
            id={id}
            className="scroll-mt-24 space-y-5 rounded-2xl bg-white p-6 md:p-8 shadow-sm border border-gray-200"
        >
            <div className="flex items-center gap-3">
                <div className={cn("flex size-10 items-center justify-center rounded-full", iconWrap)}>
                    <MaterialIcon name={icon} />
                </div>
                <div>
                    <h2 className="text-2xl font-extrabold">{title}</h2>
                    {subtitle ? <p className="text-gray-500 mt-1">{subtitle}</p> : null}
                </div>
            </div>
            {children}
        </section>
    );
}

function TrainingHomePlaceholder() {
    return (
        <div className="max-w-5xl mx-auto px-6 py-10">
            <div className="rounded-2xl bg-white border border-gray-200 p-8 shadow-sm">
                <h1 className="text-3xl font-black tracking-tight">Allenamento</h1>
                <p className="text-gray-600 mt-2">
                    Onboarding completato ✅ Qui puoi mostrare la tua home training (piano, sessioni, progressi, ecc.).
                </p>
                <div className="mt-6 flex gap-3 flex-wrap">
                    <button className="px-5 py-3 rounded-xl bg-emerald-400 text-[#102216] font-extrabold">
                        Vai al piano di oggi
                    </button>
                    <button className="px-5 py-3 rounded-xl border border-gray-200 font-bold">
                        Modifica preferenze
                    </button>
                </div>
            </div>
        </div>
    );
}

export default function TrainingOnboardingPage() {
    const [onboardingDone, setOnboardingDone] = useState(false);

    // Stato form
    const [objective, setObjective] = useState("weight_loss");
    const [level, setLevel] = useState("intermediate");

    const [days, setDays] = useState({
        Lun: false,
        Mar: true,
        Mer: true,
        Gio: false,
        Ven: true,
        Sab: false,
        Dom: false,
    });

    const [duration, setDuration] = useState("45");
    const [equipment, setEquipment] = useState("home_basic");

    const [limits, setLimits] = useState({
        spalle: false,
        schiena_bassa: false,
        ginocchia: true,
        polsi: false,
        caviglie: false,
    });
    const [specificCondition, setSpecificCondition] = useState(false);

    const [split, setSplit] = useState("upper_lower");
    const [cardio, setCardio] = useState("liss");

    const [pushLevel, setPushLevel] = useState(3); // 1..3
    const [rpe, setRpe] = useState(8); // 1..10

    const [loves, setLoves] = useState(["Squat", "Panca piana"]);
    const [hates, setHates] = useState(["Burpees"]);

    const [sync, setSync] = useState(true);
    const [trackSets, setTrackSets] = useState(true);

    const [noise, setNoise] = useState("normal");
    const [space, setSpace] = useState("open_room");

    // Gate "prima volta"
    useEffect(() => {
        const v = localStorage.getItem(LS_KEY);
        setOnboardingDone(v === "1");
    }, []);

    // Material Icons (una sola volta)
    useEffect(() => {
        const id = "mb-material-icons";
        if (document.getElementById(id)) return;
        const link = document.createElement("link");
        link.id = id;
        link.rel = "stylesheet";
        link.href =
            "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap";
        document.head.appendChild(link);
    }, []);

    const sections = useMemo(
        () => [
            { id: "section-objective", label: "1. Obiettivo", icon: "flag" },
            { id: "section-level", label: "2. Livello", icon: "trending_up" },
            { id: "section-availability", label: "3. Disponibilità", icon: "calendar_month" },
            { id: "section-equipment", label: "4. Attrezzatura", icon: "fitness_center" },
            { id: "section-safety", label: "5. Sicurezza", icon: "health_and_safety" },
            { id: "section-style", label: "6. Stile", icon: "style" },
            { id: "section-intensity", label: "7. Intensità", icon: "speed" },
            { id: "section-exercises", label: "8. Preferenze esercizi", icon: "thumbs_up_down" },
            { id: "section-monitoring", label: "9. Monitoraggio", icon: "watch" },
            { id: "section-constraints", label: "10. Vincoli", icon: "block" },
        ],
        []
    );

    const completedCount = useMemo(() => {
        // semplice: consideriamo “completo” se ha un valore
        let n = 0;
        if (objective) n++;
        if (level) n++;
        if (Object.values(days).some(Boolean)) n++;
        if (duration) n++;
        if (equipment) n++;
        n++; // safety sempre presente (anche se vuoto)
        if (split && cardio) n++;
        if (pushLevel && rpe) n++;
        n++; // likes/dislikes
        n++; // monitoring
        if (noise && space) n++;
        // Totale 10 (accorpando disponibilità giorni+durata in 1 conteggio sopra ci siamo comunque vicini)
        return Math.min(10, n);
    }, [objective, level, days, duration, equipment, split, cardio, pushLevel, rpe, noise, space]);

    const handleGenerate = () => {
        // Qui salverai su DB. Per ora: localStorage gate.
        localStorage.setItem(LS_KEY, "1");
        setOnboardingDone(true);

        // Esempio payload pronto per invio backend
        const payload = {
            objective,
            level,
            availability: {
                days: Object.entries(days)
                    .filter(([, v]) => v)
                    .map(([k]) => k),
                durationMinutes: Number(duration),
            },
            equipment,
            safety: {
                limitations: Object.entries(limits)
                    .filter(([, v]) => v)
                    .map(([k]) => k),
                specificCondition,
            },
            style: { split, cardio },
            intensity: { pushLevel, rpe },
            exercises: { loves, hates },
            monitoring: { sync, trackSets },
            constraints: { noise, space },
        };

        // eslint-disable-next-line no-console
        console.log("TRAINING_ONBOARDING_PAYLOAD", payload);
    };

    const handleReset = () => {
        localStorage.removeItem(LS_KEY);
        setOnboardingDone(false);
    }


    if (onboardingDone) {
        return (
            <div className="min-h-screen bg-[#f6f8f6] text-[#111813]">
                <header className="mb-navbar">
                    <div className="mb-brand">
                        <div className="mb-logo" aria-hidden="true">
                            <span className="mb-logoInner" />
                        </div>
                        <span className="mb-brandText">Mind&Body</span>
                    </div>

                    <nav className="mb-navLinks" aria-label="Primary">
                        <Link className="mb-link" to="/nutrition">Nutrizione</Link>
                        <Link className="mb-link" to="/training">Allenamento</Link>
                        <Link className="mb-link" to="/mental-wellbeing">Benessere Mentale</Link>
                        <Link className="mb-link" to="#community">Community</Link>
                    </nav>

                    <Link to="/account" className="mb-profileBtn" aria-label="Profilo">
                        <span className="mb-profileRing">
                            <span className="mb-profileIcon" aria-hidden="true">👤</span>
                        </span>
                    </Link>
                </header>
                <div className="max-w-5xl mx-auto px-6 py-10">
                    <div className="rounded-2xl bg-white border border-gray-200 p-8 shadow-sm">
                        <h1 className="text-3xl font-black tracking-tight">Allenamento</h1>
                        <p className="text-gray-600 mt-2">
                            Onboarding completato ✅ Qui puoi mostrare la tua home training (piano, sessioni, progressi, ecc.).
                        </p>
                        <div className="mt-6 flex gap-3 flex-wrap">
                            <Link to="/training" className="px-5 py-3 rounded-xl bg-emerald-400 text-[#102216] font-extrabold text-center" style={{ textDecoration: 'none' }}>
                                Vai al piano di oggi
                            </Link>
                            <button
                                onClick={handleReset}
                                className="px-5 py-3 rounded-xl border border-gray-200 font-bold"
                            >
                                Rifa onboarding (Reset)
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-[#f6f8f6] font-[Manrope] text-[#0f172a] selection:bg-emerald-400 selection:text-[#0f172a]">
            {/* Styles inject */}
            <style>{`
        /* ... custom styles ... */
      `}</style>

            <Navbar />

            <div className="max-w-[1440px] mx-auto flex">
                {/* Sidebar steps (desktop) */}
                <aside className="hidden lg:block w-72 sticky top-[75px] h-[calc(100vh-75px)] overflow-y-auto border-r border-gray-200 bg-white p-6">
                    <h3 className="text-xs font-black uppercase tracking-wider text-gray-500 mb-6">Passi onboarding</h3>
                    <ul className="space-y-1">
                        {sections.map((s, idx) => (
                            <li key={s.id}>
                                <a
                                    href={`#${s.id}`}
                                    className={cn(
                                        "flex items-center gap-3 px-3 py-2.5 rounded-xl font-bold transition text-sm",
                                        idx === 0 ? "bg-emerald-50 text-emerald-700" : "text-gray-600 hover:bg-gray-100"
                                    )}
                                >
                                    <MaterialIcon name={s.icon} className="text-xl" />
                                    {s.label}
                                </a>
                            </li>
                        ))}
                    </ul>
                </aside>

                {/* Main */}
                <main className="flex-1 flex flex-col items-center py-10 px-4 md:px-12 overflow-x-hidden">
                    <div className="w-full max-w-[820px] space-y-12 pb-28">
                        {/* Header */}
                        <div className="space-y-4">
                            <div className="inline-flex items-center gap-2 rounded-full bg-emerald-100 px-3 py-1 text-sm font-extrabold text-emerald-800">
                                <span className="size-2 rounded-full bg-emerald-400" />
                                Setup Allenamento
                            </div>
                            <h1 className="text-4xl md:text-5xl font-black tracking-tight">Personalizza il tuo piano</h1>
                            <p className="text-lg text-gray-600 max-w-2xl">
                                Costruiamo una routine che si adatta alla tua vita. Useremo questi dati per generare un piano su misura
                                che evolve con te.
                            </p>
                        </div>

                        {/* 1 Objective */}
                        <Section
                            id="section-objective"
                            icon="flag"
                            title="1. Obiettivo principale"
                            subtitle="Seleziona l’obiettivo principale che vuoi raggiungere nelle prossime 12 settimane."
                        >
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <RadioCard
                                    name="objective"
                                    value="weight_loss"
                                    selected={objective === "weight_loss"}
                                    onChange={setObjective}
                                    icon="scale"
                                    title="Dimagrimento & Ricomposizione"
                                    subtitle="Brucia grasso mantenendo massa muscolare"
                                />
                                <RadioCard
                                    name="objective"
                                    value="hypertrophy"
                                    selected={objective === "hypertrophy"}
                                    onChange={setObjective}
                                    icon="fitness_center"
                                    title="Ipertrofia & Massa muscolare"
                                    subtitle="Massimizza la crescita muscolare"
                                />
                                <RadioCard
                                    name="objective"
                                    value="strength"
                                    selected={objective === "strength"}
                                    onChange={setObjective}
                                    icon="bolt"
                                    title="Forza & Potenza"
                                    subtitle="Aumenta la forza nei fondamentali"
                                />
                                <RadioCard
                                    name="objective"
                                    value="endurance"
                                    selected={objective === "endurance"}
                                    onChange={setObjective}
                                    icon="directions_run"
                                    title="Resistenza & Cardio"
                                    subtitle="Migliora fiato e salute cardiovascolare"
                                />
                            </div>
                        </Section>

                        {/* 2 Level */}
                        <Section id="section-level" icon="trending_up" title="2. Livello & esperienza">
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                                <label
                                    className={cn(
                                        "cursor-pointer text-center p-6 rounded-2xl border-2 transition",
                                        level === "beginner" ? "border-emerald-500 bg-emerald-50/40" : "border-gray-200 hover:border-emerald-200"
                                    )}
                                >
                                    <input className="sr-only" type="radio" name="level" checked={level === "beginner"} onChange={() => setLevel("beginner")} />
                                    <div className="bg-emerald-100 size-12 rounded-full flex items-center justify-center mx-auto mb-3 text-emerald-700">
                                        <MaterialIcon name="child_care" />
                                    </div>
                                    <h3 className="font-extrabold mb-1">Principiante</h3>
                                    <p className="text-xs text-gray-500">Nuovo/a o riparto dopo una lunga pausa</p>
                                </label>

                                <label
                                    className={cn(
                                        "cursor-pointer text-center p-6 rounded-2xl border-2 transition",
                                        level === "intermediate" ? "border-emerald-500 bg-emerald-50/40" : "border-gray-200 hover:border-emerald-200"
                                    )}
                                >
                                    <input
                                        className="sr-only"
                                        type="radio"
                                        name="level"
                                        checked={level === "intermediate"}
                                        onChange={() => setLevel("intermediate")}
                                    />
                                    <div className="bg-emerald-100 size-12 rounded-full flex items-center justify-center mx-auto mb-3 text-emerald-700">
                                        <MaterialIcon name="hiking" />
                                    </div>
                                    <h3 className="font-extrabold mb-1">Intermedio</h3>
                                    <p className="text-xs text-gray-500">Allenamento costante da 6+ mesi</p>
                                </label>

                                <label
                                    className={cn(
                                        "cursor-pointer text-center p-6 rounded-2xl border-2 transition",
                                        level === "advanced" ? "border-emerald-500 bg-emerald-50/40" : "border-gray-200 hover:border-emerald-200"
                                    )}
                                >
                                    <input className="sr-only" type="radio" name="level" checked={level === "advanced"} onChange={() => setLevel("advanced")} />
                                    <div className="bg-emerald-100 size-12 rounded-full flex items-center justify-center mx-auto mb-3 text-emerald-700">
                                        <MaterialIcon name="sports_mma" />
                                    </div>
                                    <h3 className="font-extrabold mb-1">Avanzato</h3>
                                    <p className="text-xs text-gray-500">Allenamento intenso e regolare da 2+ anni</p>
                                </label>
                            </div>
                        </Section>

                        {/* 3 Availability */}
                        <Section id="section-availability" icon="calendar_month" title="3. Disponibilità">
                            <div className="space-y-6">
                                <div className="space-y-3">
                                    <label className="text-sm font-black uppercase text-gray-500">Quali giorni puoi allenarti?</label>
                                    <div className="flex flex-wrap gap-3">
                                        {Object.entries(days).map(([k, v]) => (
                                            <DayPill key={k} label={k[0]} checked={v} onChange={(nv) => setDays({ ...days, [k]: nv })} />
                                        ))}
                                    </div>
                                    <p className="text-sm text-gray-500">
                                        Suggerimento: per un buon compromesso, 3–4 giorni a settimana funzionano per quasi tutti.
                                    </p>
                                </div>

                                <div className="space-y-3">
                                    <label className="text-sm font-black uppercase text-gray-500">Durata per sessione</label>
                                    <div className="flex flex-wrap gap-2">
                                        <SelectPillRadio name="duration" value="20" selected={duration === "20"} onChange={setDuration}>
                                            20 min
                                        </SelectPillRadio>
                                        <SelectPillRadio name="duration" value="30" selected={duration === "30"} onChange={setDuration}>
                                            30 min
                                        </SelectPillRadio>
                                        <SelectPillRadio name="duration" value="45" selected={duration === "45"} onChange={setDuration}>
                                            45 min
                                        </SelectPillRadio>
                                        <SelectPillRadio name="duration" value="60" selected={duration === "60"} onChange={setDuration}>
                                            60+ min
                                        </SelectPillRadio>
                                    </div>
                                </div>
                            </div>
                        </Section>

                        {/* 4 Equipment */}
                        <Section id="section-equipment" icon="fitness_center" title="4. Attrezzatura & luogo">
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                {[
                                    { key: "home_none", icon: "home", title: "Casa — senza attrezzi", sub: "Solo corpo libero" },
                                    { key: "home_basic", icon: "inventory_2", title: "Casa — attrezzi base", sub: "Manubri, elastici, ecc." },
                                    { key: "gym_full", icon: "apartment", title: "Palestra completa", sub: "Macchine e bilancieri" },
                                    { key: "outdoor", icon: "park", title: "Outdoor", sub: "Corsa, bici, parco" },
                                ].map((o) => (
                                    <label
                                        key={o.key}
                                        className={cn(
                                            "flex items-start gap-3 p-4 rounded-2xl border-2 cursor-pointer transition",
                                            equipment === o.key ? "border-emerald-500 bg-emerald-50/40" : "border-gray-200 hover:border-emerald-200"
                                        )}
                                    >
                                        <input className="sr-only" type="radio" name="equipment" checked={equipment === o.key} onChange={() => setEquipment(o.key)} />
                                        <MaterialIcon name={o.icon} className="text-2xl mt-0.5 text-gray-700" />
                                        <div>
                                            <span className="font-extrabold block">{o.title}</span>
                                            <span className="text-xs text-gray-500">{o.sub}</span>
                                        </div>
                                    </label>
                                ))}
                            </div>
                        </Section>

                        {/* 5 Safety */}
                        <Section
                            id="section-safety"
                            icon="health_and_safety"
                            iconTone="danger"
                            title="5. Limitazioni & sicurezza"
                            subtitle="Seleziona eventuali zone con dolore/infortuni: escluderemo esercizi che possono peggiorare."
                        >
                            <div className="space-y-4">
                                <div className="flex flex-wrap gap-3">
                                    <ChipToggle
                                        label="Spalle"
                                        tone="danger"
                                        checked={limits.spalle}
                                        onChange={(v) => setLimits({ ...limits, spalle: v })}
                                    />
                                    <ChipToggle
                                        label="Schiena bassa"
                                        tone="danger"
                                        checked={limits.schiena_bassa}
                                        onChange={(v) => setLimits({ ...limits, schiena_bassa: v })}
                                    />
                                    <ChipToggle
                                        label="Ginocchia"
                                        tone="danger"
                                        checked={limits.ginocchia}
                                        onChange={(v) => setLimits({ ...limits, ginocchia: v })}
                                    />
                                    <ChipToggle
                                        label="Polsi"
                                        tone="danger"
                                        checked={limits.polsi}
                                        onChange={(v) => setLimits({ ...limits, polsi: v })}
                                    />
                                    <ChipToggle
                                        label="Caviglie"
                                        tone="danger"
                                        checked={limits.caviglie}
                                        onChange={(v) => setLimits({ ...limits, caviglie: v })}
                                    />
                                </div>

                                <label className="flex items-center gap-3">
                                    <input
                                        type="checkbox"
                                        className="size-5 rounded border-gray-300 accent-red-500"
                                        checked={specificCondition}
                                        onChange={(e) => setSpecificCondition(e.target.checked)}
                                    />
                                    <span className="text-sm font-semibold">
                                        Ho una condizione specifica (consigliata consulenza con un professionista)
                                    </span>
                                </label>
                            </div>
                        </Section>

                        {/* 6 Style */}
                        <Section id="section-style" icon="style" title="6. Preferenze di stile">
                            <div className="space-y-4">
                                <label className="block text-sm font-black text-gray-500 uppercase">Struttura della routine</label>
                                <div className="flex flex-col sm:flex-row gap-2">
                                    <SelectPillRadio name="split" value="full_body" selected={split === "full_body"} onChange={setSplit}>
                                        Full body
                                    </SelectPillRadio>
                                    <SelectPillRadio name="split" value="upper_lower" selected={split === "upper_lower"} onChange={setSplit}>
                                        Upper / Lower
                                    </SelectPillRadio>
                                    <SelectPillRadio name="split" value="ppl" selected={split === "ppl"} onChange={setSplit}>
                                        Push / Pull / Legs
                                    </SelectPillRadio>
                                </div>

                                <div className="pt-4">
                                    <label className="block text-sm font-black text-gray-500 uppercase mb-2">Preferenza cardio</label>
                                    <div className="flex gap-4 items-center flex-wrap">
                                        {[
                                            { key: "hiit", label: "HIIT" },
                                            { key: "liss", label: "LISS (steady)" },
                                            { key: "mix", label: "Mix" },
                                        ].map((c) => (
                                            <label key={c.key} className="inline-flex items-center gap-2 cursor-pointer font-semibold">
                                                <input
                                                    type="radio"
                                                    name="cardio"
                                                    className="accent-emerald-500"
                                                    checked={cardio === c.key}
                                                    onChange={() => setCardio(c.key)}
                                                />
                                                <span>{c.label}</span>
                                            </label>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </Section>

                        {/* 7 Intensity */}
                        <Section id="section-intensity" icon="speed" title="7. Intensità & mood">
                            <div className="space-y-8 px-1">
                                <div className="space-y-3">
                                    <div className="flex justify-between items-center gap-4">
                                        <label className="font-extrabold">Quanto vuoi spingere?</label>
                                        <span className="text-sm text-emerald-700 font-extrabold">
                                            {pushLevel === 1 ? "Rilassato" : pushLevel === 2 ? "Moderato" : "Alta intensità"}
                                        </span>
                                    </div>
                                    <input
                                        type="range"
                                        min={1}
                                        max={3}
                                        value={pushLevel}
                                        onChange={(e) => setPushLevel(Number(e.target.value))}
                                        className="w-full accent-emerald-500"
                                    />
                                    <div className="flex justify-between text-xs text-gray-400 uppercase font-black">
                                        <span>Rilassato</span>
                                        <span>Moderato</span>
                                        <span>Al massimo</span>
                                    </div>
                                </div>

                                <div className="space-y-3">
                                    <div className="flex justify-between items-center gap-4">
                                        <label className="font-extrabold">Tolleranza alla fatica (RPE)</label>
                                        <span className="text-sm text-emerald-700 font-extrabold">RPE {rpe}/10</span>
                                    </div>
                                    <input
                                        type="range"
                                        min={1}
                                        max={10}
                                        value={rpe}
                                        onChange={(e) => setRpe(Number(e.target.value))}
                                        className="w-full accent-emerald-500"
                                    />
                                    <div className="flex justify-between text-xs text-gray-400 uppercase font-black">
                                        <span>Bassa</span>
                                        <span>Molto alta</span>
                                    </div>
                                </div>
                            </div>
                        </Section>

                        {/* 8 Likes/Dislikes */}
                        <Section id="section-exercises" icon="thumbs_up_down" title="8. Mi piace / non mi piace">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-3">
                                    <label className="block text-sm font-black text-gray-500 uppercase">Mi piace…</label>
                                    <TagInput placeholder="Aggiungi esercizio..." tags={loves} setTags={setLoves} tone="green" />
                                </div>
                                <div className="space-y-3">
                                    <label className="block text-sm font-black text-gray-500 uppercase">Non voglio…</label>
                                    <TagInput placeholder="Aggiungi esercizio..." tags={hates} setTags={setHates} tone="red" />
                                </div>
                            </div>
                        </Section>

                        {/* 9 Monitoring */}
                        <Section id="section-monitoring" icon="watch" title="9. Monitoraggio">
                            <div className="divide-y divide-gray-100">
                                <div className="flex items-center justify-between py-4 gap-6">
                                    <div>
                                        <h4 className="font-extrabold">Sincronizzazione Apple Health / Google Fit</h4>
                                        <p className="text-sm text-gray-500">Sincronizza automaticamente battito e passi.</p>
                                    </div>
                                    <input type="checkbox" className="size-6 accent-emerald-500" checked={sync} onChange={(e) => setSync(e.target.checked)} />
                                </div>
                                <div className="flex items-center justify-between py-4 gap-6">
                                    <div>
                                        <h4 className="font-extrabold">Traccia ripetizioni & carichi</h4>
                                        <p className="text-sm text-gray-500">Registra manualmente serie e pesi durante l’allenamento.</p>
                                    </div>
                                    <input
                                        type="checkbox"
                                        className="size-6 accent-emerald-500"
                                        checked={trackSets}
                                        onChange={(e) => setTrackSets(e.target.checked)}
                                    />
                                </div>
                            </div>
                        </Section>

                        {/* 10 Constraints */}
                        <Section id="section-constraints" icon="block" title="10. Vincoli pratici">
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                <div className="space-y-3">
                                    <label className="font-extrabold">Rumore</label>
                                    <div className="flex gap-2">
                                        <SelectPillRadio name="noise" value="silent" selected={noise === "silent"} onChange={setNoise}>
                                            Silenzioso <span className="text-xs block text-gray-700/70 font-bold ml-2">no salti</span>
                                        </SelectPillRadio>
                                        <SelectPillRadio name="noise" value="normal" selected={noise === "normal"} onChange={setNoise}>
                                            Normale <span className="text-xs block text-gray-700/70 font-bold ml-2">ok rumore</span>
                                        </SelectPillRadio>
                                    </div>
                                </div>

                                <div className="space-y-3">
                                    <label className="font-extrabold">Spazio disponibile</label>
                                    <div className="flex gap-2">
                                        <SelectPillRadio name="space" value="mat" selected={space === "mat"} onChange={setSpace}>
                                            Tappetino
                                        </SelectPillRadio>
                                        <SelectPillRadio name="space" value="open_room" selected={space === "open_room"} onChange={setSpace}>
                                            Stanza libera
                                        </SelectPillRadio>
                                    </div>
                                </div>
                            </div>
                        </Section>
                    </div>

                    {/* Sticky CTA */}
                    <div className="fixed left-0 right-0 bottom-4 z-40 px-4">
                        <div className="max-w-[820px] mx-auto bg-white/90 backdrop-blur border border-gray-200 rounded-2xl shadow-lg p-4 flex items-center justify-between gap-6">
                            <div className="text-sm">
                                <p className="font-extrabold">{Math.min(10, completedCount)}/10 sezioni pronte</p>
                                <p className="text-gray-500">Generazione piano stimata: ~10s</p>
                            </div>
                            <button
                                type="button"
                                onClick={handleGenerate}
                                className="bg-emerald-400 hover:bg-emerald-500 text-[#111813] font-extrabold py-3 px-8 rounded-xl text-base shadow-md hover:shadow-lg transition"
                            >
                                Genera piano
                            </button>
                        </div>
                    </div>
                </main>
            </div>
        </div >
    );
}
