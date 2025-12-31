import { useMemo, useState } from "react";
import React from 'react';
import Navbar from '../components/Navbar';
import "../styles/pages/share-recipe.css";
// Reuse reusable Navbar if possible, but the provided code has its own Header.
// I will keep the user's Header for now as requested, but might refactor later if asked.
// Actually, looking at the code, it imports Navbar from "../components/Navbar" in previous steps, 
// but here it defines a local Header function. I will use the code provided.

export default function ShareRecipe() {
    const [title, setTitle] = useState("");
    const [desc, setDesc] = useState("");
    const [prepTime, setPrepTime] = useState("");
    const [servings, setServings] = useState("");
    const [difficulty, setDifficulty] = useState("Facile");
    const [calories, setCalories] = useState("");
    const [steps, setSteps] = useState("");
    const [search, setSearch] = useState("");

    const [ingredients, setIngredients] = useState([
        { id: "i1", name: "Patata dolce", qty: "2 grandi", fromBox: true },
        { id: "i2", name: "Olio d'oliva", qty: "2 cucchiai", fromBox: false },
        { id: "i3", name: "Aglio in polvere", qty: "1 cucchiaino", fromBox: false },
    ]);

    const [newIngName, setNewIngName] = useState("");
    const [newIngQty, setNewIngQty] = useState("");

    const activeBoxItems = useMemo(
        () => [
            { id: "b1", icon: "🌿", title: "Cavolo riccio biologico", sub: "Mazzo fresco", added: false },
            { id: "b2", icon: "🥔", title: "Patata dolce", sub: "Aggiunta", added: true },
            { id: "b3", icon: "🐟", title: "Filetto di salmone", sub: "2 x 150g", added: false },
            { id: "b4", icon: "🌾", title: "Quinoa", sub: "Confezione 500g", added: false },
        ],
        []
    );

    function addIngredient() {
        const name = newIngName.trim();
        const qty = newIngQty.trim();
        if (!name) return;

        setIngredients((prev) => [
            ...prev,
            { id: `i_${Date.now()}`, name, qty: qty || "", fromBox: false },
        ]);
        setNewIngName("");
        setNewIngQty("");
    }

    function removeIngredient(id) {
        setIngredients((prev) => prev.filter((x) => x.id !== id));
    }

    function updateIngredientQty(id, qty) {
        setIngredients((prev) => prev.map((x) => (x.id === id ? { ...x, qty } : x)));
    }

    function saveDraft() {
        // Demo: qui collegherai salvataggio reale (Supabase / API)
        alert("Bozza salvata (demo).");
    }

    function shareRecipe() {
        // Demo: qui collegherai pubblicazione reale
        alert("Ricetta condivisa (demo).");
    }

    return (
        <div className="sr-page">
            <Navbar />

            {/* Content moved from Header specific to this page: Search */}
            {/* I will add search functionality inside the main area for now or just ignore if user didnt ask. 
                User said "usa una navbar unica".
                I'll keep it simple: replace with Navbar. Search can be re-added in page if needed. 
            */}

            <main className="sr-main">
                <div className="sr-wrap">
                    <div className="sr-top">
                        <div>
                            <div className="sr-breadcrumbs">
                                <a href="/nutrition" className="sr-crumbLink">Nutrizione</a>
                                <span className="sr-crumbSep">›</span>
                                <span className="sr-crumbActive">Condividi ricetta</span>
                            </div>

                            <h1 className="sr-h1">Condividi la tua ricetta</h1>
                            <p className="sr-sub">Ispira la community con le tue creazioni sane.</p>
                        </div>

                        <div className="sr-actionsTop">
                            <button className="sr-btnGhost" type="button" onClick={saveDraft}>
                                Salva bozza
                            </button>
                        </div>
                    </div>

                    <div className="sr-grid">
                        {/* LEFT */}
                        <section className="sr-left">
                            {/* Card: Info Ricetta */}
                            <div className="sr-card">
                                <div className="sr-section">
                                    <label className="sr-label">Foto della ricetta</label>

                                    <div className="sr-upload" role="button" tabIndex={0}>
                                        <div className="sr-uploadInner">
                                            <div className="sr-uploadIcon" aria-hidden="true">📷</div>

                                            <div className="sr-uploadRow">
                                                <label className="sr-uploadLink" htmlFor="file-upload">
                                                    Carica un file
                                                </label>
                                                <input id="file-upload" className="sr-srOnly" type="file" />
                                                <span className="sr-uploadText">oppure trascina e rilascia</span>
                                            </div>

                                            <div className="sr-uploadHint">PNG, JPG, GIF fino a 10MB</div>
                                        </div>
                                    </div>
                                </div>

                                <div className="sr-formGrid">
                                    <div className="sr-field sr-span2">
                                        <label className="sr-label" htmlFor="title">Titolo ricetta</label>
                                        <input
                                            id="title"
                                            className="sr-input"
                                            placeholder="es. Insalata di quinoa estiva"
                                            value={title}
                                            onChange={(e) => setTitle(e.target.value)}
                                        />
                                    </div>

                                    <div className="sr-field sr-span2">
                                        <label className="sr-label" htmlFor="description">Descrizione</label>
                                        <textarea
                                            id="description"
                                            className="sr-textarea"
                                            placeholder="Raccontaci la storia dietro questo piatto..."
                                            rows={3}
                                            value={desc}
                                            onChange={(e) => setDesc(e.target.value)}
                                        />
                                    </div>

                                    <div className="sr-field">
                                        <label className="sr-label" htmlFor="prep-time">Tempo di preparazione (min)</label>
                                        <div className="sr-inputIconWrap">
                                            <span className="sr-inputIcon" aria-hidden="true">⏱️</span>
                                            <input
                                                id="prep-time"
                                                className="sr-input sr-input--icon"
                                                type="number"
                                                placeholder="30"
                                                value={prepTime}
                                                onChange={(e) => setPrepTime(e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="sr-field">
                                        <label className="sr-label" htmlFor="servings">Porzioni</label>
                                        <div className="sr-inputIconWrap">
                                            <span className="sr-inputIcon" aria-hidden="true">👥</span>
                                            <input
                                                id="servings"
                                                className="sr-input sr-input--icon"
                                                type="number"
                                                placeholder="2"
                                                value={servings}
                                                onChange={(e) => setServings(e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="sr-field">
                                        <label className="sr-label" htmlFor="difficulty">Difficoltà</label>
                                        <select
                                            id="difficulty"
                                            className="sr-select"
                                            value={difficulty}
                                            onChange={(e) => setDifficulty(e.target.value)}
                                        >
                                            <option>Facile</option>
                                            <option>Media</option>
                                            <option>Difficile</option>
                                        </select>
                                    </div>

                                    <div className="sr-field">
                                        <label className="sr-label" htmlFor="calories">Calorie (kcal)</label>
                                        <input
                                            id="calories"
                                            className="sr-input"
                                            type="number"
                                            placeholder="Opzionale"
                                            value={calories}
                                            onChange={(e) => setCalories(e.target.value)}
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* Card: Ingredienti */}
                            <div className="sr-card">
                                <div className="sr-cardHead">
                                    <div>
                                        <h3 className="sr-h3">Ingredienti</h3>
                                        <p className="sr-muted">Aggiungi ingredienti della tua box o elementi personalizzati.</p>
                                    </div>
                                    <button className="sr-linkBtn" type="button" title="Demo">
                                        ➕ Aggiungi sezione
                                    </button>
                                </div>

                                <div className="sr-ingList">
                                    {ingredients.map((it) => (
                                        <div
                                            key={it.id}
                                            className={`sr-ingRow ${it.fromBox ? "sr-ingRow--fromBox" : ""}`}
                                        >
                                            <div className="sr-ingLeft">
                                                <span className="sr-drag" aria-hidden="true">⋮⋮</span>
                                                <span className="sr-ingName">{it.name}</span>
                                                {it.fromBox && <span className="sr-badge">Dalla tua box</span>}
                                            </div>

                                            <div className="sr-ingRight">
                                                <input
                                                    className="sr-ingQty"
                                                    value={it.qty}
                                                    onChange={(e) => updateIngredientQty(it.id, e.target.value)}
                                                    placeholder="Qtà"
                                                />
                                                <button
                                                    className="sr-trash"
                                                    type="button"
                                                    onClick={() => removeIngredient(it.id)}
                                                    aria-label={`Elimina ${it.name}`}
                                                    title="Elimina"
                                                >
                                                    🗑️
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div className="sr-addRow">
                                    <input
                                        className="sr-input"
                                        placeholder="Aggiungi ingrediente (es. Sale)"
                                        value={newIngName}
                                        onChange={(e) => setNewIngName(e.target.value)}
                                    />
                                    <input
                                        className="sr-input sr-qty"
                                        placeholder="Qtà"
                                        value={newIngQty}
                                        onChange={(e) => setNewIngQty(e.target.value)}
                                    />
                                    <button className="sr-btnDark" type="button" onClick={addIngredient} aria-label="Aggiungi">
                                        ➕
                                    </button>
                                </div>
                            </div>

                            {/* Card: Preparazione */}
                            <div className="sr-card">
                                <h3 className="sr-h3">Passaggi di preparazione</h3>

                                <div className="sr-stepsWrap">
                                    <textarea
                                        className="sr-steps"
                                        rows={8}
                                        placeholder={`Step 1: Preriscalda il forno a...
Step 2: Taglia le verdure...`}
                                        value={steps}
                                        onChange={(e) => setSteps(e.target.value)}
                                    />
                                    <div className="sr-markdownHint">Supporto Markdown</div>
                                </div>
                            </div>

                            <div className="sr-bottomAction">
                                <button className="sr-cta" type="button" onClick={shareRecipe}>
                                    <span aria-hidden="true">📤</span>
                                    Condividi ricetta
                                </button>
                            </div>
                        </section>

                        {/* RIGHT */}
                        <aside className="sr-right">
                            <div className="sr-sticky">
                                <div className="sr-sideCardDark">
                                    <div className="sr-sideBadge">
                                        <span aria-hidden="true">📦</span> Nella tua box attiva
                                    </div>

                                    <div className="sr-sideTitle">Usa i tuoi ingredienti</div>
                                    <div className="sr-sideSub">Tocca “+” per aggiungerli alla ricetta.</div>

                                    <div className="sr-sideList">
                                        {activeBoxItems.map((x) => (
                                            <button
                                                key={x.id}
                                                className={`sr-boxItem ${x.added ? "is-added" : ""}`}
                                                type="button"
                                                disabled={x.added}
                                                title={x.added ? "Già aggiunto" : "Demo: aggiungi ingrediente"}
                                                onClick={() => {
                                                    if (x.added) return;
                                                    // Demo: aggiunta rapida
                                                    setIngredients((prev) => [
                                                        ...prev,
                                                        { id: `i_${Date.now()}`, name: x.title, qty: "", fromBox: true },
                                                    ]);
                                                    alert("Aggiunto (demo).");
                                                }}
                                            >
                                                <div className="sr-boxLeft">
                                                    <div className="sr-boxIcon" aria-hidden="true">{x.icon}</div>
                                                    <div>
                                                        <div className={`sr-boxTitle ${x.added ? "line" : ""}`}>{x.title}</div>
                                                        <div className="sr-boxSub">{x.sub}</div>
                                                    </div>
                                                </div>

                                                <div className={`sr-boxRight ${x.added ? "check" : "plus"}`} aria-hidden="true">
                                                    {x.added ? "✓" : "+"}
                                                </div>
                                            </button>
                                        ))}
                                    </div>

                                    <div className="sr-sideFooter">
                                        <a href="#" className="sr-sideLink">
                                            Vedi contenuto completo della box <span aria-hidden="true">↗</span>
                                        </a>
                                    </div>
                                </div>

                                <div className="sr-tips">
                                    <div className="sr-tipsHead">
                                        <div className="sr-tipsBulb" aria-hidden="true">💡</div>
                                        <div className="sr-tipsTitle">Consigli Pro</div>
                                    </div>

                                    <ul className="sr-tipsList">
                                        <li>Foto di alta qualità ottengono 3× visualizzazioni.</li>
                                        <li>Usa ingredienti della tua box per aiutare gli altri a usare i loro!</li>
                                        <li>Sii preciso nei passaggi: aiuta molto i principianti.</li>
                                    </ul>
                                </div>
                            </div>
                        </aside>
                    </div>
                </div>
            </main>
        </div>
    );
}

function Header({ search, setSearch }) {
    return (
        <header className="sr-header">
            <div className="sr-headerInner">
                <div className="sr-leftHeader">
                    <div className="sr-brand">
                        <div className="sr-brandIcon" aria-hidden="true">🧖</div>
                        <div className="sr-brandText">Mind&Body</div>
                    </div>

                    <nav className="sr-nav">
                        <a className="sr-navItem sr-navItem--active" href="/nutrition">Nutrizione</a>
                        <a className="sr-navItem" href="#">Allenamento</a>
                        <a className="sr-navItem" href="/mental-wellbeing">Benessere mentale</a>
                        <a className="sr-navItem" href="#">Community</a>
                    </nav>
                </div>

                <div className="sr-rightHeader">
                    <div className="sr-search">
                        <span className="sr-searchIcon" aria-hidden="true">🔎</span>
                        <input
                            className="sr-searchInput"
                            placeholder="Cerca ricette..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>

                    <button className="sr-bell" type="button" aria-label="Notifiche" title="Notifiche">
                        🔔
                        <span className="sr-dot" aria-hidden="true" />
                    </button>

                    <div className="sr-user">
                        <div className="sr-userText">
                            <div className="sr-userName">Alex Johnson</div>
                            <div className="sr-userTier">Membro Premium</div>
                        </div>
                        <div
                            className="sr-avatar"
                            style={{
                                backgroundImage:
                                    "url('https://lh3.googleusercontent.com/aida-public/AB6AXuAXlPhTakPqV2gBXc3aGrmOhNwPF7rxvm3oUaZW3EgFfMXov-TMPs9AEBsTRONpdzulJjzDdyCV6AfUl8U3EkGK5hdpC-zyjZKgv2BK9xGu1xbzJ4CsxVMNItWVoix6PTO9-3BITtrX3gLOzam6xxvkNTQxsDYVWpDXHth92PZZ3BE1Uk1jtQR5dhopKwtQG7wlYPjy34NyntyqH9coCmkVQ5sJpk6BvbZfjwKnB8cUyuBGF9yQ2HiY2nFS_BHvMe0wlqpPqPQOJQ')",
                            }}
                            aria-hidden="true"
                        />
                    </div>

                    <button className="sr-menuBtn" type="button" aria-label="Menu">
                        ☰
                    </button>
                </div>
            </div>
        </header>
    );
}
