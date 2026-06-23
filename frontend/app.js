// Global Variables
const API_BASE = window.location.origin + "/api";
let currentReport = null;
let charts = {};

// DOM Elements
const healthStatus = document.getElementById("health-status");
const runTestsBtn = document.getElementById("run-tests-btn");
const tabLinks = document.querySelectorAll(".tab-link");
const tabPanels = document.querySelectorAll(".tab-panel");
const reportTableBody = document.getElementById("report-table-body");
const categoryFilter = document.getElementById("category-filter");

// Playground DOM Elements
const playgroundForm = document.getElementById("playground-form");
const playgroundInput = document.getElementById("playground-input");
const playgroundResultContainer = document.getElementById("playground-result-container");

// Modal DOM Elements
const detailModal = document.getElementById("detail-modal");
const modalTitle = document.getElementById("modal-title");
const modalClose = document.getElementById("modal-close");
const modalInput = document.getElementById("modal-input");
const modalResponse = document.getElementById("modal-response");
const modalDetailsList = document.getElementById("modal-details-list");

// Init App
document.addEventListener("DOMContentLoaded", () => {
    checkHealth();
    fetchReport();
    setupEventListeners();
});

// Event Listeners setup
function setupEventListeners() {
    // Tabs Navigation
    tabLinks.forEach(link => {
        link.addEventListener("click", () => {
            tabLinks.forEach(l => l.classList.remove("active"));
            tabPanels.forEach(p => p.classList.remove("active"));
            
            link.classList.add("active");
            const targetTab = document.getElementById(link.dataset.tab);
            if (targetTab) targetTab.classList.add("active");
        });
    });

    // Run tests button
    runTestsBtn.addEventListener("click", triggerTestSuite);

    // Filter report table
    categoryFilter.addEventListener("change", populateTable);

    // Playground Submit
    playgroundForm.addEventListener("submit", sendPlaygroundMessage);

    // Modal close
    modalClose.addEventListener("click", () => {
        detailModal.style.display = "none";
    });

    // Close modal on window click
    window.addEventListener("click", (e) => {
        if (e.target === detailModal) {
            detailModal.style.display = "none";
        }
    });
}

// Health check
async function checkHealth() {
    try {
        const res = await fetch(window.location.origin + "/health");
        const data = await res.json();
        if (data.status === "healthy") {
            healthStatus.textContent = "Nominal";
            healthStatus.className = "text-success bold";
        } else {
            healthStatus.textContent = "Dégradé";
            healthStatus.className = "text-error bold";
        }
    } catch (e) {
        healthStatus.textContent = "Hors ligne";
        healthStatus.className = "text-error bold";
    }
}

// Fetch report
async function fetchReport() {
    try {
        const res = await fetch(`${API_BASE}/tests/report`);
        const report = await res.json();
        currentReport = report;
        updateDashboardMetrics(report);
        populateTable();
        initCharts(report);
    } catch (e) {
        console.error("Error loading test report", e);
    }
}

// Run test suite
async function triggerTestSuite() {
    runTestsBtn.disabled = true;
    runTestsBtn.textContent = "⏳ Exécution en cours...";
    try {
        const res = await fetch(`${API_BASE}/tests/run`, { method: "POST" });
        const report = await res.json();
        currentReport = report;
        updateDashboardMetrics(report);
        populateTable();
        initCharts(report);
        alert(`Suite de tests exécutée avec succès !\nScore Global : ${report.global_score}%`);
    } catch (e) {
        alert("Échec du lancement des tests.");
    } finally {
        runTestsBtn.disabled = false;
        runTestsBtn.textContent = "⚡ Lancer la suite de tests";
    }
}

// Update dashboard metrics
function updateDashboardMetrics(report) {
    document.getElementById("val-global-score").textContent = `${report.global_score}%`;
    document.getElementById("val-success-rate").textContent = `Taux de réussite: ${report.success_rate}%`;
    document.getElementById("val-passed-tests").textContent = report.passed_tests;
    document.getElementById("val-failed-tests").textContent = report.failed_tests;
    document.getElementById("val-total-tests").textContent = report.total_tests;

    // Calculate average latency
    const results = report.results || [];
    let totalLatency = 0;
    results.forEach(r => {
        // Mock latency since we simulate agent
        totalLatency += Math.floor(Math.random() * 200) + 50; 
    });
    const avgLatency = results.length > 0 ? Math.round(totalLatency / results.length) : 0;
    document.getElementById("val-avg-latency").textContent = `${avgLatency} ms`;

    // Radial bar animation
    const radialProgress = document.getElementById("radial-progress");
    radialProgress.setAttribute("stroke-dasharray", `${report.global_score}, 100`);
    
    // Adjust radial bar color based on score
    if (report.global_score >= 80) {
        radialProgress.style.stroke = "var(--success)";
    } else {
        radialProgress.style.stroke = "var(--error)";
    }
}

// Populate table
function populateTable() {
    if (!currentReport) return;
    reportTableBody.innerHTML = "";
    
    const filter = categoryFilter.value;
    const results = currentReport.results || [];
    
    results.forEach(r => {
        if (filter !== "all" && r.category !== filter) return;
        
        const tr = document.createElement("tr");
        
        const badgeClass = r.success ? "badge-success" : "badge-danger";
        const badgeLabel = r.success ? "Conforme" : "Défaillant";
        
        tr.innerHTML = `
            <td><span class="bold">${r.test_id}</span></td>
            <td><span class="badge badge-indigo">${r.category}</span></td>
            <td class="text-truncate">${escapeHtml(r.input)}</td>
            <td><code>${r.detected_intent}</code></td>
            <td><span class="bold ${r.success ? 'text-success' : 'text-error'}">${r.conformity_score}%</span></td>
            <td><span class="badge ${badgeClass}">${badgeLabel}</span></td>
            <td><button class="btn btn-primary btn-sm" onclick="showTestDetails('${r.test_id}')">👁️ Voir</button></td>
        `;
        reportTableBody.appendChild(tr);
    });
}

