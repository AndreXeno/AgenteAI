import React from 'react';
import Navbar from "../components/Navbar";
import { SrLayout } from "../components/Shared/SrComponents";

export default function HomePage() {
    return (
        <div className="bg-[#F6FAF9] font-[Manrope] text-[#0F172A] min-h-screen flex flex-col">
            <Navbar />

            <SrLayout>
                <section className="sr-hero">
                    <img
                        className="sr-heroImg"
                        src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2400&q=80"
                        alt="Paesaggio"
                    />
                    <div className="sr-overlay">
                        <h1 className="sr-heroTitle">
                            Il tuo percorso verso una vita
                            <br />
                            equilibrata
                        </h1>

                        <p className="sr-heroSub">
                            Unifica nutrizione, allenamento e benessere mentale con piani alimentari
                            personalizzati, programmi di allenamento su misura e supporto psicologico.
                        </p>
                    </div>
                </section>

                {/* Add a quick features grid to make use of the space better */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '32px', marginTop: '40px' }}>
                    <div className="sr-card" style={{ marginBottom: 0 }}>
                        <h3 className="sr-h3">🥗 Nutrizione</h3>
                        <p className="sr-sub" style={{ marginTop: '12px', fontSize: '16px' }}>Piani alimentari su misura per i tuoi obiettivi.</p>
                    </div>
                    <div className="sr-card" style={{ marginBottom: 0 }}>
                        <h3 className="sr-h3">💪 Allenamento</h3>
                        <p className="sr-sub" style={{ marginTop: '12px', fontSize: '16px' }}>Schede di allenamento personalizzate.</p>
                    </div>
                    <div className="sr-card" style={{ marginBottom: 0 }}>
                        <h3 className="sr-h3">🧘 Mental</h3>
                        <p className="sr-sub" style={{ marginTop: '12px', fontSize: '16px' }}>Supporto psicologico e tracciamento umore.</p>
                    </div>
                </div>

            </SrLayout>
        </div>
    );
}
