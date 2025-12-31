import React, { useMemo } from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/shared.css';

export default function Navbar() {
    const location = useLocation();

    const navLinks = useMemo(() => [
        { label: 'Nutrizione', path: '/nutrition' },
        { label: 'Allenamento', path: '/training' },
        { label: 'Benessere Mentale', path: '/mental-wellbeing' },
        { label: 'Community', path: '#community' },
    ], []);

    // Helper to determine active state style (optional, if we want to highlight active page)
    const getLinkStyle = (path) => {
        // Exact match or sub-path logic could go here
        // For now, simple exact match for highlighting or just default style
        const isActive = location.pathname.startsWith(path) && path !== '#community';
        return isActive ? { color: '#0f172a', borderColor: '#0f172a' } : {};
    };

    return (
        <header className="mb-navbar">
            <div className="mb-brand">
                <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '10px', color: 'inherit' }}>
                    <div className="mb-logo" aria-hidden="true">
                        <span className="mb-logoInner" />
                    </div>
                    <span className="mb-brandText">Mind&Body</span>
                </Link>
            </div>

            <nav className="mb-navLinks" aria-label="Primary">
                {navLinks.map((link) => (
                    <Link
                        key={link.label}
                        className="mb-link"
                        to={link.path}
                        style={getLinkStyle(link.path)}
                    >
                        {link.label}
                    </Link>
                ))}
            </nav>

            <div className="mb-profileBtn">
                <Link to="/account" aria-label="Profilo" style={{ textDecoration: 'none', display: 'block' }}>
                    <div className="tc-userDot">
                        <span style={{ fontSize: '18px' }}>👤</span>
                    </div>
                </Link>
            </div>
        </header>
    );
}
