import React, { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";

/**
 * Mind&Body - Sessione Allenamento (IT)
 * - React + Tailwind classes
 * - Dark UI (come HTML originale)
 * - Timer sessione + timer recupero + log set
 * - Sidebar istruzioni + "Prossimi"
 * - Barra progresso fissa in basso
 *
 * NOTE:
 * - In produzione: dati da API/DB (piano utente, esercizi, serie target, ecc.)
 * - Qui: demo stateful e funzionante (timer base).
 */

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

function pad2(n) {
    const x = Math.max(0, Math.floor(n));
    return x < 10 ? `0${x}` : `${x}`;
}
function formatMMSS(totalSeconds) {
    const m = Math.floor(totalSeconds / 60);
    const s = totalSeconds % 60;
    return `${pad2(m)}:${pad2(s)}`;
}

export default function WorkoutSessionPage() {
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

    // Forza dark mode su <html class="dark">
    useEffect(() => {
        document.documentElement.classList.add("dark");
        return () => document.documentElement.classList.remove("dark");
    }, []);

    // ---- Demo data ----
    const workoutHeader = useMemo(
        () => ({
            title: "Leg Day",
            week: "Settimana 4",
        }),
        []
    );

    const exercise = useMemo(
        () => ({
            setLabel: "Serie 2 di 4",
            tag: "Multiarticolare",
            name: "Back Squat con bilanciere",
            target: "Obiettivo: 10 ripetizioni @ 61 kg", // tradotto da 135 lbs (circa)
            media:
                'url("https://lh3.googleusercontent.com/aida-public/AB6AXuBD-LBZdbu4s_SN-GUJ9a38Id7TqevYc0F4_d3hi2PCa2S5-qTm9T84FvXtVxRFL4c5drIaV5hnQVn0m3F_GyzW38_vBC4NmUewX4SKwzDdS54CpQssL5Ut7_L-KLFyEVxegZEGx5ac6e9jpKmWGds9f3qDhuwxFhkLUqlc26AOSUszo3AhSBK5sUBr-bxce9B5XI4ebrgD2fhnTKwyp0z1rqFGFa1vsbQi-ndn1f6_7_F_1WKY5b6CcAE0l7OOTxtu4-rNYbhjLA")',
        }),
        []
    );

    const instructions = useMemo(
        () => [
            "Posizionati con i piedi alla larghezza delle spalle, punte leggermente verso l’esterno.",
            "Contrai l’addome e tieni il petto alto per tutta la durata del movimento.",
            "Scendi portando anche indietro e in basso finché le cosce sono parallele al pavimento.",
            "Spingi sui talloni per tornare alla posizione iniziale.",
        ],
        []
    );

    const proTip =
        "Evita che le ginocchia collassino verso l’interno mentre risali.";

    const upNext = useMemo(
        () => [
            {
                name: "Affondi camminati",
                meta: "3 serie • 12 ripetizioni",
                img:
                    'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDB6JfZ9Xgv78ivkLi0w4btbSZz3naeDpgEcF-fUY2D8vuU9Ol-xbgPYF8Bh6VQ0KvoOugRyuYQWPjpoWhiKpFwDmk6EbiYibjBpNt9Xf5FhEmBcq4_6G0RnNRl8_G3Dv-tN7Zhm6Bkvs1EKD6tAftJrag_fhdCphZ9ERmAvTHqZA7w0XjbFqXwNXW_p8y-TAxygjlRGXguXLOsxinSd14X9DBjb6SF4W0xHspRUlmdk572Qwgxi9LMHYamnnSSe_swQda93CM4Yg")',
                active: true,
            },
            {
                name: "Leg Press",
                meta: "4 serie • 10 ripetizioni",
                img:
                    'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCNgf8DGqrSMOY_6guwb3P83C97lquSsUqR18KiLa1ONOJSa1oEaBhNC25tU7QPFWHoyzsHwfgtNiYLG26_nLESkCZDGQWJ_psQkNN8dokSSxUIxFE5STfrILrjMUCsChQim1JpO3Qkpba3e3KH7gV3SeiOx2KfPe_H_RGUa723cg5yfrQm9Q0Sv8v9YqWff1gHNI_xkJQb1t7JhAM_uRFxXcLHR4pkPk0ua6TSAmb1wwO0t7crcm1cHeE-HDVDyZsT9GrVlTjHWQ")',
                active: false,
            },
        ],
        []
    );

    // ---- Timers ----
    const [sessionSeconds, setSessionSeconds] = useState(14 * 60 + 20); // 14:20 demo
    const [restSeconds, setRestSeconds] = useState(45);
    const [restRunning, setRestRunning] = useState(true);

    // Session timer always running (demo)
    useEffect(() => {
        const t = setInterval(() => setSessionSeconds((s) => s + 1), 1000);
        return () => clearInterval(t);
    }, []);

    // Rest timer
    useEffect(() => {
        if (!restRunning) return;
        if (restSeconds <= 0) return;

        const t = setInterval(() => {
            setRestSeconds((s) => (s > 0 ? s - 1 : 0));
        }, 1000);

        return () => clearInterval(t);
    }, [restRunning, restSeconds]);

    // ---- Log set inputs ----
    const [weightKg, setWeightKg] = useState(61);
    const [reps, setReps] = useState(10);

    const restProgressPct = useMemo(() => {
        // barra da 0..100 basata su 100s "virtuali" (per demo)
        const max = 100;
        const v = Math.min(max, Math.max(0, restSeconds));
        return Math.round((v / max) * 100);
    }, [restSeconds]);

    // ---- Bottom progress ----
    const [exerciseIndex, setExerciseIndex] = useState(3);
    const [exerciseTotal] = useState(10);

    const progressPct = useMemo(() => {
        const p = Math.round((exerciseIndex / exerciseTotal) * 100);
        return Math.min(100, Math.max(0, p));
    }, [exerciseIndex, exerciseTotal]);

    // ---- Actions (stub) ----
    const onEndWorkout = () => {
        // TODO: salva sessione, naviga a riepilogo
        alert("Allenamento terminato (demo).");
    };

    const onPrevExercise = () => {
        setExerciseIndex((x) => Math.max(1, x - 1));
    };

    const onNextExercise = () => {
        setExerciseIndex((x) => Math.min(exerciseTotal, x + 1));
    };

    const onCompleteSet = () => {
        // TODO: salva log set (peso/reps) + avanzamento serie
        alert(`Serie completata: ${reps} reps @ ${weightKg} kg (demo).`);
        setRestSeconds(60); // reset recupero demo
        setRestRunning(true);
    };

    // ---- Simple custom scrollbar (optional) ----
    // Se hai Tailwind global, puoi spostarlo in CSS globale:
    // .no-scrollbar::-webkit-scrollbar{display:none} ecc.
    useEffect(() => {
        const styleId = "mb-workout-scrollbar";
        if (document.getElementById(styleId)) return;
        const style = document.createElement("style");
        style.id = styleId;
        style.textContent = `
      ::-webkit-scrollbar { width: 8px; }
      ::-webkit-scrollbar-track { background: #102216; }
      ::-webkit-scrollbar-thumb { background: #28392e; border-radius: 4px; }
      ::-webkit-scrollbar-thumb:hover { background: #3b5443; }
      .no-scrollbar::-webkit-scrollbar { display:none; }
      .no-scrollbar { -ms-overflow-style:none; scrollbar-width:none; }
    `;
        document.head.appendChild(style);
    }, []);

    return (
        <div className="min-h-screen flex flex-col overflow-hidden bg-[#f6f8f6] dark:bg-[#102216] font-[Manrope] text-slate-900 dark:text-white">
            {/* TOP BAR - Unified Navbar */}
            <div className="bg-white dark:bg-[#102216]">
                <Navbar />
            </div>

            {/* SESSION CONTROLS BAR (Moved from original header) */}
            <div className="shrink-0 z-20 bg-white dark:bg-[#102216] border-b border-gray-200 dark:border-[#28392e] px-6 lg:px-10 py-3 flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="flex flex-col">
                        {/* Title was in header previously */}
                        <h2 className="text-lg font-extrabold tracking-tight">Sessione in corso</h2>
                        <span className="text-xs text-gray-500 dark:text-[#9db9a6] font-semibold">
                            {workoutHeader.title} — {workoutHeader.week}
                        </span>
                    </div>
                </div>

                {/* Timer sessione */}
                <div className="hidden md:flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-[#1c2b21] rounded-full border border-gray-200 dark:border-[#28392e]">
                    <MaterialIcon name="timer" className="text-gray-500 dark:text-[#9db9a6] text-sm" />
                    <span className="text-sm font-extrabold tabular-nums">{formatMMSS(sessionSeconds)}</span>
                </div>

                <Link
                    to="/training"
                    className="h-10 px-4 rounded-xl border border-red-500/20 bg-red-500/10 hover:bg-red-500/20 text-red-600 dark:text-red-400 font-extrabold text-sm flex items-center gap-2 transition"
                >
                    <MaterialIcon name="logout" className="text-lg" />
                    Termina
                </Link>
            </div>

            {/* MAIN LAYOUT */}
            <main className="flex-1 flex flex-col lg:flex-row overflow-hidden relative">
                {/* LEFT (focus) */}
                <section className="flex-1 flex flex-col h-full overflow-y-auto no-scrollbar">
                    <div className="p-6 lg:p-10 max-w-5xl mx-auto w-full pb-32 flex flex-col gap-6">
                        {/* Heading */}
                        <div className="flex flex-wrap items-end justify-between gap-4">
                            <div>
                                <div className="flex items-center gap-2 mb-2">
                                    <span className="px-2 py-0.5 rounded text-xs font-black bg-emerald-400 text-[#102216] uppercase tracking-wider">
                                        {exercise.setLabel}
                                    </span>
                                    <span className="px-2 py-0.5 rounded text-xs font-black bg-gray-200 dark:bg-[#28392e] text-gray-600 dark:text-gray-300 uppercase tracking-wider">
                                        {exercise.tag}
                                    </span>
                                </div>
                                <h1 className="text-3xl lg:text-4xl font-black tracking-tight">{exercise.name}</h1>
                                <p className="text-gray-500 dark:text-gray-300 mt-1 flex items-center gap-1">
                                    <MaterialIcon name="fitness_center" className="text-sm" />
                                    {exercise.target}
                                </p>
                            </div>

                            <div className="flex gap-2">
                                <button
                                    type="button"
                                    onClick={onPrevExercise}
                                    className="size-10 rounded-full bg-gray-200 dark:bg-[#28392e] hover:bg-gray-300 dark:hover:bg-[#3b5443] transition flex items-center justify-center"
                                    title="Esercizio precedente"
                                >
                                    <MaterialIcon name="skip_previous" />
                                </button>
                                <button
                                    type="button"
                                    onClick={onNextExercise}
                                    className="size-10 rounded-full bg-gray-200 dark:bg-[#28392e] hover:bg-gray-300 dark:hover:bg-[#3b5443] transition flex items-center justify-center"
                                    title="Salta / prossimo esercizio"
                                >
                                    <MaterialIcon name="skip_next" />
                                </button>
                            </div>
                        </div>

                        {/* Media */}
                        <div className="relative w-full aspect-video bg-black rounded-2xl overflow-hidden group shadow-2xl shadow-black/50 border border-gray-800 dark:border-[#28392e]">
                            <div
                                className="absolute inset-0 bg-cover bg-center opacity-80"
                                style={{ backgroundImage: exercise.media }}
                                aria-label="Media esercizio"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
                            <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between">
                                <button
                                    type="button"
                                    className="flex items-center gap-2 bg-white/10 hover:bg-white/20 backdrop-blur-md px-3 py-1.5 rounded-lg text-white text-sm font-semibold transition border border-white/10"
                                >
                                    <MaterialIcon name="play_circle" className="text-lg" />
                                    Guarda tutorial
                                </button>
                                <button
                                    type="button"
                                    className="p-2 bg-white/10 hover:bg-white/20 backdrop-blur-md rounded-lg text-white transition border border-white/10"
                                    aria-label="Audio"
                                >
                                    <MaterialIcon name="volume_up" className="text-lg" />
                                </button>
                            </div>
                        </div>

                        {/* Timer + Log */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-2">
                            {/* Rest timer */}
                            <div className="bg-white dark:bg-[#1c2b21] rounded-2xl p-6 border border-gray-200 dark:border-[#28392e] shadow-sm flex flex-col justify-between items-center gap-4 relative overflow-hidden">
                                <div className="absolute top-0 left-0 w-full h-1 bg-gray-200 dark:bg-[#28392e]">
                                    <div className="h-full bg-emerald-400" style={{ width: `${restProgressPct}%` }} />
                                </div>

                                <h3 className="text-sm font-black uppercase tracking-widest text-gray-500 dark:text-[#9db9a6] mt-2">
                                    Timer recupero
                                </h3>

                                <div className="text-6xl font-black tabular-nums tracking-tighter">
                                    {formatMMSS(restSeconds)}
                                </div>

                                <div className="flex gap-3 w-full">
                                    <button
                                        type="button"
                                        onClick={() => setRestSeconds((s) => s + 10)}
                                        className="flex-1 py-3 rounded-xl bg-gray-100 dark:bg-[#28392e] font-extrabold hover:bg-gray-200 dark:hover:bg-[#3b5443] transition flex items-center justify-center gap-2"
                                    >
                                        <MaterialIcon name="add_circle" />
                                        +10s
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setRestRunning((r) => !r)}
                                        className="flex-1 py-3 rounded-xl bg-gray-100 dark:bg-[#28392e] font-extrabold hover:bg-gray-200 dark:hover:bg-[#3b5443] transition flex items-center justify-center gap-2"
                                    >
                                        <MaterialIcon name={restRunning ? "pause" : "play_arrow"} />
                                        {restRunning ? "Pausa" : "Riprendi"}
                                    </button>
                                </div>
                            </div>

                            {/* Log set */}
                            <div className="bg-white dark:bg-[#1c2b21] rounded-2xl p-6 border border-gray-200 dark:border-[#28392e] shadow-sm flex flex-col gap-4">
                                <div className="flex justify-between items-center">
                                    <h3 className="text-sm font-black uppercase tracking-widest text-gray-500 dark:text-[#9db9a6]">
                                        Registra serie
                                    </h3>
                                    <button type="button" className="text-emerald-400 text-sm font-extrabold hover:underline">
                                        Storico
                                    </button>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    {/* Peso */}
                                    <div className="space-y-1">
                                        <label className="text-xs text-gray-500 dark:text-gray-300 font-semibold">
                                            Peso (kg)
                                        </label>
                                        <div className="relative">
                                            <input
                                                className="w-full bg-gray-50 dark:bg-[#102216] border border-gray-200 dark:border-[#28392e] rounded-xl px-4 py-3 text-xl font-black focus:ring-2 focus:ring-emerald-400 focus:border-transparent outline-none text-center"
                                                type="number"
                                                value={weightKg}
                                                onChange={(e) => setWeightKg(Number(e.target.value))}
                                            />
                                            <div className="absolute inset-y-0 right-0 flex flex-col border-l border-gray-200 dark:border-[#28392e]">
                                                <button
                                                    type="button"
                                                    onClick={() => setWeightKg((w) => w + 1)}
                                                    className="flex-1 px-2 hover:bg-gray-200 dark:hover:bg-[#28392e] rounded-tr-xl text-gray-400 hover:text-white"
                                                    aria-label="Aumenta peso"
                                                >
                                                    <MaterialIcon name="arrow_drop_up" className="text-sm" />
                                                </button>
                                                <button
                                                    type="button"
                                                    onClick={() => setWeightKg((w) => Math.max(0, w - 1))}
                                                    className="flex-1 px-2 hover:bg-gray-200 dark:hover:bg-[#28392e] rounded-br-xl text-gray-400 hover:text-white"
                                                    aria-label="Diminuisci peso"
                                                >
                                                    <MaterialIcon name="arrow_drop_down" className="text-sm" />
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Reps */}
                                    <div className="space-y-1">
                                        <label className="text-xs text-gray-500 dark:text-gray-300 font-semibold">
                                            Ripetizioni
                                        </label>
                                        <div className="relative">
                                            <input
                                                className="w-full bg-gray-50 dark:bg-[#102216] border border-gray-200 dark:border-[#28392e] rounded-xl px-4 py-3 text-xl font-black focus:ring-2 focus:ring-emerald-400 focus:border-transparent outline-none text-center"
                                                type="number"
                                                value={reps}
                                                onChange={(e) => setReps(Number(e.target.value))}
                                            />
                                            <div className="absolute inset-y-0 right-0 flex flex-col border-l border-gray-200 dark:border-[#28392e]">
                                                <button
                                                    type="button"
                                                    onClick={() => setReps((r) => r + 1)}
                                                    className="flex-1 px-2 hover:bg-gray-200 dark:hover:bg-[#28392e] rounded-tr-xl text-gray-400 hover:text-white"
                                                    aria-label="Aumenta ripetizioni"
                                                >
                                                    <MaterialIcon name="arrow_drop_up" className="text-sm" />
                                                </button>
                                                <button
                                                    type="button"
                                                    onClick={() => setReps((r) => Math.max(0, r - 1))}
                                                    className="flex-1 px-2 hover:bg-gray-200 dark:hover:bg-[#28392e] rounded-br-xl text-gray-400 hover:text-white"
                                                    aria-label="Diminuisci ripetizioni"
                                                >
                                                    <MaterialIcon name="arrow_drop_down" className="text-sm" />
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <button
                                    type="button"
                                    onClick={onCompleteSet}
                                    className="w-full mt-auto bg-emerald-400 hover:bg-emerald-300 text-[#102216] text-lg font-black py-3.5 rounded-xl shadow-lg shadow-emerald-400/20 transition flex items-center justify-center gap-2"
                                >
                                    <MaterialIcon name="check_circle" />
                                    Completa serie
                                </button>
                            </div>
                        </div>
                    </div>
                </section>

                {/* RIGHT SIDEBAR */}
                <aside className="w-full lg:w-96 bg-white dark:bg-[#0d1c12] border-l border-gray-200 dark:border-[#28392e] flex flex-col h-full overflow-y-auto z-10">
                    <div className="p-6 space-y-8">
                        {/* Instructions */}
                        <div className="space-y-4">
                            <h3 className="text-lg font-extrabold flex items-center gap-2">
                                <MaterialIcon name="info" className="text-emerald-400" />
                                Istruzioni
                            </h3>

                            <div className="space-y-4 text-sm text-gray-600 dark:text-gray-200 leading-relaxed">
                                {instructions.map((txt, idx) => (
                                    <div key={idx} className="flex gap-3">
                                        <span className="flex-shrink-0 size-6 rounded-full bg-gray-100 dark:bg-[#1c2b21] text-xs font-black flex items-center justify-center border border-gray-200 dark:border-[#28392e]">
                                            {idx + 1}
                                        </span>
                                        <p>{txt}</p>
                                    </div>
                                ))}
                            </div>

                            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-xl border border-blue-100 dark:border-blue-900/50">
                                <p className="text-xs text-blue-800 dark:text-blue-200 font-semibold flex gap-2">
                                    <MaterialIcon name="lightbulb" className="text-sm" />
                                    <span>
                                        <strong>Consiglio pro:</strong> {proTip}
                                    </span>
                                </p>
                            </div>
                        </div>

                        <div className="h-px bg-gray-200 dark:bg-[#28392e]" />

                        {/* Up Next */}
                        <div className="space-y-4">
                            <h3 className="text-sm font-black uppercase tracking-widest text-gray-500 dark:text-[#9db9a6]">
                                Prossimi
                            </h3>

                            {upNext.map((x) => (
                                <button
                                    key={x.name}
                                    type="button"
                                    className={cn(
                                        "w-full text-left group rounded-xl p-3 flex gap-3 items-center border transition",
                                        "bg-gray-50 dark:bg-[#1c2b21] border-transparent hover:border-emerald-400/50",
                                        x.active ? "" : "opacity-60 hover:opacity-100"
                                    )}
                                >
                                    <div
                                        className="size-16 rounded-lg bg-gray-200 dark:bg-[#28392e] bg-cover bg-center flex-shrink-0"
                                        style={{ backgroundImage: x.img }}
                                        aria-label={`Anteprima ${x.name}`}
                                    />
                                    <div className="flex flex-col">
                                        <span className="text-sm font-extrabold text-slate-900 dark:text-white group-hover:text-emerald-400 transition">
                                            {x.name}
                                        </span>
                                        <span className="text-xs text-gray-500 dark:text-gray-300">{x.meta}</span>
                                    </div>
                                    {x.active ? (
                                        <MaterialIcon
                                            name="arrow_forward"
                                            className="ml-auto text-gray-400 group-hover:text-emerald-400"
                                        />
                                    ) : null}
                                </button>
                            ))}
                        </div>
                    </div>
                </aside>
            </main>

            {/* BOTTOM PROGRESS */}
            <footer className="fixed bottom-0 left-0 right-0 z-50 bg-white dark:bg-[#1c2b21] border-t border-gray-200 dark:border-[#28392e] p-4">
                <div className="max-w-[1920px] mx-auto flex flex-col md:flex-row gap-4 items-center justify-between px-4 lg:px-6">
                    <div className="flex-1 w-full md:w-auto">
                        <div className="flex justify-between mb-2">
                            <p className="text-sm font-extrabold">
                                Esercizio {exerciseIndex} di {exerciseTotal}
                            </p>
                            <p className="text-emerald-400 text-sm font-extrabold">{progressPct}%</p>
                        </div>

                        <div className="h-2.5 w-full bg-gray-200 dark:bg-[#3b5443] rounded-full overflow-hidden">
                            <div
                                className="h-full bg-emerald-400 rounded-full transition-all duration-500 ease-out shadow-[0_0_10px_#13ec5b]"
                                style={{ width: `${progressPct}%` }}
                            />
                        </div>
                    </div>

                    <div className="hidden md:flex items-center gap-6 text-sm font-semibold text-gray-500 dark:text-gray-300">
                        <div className="flex items-center gap-2">
                            <MaterialIcon name="local_fire_department" className="text-emerald-400 text-lg" />
                            <span>320 kcal bruciate</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <MaterialIcon name="monitor_heart" className="text-emerald-400 text-lg" />
                            <span>124 BPM</span>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
}