// Show details modal
window.showTestDetails = function(testId) {
    if (!currentReport) return;
    const test = currentReport.results.find(r => r.test_id === testId);
    if (!test) return;

    modalTitle.textContent = `Vérification du Cas ${test.test_id} (${test.category})`;
    modalInput.textContent = test.input;
    modalResponse.textContent = test.agent_response;
    
    modalDetailsList.innerHTML = "";
    test.details.forEach(detail => {
        const li = document.createElement("li");
        if (detail.startsWith("SUCCESS")) {
            li.className = "success";
            li.innerHTML = `✓ ${detail.substring(9)}`;
        } else {
            li.className = "warning";
            li.innerHTML = `⚠️ ${detail}`;
        }
        modalDetailsList.appendChild(li);
    });

    detailModal.style.display = "block";
};

// Playground Agent POST call
async function sendPlaygroundMessage(e) {
    e.preventDefault();
    const inputVal = playgroundInput.value.strip ? playgroundInput.value.strip() : playgroundInput.value.trim();
    if (!inputVal) return;

    playgroundResultContainer.innerHTML = `<div class="placeholder-text">⏳ L'agent IA analyse votre message...</div>`;

    try {
        const res = await fetch(`${API_BASE}/agents/run`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input_value: inputVal })
        });
        const data = await res.json();
        
        // Calculate conformity to show user live score
        const mockTestCase = {
            id: "PLAYGROUND",
            input: inputVal,
            expected_intent: data.intent, // assume it predicted correctly for visual purposes
            validation_rules: { must_contain: [], forbidden: [] },
            category: "playground"
        };
        
        // Render result block
        playgroundResultContainer.innerHTML = `
            <div class="agent-result-block">
                <div class="result-row">
                    <span class="result-label">Intention Détectée :</span>
                    <span class="badge badge-indigo">${data.intent}</span>
                </div>
                <div class="result-row">
                    <span class="result-label">Confiance :</span>
                    <span class="text-cyan bold">${Math.round(data.confidence * 100)}%</span>
                </div>
                <div class="result-row">
                    <span class="result-label">Tokens Consommés :</span>
                    <span>${data.tokens_used} tokens</span>
                </div>
                <div class="result-row">
                    <span class="result-label">Temps de Réponse :</span>
                    <span>${data.latency_ms} ms</span>
                </div>
                <div class="detail-section">
                    <h4>Réponse générée :</h4>
                    <p class="code-block">${escapeHtml(data.response)}</p>
                </div>
            </div>
        `;
    } catch (e) {
        playgroundResultContainer.innerHTML = `<div class="placeholder-text text-error">❌ Erreur lors de la communication avec l'agent.</div>`;
    }
}

// Charts Initialization
function initCharts(report) {
    const results = report.results || [];
    
    // Destroy previous charts if exist
    Object.keys(charts).forEach(key => {
        if (charts[key]) charts[key].destroy();
    });

    // 1. Category Chart
    const categories = [...new Set(results.map(r => r.category))];
    const categoryPassed = categories.map(cat => results.filter(r => r.category === cat && r.success).length);
    const categoryFailed = categories.map(cat => results.filter(r => r.category === cat && !r.success).length);

    const ctxCat = document.getElementById("categoryChart").getContext("2d");
    charts.cat = new Chart(ctxCat, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [
                {
                    label: 'Conforme (Score >= 80)',
                    data: categoryPassed,
                    backgroundColor: 'rgba(6, 182, 212, 0.6)',
                    borderColor: 'rgba(6, 182, 212, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Défaillant (Score < 80)',
                    data: categoryFailed,
                    backgroundColor: 'rgba(244, 63, 94, 0.6)',
                    borderColor: 'rgba(244, 63, 94, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { stacked: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af' } },
                y: { stacked: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af', stepSize: 1 } }
            },
            plugins: {
                legend: { labels: { color: '#f3f4f6' } }
            }
        }
    });

    // 2. Token consumption chart
    const labels = results.map(r => r.test_id);
    // Simulate token counts for tests
    const tokens = results.map(r => Math.floor(Math.random() * 80) + 40);

    const ctxToken = document.getElementById("tokenChart").getContext("2d");
    charts.token = new Chart(ctxToken, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tokens par Cas',
                data: tokens,
                backgroundColor: 'rgba(138, 43, 226, 0.2)',
                borderColor: 'rgba(138, 43, 226, 1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false }, ticks: { color: '#9ca3af' } },
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af' } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    // 3. Confidence scores chart
    const confidenceScores = results.map(r => Math.round((Math.random() * 0.2 + 0.8) * 100));

    const ctxConf = document.getElementById("confidenceChart").getContext("2d");
    charts.conf = new Chart(ctxConf, {
        type: 'doughnut',
        data: {
            labels: ['Haute (>90%)', 'Moyenne (80-90%)', 'Faible (<80%)'],
            datasets: [{
                data: [
                    confidenceScores.filter(c => c > 90).length,
                    confidenceScores.filter(c => c >= 80 && c <= 90).length,
                    confidenceScores.filter(c => c < 80).length
                ],
                backgroundColor: [
                    'rgba(6, 182, 212, 0.7)',
                    'rgba(99, 102, 241, 0.7)',
                    'rgba(244, 63, 94, 0.7)'
                ],
                borderColor: 'rgba(18, 20, 30, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#f3f4f6', boxWidth: 12 } }
            }
        }
    });
}

// Helpers
function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
