import React from 'react';
import Navbar from "../components/Navbar";

export default function HomePage() {
    return (
        <div className="min-h-screen bg-[#F6FAF9] font-[Manrope] text-[#0F172A]">
            <Navbar />

            <main className="max-w-7xl mx-auto px-6 py-8 flex flex-col gap-12">
                <section className="mb-heroCard">
                    <img
                        className="mb-heroImg"
                        src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2400&q=80"
                        alt="Paesaggio"
                    />
                    <div className="mb-overlay" />

                    <div className="mb-heroContent">
                        <h1 className="mb-title">
                            Il tuo percorso verso una vita
                            <br />
                            equilibrata
                        </h1>

                        <p className="mb-subtitle">
                            Unifica nutrizione, allenamento e benessere mentale con piani alimentari
                            personalizzati, programmi di allenamento su misura e supporto psicologico.
                        </p>
                    </div>
                </section>
            </main>
        </div>
    );
}
