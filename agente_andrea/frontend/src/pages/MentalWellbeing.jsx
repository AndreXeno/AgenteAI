import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Navbar from "../components/Navbar";
import {
    SrLayout,
    SrCard,
    SrButton,
    SrSectionHead,
    SrGrid,
    SrBadge
} from "../components/Shared/SrComponents";


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

            <SrLayout>
                <div style={{ marginBottom: '40px' }}>
                    <h1 className="sr-h1">Il tuo spazio sicuro</h1>
                    <p className="sr-sub">Monitora il tuo benessere e connettiti con esperti.</p>
                </div>

                <div style={{ marginBottom: '40px' }}>
                    <SrCard
                        className="mbw-moodCard"
                        title="Come ti senti oggi?"
                        subtitle="L'autoconsapevolezza è il primo passo."
                        action={
                            <Link to="/diary">
                                <SrButton variant="cta" style={{ boxShadow: '0 4px 14px 0 rgba(16, 185, 129, 0.39)' }}>
                                    <span style={{ marginRight: '8px', fontSize: '20px' }}>+</span> Registra Umore
                                </SrButton>
                            </Link>
                        }
                    />
                </div>

                <SrSectionHead
                    title="I nostri specialisti"
                    subtitle="Prenota o chatta con psicologi certificati"
                    action={<a href="#" className="sr-linkBtn">Vedi tutti</a>}
                    className="mbw-section"
                />

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '32px', marginBottom: '48px' }}>
                    {/* Therapists */}
                    <SrCard>
                        <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
                            <div style={{ fontSize: '32px', background: '#f1f5f9', width: '60px', height: '60px', display: 'grid', placeItems: 'center', borderRadius: '50%' }}>
                                👩‍⚕️
                            </div>
                            <div>
                                <h3 style={{ margin: '0 0 4px', fontSize: '18px' }}>Dr. Anika Sharma</h3>
                                <p style={{ margin: 0, color: 'var(--muted)', fontSize: '14px' }}>Psicologa Sportiva</p>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '8px', fontSize: '14px', fontWeight: 600 }}>
                                    <span style={{ color: '#F59E0B' }}>★</span> 4.9 <span style={{ color: 'var(--muted)', fontWeight: 400 }}>(120 recensioni)</span>
                                </div>
                            </div>
                        </div>
                        <div style={{ display: 'flex', gap: '8px', marginBottom: '24px' }}>
                            <SrBadge style={{ background: '#DBEAFE', color: '#1E40AF' }}>Ansia</SrBadge>
                            <SrBadge style={{ background: '#F3E8FF', color: '#6B21A8' }}>Performance</SrBadge>
                        </div>
                        <Link to="/psychologist/anika-sharma">
                            <SrButton variant="ghost" style={{ width: '100%' }}>Contatta</SrButton>
                        </Link>
                    </SrCard>

                    <SrCard>
                        <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
                            <div style={{ fontSize: '32px', background: '#fffbeb', width: '60px', height: '60px', display: 'grid', placeItems: 'center', borderRadius: '50%' }}>
                                👨‍⚕️
                            </div>
                            <div>
                                <h3 style={{ margin: '0 0 4px', fontSize: '18px' }}>Dr. Marco Rossi</h3>
                                <p style={{ margin: 0, color: 'var(--muted)', fontSize: '14px' }}>Psicoterapeuta Cognitivo</p>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '8px', fontSize: '14px', fontWeight: 600 }}>
                                    <span style={{ color: '#F59E0B' }}>★</span> 4.8 <span style={{ color: 'var(--muted)', fontWeight: 400 }}>(98 recensioni)</span>
                                </div>
                            </div>
                        </div>
                        <div style={{ display: 'flex', gap: '8px', marginBottom: '24px' }}>
                            <SrBadge style={{ background: '#dcfce7', color: '#166534' }}>Stress</SrBadge>
                            <SrBadge style={{ background: '#ffedd5', color: '#9a3412' }}>Burnout</SrBadge>
                        </div>
                        <SrButton variant="ghost" style={{ width: '100%' }}>Contatta</SrButton>
                    </SrCard>
                </div>

                {/* Chat AI Section - Moved to bottom and full width */}
                <h2 className="sr-h1" style={{ fontSize: '32px', marginBottom: '24px' }}>AI Assistant</h2>
                <SrCard className="sr-card" style={{ padding: 0, overflow: 'hidden' }}>
                    <div style={{ padding: '24px 24px 0' }}>
                        <div className="sr-cardHead">
                            <div>
                                <h3 className="sr-h3">Chat Integrata ✨</h3>
                                <p className="sr-sub" style={{ fontSize: '14px', marginTop: '4px' }}>Parla liberamente, sono qui per ascoltarti.</p>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 700, color: '#10B981', background: 'rgba(16, 185, 129, 0.1)', padding: '4px 10px', borderRadius: '999px' }}>
                                <span style={{ width: '6px', height: '6px', background: '#10B981', borderRadius: '50%' }}></span> Online
                            </div>
                        </div>
                    </div>

                    <div style={{ padding: '0 24px 24px' }}>
                        <div className="sr-chatContainer" style={{ height: '500px' }}> {/* Increased height for full page feel */}
                            {messages.map((msg) => (
                                <div key={msg.id} className={`sr-chatBubbleRow ${msg.sender === 'user' ? 'sr-user' : ''}`}>
                                    {msg.sender === 'bot' && (
                                        <div className="sr-chatAvatar">🤖</div>
                                    )}
                                    <div className={`sr-chatBubble ${msg.sender === 'user' ? 'sr-user' : 'sr-bot'}`}>
                                        {msg.text}
                                    </div>
                                </div>
                            ))}
                            {isLoading && (
                                <div className="sr-chatBubbleRow">
                                    <div className="sr-chatAvatar">🤖</div>
                                    <div className="sr-chatBubble sr-bot">
                                        <span className="animate-pulse">...</span>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        <form className="sr-chatInputBar" onSubmit={handleSendMessage} style={{ padding: '12px' }}>
                            <input
                                type="text"
                                className="sr-chatInput"
                                placeholder="Scrivi qui il tuo pensiero..."
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                style={{ fontSize: '18px' }}
                            />
                            <SrButton type="submit" variant="dark" style={{ padding: '14px 32px', borderRadius: '14px', fontSize: '16px' }}>
                                Invia messaggio
                            </SrButton>
                        </form>
                    </div>
                </SrCard>

            </SrLayout>
        </div>
    );
};

export default MentalWellbeing;
