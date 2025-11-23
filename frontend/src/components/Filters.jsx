import React from 'react';

const Filters = ({ filters, setFilters }) => {
    return (
        <div className="space-y-6">
            {/* Match Score Filter */}
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-4">Match Score</h3>
                <div className="space-y-2">
                    <label className="flex items-center justify-between">
                        <span className="text-sm text-gray-700">Minimum: {filters.minMatchScore}%</span>
                    </label>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        step="5"
                        value={filters.minMatchScore}
                        onChange={(e) => setFilters({ ...filters, minMatchScore: parseInt(e.target.value) })}
                        className="w-full accent-blue-600"
                    />
                    <div className="flex justify-between text-xs text-gray-500">
                        <span>0%</span>
                        <span>50%</span>
                        <span>100%</span>
                    </div>
                </div>
            </div>

            {/* Job Type */}
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-4">Job Type</h3>
                <div className="space-y-3">
                    <label className="flex items-center">
                        <input
                            type="checkbox"
                            checked={filters.remote}
                            onChange={(e) => setFilters({ ...filters, remote: e.target.checked })}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-3 text-sm text-gray-700">Remote</span>
                    </label>
                    <label className="flex items-center">
                        <input
                            type="checkbox"
                            checked={filters.fullTime}
                            onChange={(e) => setFilters({ ...filters, fullTime: e.target.checked })}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-3 text-sm text-gray-700">Full-time</span>
                    </label>
                </div>
            </div>

            {/* Date Posted */}
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-4">Date Posted</h3>
                <div className="space-y-2">
                    <label className="flex items-center">
                        <input
                            type="radio"
                            name="datePosted"
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                        />
                        <span className="ml-3 text-sm text-gray-700">Last 24 hours</span>
                    </label>
                    <label className="flex items-center">
                        <input
                            type="radio"
                            name="datePosted"
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                        />
                        <span className="ml-3 text-sm text-gray-700">Last 3 days</span>
                    </label>
                    <label className="flex items-center">
                        <input
                            type="radio"
                            name="datePosted"
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                        />
                        <span className="ml-3 text-sm text-gray-700">Last 7 days</span>
                    </label>
                </div>
            </div>

            {/* Salary Estimate */}
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-4">Salary Estimate</h3>
                <div className="space-y-2">
                    {['$40,000+', '$60,000+', '$80,000+', '$100,000+', '$120,000+'].map(range => (
                        <label key={range} className="flex items-center">
                            <input
                                type="checkbox"
                                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                            />
                            <span className="ml-3 text-sm text-gray-700">{range}</span>
                        </label>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Filters;
