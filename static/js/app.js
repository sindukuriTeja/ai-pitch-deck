let selectedTheme = null;
let currentStep = 1;
let ws = null;

// Icons map for themes
const ICONS = {
    rocket: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path></svg>',
    heart: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>',
    chart: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="20" x2="12" y2="10"></line><line x1="18" y1="20" x2="18" y2="4"></line><line x1="6" y1="20" x2="6" y2="16"></line></svg>',
    palette: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="8" r="1.5" fill="currentColor"></circle><circle cx="8" cy="12" r="1.5" fill="currentColor"></circle><circle cx="16" cy="12" r="1.5" fill="currentColor"></circle><circle cx="12" cy="16" r="1.5" fill="currentColor"></circle></svg>',
    cart: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>',
    book: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>',
    building: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="6" x2="9" y2="6"></line><line x1="15" y1="6" x2="15" y2="6"></line><line x1="9" y1="10" x2="9" y2="10"></line><line x1="15" y1="10" x2="15" y2="10"></line><line x1="9" y1="14" x2="9" y2="14"></line><line x1="15" y1="14" x2="15" y2="14"></line></svg>',
    utensils: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path><line x1="7" y1="2" x2="7" y2="22"></line><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3"></path><line x1="18" y1="22" x2="18" y2="15"></line></svg>',
    cloud: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"></path></svg>',
    leaf: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 20A7 7 0 0 1 9.8 6.9C15.5 4.9 17 3.5 19 2c1 2 2 4.5 2 8 0 5.5-4.78 10-10 10z"></path><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path></svg>',
    gem: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="6 3 18 3 22 9 12 22 2 9"></polygon><line x1="2" y1="9" x2="22" y2="9"></line><line x1="12" y1="22" x2="8" y2="9"></line><line x1="12" y1="22" x2="16" y2="9"></line></svg>',
    trophy: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20 7 22"></path><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20 17 22"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path></svg>',
};

// Load themes on page load
document.addEventListener('DOMContentLoaded', loadThemes);

async function loadThemes() {
    try {
        const resp = await fetch('/api/themes');
        const data = await resp.json();
        renderThemes(data.themes);
    } catch (e) {
        console.error('Failed to load themes:', e);
    }
}

function renderThemes(themes) {
    const grid = document.getElementById('themes-grid');
    grid.innerHTML = themes.map(t => `
        <div class="theme-card" data-theme="${t.id}" onclick="selectTheme('${t.id}')">
            <div class="theme-colors">
                <div class="theme-color-swatch large" style="background:${t.colors.primary}"></div>
                <div class="theme-color-swatch" style="background:${t.colors.secondary}"></div>
                <div class="theme-color-swatch" style="background:${t.colors.accent}"></div>
            </div>
            <div class="theme-name">${t.name}</div>
            <div class="theme-desc">${t.description}</div>
            <div class="theme-industry">${t.industry}</div>
        </div>
    `).join('');

    // Add continue button
    grid.insertAdjacentHTML('afterend',
        '<button class="theme-next-btn" id="theme-next" onclick="goToStep(2)">Continue with Selected Theme</button>'
    );
}

function selectTheme(themeId) {
    selectedTheme = themeId;
    document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('selected'));
    document.querySelector(`[data-theme="${themeId}"]`).classList.add('selected');
    document.getElementById('theme-next').classList.add('enabled');
}

function goToStep(step) {
    if (step === 2 && !selectedTheme) return;
    currentStep = step;

    // Update step indicators
    document.querySelectorAll('.steps-bar .step').forEach((el, i) => {
        el.classList.remove('active', 'done');
        if (i + 1 < step) el.classList.add('done');
        if (i + 1 === step) el.classList.add('active');
    });

    // Show step content
    document.querySelectorAll('.step-content').forEach(el => el.classList.remove('active'));
    document.getElementById(`step${step}`).classList.add('active');
}

// Form submission
document.getElementById('brief-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    goToStep(3);

    const payload = {
        brand_name: document.getElementById('brand_name').value,
        problem_statement: document.getElementById('problem_statement').value,
        target_audience: document.getElementById('target_audience').value,
        tone: document.getElementById('tone').value,
        theme_id: selectedTheme,
        additional_context: document.getElementById('additional_context').value || '',
    };

    try {
        const resp = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        const data = await resp.json();
        connectWebSocket(data.task_id);
        pollStatus(data.task_id);
    } catch (e) {
        document.getElementById('progress-message').textContent = 'Error starting generation. Please try again.';
    }
});

function connectWebSocket(taskId) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/ws/${taskId}`);
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateProgress(data);
    };
    ws.onerror = () => { /* Fallback to polling */ };
}

async function pollStatus(taskId) {
    const poll = async () => {
        try {
            const resp = await fetch(`/api/status/${taskId}`);
            const data = await resp.json();
            updateProgress(data);
            if (data.status !== 'complete' && data.status !== 'error') {
                setTimeout(poll, 1500);
            }
        } catch (e) {
            setTimeout(poll, 2000);
        }
    };
    setTimeout(poll, 2000);
}

const STAGE_MAP = {
    'researching': 'research',
    'strategizing': 'strategy',
    'creating': 'creative',
    'structuring': 'structure',
    'reviewing': 'review',
    'building': 'build',
};

const STAGE_ORDER = ['research', 'strategy', 'creative', 'structure', 'review', 'build'];

function updateProgress(data) {
    document.getElementById('progress-bar').style.width = data.progress + '%';
    document.getElementById('progress-percent').textContent = data.progress + '%';
    document.getElementById('progress-message').textContent = data.message;

    // Update agent stages
    const currentStage = STAGE_MAP[data.status];
    if (currentStage) {
        const idx = STAGE_ORDER.indexOf(currentStage);
        STAGE_ORDER.forEach((stage, i) => {
            const el = document.getElementById(`stage-${stage}`);
            el.classList.remove('active', 'done');
            if (i < idx) el.classList.add('done');
            if (i === idx) el.classList.add('active');
        });
    }

    if (data.status === 'complete') {
        // Mark all stages done
        STAGE_ORDER.forEach(stage => {
            const el = document.getElementById(`stage-${stage}`);
            el.classList.remove('active');
            el.classList.add('done');
        });

        document.getElementById('progress-view').style.display = 'none';
        document.getElementById('complete-view').style.display = 'block';
        document.getElementById('download-btn').href = data.download_url;
        if (ws) ws.close();
    }

    if (data.status === 'error') {
        document.getElementById('progress-title').textContent = 'Generation Failed';
        document.getElementById('progress-message').textContent = data.message;
        document.querySelector('.spinner').style.display = 'none';
    }
}

function resetApp() {
    selectedTheme = null;
    currentStep = 1;
    document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('selected'));
    document.getElementById('theme-next').classList.remove('enabled');
    document.getElementById('brief-form').reset();
    document.getElementById('progress-view').style.display = 'block';
    document.getElementById('complete-view').style.display = 'none';
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('progress-percent').textContent = '0%';
    document.querySelector('.spinner').style.display = 'block';
    STAGE_ORDER.forEach(stage => {
        const el = document.getElementById(`stage-${stage}`);
        el.classList.remove('active', 'done');
    });
    goToStep(1);
}
