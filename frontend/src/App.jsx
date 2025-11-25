import React, { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';

// Eager loading for critical routes
import Login from './pages/Login';
import Register from './pages/Register';
import JobListing from './pages/JobListing';

// Lazy loading for non-critical routes
const Dashboard = lazy(() => import('./pages/Dashboard'));
const ResumeUpload = lazy(() => import('./pages/ResumeUpload'));
const Settings = lazy(() => import('./pages/Settings'));
const Interview = lazy(() => import('./pages/Interview'));
const CoverLetter = lazy(() => import('./pages/CoverLetter'));
const Applications = lazy(() => import('./pages/Applications'));
const JobDetail = lazy(() => import('./pages/JobDetail'));
const NotFound = lazy(() => import('./pages/NotFound'));

// Loading fallback component
const PageLoader = () => (
  <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
    <div className="text-center">
      <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400"></div>
      <p className="mt-4 text-gray-600 dark:text-gray-400">Loading...</p>
    </div>
  </div>
);

const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <PageLoader />;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <ThemeProvider>
      <Router>
        <AuthProvider>
          <Suspense fallback={<PageLoader />}>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              {/* Public Routes */}
              <Route path="/" element={<JobListing />} />
              <Route path="/jobs/:jobId" element={<JobDetail />} />

              {/* Protected Routes */}
              <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
              <Route path="/resumes" element={<PrivateRoute><ResumeUpload /></PrivateRoute>} />
              <Route path="/interview" element={<PrivateRoute><Interview /></PrivateRoute>} />
              <Route path="/cover-letter" element={<PrivateRoute><CoverLetter /></PrivateRoute>} />
              <Route path="/applications" element={<PrivateRoute><Applications /></PrivateRoute>} />
              <Route path="/settings" element={<PrivateRoute><Settings /></PrivateRoute>} />

              {/* 404 Catch-all */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </Suspense>
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default App;
