import Navbar from "../components/Navbar";
import { Link } from "react-router-dom";
import "../styles/pages/box.css";
import { useState } from "react";

export default function BoxSetup() {
    const [selectedBox, setSelectedBox] = useState(null);

    return (
        <div className="bg-[#f8fafc] min-h-screen text-[#0f172a] font-[Manrope]">
            <Navbar />

            <main className="max-w-6xl mx-auto px-6 py-10">
                <div className="mb-wrap">
                    <div className="mb-breadcrumbs">
                        <a href="#" className="mb-crumb">Profilo</a>
                        <span className="mb-sep">/</span>
                        <a href="#" className="mb-crumb">Nutrizione</a>
                        <span className="mb-sep">/</span>
                        <span className="mb-crumbActive">Impostazione Box</span>
                    </div>

                    <div className="mb-cols">
                        {/* LEFT */}
                        <section className="mb-left">
                            <div className="mb-hero">
                                <h1 className="mb-h1">
                                    Personalizza la tua Box <span className="mb-grad">selezionata dallo Chef</span>
                                </h1>
                                <p className="mb-sub">
                                    Abbiamo analizzato i tuoi bisogni nutrizionali. Ecco come i nostri chef costruiranno la tua settimana in base ai tuoi obiettivi.
                                </p>
                            </div>

                            <div className="mb-card">
                                <div className="mb-cardHead">
                                    <div className="mb-cardTitleRow">
                                        <span className="mb-icon" aria-hidden="true">🛡️</span>
                                        <h2 className="mb-h2">I tuoi vincoli alimentari</h2>
                                    </div>
                                    <button className="mb-linkBtn" type="button">
                                        Modifica preferenze <span aria-hidden="true">✎</span>
                                    </button>
                                </div>

                                <p className="mb-muted">
                                    Gli chef escluderanno rigorosamente quanto segue dai tuoi pasti.
                                </p>

                                <div className="mb-pillRow">
                                    <div className="tag tag--teal">
                                        <span className="mb-pillIcon" aria-hidden="true">✅</span>
                                        <span>Senza glutine</span>
                                    </div>
                                    <div className="tag tag--teal">
                                        <span className="mb-pillIcon" aria-hidden="true">✅</span>
                                        <span>No coriandolo</span>
                                    </div>
                                    <div className="tag tag--active">
                                        <span className="mb-pillIcon" aria-hidden="true">🏋️</span>
                                        <span>Obiettivo alto contenuto proteico</span>
                                    </div>
                                </div>
                            </div>

                            <div className="mb-chef">
                                <div
                                    className="mb-chefBg"
                                    style={{
                                        backgroundImage:
                                            "url('https://lh3.googleusercontent.com/aida-public/AB6AXuAQrUU50Zm24NfKGyLcjIvqioyhN3Pl-V5FPLk7aKMb1SQseNOmy2wsf9DdBS5kWLqX0a_HOb-zcxkefDYgeMqS10umpRJPGyPwPxqD8c_SywtIDsmlCrr9mTVZZcUQiWJ601UWXAk5QOt2u6xM0JX6a9W5ROy-P84hYXsgXYVYwRwsMN4i6CV-PZ9iPvw0uZLdVlSsUgiFi8lyRav5W6fjmbwoWM6YR73kR8J3QJZ6-cExKvrIH9mO4HZ3w4E7FJ0y1s4CL8rqDQ')",
                                    }}
                                    aria-hidden="true"
                                />
                                <div className="mb-chefOverlay" aria-hidden="true" />

                                <div className="mb-chefInner">
                                    <div className="mb-chefQuoteRow">
                                        <div className="mb-chefAvatar">
                                            <img
                                                alt="Chef Marcus"
                                                src="https://lh3.googleusercontent.com/aida-public/AB6AXuCuzJHWVhPUVxWInsc64ALBjoUdq8EDFB8PdItXwdjh63W-71lPzBu2toR8DQLDWW64PwMS7GXKNjZ45JbMDKpoJ5ueACRHqjhHcn5tKyYKCijyUFbKL3C9eb_jsPF46nsq_UWFoPwLZVI6Ww7YRNfTJOpZoquWlESTeHpua2hH3eAjrJcxohjbltrqQ33TiL-BaODAN3wi0WTefbNstILc8m2nzboCowLaghe4TNuT3ub-SNo4KQRi-S5s4AnrqoDtm50wAl3qVQ"
                                            />
                                        </div>

                                        <div>
                                            <p className="mb-quote">
                                                “Ho creato il menu di questa settimana per raggiungere i tuoi target proteici mantenendo varietà e sapori freschi. Il salmone al limone ed erbe è uno dei miei preferiti.”
                                            </p>
                                            <p className="mb-chefName">— Chef Marcus, Responsabile Nutrizione</p>
                                        </div>
                                    </div>

                                    <div className="mb-chefBadges">
                                        <div className="mb-chefBadge">
                                            <span aria-hidden="true">🌿</span>
                                            <span>Ingredienti freschi</span>
                                        </div>
                                        <div className="mb-chefBadge">
                                            <span aria-hidden="true">✔️</span>
                                            <span>Approvato da nutrizionista</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* RIGHT */}
                        <aside className="mb-right">
                            <div className="mb-card mb-card--shadow">
                                <div className="mb-boxHead">
                                    <div>
                                        <h3 className="mb-h3">La tua prossima Box</h3>
                                        <p className="mb-muted">Consegna per lunedì prossimo</p>
                                    </div>
                                </div>

                                <div className="mb-boxList">
                                    <div className="mb-boxItem">
                                        <div className="mb-boxIcon mb-boxIcon--green" aria-hidden="true">🍽️</div>
                                        <div>
                                            <div className="mb-boxTitle">5 cene selezionate dallo chef</div>
                                            <div className="mb-muted">Macro bilanciati, pronte in 15 minuti. Include le tue opzioni di pesce preferite.</div>
                                        </div>
                                    </div>

                                    <div className="mb-boxItem">
                                        <div className="mb-boxIcon mb-boxIcon--orange" aria-hidden="true">⚡</div>
                                        <div>
                                            <div className="mb-boxTitle">3 snack energizzanti</div>
                                            <div className="mb-muted">Carburante pre-allenamento pensato per performance elevate.</div>
                                        </div>
                                    </div>

                                    <div className="mb-boxItem">
                                        <div className="mb-boxIcon mb-boxIcon--purple" aria-hidden="true">🎁</div>
                                        <div>
                                            <div className="mb-boxTitle">1 sorpresa settimanale</div>
                                            <div className="mb-muted">Bevanda funzionale o dessert da provare.</div>
                                        </div>
                                    </div>
                                </div>

                                <div className="mb-total">
                                    <span className="mb-muted">Totale elementi</span>
                                    <span className="mb-totalNum">9</span>
                                </div>

                                <div className="mb-actions">
                                    <Link className="btn-primary" to="/box/pagamento" style={{ width: '100%', justifyContent: 'center' }}>
                                        Procedi alla consegna <span aria-hidden="true">→</span>
                                    </Link>

                                    <button className="btn-outline" type="button" style={{ width: '100%' }}>
                                        Vedi ricette di esempio
                                    </button>

                                    <p className="mb-footnote">Puoi mettere in pausa o saltare le settimane quando vuoi.</p>
                                </div>
                            </div>

                            <div className="mb-trust">
                                <div className="mb-trustItem"><span aria-hidden="true">🚚</span> Spedizione gratuita</div>
                                <div className="mb-trustItem"><span aria-hidden="true">♻️</span> Riciclabile</div>
                                <div className="mb-trustItem"><span aria-hidden="true">🏅</span> Rimborso garantito</div>
                            </div>
                        </aside>
                    </div>
                </div>
            </main>
        </div>
    );
}
