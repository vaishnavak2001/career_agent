import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
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
    const [sortBy, setSortBy] = useState('match_score');
    const [page, setPage] = useState(1);
    const [totalJobs, setTotalJobs] = useState(0);
    const navigate = useNavigate();

    const PAGE_SIZE = 20;

    const loadJobs = useCallback(async (shouldScrape = false) => {
        try {
            setLoading(true);

            if (shouldScrape && filters.keyword && filters.location) {
                try {
                    // Trigger scrape first
                    await api.triggerScrape(filters.location, filters.keyword);
                    toast.success('Scraping started...');
                } catch (err) {
                    console.error("Scraping failed, fetching existing jobs:", err);
                    toast.warning('Scraping failed, showing existing jobs');
                }
            }

            const response = await api.getJobs({
                ...filters,
                skip: (page - 1) * PAGE_SIZE,
                limit: PAGE_SIZE
            });

            // Handle different response formats
            if (response.data && Array.isArray(response.data)) {
                setJobs(response.data);
                setTotalJobs(response.total || response.data.length);
            } else if (Array.isArray(response)) {
                setJobs(response);
                setTotalJobs(response.length);
            } else {
                setJobs([]);
                setTotalJobs(0);
            }
        } catch (error) {
            console.error('Error loading jobs:', error);
            toast.error('Failed to load jobs');
        } finally {
            setLoading(false);
        }
    }, [filters, page]);

    useEffect(() => {
        loadJobs();
    }, [loadJobs]);

    const handleApply = async (jobId) => {
        try {
            await api.applyToJob(jobId);
            toast.success('Application submitted!');
        } catch (error) {
            console.error('Error applying:', error);
            toast.error('Failed to apply to job');
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
                                onClick={() => loadJobs(true)}
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
                                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                                <h3 className="mt-2 text-sm font-medium text-gray-900">No jobs found</h3>
                                <p className="mt-1 text-sm text-gray-500">
                                    Try adjusting your search or filters to find what you're looking for.
                                </p>
                                <div className="mt-6">
                                    <button
                                        onClick={() => setFilters({ keyword: '', location: '', remote: false, fullTime: false, minMatchScore: 70 })}
                                        className="text-blue-600 hover:underline"
                                    >
                                        Clear filters
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {sortedJobs.map(job => (
                                    <JobCard
                                        key={job.id}
                                        job={job}
                                        onClick={() => navigate(`/jobs/${job.id}`)}
                                        onApply={() => handleApply(job.id)}
                                        isSelected={false}
                                    />
                                ))}
                            </div>
                        )}

                        {/* Pagination */}
                        {!loading && sortedJobs.length > 0 && (
                            <div className="mt-8 flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 rounded-lg">
                                <div className="flex flex-1 justify-between sm:hidden">
                                    <button
                                        onClick={() => setPage(p => Math.max(1, p - 1))}
                                        disabled={page === 1}
                                        className={`relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium ${page === 1 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-50'}`}
                                    >
                                        Previous
                                    </button>
                                    <button
                                        onClick={() => setPage(p => p + 1)}
                                        disabled={jobs.length < PAGE_SIZE}
                                        className={`relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium ${jobs.length < PAGE_SIZE ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-50'}`}
                                    >
                                        Next
                                    </button>
                                </div>
                                <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                                    <div>
                                        <p className="text-sm text-gray-700">
                                            Showing <span className="font-medium">{(page - 1) * PAGE_SIZE + 1}</span> to{' '}
                                            <span className="font-medium">{Math.min(page * PAGE_SIZE, totalJobs)}</span> of{' '}
                                            <span className="font-medium">{totalJobs}</span> results
                                        </p>
                                    </div>
                                    <div>
                                        <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                                            <button
                                                onClick={() => setPage(p => Math.max(1, p - 1))}
                                                disabled={page === 1}
                                                className={`relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 ${page === 1 ? 'cursor-not-allowed' : 'hover:bg-gray-50 focus:z-20'}`}
                                            >
                                                <span className="sr-only">Previous</span>
                                                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                                    <path fillRule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clipRule="evenodd" />
                                                </svg>
                                            </button>
                                            <span className="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300">
                                                Page {page}
                                            </span>
                                            <button
                                                onClick={() => setPage(p => p + 1)}
                                                disabled={jobs.length < PAGE_SIZE}
                                                className={`relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 ${jobs.length < PAGE_SIZE ? 'cursor-not-allowed' : 'hover:bg-gray-50 focus:z-20'}`}
                                            >
                                                <span className="sr-only">Next</span>
                                                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                                    <path fillRule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clipRule="evenodd" />
                                                </svg>
                                            </button>
                                        </nav>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </Layout>
    );
};

export default JobListing;
