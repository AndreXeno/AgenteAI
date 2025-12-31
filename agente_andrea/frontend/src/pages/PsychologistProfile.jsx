import React from 'react';
import { Link, useParams } from 'react-router-dom';
import "../styles/pages/therapist.css";

const DAYS = ["Lu", "Ma", "Me", "Gi", "Ve", "Sa", "Do"];

// Calendario “statico” come mockup (Giugno 2024 con 30 giorni)
function AvailabilityCard() {
    const blanks = 3; // per far iniziare “1” sotto “Gi” come nello screenshot
    const days = Array.from({ length: 30 }, (_, i) => i + 1);

    return (
        <aside className="tp-card tp-card--pad">
            <div className="tp-cardHead">
                <div className="tp-cardTitle">Disponibilità</div>
                <div className="tp-cardMeta">Giugno 2024</div>
            </div>

            <div className="tp-cal">
                {DAYS.map((d) => (
                    <div className="tp-calDow" key={d}>{d}</div>
                ))}

                {Array.from({ length: blanks }).map((_, i) => (
                    <div className="tp-calEmpty" key={`e-${i}`} />
                ))}

                {days.map((n) => (
                    <div className="tp-calDay" key={n}>{n}</div>
                ))}
            </div>
        </aside>
    );
}

function ContactCard({ id }) {
    return (
        <aside className="tp-card tp-card--pad tp-contactCard">
            <div className="tp-contactTitle">Hai dubbi?</div>
            <div className="tp-contactSub">Invia un messaggio a Dr Sharma.</div>
            <Link to={`/psychologist/${id}/contact`}>
                <button className="btn-outline" style={{ width: '100%' }}>Contattami</button>
            </Link>
        </aside>
    );
}

function Pill({ children, tone = "blue" }) {
    return <span className={`tag tag--${tone}`}>{children}</span>;
}

function CheckItem({ children }) {
    return (
        <div className="tp-checkItem">
            <span className="tp-check" aria-hidden="true">✓</span>
            <span className="tp-checkText">{children}</span>
        </div>
    );
}

function Review({ name, text }) {
    return (
        <div className="tp-review">
            <div className="tp-reviewTop">
                <div className="tp-reviewAvatar" aria-hidden="true">👤</div>
                <div className="tp-reviewInfo">
                    <div className="tp-reviewName">{name}</div>
                    <div className="tp-stars" aria-label="5 stelle">
                        {"★★★★★"}
                    </div>
                </div>
            </div>
            <p className="tp-reviewText">“{text}”</p>
        </div>
    );
}


export default function PsychologistProfile() {
    const { id } = useParams(); // Should contain 'anika-sharma'

    return (
        <div className="tp-page">
            <Navbar />

            <main className="tp-main">
                <div className="tp-grid">
                    {/* LEFT COLUMN */}
                    <section className="tp-left">
                        {/* Profile header card */}
                        <div className="tp-card tp-profileCard">
                            <div className="tp-profileTop">
                                <div className="tp-photoWrap">
                                    <img
                                        className="tp-photo"
                                        src="https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80"
                                        alt="Dr. Anika Sharma"
                                    />
                                    <span className="tp-onlineDot" aria-hidden="true" />
                                </div>

                                <div className="tp-profileInfo">
                                    <h1 className="tp-name">Dr. Anika Sharma</h1>
                                    <div className="tp-role">
                                        Psicologa Autorizzata e Coach della Performance Mentale
                                    </div>

                                    <div className="tp-pills">
                                        <Pill tone="blue">Ansia</Pill>
                                        <Pill tone="purple">Gestione dello Stress</Pill>
                                        <Pill tone="pink">Relazioni</Pill>
                                    </div>

                                    <button className="btn-outline">Prenota Sessione</button>
                                </div>
                            </div>

                            <div className="tp-section">
                                <h2 className="tp-h2">Chi Sono</h2>
                                <p className="tp-par">
                                    Con oltre 12 anni di esperienza clinica e sul campo, sono specializzata nella
                                    psicofisiologia della prestazione e nel supporto ad atleti che affrontano blocchi mentali,
                                    cali prestazionali o il burnout atletico. Il mio approccio integra protocolli
                                    cognitivo-comportamentali con tecniche avanzate di mental training, focalizzate sulla
                                    gestione dei fattori psicologici che influenzano l'allenamento e la gara. Lavoro a stretto
                                    contatto con l'atleta per identificare le barriere cognitive che inibiscono la costanza e
                                    per riattivare la motivazione intrinseca, trasformando l'ansia pre-agonistica in arousal
                                    funzionale. Credo che una mente ben strutturata sia la base della disciplina fisica:
                                    aiuto i miei pazienti a sviluppare strategie di regolazione emotiva e focus attentivo,
                                    strumenti indispensabili per ritrovare la spinta agonistica e raggiungere il Peak
                                    Performance in modo sostenibile.
                                </p>
                            </div>
                        </div>

                        {/* Approcci terapeutici */}
                        <div className="tp-card tp-card--pad">
                            <h2 className="tp-h2">Approcci Terapeutici</h2>

                            <div className="tp-approaches">
                                <CheckItem>Terapia Cognitivo Comportamentale (CBT)</CheckItem>
                                <CheckItem>Riduzione dello Stress Basata sulla Mindfulness (MBSR) per il Focus Competitivo</CheckItem>
                                <CheckItem>Terapia Focalizzata sulle Emozioni (EFT) per la Resilienza al Burnout</CheckItem>
                                <CheckItem>
                                    Terapia Breve Focalizzata sulla Soluzione (SFBT) per la Riacquisizione della Spinta
                                    all'Allenamento
                                </CheckItem>
                            </div>
                        </div>

                        {/* Recensioni */}
                        <div className="tp-card tp-card--pad">
                            <h2 className="tp-h2">Recensioni dei Pazienti</h2>

                            <div className="tp-reviews">
                                <Review
                                    name="Sarah L."
                                    text="La Dr.ssa Sharma ha creato un ambiente accogliente e non giudicante. La sua guida è stata inestimabile nell'aiutarmi a gestire la mia ansia. La raccomando vivamente."
                                />
                                <div className="tp-divider" />
                                <Review
                                    name="Mark T."
                                    text="Lavorare con la Dr.ssa Sharma è stata un'esperienza trasformativa. Le sue intuizioni sulla gestione dello stress hanno migliorato significativamente il mio equilibrio vita–lavoro."
                                />
                            </div>
                        </div>
                    </section>

                    {/* RIGHT COLUMN */}
                    <aside className="tp-rightCol">
                        <AvailabilityCard />
                        <ContactCard id={id || 'anika-sharma'} />
                    </aside>
                </div>
            </main>
        </div>
    );
}
