import React, { useMemo, useState } from "react";
import { Link } from 'react-router-dom';
import "../styles/pages/nutrition-dashboard.css";

import Navbar from "../components/Navbar";

const COMMUNITY_RECIPES = [
    {
        title: "Avocado Smash del Mattino",
        author: "@sarah_fit",
        likes: "1.2k",
        img: "https://lh3.googleusercontent.com/aida-public/AB6AXuB1wFsEbhoKeOcXFKm_2qNA6hX2GJJu6kmNEEDKe_sDJ6DXwKNovcDsqI1ZujQeOZCXsUNkqI1ZdwitNM6pYTlJEG3ZJ9T8mfThB-FhnUCqe52pcJIS84ArBfWeqZUlQaXn_e4a56guvbcO_LHmQfLBza7Dr9zm4xoenNwx1WvnBt5iSm-4pD9Hp0eCo3gR2JGjiXT44quk8YrjgO_orKM6B_0kE667B8caqNHY6ruvDCsjBTys0_ioDdnnlti6NJUgWCZlbTtvgQ",
    },
    {
        title: "Porridge Proteico ai Frutti di Bosco",
        author: "@mike_lifts",
        likes: "850",
        img: "https://lh3.googleusercontent.com/aida-public/AB6AXuCneGQMbA_4MPT8CBmXKUOg8F0woA6iHk0iA_QtN4kwOEYKdBwwVtEXC81McZS0FofU426Ghts-QrkUKuTs4T9W5Qcx1qeuCeWkw1zrgyhWuCd8EfjLjbZg3v11OC4JhF1j-N2aRV2i3ap6P2xxEC3qOMm_RNx1FEepj-KBCdWqvvw8toAFTqMzyPaEuinIGinGJLXUNsWnvZo0hXfwoIW3E91XHj4RnDzXwwCrvtKyhsMJTc0v57A1QU486YUAC4_2JUz285M-XA",
    },
    {
        title: "Rice Bowl Post-Workout",
        author: "@jessica_runs",
        likes: "620",
        img: "https://lh3.googleusercontent.com/aida-public/AB6AXuAaHwW4DRaioWSYHcTRlp5IPFiZUlpr0Gdrvdh9_KFnmwXquDSqksmyrU6pzea4U9CYwlXYJ4GLKLh4WIR881xPDpW7Oit8yz4_d3rhMx_vdcrY0VXIpB3fwvG-qjPPuLhE2ZuYSiYEgvtml08D8OLkn7swNTiCw5-mWyqXyZKVqcicdTZxz1mDrCY070pK7RHl3TduCjbxLG3u_IL0ODAGHj6xuApp148A847ogu9iKxCjCZ6UXjLTredJU7ywFPszyx_aWxCp_g",
    },
    {
        title: "Smoothie Detox Verde",
        author: "@health_guru",
        likes: "540",
        img: "https://lh3.googleusercontent.com/aida-public/AB6AXuAEVEipcQd8Wv3vqgMxe2QpRm-2kjq-HnGDNrO46CN4kLwgpmTU40AjxEZc7NerqDhTufleocbzbJuz93xpgsj2hsbc-8MnD-dX0G4QrffU-8HiAMEMhD4c8HP1rW2FkK3dJ0ffjBHrJTcUiCXyvPKtLCD1iKMuvrtYDQ-Dc4qGHEqrmnCBhmuKgWs2TH90kbZTQefjLiW32EsRWNowXGD4TVDGTHYo3EbiPL5OIHGbCE9gNBtLHW_Tth52pT6jcV2zRKAxRFmlhw",
    },
];

