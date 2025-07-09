// Professional Strategic Risk Monitor Dashboard
let socket;
let riskChart;
let lastDataUpdate = null;
let previousRiskScore = null;

// Initialize dashboard with professional UX features
document.addEventListener('DOMContentLoaded', function() {
    initializeSocket();
    initializeCharts();
    initializeInteractions();
    loadInitialData();
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-refresh every 30 seconds
    setInterval(requestUpdate, 30000);
    
    // Default to 1M view
    document.getElementById('range1m').checked = true;
});

// Initialize professional interactions
function initializeInteractions() {
    // Copy recommendations functionality
    document.getElementById('copy-recommendations').addEventListener('click', function() {
        const recommendations = document.getElementById('recommendations').innerText;
        navigator.clipboard.writeText(recommendations).then(() => {
            showNotification('Recommendations copied to clipboard', 'success');
        }).catch(() => {
            showNotification('Failed to copy recommendations', 'error');
        });
    });
    
    // Time range controls
    document.querySelectorAll('input[name="timeRange"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                loadHistoricalData(parseInt(this.value));
            }
        });
    });
    
    // Component hover effects
    document.querySelectorAll('.component-segment').forEach(segment => {
        segment.addEventListener('mouseenter', function() {
            showComponentTooltip(this);
        });
    });
}

// Initialize enhanced Socket.IO connection
function initializeSocket() {
    socket = io();
    
    socket.on('connect', function() {
        updateConnectionStatus('Connected', 'success');
        console.log('Professional dashboard connected');
    });
    
    socket.on('disconnect', function() {
        updateConnectionStatus('Disconnected', 'danger');
        console.log('Dashboard disconnected');
    });
    
    socket.on('risk_update', function(data) {
        updateRiskData(data);
        console.log(`Risk update: ${data.risk_score.level} (${data.risk_score.value})`);
    });
    
    socket.on('error', function(error) {
        console.error(`Dashboard error: ${error.message}`);
    });
}

// Initialize professional charts with enhanced features
function initializeCharts() {
    // Enhanced Risk History Chart with moving average
    const riskCtx = document.getElementById('riskChart').getContext('2d');
    riskChart = new Chart(riskCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Risk Score',
                data: [],
                borderColor: '#DC2626',
                backgroundColor: 'rgba(220, 38, 38, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointHoverRadius: 6,
                borderWidth: 2
            }, {
                label: '7-Day Average',
                data: [],
                borderColor: '#6B7280',
                backgroundColor: 'transparent',
                borderDash: [5, 5],
                fill: false,
                tension: 0.4,
                pointRadius: 0,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(75, 85, 99, 0.1)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(75, 85, 99, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#374151',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + '%';
                        }
                    }
                }
            },
            elements: {
                point: {
                    hoverBorderWidth: 3
                }
            }
        }
    });
}

// Load initial data
function loadInitialData() {
    console.log('Starting to load initial data...');
    
    // Try quick data first, then fallback to full data
    fetch('/api/quick_data')
        .then(response => {
            console.log('Quick data response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received quick data:', data);
            if (data && data.success) {
                updateRiskData(data);
                updateConnectionStatus('Connected', 'success');
                logUpdate('Data loaded successfully from ' + (data.source || 'API'));
                
                // If we got database data, also try to get fresh data in background
                if (data.source === 'database') {
                    setTimeout(() => loadFreshData(), 1000);
                }
            } else {
                console.error('Quick API returned error:', data ? data.error : 'No data received');
                // Fallback to full API
                loadFreshData();
            }
        })
        .catch(error => {
            console.error('Error loading quick data:', error);
            console.log('Falling back to fresh data...');
            loadFreshData();
        });
    
    // Load historical data
    loadHistoricalData();
}

// Load fresh data from full API
function loadFreshData() {
    console.log('Loading fresh data...');
    fetch('/api/risk_data')
        .then(response => {
            console.log('Fresh data response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received fresh data:', data);
            if (data.success) {
                updateRiskData(data);
                updateConnectionStatus('Connected', 'success');
                logUpdate('Fresh data loaded successfully');
            } else {
                console.error('Fresh API returned error:', data.error || 'Unknown error');
                updateConnectionStatus('API Error', 'warning');
                logUpdate('API Error: ' + (data.error || 'Unknown'));
            }
        })
        .catch(error => {
            console.error('Error loading fresh data:', error);
            updateConnectionStatus('Connection Error', 'danger');
            logUpdate('Error loading fresh data: ' + error.message);
        });
}

// Load historical data for chart
function loadHistoricalData(days = 30) {
    console.log('Starting to load historical data...');
    fetch(`/api/simple_historical`)
        .then(response => {
            console.log('Historical data response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Historical data response:', data);
            console.log('Data type:', typeof data, 'Success:', data.success, 'Data length:', data.data ? data.data.length : 'undefined');
            
            if (data && data.success === true && data.data && Array.isArray(data.data) && data.data.length > 0) {
                console.log('SUCCESS: Updating chart with', data.data.length, 'data points');
                updateHistoricalChart(data.data);
            } else {
                console.log('FAILED: No historical data available');
                console.log('- Success:', data.success);
                console.log('- Data exists:', !!data.data);
                console.log('- Data is array:', Array.isArray(data.data));
                console.log('- Data length:', data.data ? data.data.length : 'N/A');
                console.log('- Error:', data.error || 'No error message');
            }
        })
        .catch(error => {
            console.error('Error loading historical data:', error);
        });
}

