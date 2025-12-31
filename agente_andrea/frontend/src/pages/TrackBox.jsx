
import Navbar from "../components/Navbar";
import "../styles/pages/box.css";
import "../styles/pages/tracking.css";

export default function TrackBox() {
    return (
        <div className="mb-page">
            <Navbar />

            <main className="mb-main">
                <div className="mb-wrap">


                    <div className="trk-grid">
                        {/* LEFT */}
                        <section className="trk-left">
                            <div className="trk-card">
                                <div className="trk-timeline">
                                    <div className="trk-line" aria-hidden="true" />
                                    <div className="trk-progress" aria-hidden="true" style={{ width: "65%" }} />

                                    <div className="trk-steps">
                                        <Step done label="Confermato" icon="✓" />
                                        <Step done label="Preparazione" icon="🍳" />
                                        <Step done label="Spedito" icon="🚚" />
                                        <Step current label="In consegna" icon="🚚" badge="Live" />
                                        <Step label="Consegnato" icon="📦" dim />
                                    </div>
                                </div>
                            </div>

                            <div className="trk-mapCard">
                                <div className="trk-map">
                                    <div
                                        className="trk-mapBg"
                                        style={{
                                            backgroundImage:
                                                "url('https://lh3.googleusercontent.com/aida-public/AB6AXuASWh4ID-YpQxGyAcpibHoU7tDr-R3h2lTJTF1peBbACYy699QCI6rKbtlFNzIf2fgcJAnMEKBMOWkFd8jp3-n9Pb4_FHbvitwgPo738dPND0bBht7lLB4L5hyrpJLhXNmSrSMSqG0d7zbcjZGgIgXYrIe8UoGSq2OiLqaya2TxJPl5QfmqHCiYRhtPqs38SVlnpb71YwStZmx-KXreehCPMm7cVsXybPK6cuiObkrvAB0Yw2b7b7EW5-kjTrUFB8DBxzIsahDDfg')",
                                        }}
                                        aria-hidden="true"
                                    />
                                    <div className="trk-mapOverlay" aria-hidden="true" />

                                    <div className="trk-pin">
                                        <div className="trk-ping" aria-hidden="true" />
                                        <div className="trk-pinIcon" aria-hidden="true">🚚</div>
                                        <div className="trk-pinLabel">A 5 minuti</div>
                                    </div>

                                    <div className="trk-mapControls">
                                        <button className="trk-ctrl" type="button" aria-label="Zoom in">+</button>
                                        <button className="trk-ctrl" type="button" aria-label="Zoom out">−</button>
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* RIGHT */}
                        <aside className="trk-right">
                            <div className="trk-card">
                                <div className="trk-miniTitle">Il tuo corriere</div>

                                <div className="trk-courier">
                                    <div
                                        className="trk-avatar"
                                        style={{
                                            backgroundImage:
                                                "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCTE9nYtGw4t7-MXfcIUsaPMUVRk64uezbkROKJ-gXGg9fgb3B4byTvU_wmoIx5ykWLVftPob9y5t8hZ9Yf5iLbAIGMyCatINhJxyzcRT81hG1ltXBuMc6hY2ZV8LscLKM-SoSm130iZMejvg9vuDPr_7leZkIBoKBDMkAr0ht4yA5wnu3X0QjW4sZL1d4rUQENXYMV3IMi3o-cj_jSholetTAsQnXEfnyko2PqUQjqErXkIuYuDAgwcD-XP_cLDgkhyH1eJN4YhQ')",
                                        }}
                                        aria-hidden="true"
                                    />
                                    <div className="trk-courierText">
                                        <div className="trk-courierName">Marcus T.</div>
                                        <div className="mb-muted">4.9 • Furgone elettrico</div>
                                    </div>

                                    <button className="trk-call" type="button" title="Chiama corriere" aria-label="Chiama corriere">
                                        📞
                                    </button>
                                </div>
                            </div>

                            <div className="trk-card">
                                <div className="trk-cardHeadRow">
                                    <div className="trk-miniTitle">Cosa contiene</div>
                                    <button className="mb-linkBtn" type="button">Vedi tutto</button>
                                </div>

                                <div className="trk-inside">
                                    <InsideItem
                                        title="Green Goddess Bowl"
                                        subtitle="2 porzioni • Vegan"
                                        img="https://lh3.googleusercontent.com/aida-public/AB6AXuA64_J64b0Ry6X-PsztUurI2bJ5CFTOMz97DzmyMyjZHC-KG0xb4Fof6ewghEI9dR0zqoZsQlxwSFc6c1Xo1XNLTI_a0fgl9bJGyER4eb-fHGA4Pp9QiYlt4pyb2RUGuWIZ8pQh7lNjMOCcQHqm_2KQjjUmID7yyKZ2jEKdh19gcgEeI4g7jUSwO6BKrbJLYBOnRZk-w93UZ6FdZSknYwirWaFaDGYCltxDVJGgEWodTksGBVoIenl3SWXQcf0TnCGUrl49m3Bn-Q"
                                    />
                                    <InsideItem
                                        title="Lean Protein Pack"
                                        subtitle="4 porzioni • Alto Proteine"
                                        img="https://lh3.googleusercontent.com/aida-public/AB6AXuDphHVo8lhXyfE_kzifDwO-gtvYOuQCDOH-Ghi3EKoJOGsvy3RSWm6dESCqqcfk66IFrKMfdmC0SDw1X_KpZzqBfv_PBIHl4ov9wLmG9W0gFr2SICvda2_U9MDdkzKRuf56_jMencUTLcpMlYtsQH-FkvsHHTeEKHxMy072DFMQ9HXAfQoshIFNBJsal9eMSapEA_YjJmIMjENIHha_gdr_iHkOqgGKFk0bTCaiR9HOuXLBVm7Bg_AaR01Ly-i-GDqSQaYzSXMJqQ"
                                    />
                                    <InsideItem
                                        title="Mix verdure bio"
                                        subtitle="1,5kg • Crudo"
                                        img="https://lh3.googleusercontent.com/aida-public/AB6AXuBrnel8rdNqdgYm8cAmeUI4S-kjUvIF_GTRpbWHPZQKBH84FUIYE_MbQmd41QAJzrAbhHPlAYu0PSmKwn427vFafkHmBlJNKS-1rF1_MEUAHtrfvVlKCmUkS0eInpbflTSD8XoFVALdMw3ATu68-Bm1BTmX21sAzjDRPE7H8sOG0N8bFWEVgZj2fQPnrogaYaIOxMWIb_A6ef1M0kDGFUlq9m2wwba6N75j-amoZ6DobLw4hc2peaBa8z5kMHMDcOwfCigUBLcy0A"
                                    />
                                </div>
                            </div>

                            <div className="trk-support">
                                <div className="trk-supportMini">Centro assistenza</div>
                                <div className="trk-supportTitle">Problemi con l’ordine?</div>
                                <p className="trk-supportText">Il nostro team è disponibile 24/7 per aiutarti.</p>
                                <button className="trk-supportBtn" type="button">
                                    Chatta con il supporto <span aria-hidden="true">→</span>
                                </button>
                            </div>
                        </aside>
                    </div>
                </div >
            </main >
        </div >
    );
}

function Step({ done, current, dim, label, icon, badge }) {
    return (
        <div className={`trk - step ${dim ? "is-dim" : ""} `}>
            <div className={`trk - stepDot ${done ? "is-done" : ""} ${current ? "is-current" : ""} `}>
                <span aria-hidden="true">{icon}</span>
                {badge && <span className="trk-live">{badge}</span>}
            </div>
            <div className={`trk - stepLabel ${current ? "is-current" : ""} `}>{label}</div>
        </div>
    );
}

function InsideItem({ title, subtitle, img }) {
    return (
        <div className="trk-insideItem">
            <div className="trk-insideImg" style={{ backgroundImage: `url('${img}')` }} aria-hidden="true" />
            <div className="trk-insideText">
                <div className="trk-insideTitle">{title}</div>
                <div className="mb-muted">{subtitle}</div>
            </div>
        </div>
    );
}