const RECOMMENDED = [
    {
        minutes: "15 min",
        badge: "Alto Proteine",
        badgeTone: "primary",
        title: "Insalatona Green Goddess",
        desc: "Un mix fresco di cavolo riccio, spinaci e avocado con dressing al limone.",
        img: "https://lh3.googleusercontent.com/aida-public/AB6AXuDYMuWjw9XbQXfk0bQjv7aj2ZxlTvtpu9-w3GzPZLPsnwgJG5PhBldeorOae1ZQ9u-j9q0PpXM6jU8k3vadXR2yn68Jm5SLvtr_z_snTuKxajO8kFPic86UMIT35v8KhgAQVpFfkOGbH52_9h2CnChvKPepCx_ti3IwsO0vRhJ2k7nhiXlibXQku7UhWGFol40xhr8bVfEI1ZsyXJ94_EQ-LbZBaB8AcKHQ97-Ymq2-IvlrX4El3-i7_lnMnsP7-M1Z8VcWibtbwg",
    },
    {
        minutes: "25 min",
        badge: "Keto Friendly",
        badgeTone: "blue",
        title: "Salmone & Asparagi alla Griglia",
        desc: "Salmone alla griglia servito con asparagi croccanti.",
        img: "https://lh3.googleusercontent.com/aida-public/AB6AXuAlKqiqU9CvqAerLYsAh_MRdd9A27xC25EVpdqit1v-F0cHdINynyjTGsAHa2X_iOQIMMLteNGImXhpRwAdNw7912mGaVAAQ9zEWPZUmBnTpfkbNr0ljpGrrE9SF_FXGl9btvN8ULsi7Y0WLObOdNtiTs48Pg66_NQmo312SGwKS69S3kYmSvVhx3YJJjFtMzrQOj9rDa3ppas8Cyvj4vDFes21--thYgFhv8WM6nDgKXSYXKlaCRWK8hnZFOYnaLT5_CoJ1K_NBA",
    },
    {
        minutes: "20 min",
        badge: "Vegan",
        badgeTone: "orange",
        title: "Bowl di Quinoa Arcobaleno",
        desc: "Ricca di fibre e colori, perfetta per un pranzo leggero.",
        img: "https://lh3.googleusercontent.com/aida-public/AB6AXuDTX2qjz1yRUlLiOpGf4n_Mr4thM_C2X7bJup-vUg9ROIw966c1ex9_n7-Ud7A7-L0wGesenfDfpqEmVrzK-VBWuGoRoxM9aZTLXY4XCl0fE_a82tlkn88q4AuTf-8wYZXEcLaKn-fEKfobwOXjPJozA6SBCoQolyoFv0p6Y5pFcNTg7yr0ZeCOKs8iRvizT_YNWShn6bcQY-hOFEzwkID5eVm-oivisn5pHpBxSWKzODKviM_sMkcG0XNEvgyE8QdScGFKvbAz2w",
    },
    {
        minutes: "35 min",
        badge: "Bilanciata",
        badgeTone: "primary",
        title: "Pollo Arrosto & Patata Dolce",
        desc: "Comfort food in versione più leggera, con meno olio.",
        img: "https://lh3.googleusercontent.com/aida-public/AB6AXuC8kiHf-SrnABnCbl9iW7VlCP7daX-QXlRhnWQEr_N6P19lr314FXXZW-UOnHFu2bYsfdU8EX5iFlzFh-fQVE3srxHZKG3L-b6Aapkb3C4vv9JAlLy92KK1czBQyWSosfwFnYtBxHoKMXjvBv-LUPXCzEgqVeotESOrSgZXYdmg2-nqUGf3pOmRi7pwfqw8WK-Bj7AtfF1KtJ40AWVa_e18gdS-1jv-HkdYK_XQdbVZzEgfmnpCxUNxygD7GeOchEQ5CW78a0xjsQ",
    },
];

function Tag({ active, children }) {
    return <button className={`tag ${active ? "tag--active" : "tag--outline"}`} type="button">{children}</button>;
}

function RecipeCard({ r }) {
    return (
        <article className="nd-recipeCard">
            <div className="nd-recipeImg" style={{ backgroundImage: `url('${r.img}')` }} />
            <div className="nd-recipeBody">
                <div>
                    <h4 className="nd-recipeTitle">{r.title}</h4>
                    <div className="nd-recipeBy">
                        di <span className="nd-author">{r.author}</span>
                    </div>
                </div>

                <div className="nd-recipeBottom">
                    <div className="nd-like">
                        <span aria-hidden="true">👍</span> {r.likes}
                    </div>
                    <button className="nd-linkBtn" type="button">Vedi ricetta</button>
                </div>
            </div>
        </article>
    );
}

function RecommendedCard({ c }) {
    return (
        <article className="nd-recCard">
            <div className="nd-recImgWrap">
                <div className="nd-recImg" style={{ backgroundImage: `url('${c.img}')` }} />
                <button className="nd-favBtn" type="button" aria-label="Aggiungi ai preferiti">♡</button>
            </div>

            <div className="nd-recBody">
                <div className="nd-recMeta">
                    <span className="nd-clock">⏱ {c.minutes}</span>
                    <span className="nd-dot">•</span>
                    <span className={`tag tag--${c.badgeTone}`}>{c.badge}</span>
                </div>
                <h4 className="nd-recTitle">{c.title}</h4>
                <p className="nd-recDesc">{c.desc}</p>
            </div>
        </article>
    );
}

