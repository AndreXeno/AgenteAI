import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import "../styles/shared.css";

/**
 * Training Dashboard (IT) - Pagina Allenamento
 * Da mostrare SOLO se l'utente ha già completato l'onboarding/piano.
 *
 * Gate:
 * - localStorage key: "mb_training_onboarding_done" === "1"
 * - Se non completato => mostra <TrainingOnboardingPlaceholder />
 *
 * Nota: in produzione meglio leggere questo flag da DB (Supabase) per utente.
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

// ... imports already there ...
// I will just remove the local Navbar function.
// Actually, previous edit might have failed to add import if I pasted full file content in previous thought but only partial in tool.
// Let's just remove the local Navbar function and ensure import is at top.

// Wait, I can't "ensure import is at top" easily with replace_file_content without viewing.
// But I added `import Navbar from "../components/Navbar";` in the previous call.
// The mistake was defining `function Navbar() {...}` inside.

// Strategy: Delete the local `function Navbar() {...}` block.


function TrainingOnboardingPlaceholder() {
    return (
        <div className="min-h-screen bg-[#f6f8f6]">
            <Navbar />

            <main className="max-w-4xl mx-auto px-4 md:px-10 py-10">
                <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm">
                    <h1 className="text-3xl font-black tracking-tight">Prima crea il tuo piano</h1>
                    <p className="text-gray-600 mt-2">
                        Sembra che tu non abbia ancora completato l’onboarding allenamento. Completa le preferenze per generare il piano.
                    </p>
                    <div className="mt-6 flex gap-3 flex-wrap">
                        <Link to="/training/setup" className="px-5 py-3 rounded-xl bg-emerald-400 hover:bg-emerald-500 text-[#102216] font-extrabold transition">
                            Vai al setup
                        </Link>
                        <Link to="/" className="px-5 py-3 rounded-xl border border-gray-200 font-bold hover:bg-gray-50 transition">
                            Torna alla dashboard
                        </Link>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default function TrainingDashboardPage() {
    const [hasPlan, setHasPlan] = useState(false);

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

    // Gate "ha già creato il piano"
    useEffect(() => {
        const v = localStorage.getItem(LS_KEY);
        setHasPlan(v === "1");
    }, []);

    // Dati demo (poi li sostituisci con API/DB)
    const userName = "Alex";

    const stats = useMemo(
        () => [
            { label: "Allenamenti", value: "3", delta: "+1 vs settimana scorsa", icon: "fitness_center" },
            { label: "Minuti attivi", value: "450", delta: "+12% vs settimana scorsa", icon: "timer" },
            { label: "Streak", value: "5 giorni", delta: "Continua così!", icon: "local_fire_department" },
        ],
        []
    );

    const nextWorkout = useMemo(
        () => ({
            tag: "Alta intensità",
            tagTone: "danger",
            category: "Parte superiore",
            title: "Upper Body Power",
            desc: "Focus su petto, spalle e tricipiti. Ti servono manubri e tappetino.",
            meta: [
                { icon: "schedule", text: "45 min" },
                { icon: "local_fire_department", text: "320 kcal" },
                { icon: "fitness_center", text: "Manubri" },
            ],
            image:
                'url("https://lh3.googleusercontent.com/aida-public/AB6AXuACFE65MKPBlyd0X-2KXe4TqPMkhHsqKvKd5iW2_Jg7eKGcKIaCTnlC5W1kEyOzMIJEbL5iPJ0GRcYsm08_R_WxBpMJTJrepy24372KxAmWdly6ODpAjW9k6PX1sy-7OjUM6bci96rUB_spp1t2EKulXdjauiNp2rP_m8rVLpKndNOSNKWkMvWF7sniFnnTlSKCL8vELUDF2NUGwYB1bgkepWAAAwLiM8GCXKdNOVqBRtbOISppVA73Erfm1xkAXhp-RZKPK14esg")',
        }),
        []
    );

    const previous = useMemo(
        () => [
            {
                icon: "directions_run",
                iconBg: "bg-blue-100 text-blue-600",
                title: "Corsa mattutina",
                subtitle: "Ieri • 07:00",
                rightTop: "5,2 km",
                rightBottom: "32 min",
            },
            {
                icon: "self_improvement",
                iconBg: "bg-orange-100 text-orange-600",
                title: "Vinyasa Flow",
                subtitle: "Lun 24 Ott • 18:30",
                rightTop: "180 kcal",
                rightBottom: "45 min",
            },
            {
                icon: "fitness_center",
                iconBg: "bg-purple-100 text-purple-600",
                title: "Leg Day Blast",
                subtitle: "Sab 22 Ott • 10:00",
                rightTop: "450 kcal",
                rightBottom: "60 min",
            },
        ],
        []
    );

    const trainerTip = useMemo(
        () => ({
            coach: "Coach Mike",
            role: "Personal Trainer",
            quote:
                "Non saltare il defaticamento! È essenziale per il recupero. Prova questa routine di stretching da 5 minuti dopo la sessione upper body.",
            coachImg:
                'url("https://lh3.googleusercontent.com/aida-public/AB6AXuBhwpjNvn6qrvPBpyvtHIGlD6aQT_YtW0npFKF-5WMYHZDc5euxlrFFz7IG-62Lwpz9PIC_179knUf7ja6YMD0wV_crc6NZ0Uc-_3zNh5W1d3brCrr5Lv4g8x06lJJzSU9EvDTcqCH-CEXgk6EUFk33fKm_IWAlnq1w-_r-FsCTwd3tHfFjzqMDIvxI0obFsyW3Wd_6y3VmToKagu77xnPGI2vz5RSO48rQH9WncCzFwvuwVLakkeM4ck3Vk2EYOfk2Iq4gVUZGTA")',
        }),
        []
    );

    const friends = useMemo(
        () => [
            {
                name: "Sarah Jenkins",
                time: "2 min fa",
                line: (
                    <>
                        Ha completato <span className="text-[#111813] font-semibold">HIIT Cardio</span>
                    </>
                ),
                avatar:
                    'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDZ5EBManQhK4y-JDHHeafFyIMWLE5vvU8HI_lZED35UJJPU7EHW-Ax3vC-6AgkQI02GuL_TJL8wLdfj4og7DqZiPtxTsHkkDC2dSEAJ5F0WdZvFlXnH4F9ZNx_PaohoyAiU6l_9E_dBncBzTy1wrp9UZ77RF6JKhbUh2gwq39OkAFI62B_sea0Q3x49L9yw1UhbuL_30SiHhcjcME62bEqoIZuMZ9HGLkl45MpJx335gDyEyvEZJfScob-Oz5Y3uKyTX5nmKrPEw")',
                online: true,
                action: true,
            },
            {
                name: "David Chen",
                time: "1h fa",
                line: (
                    <>
                        Ha ottenuto il badge: <span className="text-orange-500 font-semibold">Early Bird</span> 🏆
                    </>
                ),
                avatar:
                    'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAhaGre_g7FMKw3HwrEjF2Cmy9ufOupuCCPTeKOimmUu35la34nBFgAbmB9FLzhu4sRZpp8HWeNAgOUsqlj42OtBDclhKv_a_QzOinVvb3dU1FCQW-bTpD5gftOdfBTG4un1-fzrPVQZe3K8PrzpcDdKZpWe8_aZa_i73F7iRdxtTX2baNHR26uJKOx9p6zU33Rhd4SGhB3wbTl5EWN4nHktecSsXI5SGNpy8lFLf6wuQEXxDQ-rNEokixv-TjV9ux7KoOKA4CN2w")',
                online: false,
                action: false,
            },
            {
                name: "Elena Rodriguez",
                time: "3h fa",
                line: <>Ha finito una corsa da 5 km</>,
                avatar:
                    'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCSdQYzzGWcCCPlHN-Zq8uqOQYa_GyxBPQyZeHZMS_q-Q1fkFNfbQfboBqxGDy_paKPyQr6UfJSpQdK2UQiCyjKthGfdiGqiRxEWChJRVFsY9GUjDzwOyVAMHkw_dS3KQObyPw2584Rm6CWp2vTn-ItPjEb65KvKNdkr5_nsXxT7BiBZA69JzNfW1QZQuPS8p7tSDRXcvYDoHOAtO4zha6NajCXkXbZ_DHKS0S6e0uc78Ebx5sIkcGRKq6UnSiXepgIbI1VhRhU-A")',
                online: false,
                action: false,
            },
        ],
        []
    );

    if (!hasPlan) return <TrainingOnboardingPlaceholder />;

    return (
        <div className="min-h-screen flex flex-col bg-[#f6f8f6] text-[#111813] selection:bg-emerald-400 selection:text-black">
            <Navbar />

            {/* MAIN */}
            <main className="flex-1 w-full max-w-7xl mx-auto px-4 md:px-10 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* LEFT */}
                    <div className="lg:col-span-8 flex flex-col gap-8">
                        <div className="flex flex-col gap-2">
                            <h1 className="text-4xl font-black tracking-tight">Dashboard Allenamento</h1>
                            <p className="text-[#61896f] text-lg">Pronto a spaccare oggi, {userName}?</p>
                        </div>

                        {/* Stats */}
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            {stats.map((s) => (
                                <div
                                    key={s.label}
                                    className="flex flex-col gap-2 rounded-2xl p-5 bg-white border border-[#f0f4f2] shadow-sm"
                                >
                                    <div className="flex items-center justify-between">
                                        <p className="text-[#61896f] text-sm font-semibold">{s.label}</p>
                                        <MaterialIcon name={s.icon} className="text-emerald-400 text-xl" />
                                    </div>
                                    <p className="text-3xl font-extrabold">{s.value}</p>
                                    <p className="text-[#078829] text-sm font-semibold">{s.delta}</p>
                                </div>
                            ))}
                        </div>

                        {/* Next Workout */}
                        <div className="flex flex-col gap-4">
                            <h3 className="text-xl font-extrabold">Prossimo allenamento</h3>

                            <div className="bg-white rounded-2xl shadow-sm border border-[#f0f4f2] overflow-hidden flex flex-col md:flex-row group cursor-pointer transition hover:shadow-md">
                                <div
                                    className="w-full md:w-2/5 aspect-video md:aspect-auto bg-cover bg-center relative"
                                    style={{ backgroundImage: nextWorkout.image }}
                                    aria-label="Immagine allenamento"
                                >
                                    <div className="absolute inset-0 bg-black/10 group-hover:bg-black/0 transition-colors" />
                                    <div className="absolute bottom-3 left-3 bg-white/90 backdrop-blur-sm px-2 py-1 rounded text-xs font-black uppercase tracking-wider">
                                        {nextWorkout.category}
                                    </div>
                                </div>

                                <div className="flex-1 p-6 flex flex-col justify-center">
                                    <div className="flex items-start justify-between mb-2 gap-3">
                                        <h4 className="text-2xl font-extrabold leading-tight">{nextWorkout.title}</h4>
                                        <span className="bg-red-100 text-red-700 text-xs px-2 py-1 rounded-lg font-black whitespace-nowrap">
                                            {nextWorkout.tag}
                                        </span>
                                    </div>
                                    <p className="text-[#61896f] mb-6">{nextWorkout.desc}</p>

                                    <div className="flex flex-wrap items-center gap-6 text-sm text-gray-700 font-semibold mb-6">
                                        {nextWorkout.meta.map((m) => (
                                            <div key={m.text} className="flex items-center gap-1.5">
                                                <MaterialIcon name={m.icon} className="text-lg" />
                                                {m.text}
                                            </div>
                                        ))}
                                    </div>

                                    <Link
                                        to="/training/session"
                                        className="w-full md:w-auto bg-emerald-400 hover:bg-[#0fd650] text-[#0a2815] font-extrabold py-3 px-6 rounded-xl flex items-center justify-center gap-2 transition"
                                        style={{ textDecoration: 'none' }}
                                    >
                                        <MaterialIcon name="play_arrow" />
                                        Avvia allenamento
                                    </Link>
                                </div>
                            </div>
                        </div>

                        {/* Previous workouts */}
                        <div className="flex flex-col gap-4">
                            <div className="flex items-center justify-between">
                                <h3 className="text-xl font-extrabold">Allenamenti precedenti</h3>
                                <a className="text-emerald-600 text-sm font-extrabold hover:underline" href="#">
                                    Vedi tutti
                                </a>
                            </div>

                            <div className="bg-white rounded-2xl border border-[#f0f4f2] divide-y divide-[#f0f4f2] overflow-hidden">
                                {previous.map((w) => (
                                    <div key={w.title} className="p-4 flex items-center gap-4 hover:bg-[#f6f8f6] transition">
                                        <div className={cn("size-12 rounded-xl flex items-center justify-center shrink-0", w.iconBg)}>
                                            <MaterialIcon name={w.icon} />
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className="font-extrabold truncate">{w.title}</p>
                                            <p className="text-[#61896f] text-sm">{w.subtitle}</p>
                                        </div>
                                        <div className="text-right shrink-0">
                                            <p className="font-extrabold">{w.rightTop}</p>
                                            <p className="text-[#61896f] text-sm">{w.rightBottom}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* RIGHT */}
                    <div className="lg:col-span-4 flex flex-col gap-8">
                        {/* Trainer tips */}
                        <div className="flex flex-col gap-4">
                            <h3 className="text-xl font-extrabold">Consigli del coach</h3>

                            <div className="bg-gradient-to-br from-[#102216] to-[#1a3a25] rounded-2xl p-5 text-white shadow-md relative overflow-hidden">
                                <div className="absolute -right-4 -top-4 w-24 h-24 bg-emerald-400/20 rounded-full blur-xl" />
                                <div className="flex items-center gap-3 mb-4 relative z-10">
                                    <div
                                        className="size-12 rounded-full border-2 border-emerald-400 bg-cover bg-center"
                                        style={{ backgroundImage: trainerTip.coachImg }}
                                        aria-label="Avatar coach"
                                    />
                                    <div>
                                        <p className="font-extrabold text-sm">{trainerTip.coach}</p>
                                        <p className="text-emerald-300 text-xs font-semibold uppercase tracking-wider">{trainerTip.role}</p>
                                    </div>
                                </div>

                                <p className="text-sm text-gray-200 mb-4 leading-relaxed relative z-10">“{trainerTip.quote}”</p>

                                <button
                                    type="button"
                                    className="w-full bg-white/10 hover:bg-white/20 border border-white/20 text-white text-sm font-semibold py-2.5 rounded-xl transition relative z-10 flex items-center justify-center gap-2"
                                >
                                    <MaterialIcon name="play_circle" className="text-lg" />
                                    Vedi routine
                                </button>
                            </div>
                        </div>

                        {/* Friends activity */}
                        <div className="flex flex-col gap-4">
                            <div className="flex items-center justify-between">
                                <h3 className="text-xl font-extrabold">Attività amici</h3>
                                <div className="flex -space-x-2">
                                    <div
                                        className="size-6 rounded-full border border-white bg-cover bg-center"
                                        style={{
                                            backgroundImage:
                                                'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAvEKl-80ftfv3AIuoj0f3HNWrhyMiuM4COfi7XtS2R7l4GhPE0hMn8bfi63yuTdMGP6XgqsyisrKq3g7_xrFh8IYJ9nGc8BVHXSfrSafRpr6-2cl3v5sok4S23uhkVkpGMl_Bl80L3GKKcA6F_QXFahwy4jPHTx4I7uvhVmOcDJtGIbO9U3Yu7kcu-qUvtzdr6s3T92pXAE74TMivFCgMSHnlz67iHNNUkK95B7VW9udR3t8P3VrLnlkCeJ-sXIYORF23yVbsZzw")',
                                        }}
                                        aria-label="Avatar amico 1"
                                    />
                                    <div
                                        className="size-6 rounded-full border border-white bg-cover bg-center"
                                        style={{
                                            backgroundImage:
                                                'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAwSwglL4b-ATuT5RXQdF934w1xkSL-FYi7i02w0-hosGImFhX0n8iPS29xlXgftevdsO9nUCz6q1U6LnNtJuIHh3vNQpIMKqdFTRoYoTyKejQhksbOOK0L9sQvoZUweJOnq-otbi5psxxRdvhwjP3Z39JziBuRiKpCNfGpIT_YIPak6oNXoEF1q_k1LPgi59vjbk0dQBdKplPPAaPyioDhr2MpDIwRoUh7lelN3gZuriwrgXRLzfGj_nvKhH2ccgd79iU0P2acGw")',
                                        }}
                                        aria-label="Avatar amico 2"
                                    />
                                    <div className="size-6 rounded-full border border-white bg-gray-100 flex items-center justify-center text-[10px] font-black text-gray-500">
                                        +12
                                    </div>
                                </div>
                            </div>

                            <div className="bg-white rounded-2xl border border-[#f0f4f2] p-4 flex flex-col gap-5">
                                {friends.map((f, idx) => (
                                    <React.Fragment key={f.name}>
                                        <div className="flex gap-3">
                                            <div className="relative">
                                                <div
                                                    className="size-10 rounded-full bg-cover bg-center"
                                                    style={{ backgroundImage: f.avatar }}
                                                    aria-label={`Avatar ${f.name}`}
                                                />
                                                {f.online ? (
                                                    <div className="absolute -bottom-1 -right-1 bg-green-500 size-3 rounded-full border-2 border-white" />
                                                ) : null}
                                            </div>

                                            <div className="flex-1">
                                                <div className="flex justify-between items-start gap-3">
                                                    <p className="text-sm font-extrabold">{f.name}</p>
                                                    <span className="text-xs text-[#61896f]">{f.time}</span>
                                                </div>
                                                <p className="text-xs text-[#61896f] mt-0.5">{f.line}</p>

                                                {f.action ? (
                                                    <div className="mt-2 flex gap-2">
                                                        <button
                                                            type="button"
                                                            className="text-xs font-extrabold text-emerald-700 bg-emerald-100 hover:bg-emerald-200 px-2 py-1 rounded-lg transition"
                                                        >
                                                            👏 Incoraggia
                                                        </button>
                                                    </div>
                                                ) : null}
                                            </div>
                                        </div>

                                        {idx !== friends.length - 1 ? <hr className="border-[#f0f4f2]" /> : null}
                                    </React.Fragment>
                                ))}

                                <button
                                    type="button"
                                    className="w-full mt-2 text-sm text-[#61896f] hover:text-[#111813] font-semibold py-2 rounded-xl hover:bg-gray-50 transition"
                                >
                                    Vedi tutta l’attività
                                </button>
                            </div>
                        </div>

                        {/* Dev-only: reset onboarding */}
                        <div className="rounded-2xl border border-gray-200 bg-white p-4">
                            <p className="text-sm font-extrabold">Debug</p>
                            <p className="text-xs text-gray-500 mt-1">
                                Reset rapido per rivedere il setup (solo dev).
                            </p>
                            <button
                                type="button"
                                onClick={() => {
                                    localStorage.removeItem(LS_KEY);
                                    setHasPlan(false);
                                }}
                                className="mt-3 w-full rounded-xl border border-gray-200 py-2.5 font-extrabold hover:bg-gray-50 transition"
                            >
                                Reset onboarding
                            </button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
