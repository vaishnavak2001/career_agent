// API Base URL
const API_BASE = 'http://127.0.0.1:8000';

// State
let currentResume = '';
let jobs = [];
let dashboardData = null;

// DOM Elements
const jobsTab = document.getElementById('jobsTab');
const dashboardTab = document.getElementById('dashboardTab');
const resumeTab = document.getElementById('resumeTab');
const navLinks = document.querySelectorAll('.nav-link');
const jobsGrid = document.getElementById('jobsGrid');
const searchBtn = document.getElementById('searchBtn');
const roleInput = document.getElementById('roleInput');
const locationInput = document.getElementById('locationInput');
const modal = document.getElementById('jobModal');
const modalOverlay = document.getElementById('modalOverlay');
const modalClose = document.getElementById('modalClose');

// Tab Switching
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const tabName = link.dataset.tab;

        // Update active nav
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');

        // Show correct tab
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });

        if (tabName === 'jobs') {
            jobsTab.classList.add('active');
        } else if (tabName === 'dashboard') {
            dashboardTab.classList.add('active');
            loadDashboard();
        } else if (tabName === 'resume') {
            resumeTab.classList.add('active');
        }
    });
});

// Search Jobs
searchBtn.addEventListener('click', async () => {
    const role = roleInput.value || 'Software Engineer';
    const location = locationInput.value || 'Remote';

    searchBtn.disabled = true;
    searchBtn.innerHTML = '<span>Searching...</span>';

    try {
        const response = await fetch(`${API_BASE}/jobs/scrape`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                region: location,
                role: role,
                platforms: ['LinkedIn', 'Indeed']
            })
        });

        if (response.ok) {
            await loadJobs();
        }
    } catch (error) {
        console.error('Search error:', error);
    } finally {
        searchBtn.disabled = false;
        searchBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M9 2C5.13 2 2 5.13 2 9C2 12.87 5.13 16 9 16C12.87 16 16 12.87 16 9C16 5.13 12.87 2 9 2Z" stroke="white" stroke-width="2"/>
                <path d="M14 14L18 18" stroke="white" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Find Jobs
        `;
    }
});

// Load Jobs
async function loadJobs() {
    const excludeScams = document.getElementById('excludeScamsFilter').checked;
    const minMatch = document.getElementById('matchFilter').value;

    jobsGrid.innerHTML = '<div class="loading">Loading jobs...</div>';

    try {
        const response = await fetch(
            `${API_BASE}/jobs?exclude_scams=${excludeScams}&min_match_score=${minMatch}`
        );
        const data = await response.json();
        jobs = data.jobs || [];

        // Update stats
        document.getElementById('totalJobs').textContent = data.count || 0;
        document.getElementById('highMatchJobs').textContent =
            jobs.filter(j => j.match_score >= 70).length;

        // Render jobs
        if (jobs.length === 0) {
            jobsGrid.innerHTML = `
                <div class="empty-state">
                    <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                        <rect x="8" y="16" width="48" height="40" rx="4" stroke="currentColor" stroke-width="3"/>
                        <circle cx="32" cy="32" r="8" stroke="currentColor" stroke-width="3"/>
                    </svg>
                    <h3>No jobs found</h3>
                    <p>Try searching for jobs using the search bar above</p>
                </div>
            `;
        } else {
            jobsGrid.innerHTML = jobs.map(job => createJobCard(job)).join('');

            // Add click handlers
            document.querySelectorAll('.job-card').forEach((card, index) => {
                card.addEventListener('click', () => openJobModal(jobs[index]));
            });
        }
    } catch (error) {
        console.error('Load jobs error:', error);
        jobsGrid.innerHTML = '<div class="error">Failed to load jobs</div>';
    }
}

// Create Job Card
function createJobCard(job) {
    const matchClass = job.match_score >= 70 ? 'match-high' :
        job.match_score >= 50 ? 'match-medium' : 'match-low';

    const skills = job.parsed_data?.skills || [];
    const scamBadge = job.is_scam ? '<span class="scam-badge">⚠️ Potential Scam</span>' : '';

    return `
        <div class="job-card" data-job-id="${job.id}">
            <div class="job-card-header">
                <div>
                    <div class="job-title">${job.title}</div>
                    <div class="job-company">${job.company}</div>
                </div>
                <div class="match-badge ${matchClass}">
                    ${job.match_score ? `${Math.round(job.match_score)}% Match` : 'Not scored'}
                </div>
            </div>
            <div class="job-meta">
                <span>📍 ${job.location}</span>
                <span>🕒 ${formatDate(job.scraped_at)}</span>
                ${scamBadge}
            </div>
            <div class="job-description">
                ${job.raw_description ? job.raw_description.substring(0, 200) + '...' : 'No description available'}
            </div>
            ${skills.length > 0 ? `
                <div class="job-skills">
                    ${skills.slice(0, 5).map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `;
}

// Open Job Modal
async function openJobModal(job) {
    document.getElementById('modalJobTitle').textContent = job.title;
    document.getElementById('modalCompany').textContent = job.company;
    document.getElementById('modalLocation').textContent = job.location;
    document.getElementById('modalDescription').textContent =
        job.raw_description || 'No description available';

    const matchClass = job.match_score >= 70 ? 'match-high' :
        job.match_score >= 50 ? 'match-medium' : 'match-low';
    const matchBadge = document.getElementById('modalMatch');
    matchBadge.className = `match-badge ${matchClass}`;
    matchBadge.textContent = job.match_score ? `${Math.round(job.match_score)}% Match` : 'Not scored';

    const skills = job.parsed_data?.skills || [];
    if (skills.length > 0) {
        document.getElementById('modalSkills').innerHTML = `
            <div class="job-skills">
                ${skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
            </div>
        `;
    }

    // Cover letter button
    document.getElementById('generateCoverLetterBtn').onclick = async () => {
        await generateCoverLetter(job.id);
    };

    modal.classList.add('active');
}

// Close Modal
modalClose.addEventListener('click', () => modal.classList.remove('active'));
modalOverlay.addEventListener('click', () => modal.classList.remove('active'));

// Generate Cover Letter
async function generateCoverLetter(jobId) {
    const resume = document.getElementById('resumeText').value ||
        'Experienced software engineer with 5+ years in full-stack development';

    const coverLetterSection = document.getElementById('coverLetterSection');
    const coverLetterText = document.getElementById('coverLetterText');

    coverLetterSection.style.display = 'block';
    coverLetterText.value = 'Generating cover letter...';

    try {
        const response = await fetch(`${API_BASE}/cover-letter/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                job_id: jobId,
                resume_text: resume,
                personality: 'professional'
            })
        });

        const data = await response.json();
        coverLetterText.value = data.cover_letter;
    } catch (error) {
        console.error('Cover letter error:', error);
        coverLetterText.value = 'Failed to generate cover letter. Please try again.';
    }
}

// Load Dashboard
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard/stats`);
        const data = await response.json();
        dashboardData = data;

        // Update metrics
        document.getElementById('metricJobsScraped').textContent =
            data.overview.total_jobs_scraped;
        document.getElementById('metricMatched').textContent =
            data.overview.matched_jobs;
        document.getElementById('metricApplications').textContent =
            data.overview.total_applied;
        document.getElementById('metricScams').textContent =
            data.overview.scams_detected;

        document.getElementById('metricMatchRate').textContent =
            `${data.performance.match_rate}% match rate`;
        document.getElementById('metricAppSuccess').textContent =
            `${Math.round(data.performance.application_success_rate * 100)}% success rate`;

        // Top skills
        const skillsList = document.getElementById('topSkillsList');
        if (data.top_skills && data.top_skills.length > 0) {
            skillsList.innerHTML = data.top_skills.map(skill => `
                <div class="skill-item">
                    <span class="skill-name">${skill.skill}</span>
                    <span class="skill-count">${skill.count} jobs</span>
                </div>
            `).join('');
        } else {
            skillsList.innerHTML = '<div class="empty-state">No skills data yet</div>';
        }

        // Companies
        const companiesList = document.getElementById('companiesList');
        if (data.company_breakdown && data.company_breakdown.length > 0) {
            companiesList.innerHTML = data.company_breakdown.map(company => `
                <div class="company-item">
                    <span class="company-name">${company.company}</span>
                    <span class="company-count">${company.jobs} jobs</span>
                </div>
            `).join('');
        } else {
            companiesList.innerHTML = '<div class="empty-state">No company data yet</div>';
        }
    } catch (error) {
        console.error('Dashboard error:', error);
    }
}

// Resume Functions
document.getElementById('saveResumeBtn').addEventListener('click', () => {
    currentResume = document.getElementById('resumeText').value;
    alert('Resume saved! Use it for match scoring and cover letters.');
});

document.getElementById('searchProjectsBtn').addEventListener('click', async () => {
    const keywords = document.getElementById('projectKeywords').value.split(',').map(k => k.trim());
    const projectsList = document.getElementById('projectsList');

    projectsList.innerHTML = '<div class="loading">Searching projects...</div>';

    try {
        const response = await fetch(`${API_BASE}/projects/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(keywords)
        });

        const data = await response.json();
        const projects = data.projects || [];

        if (projects.length > 0) {
            projectsList.innerHTML = projects.map(project => `
                <div class="project-item">
                    <div class="project-name">${project.name}</div>
                    <div class="project-description">${project.description}</div>
                    <a href="${project.url}" target="_blank" class="project-url">View on ${project.source}</a>
                </div>
            `).join('');
        } else {
            projectsList.innerHTML = '<div class="empty-state">No projects found</div>';
        }
    } catch (error) {
        console.error('Project search error:', error);
    }
});

// Filter Change Handlers
document.getElementById('excludeScamsFilter').addEventListener('change', loadJobs);
document.getElementById('matchFilter').addEventListener('change', loadJobs);

// Utility Functions
function formatDate(dateString) {
    if (!dateString) return 'Recently';
    const date = new Date(dateString);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000 / 60 / 60 / 24);

    if (diff === 0) return 'Today';
    if (diff === 1) return 'Yesterday';
    if (diff < 7) return `${diff} days ago`;
    return date.toLocaleDateString();
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadJobs();
});
