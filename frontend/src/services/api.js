const getBaseUrl = () => {
    let url = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
    // Ensure URL ends with /api/v1
    if (!url.endsWith('/api/v1')) {
        // Remove trailing slash if present before appending
        url = url.replace(/\/$/, "") + '/api/v1';
    }
    return url;
};

const BASE_URL = getBaseUrl();

const api = {
    getJobs: async (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.keyword) params.append('keyword', filters.keyword);
        if (filters.location) params.append('location', filters.location);
        if (filters.skip) params.append('skip', filters.skip);
        if (filters.limit) params.append('limit', filters.limit);

        const response = await fetch(`${BASE_URL}/jobs/?${params.toString()}`);
        if (!response.ok) {
            throw new Error('Failed to fetch jobs');
        }
        return response.json();
    },

    triggerScrape: async (region, role) => {
        const params = new URLSearchParams({ region, role });
        const response = await fetch(`${BASE_URL}/jobs/scrape?${params.toString()}`, {
            method: 'POST'
        });
        if (!response.ok) {
            throw new Error('Failed to trigger scrape');
        }
        return response.json();
    },

    applyToJob: async (jobId) => {
        const response = await fetch(`${BASE_URL}/applications/apply/${jobId}`, {
            method: 'POST'
        });
        if (!response.ok) {
            throw new Error('Failed to apply to job');
        }
        return response.json();
    },

    uploadResume: async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${BASE_URL}/resumes/upload`, {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            throw new Error('Failed to upload resume');
        }
        return response.json();
    },

    getStats: async () => {
        const response = await fetch(`${BASE_URL}/dashboard/stats`);
        if (!response.ok) {
            // Return mock stats if endpoint fails (for dev/demo)
            return {
                jobs_scraped: 0,
                applications_sent: 0,
                interviews: 0,
                scams_blocked: 0
            };
        }
        return response.json();
    }
};

export default api;
