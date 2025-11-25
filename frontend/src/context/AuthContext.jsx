import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import api from '../services/api';

const AuthContext = createContext(null);

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // Check if user is authenticated on mount
    useEffect(() => {
        const initAuth = async () => {
            const savedToken = localStorage.getItem('token');
            if (savedToken) {
                try {
                    const userData = await api.getMe();
                    setUser(userData);
                    setToken(savedToken);
                } catch (error) {
                    console.error('Failed to fetch user:', error);
                    // Token is invalid, clear it
                    localStorage.removeItem('token');
                    setToken(null);
                }
            }
            setLoading(false);
        };

        initAuth();
    }, []);

    const login = async (username, password) => {
        try {
            const response = await api.login(username, password);
            const accessToken = response.access_token;

            localStorage.setItem('token', accessToken);
            setToken(accessToken);

            // Fetch user data
            const userData = await api.getMe();
            setUser(userData);

            toast.success('Welcome back!');
            navigate('/dashboard');

            return { success: true };
        } catch (error) {
            console.error('Login error:', error);
            toast.error('Invalid credentials. Please try again.');
            return { success: false, error: error.message };
        }
    };

    const register = async (email, password, fullName) => {
        try {
            await api.register(email, password, fullName);
            toast.success('Account created! Please log in.');
            navigate('/login');
            return { success: true };
        } catch (error) {
            console.error('Registration error:', error);
            toast.error('Registration failed. Email may already be in use.');
            return { success: false, error: error.message };
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        toast.info('You have been logged out.');
        navigate('/login');
    };

    const value = {
        user,
        token,
        isAuthenticated: !!token,
        loading,
        login,
        register,
        logout
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;
