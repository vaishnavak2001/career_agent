const API_BASE_URL = 'http://127.0.0.1:8000';

export const api = {
    async getJobs() {
        const response = await fetch(`${API_BASE_URL}/jobs`);
        if (!response.ok) throw new Error('Failed to fetch jobs');
        return response.json();
    },

    async getStats() {
        const response = await fetch(`${API_BASE_URL}/dashboard/stats`);
        if (!response.ok) throw new Error('Failed to fetch stats');
        return response.json();
    },

    async triggerScrape(region, role) {
        const response = await fetch(`${API_BASE_URL}/jobs/scrape?region=${encodeURIComponent(region)}&role=${encodeURIComponent(role)}`, {
            method: 'POST'
        });
        if (!response.ok) throw new Error('Failed to trigger scrape');
        return response.json();
    },

    async runAgent(input) {
        const response = await fetch(`${API_BASE_URL}/agent/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input }),
        });
        if (!response.ok) throw new Error('Failed to run agent');
        return response.json();
    }
};
