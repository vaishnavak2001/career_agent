import React from 'react';

const JobCard = ({ job, onClick, onApply, isSelected }) => {
    const matchScoreColor = (score) => {
        if (score >= 85) return 'text-green-700 bg-green-100';
        if (score >= 70) return 'text-yellow-700 bg-yellow-100';
        return 'text-gray-700 bg-gray-100';
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 1) return 'Posted today';
        if (diffDays < 7) return `Posted ${diffDays} days ago`;
        return `Posted ${Math.floor(diffDays / 7)} weeks ago`;
    };

    return (
        <div
            className={`glass card-hover border rounded-lg p-5 cursor-pointer animate-fade-in ${isSelected ? 'border-blue-500 dark:border-blue-400 shadow-md' : 'border-gray-200 dark:border-gray-700'
                }`}
            onClick={onClick}
        >
            <div className="flex justify-between items-start">
                <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 hover:text-blue-600 dark:hover:text-blue-400 mb-1 transition-colors">
                        {job.title}
                    </h3>
                    <p className="text-gray-700 dark:text-gray-300 font-medium mb-2">{job.company}</p>
                    <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mb-3">
                        <span className="flex items-center">
                            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            {job.location}
                        </span>
                        {job.is_remote && (
                            <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                                Remote
                            </span>
                        )}
                    </div>

                    {job.parsed_json?.required_skills && (
                        <div className="flex flex-wrap gap-2 mb-3">
                            {job.parsed_json.required_skills.slice(0, 4).map((skill, idx) => (
                                <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
                                    {skill}
                                </span>
                            ))}
                        </div>
                    )}

                    <div className="flex items-center gap-4 text-xs text-gray-500">
                        <span>{formatDate(job.posted_date || job.scraped_at)}</span>
                        <span>•</span>
                        <span>{job.source}</span>
                        {job.is_scam && (
                            <>
                                <span>•</span>
                                <span className="text-red-600 font-semibold">⚠️ Potential Scam</span>
                            </>
                        )}
                    </div>
                </div>

                <div className="flex flex-col items-end gap-3 ml-4">
                    {job.match_score !== undefined && (
                        <div className={`px-3 py-1 rounded-full text-sm font-semibold ${matchScoreColor(job.match_score)}`}>
                            {job.match_score}% Match
                        </div>
                    )}
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onApply();
                        }}
                        disabled={job.is_scam}
                        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${job.is_scam
                            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                            : 'bg-blue-600 text-white hover:bg-blue-700'
                            }`}
                    >
                        {job.is_scam ? 'Flagged' : 'Apply'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default JobCard;
