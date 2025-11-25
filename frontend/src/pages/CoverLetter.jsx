import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import api from '../services/api';
import { toast } from 'react-toastify';

const CoverLetter = () => {
    const [jobs, setJobs] = useState([]);
    const [resumes, setResumes] = useState([]);
    const [selectedJob, setSelectedJob] = useState('');
    const [selectedResume, setSelectedResume] = useState('');
    const [loading, setLoading] = useState(false);
    const [generatedLetter, setGeneratedLetter] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [jobsData, resumesData] = await Promise.all([
                    api.getJobs({ limit: 100 }), // Fetch recent jobs
                    api.getResumes()
                ]);
                setJobs(jobsData.data || jobsData);
                setResumes(resumesData);
            } catch (error) {
                console.error('Error fetching data:', error);
                toast.error('Failed to load jobs or resumes');
            }
        };
        fetchData();
    }, []);

    const handleGenerate = async () => {
        if (!selectedJob || !selectedResume) {
            toast.warning('Please select both a job and a resume');
            return;
        }

        setLoading(true);
        try {
            const response = await api.generateCoverLetter(selectedJob, selectedResume);
            setGeneratedLetter(response.cover_letter || response.content || response);
            toast.success('Cover letter generated!');
        } catch (error) {
            console.error('Error generating cover letter:', error);
            toast.error('Failed to generate cover letter');
        } finally {
            setLoading(false);
        }
    };

    const handleCopy = () => {
        navigator.clipboard.writeText(generatedLetter);
        toast.success('Copied to clipboard!');
    };

    return (
        <Layout>
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Cover Letter Generator</h1>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    {/* Job Selection */}
                    <div className="bg-white shadow rounded-lg p-6">
                        <h2 className="text-lg font-medium text-gray-900 mb-4">1. Select Job</h2>
                        <select
                            value={selectedJob}
                            onChange={(e) => setSelectedJob(e.target.value)}
                            className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="">-- Select a Job --</option>
                            {jobs.map((job) => (
                                <option key={job.id} value={job.id}>
                                    {job.title} at {job.company}
                                </option>
                            ))}
                        </select>
                        {jobs.length === 0 && (
                            <p className="mt-2 text-sm text-gray-500">No jobs found. Go to "Find Jobs" to scrape some.</p>
                        )}
                    </div>

                    {/* Resume Selection */}
                    <div className="bg-white shadow rounded-lg p-6">
                        <h2 className="text-lg font-medium text-gray-900 mb-4">2. Select Resume</h2>
                        <select
                            value={selectedResume}
                            onChange={(e) => setSelectedResume(e.target.value)}
                            className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="">-- Select a Resume --</option>
                            {resumes.map((resume) => (
                                <option key={resume.id} value={resume.id}>
                                    {resume.filename || `Resume ${resume.id}`}
                                </option>
                            ))}
                        </select>
                        {resumes.length === 0 && (
                            <p className="mt-2 text-sm text-gray-500">No resumes found. Go to "Resumes" to upload one.</p>
                        )}
                    </div>
                </div>

                <div className="flex justify-center mb-8">
                    <button
                        onClick={handleGenerate}
                        disabled={loading || !selectedJob || !selectedResume}
                        className={`px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:text-lg ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
                    >
                        {loading ? 'Generating...' : 'Generate Cover Letter'}
                    </button>
                </div>

                {/* Result */}
                {generatedLetter && (
                    <div className="bg-white shadow rounded-lg p-8">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold text-gray-900">Generated Cover Letter</h2>
                            <button
                                onClick={handleCopy}
                                className="text-blue-600 hover:text-blue-800 font-medium text-sm"
                            >
                                Copy to Clipboard
                            </button>
                        </div>
                        <div className="prose max-w-none whitespace-pre-wrap text-gray-700 bg-gray-50 p-6 rounded-md border border-gray-200">
                            {generatedLetter}
                        </div>
                    </div>
                )}
            </div>
        </Layout>
    );
};

export default CoverLetter;
