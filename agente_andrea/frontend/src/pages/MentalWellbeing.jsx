import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Navbar from "../components/Navbar";
import "../styles/pages/mental-wellbeing.css";

const MentalWellbeing = () => {
    const [messages, setMessages] = useState([
        { id: 'welcome', sender: 'bot', text: 'Ciao! Sono qui per supportarti. Se hai pensieri che ti preoccupano o vuoi semplicemente parlare, sono in ascolto.' }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputValue.trim()) return;

        const userMsg = { id: Date.now(), sender: 'user', text: inputValue };
        setMessages(prev => [...prev, userMsg]);
        setInputValue('');
        setIsLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg.text, username: 'guest' })
            });
            const data = await response.json();

            const botMsg = { id: Date.now() + 1, sender: 'bot', text: data.response };
            setMessages(prev => [...prev, botMsg]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, { id: Date.now() + 1, sender: 'bot', text: 'Mi dispiace, si è verificato un errore di connessione.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="mbw-page">
            <Navbar />

            <main className="mbw-main">
                <div className="mbw-hero">
                    <h1 className="mbw-title">Il tuo spazio sicuro</h1>
                    <p className="mbw-subtitle">Monitora il tuo benessere e connettiti con esperti.</p>
                </div>

                <div className="mbw-moodCard">
                    <div>
                        <h2 className="mbw-moodTitle">Come ti senti oggi?</h2>
                        <p className="mbw-moodSub">L'autoconsapevolezza è il primo passo.</p>
                    </div>
                    <Link to="/diary">
                        <button className="mbw-primaryBtn">
                            <span className="mbw-primaryIcon">+</span> Registra Umore
                        </button>
                    </Link>
                </div>

                <section className="mbw-section">
                    <div className="mbw-sectionHeader">
                        <div>
                            <h2 className="mbw-sectionTitle">I nostri specialisti</h2>
                            <p className="mbw-sectionSub">Prenota o chatta con psicologi certificati</p>
                        </div>
                        <a href="#" className="mbw-seeAll">Vedi tutti</a>
                    </div>

                    <div className="mbw-grid">
                        <div className="mb-therapistCard">
                            <div className="mb-therapistTop">
                                <div className="mb-avatar">
                                    <span className="mb-avatarIcon">👩‍⚕️</span>
                                </div>
                                <div>
                                    <h3 className="mb-therapistName">Dr. Anika Sharma</h3>
                                    <p className="mb-therapistRole">Psicologa Sportiva</p>
                                    <div className="mb-rating">
                                        <span className="mb-star">★</span> 4.9 <span className="mb-ratingMeta">(120 recensioni)</span>
                                    </div>
                                </div>
                            </div>
                            <div className="mb-chips">
                                <span className="mb-chip mb-chip--blue">Ansia</span>
                                <span className="mb-chip mb-chip--purple">Performance</span>
                            </div>
                            <Link to="/psychologist/anika-sharma">
                                <button className="mb-outlineBtn">Contatta</button>
                            </Link>
                        </div>
                    </div>
                </section>

                <section className="mb-chatCard">
                    <div className="mb-chatHeader">
                        <div>
                            <Link to="/chat" style={{ textDecoration: 'none', color: 'inherit' }}>
                                <div className="mb-chatTitle" style={{ cursor: 'pointer' }}>AI Assistant ↗</div>
                            </Link>
                            <div className="mb-chatSubtitle">Sempre disponibile per ascoltarti</div>
                        </div>
                        <div className="mb-online">
                            <span className="mb-dot"></span> Online
                        </div>
                    </div>
                    <div className="mb-chatBody">
                        {messages.map((msg) => (
                            <div key={msg.id} className={`mb-bubbleRow ${msg.sender === 'user' ? 'mb-user' : ''}`}>
                                {msg.sender === 'bot' && (
                                    <div className="mb-botAvatar">🤖</div>
                                )}
                                <div className={`mb-bubble ${msg.sender === 'user' ? 'mb-bubble-user' : 'mb-bubble-bot'}`}>
                                    {msg.text}
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="mb-bubbleRow">
                                <div className="mb-botAvatar">🤖</div>
                                <div className="mb-bubble mb-bubble-bot">
                                    Sta scrivendo...
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                    <form className="mb-chatInputBar" onSubmit={handleSendMessage}>
                        <input
                            type="text"
                            className="mb-chatInput"
                            placeholder="Scrivi qui..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                        />
                    </form>
                </section>
            </main>
        </div>
    );
};

export default MentalWellbeing;
