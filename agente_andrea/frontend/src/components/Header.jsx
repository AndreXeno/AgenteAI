import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
    const location = useLocation();

    const isActive = (path) => {
        const activeClasses = "text-primary font-semibold border-b-2 border-primary pb-1";
        const inactiveClasses = "text-text-light-secondary dark:text-text-dark-secondary hover:text-text-light-primary dark:hover:text-text-dark-primary transition-colors";
        return location.pathname === path ? activeClasses : inactiveClasses;
    }

    return (
        <header className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-8">
                <Link to="/" className="flex items-center space-x-2">
                    <svg className="w-8 h-8 text-primary" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M11.9999 15.0832C11.9999 15.0832 8.41659 14.0832 7.16659 10.4998C5.91659 6.9165 8.91659 3.58317 11.9999 4.4165C15.0832 5.24984 16.9166 9.4165 11.9999 15.0832Z"
                            fill="#45D4B3"></path>
                        <path
                            d="M12.0001 15.0832C12.0001 15.0832 15.5834 14.0832 16.8334 10.4998C18.0834 6.9165 15.0834 3.58317 12.0001 4.4165C8.91675 5.24984 7.08342 9.4165 12.0001 15.0832Z"
                            fill="#45D4B3" fillOpacity="0.6"></path>
                        <path d="M12 15.0833V20.5" stroke="#45D4B3" strokeLinecap="round" strokeWidth="1.5"></path>
                    </svg>
                    <span className="font-bold text-xl text-text-light-primary dark:text-text-dark-primary">Mind&Body</span>
                </Link>
                <nav className="hidden md:flex items-center space-x-8 text-text-light-secondary dark:text-text-dark-secondary">
                    <Link className={isActive('/nutrition')} to="/nutrition">Nutrizione</Link>
                    <Link className={isActive('#')} to="#">Allenamento</Link>
                    <Link className={isActive('/mental-wellbeing')} to="/mental-wellbeing">Benessere Mentale</Link>
                    <Link className={isActive('#')} to="#">Community</Link>
                </nav>
            </div>

            <div className="flex items-center space-x-4">
                <button className="p-2 rounded-full hover:bg-white dark:hover:bg-surface-dark transition-colors">
                    <span className="material-symbols-outlined text-text-light-secondary dark:text-text-dark-secondary">notifications</span>
                </button>
                <div className="w-10 h-10 bg-orange-200 rounded-full"></div>
            </div>
        </header>
    );
};

export default Header;
