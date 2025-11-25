import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import api from '../services/api';

const StatCard = ({ title, value, change, positive }) => (
    <div className="glass card-hover overflow-hidden shadow-lg rounded-lg animate-fade-in">
        <div className="p-5">
            <div className="flex items-center">
                <div className="ml-5 w-0 flex-1">
                    <dl>
                        <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">{title}</dt>
                        <dd>
                            <div className="text-lg font-medium text-gray-900 dark:text-gray-100">{value}</div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
        <div className="bg-gray-50 dark:bg-gray-800 bg-opacity-50 px-5 py-3 transition-colors">
            <div className="text-sm">
                <span className={`font-medium ${positive ? 'text-green-700 dark:text-green-400' : 'text-red-700 dark:text-red-400'}`}>
                    {change}
                </span>{' '}
                <span className="text-gray-500 dark:text-gray-400">from last week</span>
            </div>
        </div>
    </div>
);

const Dashboard = () => {
    const [stats, setStats] = useState({
        jobs_scraped: 0,
        applications_sent: 0,
        interviews: 0,
        scams_blocked: 0
    });
    const [scraping, setScraping] = useState(false);

    const fetchStats = async () => {
        try {
            const data = await api.getStats();
            setStats(data);
        } catch (e) {
            console.error("Failed to fetch stats", e);
        }
    };

    useEffect(() => {
        fetchStats();
    }, []);

    const handleScrape = async () => {
        setScraping(true);
        try {
            await api.triggerScrape('San Francisco', 'Python Developer');
            toast.success('Scraping started! Refresh the feed in a moment.');
            fetchStats();
        } catch (error) {
            console.error('Scraping error:', error);
            toast.error('Failed to start scraping');
        } finally {
            setScraping(false);
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100">Overview</h2>
                <button
                    onClick={handleScrape}
                    disabled={scraping}
                    className={`bg-primary text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 dark:hover:bg-blue-600 transition-all hover-scale ${scraping ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                    {scraping ? 'Scraping...' : 'Scrape New Jobs'}
                </button>
            </div>

            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
                <StatCard title="Jobs Scraped" value={stats.jobs_scraped} change="+12%" positive={true} />
                <StatCard title="Applications Sent" value={stats.applications_sent} change="+5%" positive={true} />
                <StatCard title="Interviews" value={stats.interviews} change="0%" positive={true} />
                <StatCard title="Scams Blocked" value={stats.scams_blocked} change="-2%" positive={false} />
            </div>
        </div>
    );
};

export default Dashboard;
