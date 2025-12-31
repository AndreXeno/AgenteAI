import typography from '@tailwindcss/typography';
import forms from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: "#45D4B3",
                    light: "#E1F9F4"
                },
                "background-light": "#FFFFFF",
                "background-dark": "#111827",
                "surface-light": "#F8FAFC",
                "surface-dark": "#1F2937",
                "text-light-primary": "#1E293B",
                "text-dark-primary": "#F9FAFB",
                "text-light-secondary": "#64748B",
                "text-dark-secondary": "#9CA3AF",
                "border-light": "#E2E8F0",
                "border-dark": "#374151"
            },
            fontFamily: {
                display: ["Sora", "sans-serif"],
            },
            borderRadius: {
                DEFAULT: "1rem",
                lg: "1.25rem",
                xl: "1.5rem",
                "2xl": "2rem",
            },
        },
    },
    plugins: [
        typography,
        forms,
    ],
}