export default function NutritionDashboard() {
    const recipes = useMemo(() => COMMUNITY_RECIPES, []);

    return (
        <div className="nd-page">
            <Navbar />

            <main className="nd-main">
                <div className="nd-wrap">
                    {/* header */}
                    <div className="nd-header">
                        <div>
                            <h1 className="nd-h1">Dashboard Nutrizione</h1>
                            <p className="nd-sub">
                                Esplora le ricette della community e gestisci la tua alimentazione.
                            </p>
                        </div>

                        <Link className="btn-primary" to="/share-recipe" style={{ textDecoration: 'none' }}>
                            <span aria-hidden="true">✎</span> Condividi ricetta
                        </Link>
                    </div>

                    {/* grid */}
                    <div className="nd-grid">
                        {/* left */}
                        <section className="nd-left">
                            <div className="nd-row">
                                <h2 className="nd-h2">Ricette della Community</h2>
                                <div className="nd-tags">
                                    <Tag active>Tutte</Tag>
                                    <Tag>Colazione</Tag>
                                    <Tag>Pranzo</Tag>
                                    <Tag>Cena</Tag>
                                </div>
                            </div>

                            <div className="nd-banner">
                                <div className="nd-bannerLeft">
                                    <div className="nd-spark" aria-hidden="true">✦</div>
                                    <div>
                                        <div className="nd-bannerTitle">Hai una ricetta sana “segreta”?</div>
                                        <div className="nd-bannerSub">Condividila con oltre 50k membri</div>
                                    </div>
                                </div>

                                <Link className="nd-bannerBtn" to="/share-recipe" style={{ textDecoration: 'none' }}>Condividi ora</Link>
                            </div>

                            <div className="nd-recipeGrid">
                                {recipes.map((r) => (
                                    <RecipeCard key={r.title} r={r} />
                                ))}
                            </div>
                        </section>

                        {/* right */}
                        <aside className="nd-right">
                            <div className="nd-card">
                                <div className="nd-cardHead">
                                    <h3 className="nd-h3">Più votate</h3>
                                    <button className="nd-miniLink" type="button">Vedi tutte</button>
                                </div>

                                <div className="nd-leaderboard">
                                    <div className="nd-rankRow">
                                        <div className="nd-rank nd-rank--gold">1</div>
                                        <div className="nd-rankImg" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuC0zOsXh3K4mgTewSkUl1RCuuSUD4ERwlyIgnce3d1JdmjBV-RB5sH6oLIPy-biLL8ydk5CA3VWj5PTcqt3cv5K11XUwnNYFbj2Qp3KEtQNFkKnA9P3RpnT977Fb8clxeAcKXgNPI-5D3rT3uxUJ69wiLeGPr-QvgXahe_yjgWmKBT8D1EnkbQW8swu1aCjP2fYXdarUUJ_lsumHbWQNL1LF38gJouQDQa14RZjIy0pAoR6hmxh1KbVKbTZfd4c_pUBSYkA5PLXaw')" }} />
                                        <div className="nd-rankText">
                                            <div className="nd-rankName">Tacos di tofu piccanti</div>
                                            <div className="nd-rankVotes">2.4k voti</div>
                                        </div>
                                        <div className="nd-trophy" aria-hidden="true">🏆</div>
                                    </div>

                                    <div className="nd-sep" />

                                    <div className="nd-rankRow">
                                        <div className="nd-rank nd-rank--silver">2</div>
                                        <div className="nd-rankImg" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuASOX5zV3FYaqJXeieXE-eJqtTzsjz4WwxeObtXNIK4x863MKXv_ha4VLKYMGmoKpMgsTKPU8gnSUcntYvhB7TYHa0HeOKHgO4_PlExorfSfOq_lk3Juk3c__UUZ7mo8-0JurrDuVXRWvhUa3Oqfzq23fjikl2Zr7-2EvWGU8pfhI1kPukDVyAWLqBDAegI6ztpjukaBzODoI3KHZd1zavtix_fq208M9DDSTFQ9g5jx0_Oc5CGGt_PZEL0jFAjyCRZdgbc2DT7hg')" }} />
                                        <div className="nd-rankText">
                                            <div className="nd-rankName">Pasta al pesto cremosa</div>
                                            <div className="nd-rankVotes">1.8k voti</div>
                                        </div>
                                    </div>

                                    <div className="nd-sep" />

                                    <div className="nd-rankRow">
                                        <div className="nd-rank nd-rank--bronze">3</div>
                                        <div className="nd-rankImg" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCqZzG0kKsegwpydEVB9BCbpkvnT3aNHZQ3j8C10EkFhe6-_mI9PjQgckJc_-wWLBf1vu8uyflfA_ZACGyCPHA6irLM9cKsXPyL4nAgDqVReiQKxpYK2MCPZiAC5Is9Y5DUf_uJFKPJCRATnpYEIZNNck_RaRkrieSEY7JfP7G0zlxogXdV8CjINiSFOTR6LmewfWsdYFyhmyBm7qYsfQCqjPjnWnN2LV_1JZv9UwBpVGhGVDHsAMATvQmvKwqhEzImmZEOKNeUaw')" }} />
                                        <div className="nd-rankText">
                                            <div className="nd-rankName">Acai power bowl</div>
                                            <div className="nd-rankVotes">1.5k voti</div>
                                        </div>
                                    </div>

                                    <div className="nd-sep" />

                                    <div className="nd-rankRow nd-rankRow--dim">
                                        <div className="nd-rank nd-rank--plain">4</div>
                                        <div className="nd-rankImg" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuChvWRaigrqXA6F2RLdjucWymH-Yw4NA6B5aqDEm-3PhAck92pt1j6qfg2rXno-IY6i5TE0ezLf-YxXeiEui8Bl8euJ8lJkqVS1GZSbPs3uJMjF9sEVc6TONNQD9VUaWpjTjM_m1ynWxqLnNfV5-fVtsvhhuKkcg2ModAR1UPEyRK5To0g2SCVAOIhvicQQMpg4qa4J-NaEt6V0xAne1R6xkVWD7hUva6D-N8hOraCGOtuczfccDRkNCe7dikVY8b65RncWrWuWFg')" }} />
                                        <div className="nd-rankText">
                                            <div className="nd-rankName">Macedonia fresca</div>
                                            <div className="nd-rankVotes">980 voti</div>
                                        </div>
                                    </div>
                                </div>

                                <button className="nd-softBtn" type="button">Vedi classifica completa</button>
                            </div>

                            <div className="nd-card nd-boxCard">
                                <div className="nd-boxTop">
                                    <div>
                                        <div className="nd-pill">
                                            <span aria-hidden="true">🚚</span> Prossima: Mar
                                        </div>
                                        <h3 className="nd-h3">La tua Box Settimanale</h3>
                                    </div>
                                    <div className="nd-boxIcon" aria-hidden="true">📦</div>
                                </div>

                                <div className="nd-boxRow">
                                    <div
                                        className="nd-boxImg"
                                        style={{
                                            backgroundImage:
                                                "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCD1dXd7sifkOKeGKxrEwOqAztMD8xxEv9cP3UAM4IP6TDSjfZbubIUsPQkN4CcIkC0NrjeD4djQYVRgeo4VhY-G6ywvGbIqVLQZvKeytSEdUBFc7woXqJILtadWXcN3aCOIp2UdUsIIst_r9lbyh4wdRIovxwBhMy3VIKFK3RjC3ICwCsF1bR4edhI8GLsXDnyMxi2esaeOcZUz3w4Is1i1K8hRXaiYimrhIBtsnCQSuCifkgw0jXBACE_wvPIZcDOfsf4yIdoAA')",
                                        }}
                                    />
                                    <p className="nd-boxText">
                                        Gli ingredienti selezionati per la prossima settimana sono pronti per la revisione.
                                    </p>
                                </div>

                                <Link className="nd-outlineBtn" to="/box/setup" style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}>Personalizza ordine</Link>
                            </div>
                        </aside>
                    </div>

                    {/* recommended */}
                    <section className="nd-recommended">
                        <div className="nd-recHead">
                            <h2 className="nd-h2">Consigliate per te</h2>
                            <div className="nd-arrows">
                                <button className="nd-arrow" type="button" aria-label="Indietro">‹</button>
                                <button className="nd-arrow" type="button" aria-label="Avanti">›</button>
                            </div>
                        </div>

                        <div className="nd-recGrid">
                            {RECOMMENDED.map((c) => (
                                <RecommendedCard key={c.title} c={c} />
                            ))}
                        </div>
                    </section>
                </div>
            </main>
        </div>
    );
}
