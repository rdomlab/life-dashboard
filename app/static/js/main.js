// Main JavaScript for Life Dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Load initial dashboard content
    loadDashboard();

    // Set up navigation
    setupNavigation();

    // Set up AI insights form
    setupAIInsights();

    // Set up memory form
    setupMemory();
});

function loadDashboard() {
    // Load initial dashboard content
    fetch('/api/metrics')
        .then(response => response.json())
        .then(data => {
            displayDashboard(data);
        })
        .catch(error => {
            console.error('Error loading dashboard:', error);
            document.getElementById('dashboard-content').innerHTML =
                '<div class="error">Error loading dashboard data</div>';
        });
}

function displayDashboard(data) {
    const content = document.getElementById('dashboard-content');

    let html = `
        <div class="dashboard-grid">
            <div class="card">
                <h2>Tasks</h2>
                <ul>
    `;

    if (data.tasks && data.tasks.length > 0) {
        data.tasks.slice(0, 5).forEach(task => {
            const priorityClass = `priority-${task.priority}`;
            html += `
                <li>
                    <strong class="${priorityClass}">${task.title}</strong>
                    <p>${task.description}</p>
                    <small>Due: ${formatDate(task.due_date)}</small>
                </li>
            `;
        });
    } else {
        html += '<li>No tasks found</li>';
    }

    html += `
                </ul>
            </div>

            <div class="card">
                <h2>Calendar Events</h2>
                <ul>
    `;

    if (data.calendar_events && data.calendar_events.length > 0) {
        data.calendar_events.slice(0, 5).forEach(event => {
            html += `
                <li>
                    <strong>${event.title}</strong>
                    <p>${event.description}</p>
                    <small>${formatDateTime(event.start_time)}</small>
                </li>
            `;
        });
    } else {
        html += '<li>No events found</li>';
    }

    html += `
                </ul>
            </div>

            <div class="card">
                <h2>Health Logs</h2>
                <ul>
    `;

    if (data.health_logs && data.health_logs.length > 0) {
        data.health_logs.slice(0, 5).forEach(log => {
            html += `
                <li>
                    <strong>${formatDate(log.date)}</strong>
                    <p>Steps: ${log.steps}, Calories: ${log.calories}</p>
                    <p>Sleep: ${log.sleep_hours} hours, Mood: ${log.mood}</p>
                </li>
            `;
        });
    } else {
        html += '<li>No health logs found</li>';
    }

    html += `
                </ul>
            </div>
        </div>
    `;

    content.innerHTML = html;
}

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));

            // Add active class to clicked link
            this.classList.add('active');

            // Load content based on link
            const target = this.getAttribute('href');
            if (target === '#dashboard') {
                loadDashboard();
            } else if (target === '#ai') {
                loadAIInsights();
            } else if (target === '#memory') {
                loadMemory();
            }
        });
    });
}

function setupAIInsights() {
    const form = document.getElementById('ai-insights-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const prompt = document.getElementById('ai-prompt').value;
            generateAIInsight(prompt);
        });
    }
}

function setupMemory() {
    const form = document.getElementById('memory-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const text = document.getElementById('memory-text').value;
            addToMemory(text);
        });
    }
}

function loadAIInsights() {
    const content = document.getElementById('dashboard-content');
    content.innerHTML = `
        <div class="ai-insights">
            <h2>AI Insights</h2>
            <form id="ai-insights-form">
                <textarea id="ai-prompt" name="text" placeholder="Ask for AI insights (e.g., 'Summarize my week', 'What should I focus on today?')"></textarea>
                <button type="submit">Generate Insight</button>
            </form>
            <div id="ai-result"></div>
        </div>

        <div class="ai-insights">
            <h2>Quick Actions</h2>
            <button onclick="summarizeWeek()">Summarize Week</button>
            <button onclick="generatePlan()">Generate 3-Day Plan</button>
        </div>
    `;
}

function loadMemory() {
    const content = document.getElementById('dashboard-content');
    content.innerHTML = `
        <div class="memory-section">
            <h2>Semantic Memory</h2>
            <form id="memory-form">
                <textarea id="memory-text" placeholder="Add to memory..."></textarea>
                <button type="submit">Add to Memory</button>
            </form>
            <div id="memory-list"></div>
        </div>
    `;

    // Load memory entries
    fetch('/api/memory')
        .then(response => response.json())
        .then(data => {
            displayMemory(data.memory);
        })
        .catch(error => {
            console.error('Error loading memory:', error);
        });
}

function displayMemory(entries) {
    const list = document.getElementById('memory-list');
    if (!list) return;

    if (entries && entries.length > 0) {
        let html = '<div class="memory-list">';
        entries.forEach(entry => {
            html += `
                <div class="memory-entry">
                    <p>${entry.text}</p>
                    <small>${formatDateTime(entry.timestamp)}</small>
                </div>
            `;
        });
        html += '</div>';
        list.innerHTML = html;
    } else {
        list.innerHTML = '<p>No memory entries found</p>';
    }
}

function generateAIInsight(prompt) {
    const resultDiv = document.getElementById('ai-result');
    if (!resultDiv) return;

    resultDiv.innerHTML = '<div class="loading">Generating insight...</div>';

    fetch('/api/ai/insight', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({text: prompt})
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = `<div class="result"><p>${data.insight}</p></div>`;
    })
    .catch(error => {
        console.error('Error generating insight:', error);
        resultDiv.innerHTML = '<div class="error">Error generating insight</div>';
    });
}

function summarizeWeek() {
    const resultDiv = document.getElementById('ai-result');
    if (!resultDiv) return;

    resultDiv.innerHTML = '<div class="loading">Summarizing week...</div>';

    fetch('/api/ai/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = `<div class="result"><p>${data.summary}</p></div>`;
    })
    .catch(error => {
        console.error('Error summarizing week:', error);
        resultDiv.innerHTML = '<div class="error">Error summarizing week</div>';
    });
}

function generatePlan() {
    const resultDiv = document.getElementById('ai-result');
    if (!resultDiv) return;

    resultDiv.innerHTML = '<div class="loading">Generating plan...</div>';

    fetch('/api/ai/plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({days: 3})
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = `<div class="result"><p>${data.plan}</p></div>`;
    })
    .catch(error => {
        console.error('Error generating plan:', error);
        resultDiv.innerHTML = '<div class="error">Error generating plan</div>';
    });
}

function addToMemory(text) {
    fetch('/api/memory/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({text: text})
    })
    .then(response => response.json())
    .then(data => {
        alert('Added to memory successfully');
        // Reload memory
        loadMemory();
    })
    .catch(error => {
        console.error('Error adding to memory:', error);
        alert('Error adding to memory');
    });
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function formatDateTime(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString();
}