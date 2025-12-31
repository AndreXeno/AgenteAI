import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

const AIChat = () => {
    const [messages, setMessages] = useState([
        { id: 'welcome', sender: 'bot', text: 'Ciao! Sono Mind&Body, il tuo coach personale. Come posso aiutarti oggi?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const chatContainerRef = useRef(null);

    const scrollToBottom = () => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async () => {
        if (!input.trim()) return;

        const userMsg = { id: Date.now(), sender: 'user', text: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
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
            console.error('Error:', error);
            setMessages(prev => [...prev, { id: Date.now() + 1, sender: 'bot', text: 'Mi dispiace, si è verificato un errore di connessione.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    };

    return (
        <div className="bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-200 h-screen flex flex-col font-sans">
            <div className="bg-white">
                <Navbar />
            </div>

            <main className="flex-1 container mx-auto p-4 flex flex-col max-w-4xl">
                <div
                    ref={chatContainerRef}
                    className="flex-1 overflow-y-auto p-4 space-y-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm mb-4"
                    style={{ height: 'calc(100vh - 180px)' }}
                >
                    {messages.map((msg) => (
                        <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`p-3 rounded-lg max-w-[80%] ${msg.sender === 'user'
                                ? 'bg-blue-100 dark:bg-blue-200 text-black rounded-tr-none'
                                : 'bg-gray-100 dark:bg-gray-200 text-black rounded-tl-none'
                                }`}>
                                <p dangerouslySetInnerHTML={{
                                    __html: msg.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')
                                }} />
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="flex justify-start">
                            <div className="bg-gray-100 dark:bg-gray-200 text-black p-3 rounded-lg rounded-tl-none">
                                <p>Sta scrivendo...</p>
                            </div>
                        </div>
                    )}
                </div>

                <div className="flex space-x-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        className="flex-1 p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-400"
                        placeholder="Scrivi un messaggio..."
                    />
                    <button
                        onClick={handleSendMessage}
                        className="bg-teal-400 hover:bg-teal-500 text-white font-bold py-3 px-6 rounded-lg transition-colors cursor-pointer"
                    >
                        Invia
                    </button>
                </div>
            </main>
        </div>
    );
};

export default AIChat;