// Update risk data display
function updateRiskData(data) {
    console.log('Updating risk data with:', data);
    
    const riskScore = data.risk_score;
    const marketData = data.market_data;
    const sentimentData = data.sentiment_data;
    const llmAnalysis = data.llm_analysis;
    
    if (!riskScore || !marketData || !sentimentData) {
        console.error('Missing required data:', {riskScore, marketData, sentimentData});
        return;
    }
    
    // Update risk score display
    const riskScoreEl = document.getElementById('risk-score-value');
    const riskLevelEl = document.getElementById('risk-level');
    if (riskScoreEl) riskScoreEl.textContent = riskScore.value.toFixed(2);
    if (riskLevelEl) riskLevelEl.textContent = riskScore.level;
    
    // Update progress bar
    const progressBar = document.getElementById('risk-progress');
    if (progressBar) {
        progressBar.style.width = riskScore.value + '%';
        progressBar.className = `progress-bar ${getRiskProgressClass(riskScore.level)}`;
    }
    
    // Update market data - with safe checking
    const spyEl = document.getElementById('spy-value');
    const vixEl = document.getElementById('vix-value');
    const dxyEl = document.getElementById('dxy-value');
    
    if (spyEl && marketData.spy) spyEl.textContent = marketData.spy.toFixed(2);
    if (vixEl && marketData.vix) vixEl.textContent = marketData.vix.toFixed(2);
    if (dxyEl && marketData.dxy) dxyEl.textContent = marketData.dxy.toFixed(2);
    
    // Update sentiment data - with safe checking
    const redditEl = document.getElementById('reddit-sentiment');
    const twitterEl = document.getElementById('twitter-sentiment');
    const newsEl = document.getElementById('news-sentiment');
    
    if (redditEl && sentimentData.reddit !== undefined) redditEl.textContent = sentimentData.reddit.toFixed(3);
    if (twitterEl && sentimentData.twitter !== undefined) twitterEl.textContent = sentimentData.twitter.toFixed(3);
    if (newsEl && sentimentData.news !== undefined) newsEl.textContent = sentimentData.news.toFixed(3);
    
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
    const lastUpdateEl = document.getElementById('last-update');
    if (lastUpdateEl) {
        lastUpdateEl.textContent = new Date().toLocaleTimeString();
    }
    
    // Get ML prediction
    getMlPrediction(riskScore.value || riskScore, marketData, sentimentData);
    
    console.log('Risk data update completed successfully');
}

// Update LLM Analysis section
function updateLLMAnalysis(analysis) {
    console.log('Updating LLM analysis:', analysis);
    
    try {
        // Update Risk Assessment
        const riskAssessment = document.getElementById('risk-assessment');
        if (riskAssessment) {
            riskAssessment.textContent = analysis.risk_assessment || 'ANALYZING...';
            riskAssessment.className = 'badge bg-secondary';
        }
        
        // Update Market Narrative
        const marketNarrative = document.getElementById('market-narrative');
        if (marketNarrative) {
            marketNarrative.textContent = analysis.market_narrative || 'Analyzing current market conditions...';
        }
        
        // Update Key Concerns
        const keyConcerns = document.getElementById('key-concerns');
        if (keyConcerns && analysis.key_concerns) {
            keyConcerns.innerHTML = analysis.key_concerns.map(concern => `<li>${concern}</li>`).join('');
        } else if (keyConcerns) {
            keyConcerns.innerHTML = '<li>Loading analysis...</li>';
        }
        
        // Update Specific Recommendations
        const specificRecs = document.getElementById('specific-recommendations');
        if (specificRecs && analysis.specific_recommendations) {
            specificRecs.innerHTML = analysis.specific_recommendations.map(rec => `<li>${rec}</li>`).join('');
        } else if (specificRecs) {
            specificRecs.innerHTML = '<li>Loading recommendations...</li>';
        }
        
        // Update Watchlist
        const watchlist = document.getElementById('watchlist');
        if (watchlist && analysis.watchlist) {
            watchlist.innerHTML = analysis.watchlist.map(item => `<span class="badge bg-info me-1">${item}</span>`).join('');
        } else if (watchlist) {
            watchlist.innerHTML = '<span class="badge bg-secondary">Loading...</span>';
        }
        
        // Update Probability Scenarios
        const scenarios = document.getElementById('probability-scenarios');
        if (scenarios && analysis.probability_scenarios) {
            let scenarioHtml = '';
            Object.entries(analysis.probability_scenarios).forEach(([scenario, probability]) => {
                const percentage = Math.round(probability * 100);
                const label = scenario.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
                scenarioHtml += `<div class="d-flex justify-content-between mb-1"><span>${label}</span><span class="badge bg-info">${percentage}%</span></div>`;
            });
            scenarios.innerHTML = scenarioHtml;
        } else if (scenarios) {
            scenarios.innerHTML = '<div class="text-muted">Loading scenarios...</div>';
        }
        
        console.log('LLM analysis update completed');
    } catch (error) {
        console.error('Error updating LLM analysis:', error);
    }
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
            
            // Update additional ML displays using correct selectors
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
    if (!riskChart) {
        console.error('Risk chart not initialized');
        return;
    }
    
    if (!data || data.length === 0) {
        console.log('No data to update chart');
        return;
    }
    
    console.log('Processing', data.length, 'records for chart');
    
    // Format dates for 30-day view - show only dates, no times
    const labels = data.map(item => {
        const date = new Date(item.timestamp);
        return date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric' 
        });
    });
    const scores = data.map(item => parseFloat(item.score) || 0);
    
    console.log('Chart labels (first 5):', labels.slice(0, 5)); // Show first 5 for debugging
    console.log('Chart scores (first 5):', scores.slice(0, 5)); // Show first 5 for debugging
    console.log('Total data points:', labels.length);
    
    riskChart.data.labels = labels;
    riskChart.data.datasets[0].data = scores;
    riskChart.update();
    
    console.log('Historical chart updated successfully with', labels.length, 'days of data');
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
