import React from 'react';
import Header from './Header';

const Layout = ({ children }) => {
    return (
        <div className="bg-surface-light dark:bg-background-dark text-text-light-primary dark:text-text-dark-primary h-screen flex flex-col overflow-hidden font-display antialiased">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full flex-shrink-0">
                <Header />
            </div>
            <main className="flex-grow flex flex-col max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full pb-6 h-full overflow-hidden">
                {children}
            </main>
        </div>
    );
};

export default Layout;
