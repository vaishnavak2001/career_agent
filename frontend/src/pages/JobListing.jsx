import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import JobCard from '../components/JobCard';
import Filters from '../components/Filters';
import api from '../services/api';

const JobListing = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filters, setFilters] = useState({
        keyword: '',
        location: '',
        remote: false,
        fullTime: false,
        minMatchScore: 70
    });
    const [selectedJob, setSelectedJob] = useState(null);
    const [sortBy, setSortBy] = useState('match_score');

    useEffect(() => {
        loadJobs();
    }, [filters]);

    const loadJobs = async () => {
        try {
            setLoading(true);
            const response = await api.getJobs(filters);
            setJobs(response.data);
        } catch (error) {
            console.error('Error loading jobs:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleApply = async (jobId) => {
        try {
            await api.applyToJob(jobId);
            alert('Application submitted!');
        } catch (error) {
            console.error('Error applying:', error);
        }
    };

    const sortedJobs = [...jobs].sort((a, b) => {
        if (sortBy === 'match_score') return (b.match_score || 0) - (a.match_score || 0);
        if (sortBy === 'posted_date') return new Date(b.posted_date) - new Date(a.posted_date);
        return 0;
    });

    return (
        <Layout>
            <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-8">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h1 className="text-3xl font-bold mb-6">Find Your Next Opportunity</h1>

                    {/* Search Bar */}
                    <div className="bg-white rounded-lg shadow-lg p-4">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="relative">
                                <input
                                    type="text"
                                    placeholder="Job title, keywords, or company"
                                    value={filters.keyword}
                                    onChange={(e) => setFilters({ ...filters, keyword: e.target.value })}
                                    className="w-full px-4 py-3 border border-gray-300 rounded-md text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                />
                            </div>
                            <div className="relative">
                                <input
                                    type="text"
                                    placeholder="City, state, or remote"
                                    value={filters.location}
                                    onChange={(e) => setFilters({ ...filters, location: e.target.value })}
                                    className="w-full px-4 py-3 border border-gray-300 rounded-md text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                />
                            </div>
                            <button
                                onClick={loadJobs}
                                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-md font-semibold transition-colors"
                            >
                                Find Jobs
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    {/* Sidebar Filters */}
                    <div className="lg:col-span-1">
                        <Filters filters={filters} setFilters={setFilters} />
                    </div>

                    {/* Job List */}
                    <div className="lg:col-span-3">
                        <div className="mb-4 flex justify-between items-center">
                            <h2 className="text-xl font-bold text-gray-900">
                                {jobs.length} Jobs Found
                            </h2>
                            <select
                                value={sortBy}
                                onChange={(e) => setSortBy(e.target.value)}
                                className="border border-gray-300 rounded-md px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="match_score">Best Match</option>
                                <option value="posted_date">Date Posted</option>
                            </select>
                        </div>

                        {loading ? (
                            <div className="space-y-4">
                                {[1, 2, 3, 4].map((i) => (
                                    <div key={i} className="bg-white border border-gray-200 rounded-lg p-6 animate-pulse">
                                        <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                                        <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
                                        <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                                    </div>
                                ))}
                            </div>
                        ) : sortedJobs.length === 0 ? (
                            <div className="bg-white border border-gray-200 rounded-lg p-12 text-center">
                                <p className="text-gray-500 mb-4">No jobs found matching your criteria.</p>
                                <button
                                    onClick={() => setFilters({ keyword: '', location: '', remote: false, fullTime: false, minMatchScore: 70 })}
                                    className="text-blue-600 hover:underline"
                                >
                                    Clear filters
                                </button>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {sortedJobs.map(job => (
                                    <JobCard
                                        key={job.id}
                                        job={job}
                                        onClick={() => setSelectedJob(job)}
                                        onApply={() => handleApply(job.id)}
                                        isSelected={selectedJob?.id === job.id}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </Layout>
    );
};

export default JobListing;
