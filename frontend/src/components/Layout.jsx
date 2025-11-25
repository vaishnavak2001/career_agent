import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

const Layout = ({ children }) => {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const auth = useAuth();
    const { user, logout, isAuthenticated } = auth || {};
    const { darkMode, toggleDarkMode } = useTheme();
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path
            ? "border-blue-500 text-gray-900 dark:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
            : "border-transparent text-gray-500 dark:text-gray-400 hover:border-gray-300 hover:text-gray-700 dark:hover:text-gray-200 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors";
    };

    const mobileNavClass = (path) => {
        return location.pathname === path
            ? "bg-blue-50 dark:bg-blue-900 border-blue-500 text-blue-700 dark:text-blue-200 block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition-colors"
            : "border-transparent text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 hover:border-gray-300 hover:text-gray-800 dark:hover:text-gray-100 block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition-colors";
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 font-sans transition-colors duration-300">
            {/* Header */}
            <header className="glass sticky top-0 z-50 border-b border-gray-200 dark:border-gray-700 animate-fade-in">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex">
                            <div className="flex-shrink-0 flex items-center">
                                {/* Logo with gradient */}
                                <Link
                                    to="/"
                                    className="text-2xl font-bold gradient-primary text-transparent tracking-tight hover-scale"
                                    style={{ WebkitBackgroundClip: 'text', backgroundClip: 'text' }}
                                >
                                    CareerAgent
                                </Link>
                            </div>
                            {/* Desktop Navigation */}
                            <nav className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                <Link to="/" className={isActive('/')}>
                                    Find Jobs
                                </Link>
                                {isAuthenticated && (
                                    <>
                                        <Link to="/dashboard" className={isActive('/dashboard')}>
                                            Dashboard
                                        </Link>
                                        <Link to="/resumes" className={isActive('/resumes')}>
                                            Resumes
                                        </Link>
                                        <Link to="/interview" className={isActive('/interview')}>
                                            Interview Prep
                                        </Link>
                                        <Link to="/cover-letter" className={isActive('/cover-letter')}>
                                            Cover Letters
                                        </Link>
                                        <Link to="/applications" className={isActive('/applications')}>
                                            Applications
                                        </Link>
                                        <Link to="/settings" className={isActive('/settings')}>
                                            Settings
                                        </Link>
                                    </>
                                )}
                            </nav>
                        </div>

                        {/* Desktop Actions */}
                        <div className="hidden sm:flex items-center space-x-4">
                            {/* Dark Mode Toggle */}
                            <button
                                onClick={toggleDarkMode}
                                className="p-2 rounded-md text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all hover-scale"
                                aria-label="Toggle dark mode"
                            >
                                {darkMode ? (
                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                                    </svg>
                                ) : (
                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                                    </svg>
                                )}
                            </button>

                            {isAuthenticated ? (
                                <>
                                    <span className="text-sm text-gray-700 dark:text-gray-300 hidden md:block">
                                        Hello, {user?.full_name || 'User'}
                                    </span>
                                    <button
                                        onClick={logout}
                                        className="text-blue-600 dark:text-blue-400 font-medium text-sm hover:underline transition-colors"
                                    >
                                        Sign Out
                                    </button>
                                </>
                            ) : (
                                <>
                                    <Link to="/login" className="text-blue-600 dark:text-blue-400 font-medium text-sm hover:underline transition-colors">
                                        Upload Resume
                                    </Link>
                                    <Link to="/login" className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm rounded-md transition-all hover-scale">
                                        Sign In
                                    </Link>
                                </>
                            )}
                        </div>

                        {/* Mobile menu button */}
                        <div className="flex items-center sm:hidden space-x-2">
                            {/* Mobile Dark Mode Toggle */}
                            <button
                                onClick={toggleDarkMode}
                                className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800"
                                aria-label="Toggle dark mode"
                            >
                                {darkMode ? (
                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                                    </svg>
                                ) : (
                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                                    </svg>
                                )}
                            </button>

                            <button
                                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 dark:text-gray-300 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 transition-all"
                                aria-expanded="false"
                            >
                                <span className="sr-only">Open main menu</span>
                                {!mobileMenuOpen ? (
                                    <svg className="block h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                                    </svg>
                                ) : (
                                    <svg className="block h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                )}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Mobile menu */}
                {mobileMenuOpen && (
                    <div className="sm:hidden border-t border-gray-200 dark:border-gray-700 glass animate-slide-in-right">
                        <div className="pt-2 pb-3 space-y-1">
                            <Link to="/" className={mobileNavClass('/')} onClick={() => setMobileMenuOpen(false)}>Find Jobs</Link>
                            {isAuthenticated && (
                                <>
                                    <Link to="/dashboard" className={mobileNavClass('/dashboard')} onClick={() => setMobileMenuOpen(false)}>Dashboard</Link>
                                    <Link to="/resumes" className={mobileNavClass('/resumes')} onClick={() => setMobileMenuOpen(false)}>Resumes</Link>
                                    <Link to="/interview" className={mobileNavClass('/interview')} onClick={() => setMobileMenuOpen(false)}>Interview Prep</Link>
                                    <Link to="/cover-letter" className={mobileNavClass('/cover-letter')} onClick={() => setMobileMenuOpen(false)}>Cover Letters</Link>
                                    <Link to="/applications" className={mobileNavClass('/applications')} onClick={() => setMobileMenuOpen(false)}>Applications</Link>
                                    <Link to="/settings" className={mobileNavClass('/settings')} onClick={() => setMobileMenuOpen(false)}>Settings</Link>
                                </>
                            )}
                        </div>
                        <div className="pt-4 pb-3 border-t border-gray-200 dark:border-gray-700">
                            {isAuthenticated ? (
                                <div className="space-y-1">
                                    <div className="px-4 py-2">
                                        <div className="text-base font-medium text-gray-800 dark:text-gray-200">{user?.full_name || 'User'}</div>
                                        <div className="text-sm font-medium text-gray-500 dark:text-gray-400">{user?.email || ''}</div>
                                    </div>
                                    <button onClick={() => { logout(); setMobileMenuOpen(false); }} className="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">Sign out</button>
                                </div>
                            ) : (
                                <div className="space-y-1">
                                    <Link to="/login" className="block px-4 py-2 text-base font-medium text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors" onClick={() => setMobileMenuOpen(false)}>Sign In</Link>
                                    <Link to="/register" className="block px-4 py-2 text-base font-medium text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors" onClick={() => setMobileMenuOpen(false)}>Register</Link>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </header>

            {/* Main Content */}
            <main className="animate-fade-in">
                {children}
            </main>

            {/* Footer */}
            <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12 transition-colors">
                <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
                    <p className="text-center text-gray-400 dark:text-gray-500 text-sm">
                        &copy; 2024 Career Agent. All rights reserved.
                    </p>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
