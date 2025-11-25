import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '../context/ThemeContext';
import { AuthProvider } from '../context/AuthContext';
import NotFound from '../pages/NotFound';

describe('NotFound Page', () => {
    const renderWithProviders = (component) => {
        return render(
            <BrowserRouter>
                <ThemeProvider>
                    <AuthProvider>
                        {component}
                    </AuthProvider>
                </ThemeProvider>
            </BrowserRouter>
        );
    };

    it('renders 404 heading', () => {
        renderWithProviders(<NotFound />);
        const heading = screen.getByText('404');
        expect(heading).toBeInTheDocument();
    });

    it('renders page not found message', () => {
        renderWithProviders(<NotFound />);
        const message = screen.getByText('Page Not Found');
        expect(message).toBeInTheDocument();
    });

    it('renders home link', () => {
        renderWithProviders(<NotFound />);
        const homeLink = screen.getByText('Go Home');
        expect(homeLink).toBeInTheDocument();
        expect(homeLink.closest('a')).toHaveAttribute('href', '/');
    });

    it('renders dashboard link', () => {
        renderWithProviders(<NotFound />);
        const dashboardLink = screen.getByText('Dashboard');
        expect(dashboardLink).toBeInTheDocument();
        expect(dashboardLink.closest('a')).toHaveAttribute('href', '/dashboard');
    });
});
