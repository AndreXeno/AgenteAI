import { useEffect, useMemo, useRef, useState } from "react";
import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import "../styles/pages/chat.css";

/**
 * FUTURO (chat reale):
 * - Sostituisci `sendMessage()` e `useEffect` con chiamate REST + WebSocket/SSE.
 * - Tieni `conversationId` in URL (React Router) o in state globale.
 * - Salva i messaggi in DB: { id, conversationId, sender, text, createdAt }.
 */

const MOCK_THERAPIST = {
    id: "therapist_anika",
    name: "Dr. Anika Sharma",
    status: "Online",
    avatarUrl:
        "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=260&q=80",
};

const MOCK_SIDEBAR = {
    nextSession: {
        title: "Seduta di Terapia",
        when: "Domani, 10:00",
        meta: "45 min · Videochiamata",
    },
    profile: {
        about:
            "Specializzata nel recupero della motivazione atletica, gestione del sovraccarico mentale e superamento dei plateau di forza. La Dr. Sharma utilizza un approccio cognitivo per aiutarti a ristrutturare il tuo rapporto con la performance e la motivazione intrinseca all'allenamento.",
        tariff: "120 €/seduta",
        experience: "12 Anni",
        languages: "Inglese, Italiano",
    },
    sharedFile: {
        name: "Esercizi_Ristrutturazione_Cognitiva...",
        meta: "2.4 MB · 24 Giu",
    },
};

// Local Navbar removed. Importing shared Navbar.

function IconBtn({ label, children }) {
    return (
        <button className="tc-iconBtn" type="button" aria-label={label}>
            {children}
        </button>
    );
}

function MessageBubble({ msg }) {
    const isUser = msg.sender === "user";
    return (
        <div className={`tc-msgRow ${isUser ? "is-user" : "is-therapist"}`}>
            {!isUser && (
                <div className="tc-miniAvatar" aria-hidden="true">
                    <img src={MOCK_THERAPIST.avatarUrl} alt="" />
                </div>
            )}

            <div className="tc-bubbleWrap">
                <div className={`tc-bubble ${isUser ? "tc-bubble--user" : "tc-bubble--therapist"}`}>
                    {msg.text}
                </div>
                <div className={`tc-time ${isUser ? "tc-time--user" : ""}`}>
                    {formatTime(msg.createdAt)}
                </div>
            </div>

            {isUser && <div className="tc-userMarker" aria-hidden="true" />}
        </div>
    );
}

function TypingIndicator() {
    return (
        <div className="tc-msgRow is-therapist">
            <div className="tc-miniAvatar" aria-hidden="true">
                <img src={MOCK_THERAPIST.avatarUrl} alt="" />
            </div>
            <div className="tc-typingBubble" aria-label="Sta scrivendo">
                <span className="tc-dot" />
                <span className="tc-dot" />
                <span className="tc-dot" />
            </div>
        </div>
    );
}

function RightPanel() {
    return (
        <aside className="tc-side">
            <section className="tc-card tc-cardPad">
                <div className="tc-cardHead">
                    <div className="tc-cardTitle">Prossima Sessione</div>
                    <a className="tc-cardLink" href="#tutte">Vedi tutte</a>
                </div>

                <div className="tc-sessionBox">
                    <div className="tc-sessionIcon" aria-hidden="true">📅</div>
                    <div>
                        <div className="tc-sessionTitle">{MOCK_SIDEBAR.nextSession.title}</div>
                        <div className="tc-sessionMeta">
                            {MOCK_SIDEBAR.nextSession.when}
                            <br />
                            {MOCK_SIDEBAR.nextSession.meta}
                        </div>
                    </div>
                </div>

                <button className="tc-outlineBtn" type="button">Riprogramma</button>
            </section>

            <section className="tc-card tc-cardPad">
                <div className="tc-profTitle">{MOCK_THERAPIST.name}</div>
                <p className="tc-profText">{MOCK_SIDEBAR.profile.about}</p>

                <div className="tc-profGrid">
                    <div className="tc-k">Tariffa</div>
                    <div className="tc-v">{MOCK_SIDEBAR.profile.tariff}</div>

                    <div className="tc-k">Esperienza</div>
                    <div className="tc-v">{MOCK_SIDEBAR.profile.experience}</div>

                    <div className="tc-k">Lingue</div>
                    <div className="tc-v">{MOCK_SIDEBAR.profile.languages}</div>
                </div>

                <div className="tc-divider" />

                <div className="tc-filesTitle">File Condivisi</div>
                <div className="tc-fileRow">
                    <div className="tc-fileIcon" aria-hidden="true">📄</div>
                    <div>
                        <div className="tc-fileName">{MOCK_SIDEBAR.sharedFile.name}</div>
                        <div className="tc-fileMeta">{MOCK_SIDEBAR.sharedFile.meta}</div>
                    </div>
                </div>
            </section>
        </aside>
    );
}

function formatTime(iso) {
    try {
        const d = new Date(iso);
        return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    } catch {
        return "";
    }
}

