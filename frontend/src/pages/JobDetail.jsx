import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../services/api';
import { toast } from 'react-toastify';

const JobDetail = () => {
    const { jobId } = useParams();
    const navigate = useNavigate();
    const [job, setJob] = useState(null);
    const [loading, setLoading] = useState(true);
    const [applying, setApplying] = useState(false);

    useEffect(() => {
        const fetchJob = async () => {
            try {
                const data = await api.getJobById(jobId);
                setJob(data);
            } catch (error) {
                console.error('Error fetching job:', error);
                toast.error('Failed to load job details');
                navigate('/');
            } finally {
                setLoading(false);
            }
        };

        fetchJob();
    }, [jobId, navigate]);

    const handleApply = async () => {
        setApplying(true);
        try {
            await api.applyToJob(jobId);
            toast.success('Application submitted successfully!');
        } catch (error) {
            console.error('Error applying:', error);
            toast.error('Failed to apply to job');
        } finally {
            setApplying(false);
        }
    };

    if (loading) {
        return (
            <Layout>
                <div className="min-h-screen flex items-center justify-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>
            </Layout>
        );
    }

    if (!job) return null;

    return (
        <Layout>
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <button
                    onClick={() => navigate(-1)}
                    className="mb-6 text-blue-600 hover:text-blue-800 font-medium flex items-center"
                >
                    &larr; Back to Jobs
                </button>

                <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                    <div className="px-4 py-5 sm:px-6 flex justify-between items-start">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">{job.title}</h1>
                            <p className="mt-1 max-w-2xl text-xl text-gray-500">{job.company}</p>
                            <div className="mt-2 flex items-center text-sm text-gray-500">
                                <span className="mr-4">{job.location}</span>
                                <span className="mr-4">{job.type || 'Full-time'}</span>
                                <span>Posted: {new Date(job.posted_date).toLocaleDateString()}</span>
                            </div>
                        </div>
                        <div className="flex flex-col items-end space-y-2">
                            <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                                Match Score: {job.match_score}%
                            </div>
                            <button
                                onClick={handleApply}
                                disabled={applying}
                                className={`inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${applying ? 'opacity-75 cursor-not-allowed' : ''}`}
                            >
                                {applying ? 'Applying...' : 'Apply Now'}
                            </button>
                        </div>
                    </div>
                    <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                        <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Job Description</h3>
                        <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                            {job.description}
                        </div>
                    </div>
                    {job.requirements && (
                        <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Requirements</h3>
                            <ul className="list-disc pl-5 space-y-2 text-gray-700">
                                {Array.isArray(job.requirements)
                                    ? job.requirements.map((req, i) => <li key={i}>{req}</li>)
                                    : job.requirements.split('\n').map((req, i) => <li key={i}>{req}</li>)
                                }
                            </ul>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
};

export default JobDetail;
