import { Link } from "react-router-dom";
import { useState } from "react";
import "../styles/pages/box.css";
import "../styles/pages/payment.css";

import Navbar from '../components/Navbar';

export default function PaymentDetails() {
    const [method, setMethod] = useState("card");

    return (
        <div className="bg-[#f6faf9] min-h-screen font-[Manrope] text-[#0f172a]">
            <Navbar />

            <main className="max-w-5xl mx-auto px-6 py-12">
                <div className="mb-wrap">
                    <div className="pay-head">
                        <div className="pay-step">
                            <span>Pagamento</span>
                            <span className="pay-stepSep" aria-hidden="true">›</span>
                            <span>Step 3 di 3</span>
                        </div>

                        <h1 className="pay-h1">Dettagli di pagamento</h1>
                        <p className="mb-muted">
                            Scegli un metodo di pagamento per finalizzare la tua box benessere personalizzata.
                        </p>
                    </div>

                    <div className="pay-grid">
                        {/* LEFT */}
                        <section className="pay-left">
                            <div className="pay-tabs">
                                <button
                                    className={`pay-tab ${method === "card" ? "is-active" : ""}`}
                                    onClick={() => setMethod("card")}
                                    type="button"
                                >
                                    <span aria-hidden="true">💳</span>
                                    <span>Carta</span>
                                </button>

                                <button
                                    className={`pay-tab ${method === "paypal" ? "is-active" : ""}`}
                                    onClick={() => setMethod("paypal")}
                                    type="button"
                                >
                                    <span aria-hidden="true">👛</span>
                                    <span>PayPal</span>
                                </button>

                                <button
                                    className={`pay-tab ${method === "apple" ? "is-active" : ""}`}
                                    onClick={() => setMethod("apple")}
                                    type="button"
                                >
                                    <span aria-hidden="true">📱</span>
                                    <span>Apple Pay</span>
                                </button>
                            </div>

                            {method === "card" && (
                                <div className="pay-form">
                                    <div className="pay-field">
                                        <label className="form-label" htmlFor="card-number">Numero carta</label>
                                        <div className="pay-inputWrap">
                                            <input id="card-number" className="form-input" placeholder="0000 0000 0000 0000" />
                                            <span className="form-inputIcon" aria-hidden="true">💳</span>
                                        </div>
                                    </div>

                                    <div className="pay-row2">
                                        <div className="pay-field">
                                            <label className="form-label" htmlFor="expiry">Scadenza</label>
                                            <input id="expiry" className="form-input" placeholder="MM / AA" />
                                        </div>

                                        <div className="pay-field">
                                            <div className="pay-labelRow">
                                                <label className="form-label" htmlFor="cvc">CVC</label>
                                                <span className="pay-help" title="3 cifre sul retro della carta" aria-hidden="true">?</span>
                                            </div>
                                            <input id="cvc" className="form-input" placeholder="123" />
                                        </div>
                                    </div>

                                    <div className="pay-field">
                                        <label className="form-label" htmlFor="card-name">Intestatario</label>
                                        <input id="card-name" className="form-input" placeholder="es. Mario Rossi" />
                                    </div>

                                    <div className="pay-checks">
                                        <label className="pay-check">
                                            <input type="checkbox" defaultChecked />
                                            <span>Salva la carta per le box mensili future</span>
                                        </label>
                                        <label className="pay-check">
                                            <input type="checkbox" defaultChecked />
                                            <span>Indirizzo di fatturazione uguale alla spedizione</span>
                                        </label>
                                    </div>
                                </div>
                            )}

                            {method !== "card" && (
                                <div className="pay-placeholder">
                                    <div className="pay-placeholderTitle">Metodo in arrivo</div>
                                    <p className="mb-muted">
                                        Qui collegherai {method === "paypal" ? "PayPal" : "Apple Pay"} quando attiverai i pagamenti reali.
                                    </p>
                                </div>
                            )}
                        </section>

                        {/* RIGHT */}
                        <aside className="pay-right">
                            <div className="pay-summary">
                                <h3 className="mb-h3">Riepilogo ordine</h3>

                                <div className="pay-item">
                                    <div
                                        className="pay-itemImg"
                                        style={{
                                            backgroundImage:
                                                "url('https://lh3.googleusercontent.com/aida-public/AB6AXuAPal4tr1ZkTCRVELrrGH9uLkMllsdktOh-dfwCSnV-aF-4oPgH-99hwj7V3WvC4iTgTkFb0-u2mnfhnh5SgnGU20beAQKzG5GqKYibvpWHqzDNEj_GL70zxAtuAawyb_WiR4t8UbZr-hVGRXTezuTpIWW7V_9lofV3dT_7LToBdQkFpqTO7sY6DymXGjOJnPMQqZho8R7kWHfu9LcbldGwyHdNk1neQ4YTS849Dc8BCVZb4Y2ov4MDxCaIXTiRmbloL6_0toB1pQ')",
                                        }}
                                        aria-hidden="true"
                                    />
                                    <div className="pay-itemText">
                                        <div className="pay-itemTitle">Box Benessere Mensile</div>
                                        <div className="mb-muted">Piano: Vegan & Forza</div>
                                        <div className="pay-price">€ 89,00 / mese</div>
                                    </div>
                                </div>

                                <div className="pay-breakdown">
                                    <div className="pay-line"><span className="mb-muted">Subtotale</span><span>€ 89,00</span></div>
                                    <div className="pay-line"><span className="mb-muted">Spedizione</span><span>€ 0,00</span></div>
                                    <div className="pay-line"><span className="mb-muted">Tasse</span><span>€ 8,90</span></div>
                                </div>

                                <div className="pay-total">
                                    <div>
                                        <div className="mb-muted">Totale da pagare</div>
                                        <div className="pay-totalNum">€ 97,90</div>
                                    </div>
                                    <div className="pay-currency">EUR</div>
                                </div>

                                <Link className="btn-cta" to="/box/tracking">
                                    Completa acquisto <span aria-hidden="true">→</span>
                                </Link>

                                <div className="pay-trust">
                                    <div className="pay-trustItem"><span aria-hidden="true">🔒</span> SSL</div>
                                    <span className="pay-dot" aria-hidden="true" />
                                    <div className="pay-trustItem"><span aria-hidden="true">✅</span> Protezione pagamento</div>
                                </div>

                                <Link className="pay-back" to="/box/setup">← Torna alla box</Link>
                            </div>
                        </aside>
                    </div>
                </div>
            </main>

            <footer className="mb-footer">
                <p>© 2024 Mind&Body. Tutti i diritti riservati.</p>
            </footer>
        </div>
    );
}
