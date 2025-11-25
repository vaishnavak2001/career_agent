import React, { useState, useEffect } from 'react';
import api from '../services/api';

const ResumeViewer = ({ resumeId }) => {
    const [content, setContent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPreview = async () => {
            if (!resumeId) return;
            setLoading(true);
            try {
                const data = await api.getResumePreview(resumeId);
                setContent(data.content || data); // Adjust based on API response
            } catch (err) {
                console.error('Error fetching resume preview:', err);
                setError('Failed to load resume preview');
            } finally {
                setLoading(false);
            }
        };

        fetchPreview();
    }, [resumeId]);

    if (!resumeId) return <div className="text-gray-500 italic">Select a resume to view</div>;
    if (loading) return <div className="text-gray-500">Loading preview...</div>;
    if (error) return <div className="text-red-500">{error}</div>;

    return (
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 font-mono text-sm whitespace-pre-wrap h-[500px] overflow-y-auto">
            {content}
        </div>
    );
};

export default ResumeViewer;