export default function ContactPsychologist() {
    // In futuro: arriva da router (es. /therapists/:id/chat?conversationId=...)
    const therapist = MOCK_THERAPIST;

    // Messaggi iniziali mock (in futuro: fetch dal backend)
    const [messages, setMessages] = useState(() => [
        {
            id: "m1",
            sender: "therapist",
            text:
                "Ciao! Ho visto che ultimamente stai vivendo un calo importante di motivazione all'allenamento. Come ti senti riguardo a questa fase di stallo?",
            createdAt: new Date(Date.now() - 6 * 60 * 1000).toISOString(),
        },
        {
            id: "m2",
            sender: "user",
            text:
                "Salve Dr. Sharma. Sono bloccato. Non riesco più a sollevare gli stessi pesi di una volta e questo mi ha tolto completamente la voglia di andare in palestra.",
            createdAt: new Date(Date.now() - 3 * 60 * 1000).toISOString(),
        },
        {
            id: "m3",
            sender: "therapist",
            text:
                "Capisco perfettamente. Questa non è solo una frustrazione fisica, ma un vero e proprio blocco cognitivo legato alla performance attesa. Quali sono i pensieri dominanti quando fallisci un carico che prima gestivi?",
            createdAt: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
        },
        {
            id: "m4",
            sender: "user",
            text:
                "Penso di aver perso tutto e che non tornerò mai più al mio livello. A quel punto, mi chiedo perché allenarmi. 😓",
            createdAt: new Date(Date.now() - 1 * 60 * 1000).toISOString(),
        },
    ]);

    const [input, setInput] = useState("");
    const [isTyping, setIsTyping] = useState(false);

    const listRef = useRef(null);

    // Auto-scroll a fine chat
    useEffect(() => {
        const el = listRef.current;
        if (!el) return;
        el.scrollTop = el.scrollHeight;
    }, [messages, isTyping]);

    // ✅ Simulazione risposta psicologo (DEMO)
    // In futuro: rimuovi e usa websocket/eventi dal backend
    async function simulateTherapistReply(userText) {
        setIsTyping(true);
        await new Promise((r) => setTimeout(r, 900));

        setMessages((prev) => [
            ...prev,
            {
                id: crypto.randomUUID(),
                sender: "therapist",
                text:
                    "Grazie per averlo detto in modo così chiaro. Proviamo a distinguere tra “prestazione oggi” e “identità personale”: quando pensi “ho perso tutto”, cosa ti stai dicendo su di te come atleta/persona?",
                createdAt: new Date().toISOString(),
            },
        ]);

        setIsTyping(false);
    }

    // ✅ Punto di integrazione futura
    async function sendMessage(text) {
        // FUTURO:
        // 1) POST /api/conversations/:id/messages  (salva messaggio utente)
        // 2) WS/SSE per ricevere messaggi therapist in realtime
        // 3) gestione errori + retry
        setMessages((prev) => [
            ...prev,
            {
                id: crypto.randomUUID(),
                sender: "user",
                text,
                createdAt: new Date().toISOString(),
            },
        ]);

        // Demo reply
        await simulateTherapistReply(text);
    }

    async function onSubmit(e) {
        e.preventDefault();
        const text = input.trim();
        if (!text) return;
        setInput("");
        await sendMessage(text);
    }

    const headerTitle = useMemo(() => therapist.name, [therapist.name]);

    return (
        <div className="tc-page">
            <Navbar />

            <main className="tc-main">
                <div className="tc-layout">
                    {/* LEFT: CHAT */}
                    <section className="tc-chatCard">
                        <div className="tc-chatHeader">
                            <div className="tc-headerLeft">
                                <div className="tc-headerAvatar">
                                    <img src={therapist.avatarUrl} alt={therapist.name} />
                                    <span className="tc-onlineDot" aria-hidden="true" />
                                </div>
                                <div>
                                    <div className="tc-headerName">{headerTitle}</div>
                                    <div className="tc-headerStatus">{therapist.status}</div>
                                </div>
                            </div>

                            <div className="tc-headerActions">
                                <IconBtn label="Chiama">📞</IconBtn>
                                <IconBtn label="Videochiamata">📹</IconBtn>
                                <IconBtn label="Altro">⋮</IconBtn>
                            </div>
                        </div>

                        <div className="tc-chatBody" ref={listRef}>
                            {messages.map((m) => (
                                <MessageBubble key={m.id} msg={m} />
                            ))}
                            {isTyping && <TypingIndicator />}
                        </div>

                        <form className="tc-inputBar" onSubmit={onSubmit}>
                            <button className="tc-plusBtn" type="button" aria-label="Aggiungi allegato">
                                +
                            </button>

                            <input
                                className="tc-input"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Scrivi il tuo messaggio..."
                                aria-label="Scrivi il tuo messaggio"
                            />

                            <button className="tc-sendBtn" type="submit" aria-label="Invia">
                                ➤
                            </button>
                        </form>
                    </section>

                    {/* RIGHT: PANELS */}
                    <RightPanel />
                </div>
            </main>
        </div>
    );
}
