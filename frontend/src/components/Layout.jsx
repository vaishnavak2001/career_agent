import React from 'react';

const Layout = ({ children }) => {
    return (
        <div className="min-h-screen bg-[#f3f2f1] font-sans">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex">
                            <div className="flex-shrink-0 flex items-center">
                                {/* Logo */}
                                <span className="text-2xl font-bold text-blue-600 tracking-tight">CareerAgent</span>
                            </div>
                            <nav className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                <a href="#" className="border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                                    Find Jobs
                                </a>
                                <a href="#" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                                    Company Reviews
                                </a>
                                <a href="#" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                                    Salary Guide
                                </a>
                            </nav>
                        </div>
                        <div className="flex items-center space-x-4">
                            <button className="text-blue-600 font-medium text-sm hover:underline">Upload Resume</button>
                            <button className="text-blue-600 font-medium text-sm hover:underline">Sign In</button>
                            <span className="h-6 w-px bg-gray-200" aria-hidden="true"></span>
                            <button className="text-gray-500 font-medium text-sm hover:text-gray-900">Employers / Post Job</button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main>
                {children}
            </main>

            {/* Footer */}
            <footer className="bg-white border-t border-gray-200 mt-12">
                <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
                    <p className="text-center text-gray-400 text-sm">
                        &copy; 2024 Career Agent. All rights reserved.
                    </p>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
