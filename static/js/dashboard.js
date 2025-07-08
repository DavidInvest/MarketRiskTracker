// Dashboard JavaScript for Strategic Risk Monitor
let socket;
let riskChart;
let componentsChart;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeSocket();
    initializeCharts();
    loadInitialData();
    
    // Auto-refresh every 30 seconds
    setInterval(requestUpdate, 30000);
});

// Initialize Socket.IO connection
function initializeSocket() {
    socket = io();
    
    socket.on('connect', function() {
        updateConnectionStatus('Connected', 'success');
        logUpdate('Connected to server');
    });
    
    socket.on('disconnect', function() {
        updateConnectionStatus('Disconnected', 'danger');
        logUpdate('Disconnected from server');
    });
    
    socket.on('risk_update', function(data) {
        updateRiskData(data);
        logUpdate(`Risk update received: ${data.risk_score.level} (${data.risk_score.value})`);
    });
    
    socket.on('error', function(error) {
        logUpdate(`Error: ${error.message}`);
    });
}

// Initialize charts
function initializeCharts() {
    // Risk history chart
    const riskCtx = document.getElementById('riskChart').getContext('2d');
    riskChart = new Chart(riskCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Risk Score',
                data: [],
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            },
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });
    
    // Components chart
    const componentsCtx = document.getElementById('componentsChart').getContext('2d');
    componentsChart = new Chart(componentsCtx, {
        type: 'doughnut',
        data: {
            labels: ['VIX', 'Sentiment', 'DXY', 'Momentum'],
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: [
                    '#dc3545',
                    '#ffc107',
                    '#17a2b8',
                    '#28a745'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Load initial data
function loadInitialData() {
    fetch('/api/risk_data')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateRiskData(data);
            }
        })
        .catch(error => {
            console.error('Error loading initial data:', error);
            logUpdate('Error loading initial data');
        });
    
    // Load historical data
    loadHistoricalData();
}

// Load historical data for chart
function loadHistoricalData(days = 7) {
    fetch(`/api/historical_data?days=${days}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateHistoricalChart(data.data);
            }
        })
        .catch(error => {
            console.error('Error loading historical data:', error);
        });
}

// Update risk data display
function updateRiskData(data) {
    const riskScore = data.risk_score;
    const marketData = data.market_data;
    const sentimentData = data.sentiment_data;
    const llmAnalysis = data.llm_analysis;
    
    // Update risk score display
    document.getElementById('risk-score-value').textContent = riskScore.value;
    document.getElementById('risk-level').textContent = riskScore.level;
    
    // Update progress bar
    const progressBar = document.getElementById('risk-progress');
    progressBar.style.width = riskScore.value + '%';
    progressBar.className = `progress-bar ${getRiskProgressClass(riskScore.level)}`;
    
    // Update market data
    document.getElementById('spy-value').textContent = marketData.spy.toFixed(2);
    document.getElementById('vix-value').textContent = marketData.vix.toFixed(2);
    document.getElementById('dxy-value').textContent = marketData.dxy.toFixed(2);
    
    // Update sentiment data
    document.getElementById('reddit-sentiment').textContent = sentimentData.reddit.toFixed(3);
    document.getElementById('twitter-sentiment').textContent = sentimentData.twitter.toFixed(3);
    document.getElementById('news-sentiment').textContent = sentimentData.news.toFixed(3);
    
    // Update LLM analysis section
    updateLLMAnalysis(llmAnalysis);
    
    // Update components chart
    if (riskScore.components) {
        componentsChart.data.datasets[0].data = [
            riskScore.components.vix,
            riskScore.components.sentiment,
            riskScore.components.dxy,
            riskScore.components.momentum
        ];
        componentsChart.update();
    }
    
    // Update last update time
    document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
    
    // Get ML prediction
    getMlPrediction(riskScore.value || riskScore, marketData, sentimentData);
}

// Update LLM analysis display
function updateLLMAnalysis(llmAnalysis) {
    if (!llmAnalysis) return;
    
    // Update risk assessment
    const riskAssessmentEl = document.getElementById('llm-risk-assessment');
    if (riskAssessmentEl) {
        riskAssessmentEl.textContent = llmAnalysis.risk_assessment || 'ANALYZING...';
        riskAssessmentEl.className = 'badge ' + getRiskProgressClass(llmAnalysis.risk_assessment);
    }
    
    // Update market narrative
    const narrativeEl = document.getElementById('llm-market-narrative');
    if (narrativeEl) {
        narrativeEl.textContent = llmAnalysis.market_narrative || 'Analyzing current market conditions...';
    }
    
    // Update key concerns
    const concernsEl = document.getElementById('llm-key-concerns');
    if (concernsEl && llmAnalysis.key_concerns) {
        concernsEl.innerHTML = llmAnalysis.key_concerns
            .map(concern => `<li class="list-group-item">${concern}</li>`)
            .join('');
    }
    
    // Update recommendations
    const recommendationsEl = document.getElementById('llm-recommendations');
    if (recommendationsEl && llmAnalysis.specific_recommendations) {
        recommendationsEl.innerHTML = llmAnalysis.specific_recommendations
            .map(rec => `<li class="list-group-item">${rec}</li>`)
            .join('');
    }
    
    // Update watchlist
    const watchlistEl = document.getElementById('llm-watchlist');
    if (watchlistEl && llmAnalysis.watchlist) {
        watchlistEl.innerHTML = llmAnalysis.watchlist
            .map(item => `<span class="badge bg-secondary me-1">${item}</span>`)
            .join('');
    }
    
    // Update probability scenarios
    const scenariosEl = document.getElementById('llm-scenarios');
    if (scenariosEl && llmAnalysis.probability_scenarios) {
        const scenarios = llmAnalysis.probability_scenarios;
        let scenarioHtml = '';
        for (const [scenario, probability] of Object.entries(scenarios)) {
            const percentage = (probability * 100).toFixed(0);
            scenarioHtml += `
                <div class="d-flex justify-content-between">
                    <span>${scenario.replace(/_/g, ' ')}</span>
                    <span class="fw-bold">${percentage}%</span>
                </div>
            `;
        }
        scenariosEl.innerHTML = scenarioHtml;
    }
}

// Get ML prediction
function getMlPrediction(riskScore, marketData, sentimentData) {
    fetch('/api/ml_predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            market_data: marketData,
            sentiment_data: sentimentData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.predictions) {
            const predictions = data.predictions;
            
            // Update crash probability displays
            const crashProb1d = (predictions.crash_probability_1d * 100).toFixed(1);
            document.getElementById('crash-probability').textContent = crashProb1d + '%';
            document.getElementById('crash-progress').style.width = crashProb1d + '%';
            
            // Update any additional ML displays that might exist
            updateMLDisplay('crash-1d', crashProb1d + '%');
            updateMLDisplay('crash-7d', (predictions.crash_probability_7d * 100).toFixed(1) + '%');
            updateMLDisplay('crash-30d', (predictions.crash_probability_30d * 100).toFixed(1) + '%');
            updateMLDisplay('ml-risk', predictions.ml_risk_score.toFixed(1));
            
            // Remove loading states
            document.querySelectorAll('[data-ml-loading]').forEach(el => {
                el.textContent = el.getAttribute('data-ml-loading');
                el.removeAttribute('data-ml-loading');
            });
        }
    })
    .catch(error => {
        console.error('Error getting ML prediction:', error);
        // Show error state
        document.querySelectorAll('[data-ml-loading]').forEach(el => {
            el.textContent = 'Error';
            el.removeAttribute('data-ml-loading');
        });
    });
}

function updateMLDisplay(selector, value) {
    // Try multiple selector patterns to find the element
    const patterns = [
        selector,
        `#${selector}`,
        `.${selector}`,
        `[data-ml="${selector}"]`,
        `[id*="${selector}"]`,
        `[class*="${selector}"]`
    ];
    
    for (const pattern of patterns) {
        const elements = document.querySelectorAll(pattern);
        if (elements.length > 0) {
            elements.forEach(el => el.textContent = value);
            return;
        }
    }
    
    // Log if element not found for debugging
    console.log(`ML display element not found for: ${selector}`);
}

// Update historical chart
function updateHistoricalChart(data) {
    const labels = data.map(item => new Date(item.timestamp).toLocaleDateString());
    const scores = data.map(item => item.score);
    
    riskChart.data.labels = labels;
    riskChart.data.datasets[0].data = scores;
    riskChart.update();
}

// Get risk progress class
function getRiskProgressClass(level) {
    switch(level) {
        case 'MINIMAL': return 'bg-success';
        case 'LOW': return 'bg-info';
        case 'MEDIUM': return 'bg-warning';
        case 'HIGH': return 'bg-danger';
        case 'CRITICAL': return 'bg-dark';
        default: return 'bg-secondary';
    }
}

// Update connection status
function updateConnectionStatus(status, type) {
    const statusElement = document.getElementById('connection-status');
    statusElement.textContent = status;
    statusElement.className = `badge bg-${type}`;
}

// Log update
function logUpdate(message) {
    const logElement = document.getElementById('update-log');
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = `[${timestamp}] ${message}\n`;
    
    logElement.textContent = logEntry + logElement.textContent;
    
    // Keep only last 50 entries
    const lines = logElement.textContent.split('\n');
    if (lines.length > 50) {
        logElement.textContent = lines.slice(0, 50).join('\n');
    }
}

// Request manual update
function requestUpdate() {
    if (socket) {
        socket.emit('request_update');
        logUpdate('Manual update requested');
    }
}

// Feather icons initialization
feather.replace();
