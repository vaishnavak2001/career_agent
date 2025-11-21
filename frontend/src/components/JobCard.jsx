import React from 'react';

const JobCard = ({ job, onApply }) => {
    return (
        <div className="bg-white border border-gray-200 rounded-lg p-6 mb-4 hover:shadow-md transition-shadow cursor-pointer">
            <div className="flex justify-between items-start">
                <div>
                    <h2 className="text-xl font-bold text-gray-900 mb-1">{job.title}</h2>
                    <div className="text-gray-600 mb-2">{job.company}</div>
                    <div className="text-gray-500 text-sm mb-4">{job.location} • {job.type || 'Full-time'}</div>
                </div>
                {job.matchScore && (
                    <div className={`flex items-center justify-center h-12 w-12 rounded-full ${job.matchScore >= 80 ? 'bg-green-100 text-green-800' :
                            job.matchScore >= 50 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'
                        } font-bold text-sm`}>
                        {job.matchScore}%
                    </div>
                )}
            </div>

            <div className="mb-4">
                <ul className="list-disc list-inside text-gray-600 text-sm space-y-1">
                    {job.highlights && job.highlights.map((point, index) => (
                        <li key={index}>{point}</li>
                    ))}
                </ul>
            </div>

            <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
                <div className="text-xs text-gray-400">Posted {job.postedDate}</div>
                <div className="flex space-x-3">
                    <button className="text-primary font-medium text-sm hover:underline">
                        View Details
                    </button>
                    <button
                        onClick={() => onApply(job)}
                        className="bg-primary text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
                    >
                        Apply Now
                    </button>
                </div>
            </div>
        </div>
    );
};

export default JobCard;
