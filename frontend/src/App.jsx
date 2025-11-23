import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import JobListing from './pages/JobListing';
import Dashboard from './pages/Dashboard';
import ResumeUpload from './pages/ResumeUpload';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<JobListing />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/resumes" element={<ResumeUpload />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Router>
  );
}

export default App;
