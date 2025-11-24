const getBaseUrl = () => {
    let url = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
    if (!url.endsWith('/api/v1')) {
        url = url.replace(/\/$/, "") + '/api/v1';
    }
    return url;
};

const BASE_URL = getBaseUrl();

const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
};

const api = {
    // Auth
    login: async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        if (!response.ok) throw new Error('Login failed');
        return response.json();
    },

    register: async (email, password, fullName) => {
        const response = await fetch(`${BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, full_name: fullName })
        });
        if (!response.ok) throw new Error('Registration failed');
        return response.json();
    },

    getMe: async () => {
        const response = await fetch(`${BASE_URL}/auth/me`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error('Failed to fetch user');
        return response.json();
    },

    // Jobs
    getJobs: async (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.keyword) params.append('keyword', filters.keyword);
        if (filters.location) params.append('location', filters.location);
        if (filters.skip) params.append('skip', filters.skip);
        if (filters.limit) params.append('limit', filters.limit);

        const response = await fetch(`${BASE_URL}/jobs/?${params.toString()}`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error('Failed to fetch jobs');
        return response.json();
    },

    triggerScrape: async (region, role) => {
        const params = new URLSearchParams({ region, role });
        const response = await fetch(`${BASE_URL}/jobs/scrape?${params.toString()}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error('Failed to trigger scrape');
        return response.json();
    },

    // Applications
    applyToJob: async (jobId) => {
        const response = await fetch(`${BASE_URL}/applications/apply/${jobId}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error('Failed to apply to job');
        return response.json();
    },

    // Resumes
    uploadResume: async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${BASE_URL}/resumes/upload`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: formData
        });
        if (!response.ok) throw new Error('Failed to upload resume');
        return response.json();
    },

    // Interview Prep
    generateQuestions: async (jobTitle, company, jobDescription) => {
        const response = await fetch(`${BASE_URL}/interview/questions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            },
            body: JSON.stringify({ job_title: jobTitle, company, job_description: jobDescription })
        });
        if (!response.ok) throw new Error('Failed to generate questions');
        return response.json();
    },

    getFeedback: async (jobTitle, question, answer) => {
        const response = await fetch(`${BASE_URL}/interview/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            },
            body: JSON.stringify({ job_title: jobTitle, question, answer })
        });
        if (!response.ok) throw new Error('Failed to get feedback');
        return response.json();
    },

    // Dashboard
    getStats: async () => {
        const response = await fetch(`${BASE_URL}/dashboard/stats`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) return { jobs_scraped: 0, applications_sent: 0, interviews: 0, scams_blocked: 0 };
        return response.json();
    }
};

export default api;
