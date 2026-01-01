import React from 'react';
import "../../styles/sr-components.css";

// --- Layout Components ---

export const SrLayout = ({ children, className = "" }) => {
    return (
        <div className={`sr-main ${className}`}>
            <div className="sr-wrap">
                {children}
            </div>
        </div>
    );
};

export const SrGrid = ({ children, className = "" }) => {
    return <div className={`sr-grid ${className}`}>{children}</div>;
};

export const SrSectionHead = ({ title, subtitle, action, className = "" }) => {
    return (
        <div className={`sr-sectionHead ${className}`}>
            <div>
                {title && <h2 className="sr-h2">{title}</h2>}
                {subtitle && <p className="sr-sub">{subtitle}</p>}
            </div>
            {action && <div>{action}</div>}
        </div>
    );
};

// --- Card Components ---

export const SrCard = ({ children, className = "", title, subtitle, action }) => {
    return (
        <div className={`sr-card ${className}`}>
            {(title || action) && (
                <div className="sr-cardHead">
                    <div>
                        {title && <h3 className="sr-h3">{title}</h3>}
                        {subtitle && <p className="sr-muted">{subtitle}</p>}
                    </div>
                    {action}
                </div>
            )}
            {children}
        </div>
    );
};

export const SrSideCardDark = ({ children, className = "" }) => {
    return <div className={`sr-sideCardDark ${className}`}>{children}</div>;
};

// --- Button Components ---

export const SrButton = ({
    variant = "primary", // primary, ghost, link, dark, soft, cta
    children,
    className = "",
    ...props
}) => {
    let btnClass = "";

    switch (variant) {
        case "ghost": btnClass = "sr-btnGhost"; break;
        case "link": btnClass = "sr-linkBtn"; break;
        case "dark": btnClass = "sr-btnDark"; break;
        case "soft": btnClass = "sr-btnSoft"; break;
        case "cta": btnClass = "sr-cta"; break;
        default: btnClass = "btn-primary"; // Fallback or reuse existing primary
    }

    return (
        <button className={`${btnClass} ${className}`} type="button" {...props}>
            {children}
        </button>
    );
};

// --- Form Components ---

export const SrInput = ({ label, className = "", icon, ...props }) => {
    return (
        <div className={`sr-field ${className}`}>
            {label && <label className="sr-label">{label}</label>}
            <div className={icon ? "sr-inputIconWrap" : ""}>
                {icon && <span className="sr-inputIcon" aria-hidden="true">{icon}</span>}
                <input className={`sr-input ${icon ? "sr-input--icon" : ""}`} {...props} />
            </div>
        </div>
    );
};

export const SrTextarea = ({ label, className = "", ...props }) => {
    return (
        <div className={`sr-field ${className}`}>
            {label && <label className="sr-label">{label}</label>}
            <textarea className="sr-textarea" {...props} />
        </div>
    );
};

export const SrSelect = ({ label, children, className = "", ...props }) => {
    return (
        <div className={`sr-field ${className}`}>
            {label && <label className="sr-label">{label}</label>}
            <select className="sr-select" {...props}>
                {children}
            </select>
        </div>
    );
};

// --- Badge / Pill ---

export const SrBadge = ({ children, className = "" }) => {
    return <span className={`sr-badge ${className}`}>{children}</span>;
};

export const SrPill = ({ children, className = "" }) => {
    return <span className={`sr-pill ${className}`}>{children}</span>;
};
