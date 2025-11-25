import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import api from '../services/api';
import { toast } from 'react-toastify';

const Applications = () => {
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchApplications = async () => {
            try {
                const data = await api.getApplications();
                setApplications(data);
            } catch (error) {
                console.error('Error fetching applications:', error);
                toast.error('Failed to load applications');
            } finally {
                setLoading(false);
            }
        };

        fetchApplications();
    }, []);

    const getStatusColor = (status) => {
        switch (status.toLowerCase()) {
            case 'applied': return 'bg-blue-100 text-blue-800';
            case 'interview': return 'bg-yellow-100 text-yellow-800';
            case 'rejected': return 'bg-red-100 text-red-800';
            case 'offer': return 'bg-green-100 text-green-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    return (
        <Layout>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Application History</h1>

                {loading ? (
                    <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                        <p className="mt-2 text-gray-500">Loading applications...</p>
                    </div>
                ) : applications.length === 0 ? (
                    <div className="bg-white shadow rounded-lg p-12 text-center">
                        <p className="text-gray-500 text-lg mb-4">You haven't applied to any jobs yet.</p>
                        <a href="/" className="text-blue-600 hover:text-blue-800 font-medium">Find jobs to apply for &rarr;</a>
                    </div>
                ) : (
                    <div className="bg-white shadow overflow-hidden sm:rounded-md">
                        <ul className="divide-y divide-gray-200">
                            {applications.map((app) => (
                                <li key={app.id}>
                                    <div className="px-4 py-4 sm:px-6 hover:bg-gray-50 transition-colors">
                                        <div className="flex items-center justify-between">
                                            <div className="flex flex-col">
                                                <p className="text-lg font-medium text-blue-600 truncate">{app.job_title || 'Unknown Role'}</p>
                                                <p className="text-sm text-gray-500">{app.company_name || 'Unknown Company'}</p>
                                            </div>
                                            <div className="ml-2 flex-shrink-0 flex">
                                                <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(app.status || 'applied')}`}>
                                                    {app.status || 'Applied'}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="mt-2 sm:flex sm:justify-between">
                                            <div className="sm:flex">
                                                <p className="flex items-center text-sm text-gray-500">
                                                    Applied on {new Date(app.applied_at || app.created_at).toLocaleDateString()}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </Layout>
    );
};

export default Applications;
