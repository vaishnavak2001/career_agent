import React, { useState, useEffect } from 'react';
import JobCard from './JobCard';
import { api } from '../services/api';

const JobFeed = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchJobs = async () => {
        try {
            setLoading(true);
            const data = await api.getJobs();
            // Transform DB data to UI format if needed
            const formattedJobs = data.map(job => ({
                id: job.id,
                title: job.title,
                company: job.company,
                location: job.location,
                type: 'Full-time', // Default for now
                postedDate: new Date(job.posted_date).toLocaleDateString(),
                matchScore: job.match_score || 0,
                highlights: job.parsed_json?.skills || [],
                url: job.url
            }));
            setJobs(formattedJobs);
            setError(null);
        } catch (err) {
            console.error(err);
            setError('Failed to load jobs. Is the backend running?');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchJobs();
    }, []);

    const handleApply = (job) => {
        window.open(job.url, '_blank');
    };

    if (loading) return <div className="text-center py-10">Loading jobs...</div>;
    if (error) return <div className="text-center py-10 text-red-600">{error}</div>;

    return (
        <div className="max-w-3xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            <div className="mb-6 flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Recommended for you</h1>
                    <p className="text-gray-600">Based on your resume and preferences</p>
                </div>
                <button
                    onClick={fetchJobs}
                    className="text-primary hover:text-blue-700 text-sm font-medium"
                >
                    Refresh
                </button>
            </div>

            {jobs.length === 0 ? (
                <div className="text-center py-10 bg-white rounded-lg border border-gray-200">
                    <p className="text-gray-500">No jobs found yet. Try scraping some!</p>
                </div>
            ) : (
                <div className="space-y-4">
                    {jobs.map(job => (
                        <JobCard key={job.id} job={job} onApply={handleApply} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default JobFeed;
