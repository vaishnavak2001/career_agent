import React, { useState } from 'react';
import Layout from '../components/Layout';

const Settings = () => {
    const [settings, setSettings] = useState({
        targetRole: 'Software Engineer',
        targetRegion: 'San Francisco',
        minSalary: '120000',
        remoteOnly: false,
        autoApply: false,
        maxApplicationsPerDay: 5
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setSettings(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSave = (e) => {
        e.preventDefault();
        // TODO: Save to backend
        alert('Settings saved!');
    };

    return (
        <Layout>
            <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="bg-white shadow sm:rounded-lg overflow-hidden">
                    <div className="px-4 py-5 sm:px-6 bg-gray-50 border-b border-gray-200">
                        <h3 className="text-lg leading-6 font-medium text-gray-900">
                            Agent Settings
                        </h3>
                        <p className="mt-1 text-sm text-gray-500">
                            Configure how the autonomous agent behaves.
                        </p>
                    </div>
                    <div className="px-4 py-5 sm:p-6">
                        <form onSubmit={handleSave} className="space-y-6">
                            <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                                <div className="sm:col-span-3">
                                    <label htmlFor="targetRole" className="block text-sm font-medium text-gray-700">
                                        Target Role
                                    </label>
                                    <div className="mt-1">
                                        <input
                                            type="text"
                                            name="targetRole"
                                            id="targetRole"
                                            value={settings.targetRole}
                                            onChange={handleChange}
                                            className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-3">
                                    <label htmlFor="targetRegion" className="block text-sm font-medium text-gray-700">
                                        Target Region
                                    </label>
                                    <div className="mt-1">
                                        <input
                                            type="text"
                                            name="targetRegion"
                                            id="targetRegion"
                                            value={settings.targetRegion}
                                            onChange={handleChange}
                                            className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-3">
                                    <label htmlFor="minSalary" className="block text-sm font-medium text-gray-700">
                                        Minimum Salary (USD)
                                    </label>
                                    <div className="mt-1">
                                        <input
                                            type="number"
                                            name="minSalary"
                                            id="minSalary"
                                            value={settings.minSalary}
                                            onChange={handleChange}
                                            className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-3">
                                    <label htmlFor="maxApplicationsPerDay" className="block text-sm font-medium text-gray-700">
                                        Max Applications / Day
                                    </label>
                                    <div className="mt-1">
                                        <input
                                            type="number"
                                            name="maxApplicationsPerDay"
                                            id="maxApplicationsPerDay"
                                            value={settings.maxApplicationsPerDay}
                                            onChange={handleChange}
                                            className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="flex items-start">
                                <div className="flex items-center h-5">
                                    <input
                                        id="remoteOnly"
                                        name="remoteOnly"
                                        type="checkbox"
                                        checked={settings.remoteOnly}
                                        onChange={handleChange}
                                        className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                                    />
                                </div>
                                <div className="ml-3 text-sm">
                                    <label htmlFor="remoteOnly" className="font-medium text-gray-700">Remote Only</label>
                                    <p className="text-gray-500">Only apply to remote positions.</p>
                                </div>
                            </div>

                            <div className="flex items-start">
                                <div className="flex items-center h-5">
                                    <input
                                        id="autoApply"
                                        name="autoApply"
                                        type="checkbox"
                                        checked={settings.autoApply}
                                        onChange={handleChange}
                                        className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                                    />
                                </div>
                                <div className="ml-3 text-sm">
                                    <label htmlFor="autoApply" className="font-medium text-gray-700">Auto-Apply Mode</label>
                                    <p className="text-gray-500">Allow the agent to submit applications automatically without review (Sandbox mode recommended first).</p>
                                </div>
                            </div>

                            <div className="pt-5">
                                <div className="flex justify-end">
                                    <button
                                        type="submit"
                                        className="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                                    >
                                        Save Settings
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default Settings;
