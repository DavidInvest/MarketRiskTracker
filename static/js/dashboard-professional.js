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
    const copyBtn = document.getElementById('copy-recommendations');
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const recommendations = document.getElementById('recommendations').innerText;
            navigator.clipboard.writeText(recommendations).then(() => {
                showNotification('Recommendations copied to clipboard', 'success');
            }).catch(() => {
                showNotification('Failed to copy recommendations', 'error');
            });
        });
    }
    
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

// Load initial dashboard data with skeleton loading
function loadInitialData() {
    console.log('Starting to load initial data...');
    
    // Show skeleton loading states
    showSkeletonLoading();
    
    // Load current risk data
    fetch('/api/simple_data')
        .then(response => {
            console.log('Quick data response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Received quick data:', data);
            if (data.success) {
                updateRiskData(data);
                hideSkeletonLoading();
            }
        })
        .catch(error => {
            console.error('Error loading quick data:', error);
            showErrorState();
        });
    
    // Load historical data (default 30 days)
    loadHistoricalData(30);
}

// Show professional skeleton loading states
function showSkeletonLoading() {
    const elements = ['risk-score-value', 'spy-value', 'vix-value', 'dxy-value'];
    elements.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.classList.add('skeleton');
    });
}

// Hide skeleton loading states
function hideSkeletonLoading() {
    document.querySelectorAll('.skeleton').forEach(el => {
        el.classList.remove('skeleton');
    });
}

// Enhanced data update function with professional UX
function updateRiskData(data) {
    if (!data || !data.success) return;
    
    console.log('Updating risk data with:', data);
    
    // Store previous score for trend calculation
    const currentScore = parseFloat(document.getElementById('risk-score-value').textContent) || 0;
    previousRiskScore = currentScore;
    
    // Update timestamp
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour12: false, 
        timeZone: 'America/New_York' 
    });
    const updateElement = document.getElementById('update-timestamp');
    if (updateElement) updateElement.textContent = `Last updated ${timeString} ET`;
    
    const systemUpdateElement = document.getElementById('system-last-update');
    if (systemUpdateElement) systemUpdateElement.textContent = timeString;
    
    // Update risk score with animation
    if (data.risk_score) {
        const newScore = data.risk_score.value;
        const level = data.risk_score.level;
        
        // Animate score change
        animateValue('risk-score-value', currentScore, newScore, 1000);
        
        // Update risk level badge
        const badge = document.getElementById('risk-badge');
        if (badge) {
            badge.textContent = level;
            badge.className = `badge risk-${level.toLowerCase()}`;
        }
        
        // Update trend indicator
        updateTrendIndicator(currentScore, newScore);
        
        // Update risk components horizontal bar
        updateRiskComponents(data.risk_score.components);
    }
    
    // Update market data with trend indicators
    if (data.market_data) {
        updateMarketMetric('spy', data.market_data.spy);
        updateMarketMetric('vix', data.market_data.vix);
        updateMarketMetric('dxy', data.market_data.dxy);
    }
    
    // Update sentiment data with badges
    if (data.sentiment_data) {
        updateSentimentMetric('reddit', data.sentiment_data.reddit);
        updateSentimentMetric('twitter', data.sentiment_data.twitter);
        updateSentimentMetric('news', data.sentiment_data.news);
    }
    
    // Update AI analysis
    if (data.llm_analysis) {
        updateAIAnalysis(data.llm_analysis);
    }
    
    console.log('Risk data update completed successfully');
}

// Animate value changes for professional feel
function animateValue(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = start + (end - start) * easeOut;
        
        element.textContent = current.toFixed(1);
        element.classList.add('data-update');
        
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            setTimeout(() => element.classList.remove('data-update'), 600);
        }
    }
    
    requestAnimationFrame(update);
}

// Update trend indicator with arrows and colors
function updateTrendIndicator(oldScore, newScore) {
    const trendElement = document.getElementById('trend-indicator');
    const changeElement = document.getElementById('score-change');
    
    if (!trendElement || !changeElement) return;
    
    const change = newScore - oldScore;
    const changePercent = oldScore > 0 ? ((change / oldScore) * 100) : 0;
    
    if (Math.abs(change) < 0.1) {
        trendElement.innerHTML = '→';
        trendElement.className = 'trend-neutral';
        changeElement.textContent = 'No change';
    } else if (change > 0) {
        trendElement.innerHTML = '▲';
        trendElement.className = 'trend-up';
        changeElement.textContent = `+${change.toFixed(1)} (${changePercent.toFixed(1)}%)`;
    } else {
        trendElement.innerHTML = '▼';
        trendElement.className = 'trend-down';
        changeElement.textContent = `${change.toFixed(1)} (${changePercent.toFixed(1)}%)`;
    }
}

// Update risk components horizontal stacked bar
function updateRiskComponents(components) {
    if (!components) return;
    
    const total = Object.values(components).reduce((sum, val) => sum + val, 0);
    
    Object.keys(components).forEach(key => {
        const segment = document.getElementById(`${key.toLowerCase()}-segment`);
        if (segment) {
            const percentage = total > 0 ? (components[key] / total) * 100 : 25;
            segment.style.width = `${percentage}%`;
            
            // Add tooltip data
            segment.setAttribute('data-value', components[key]);
            segment.setAttribute('data-percentage', percentage.toFixed(1));
        }
    });
}

// Update market metrics with trend indicators
function updateMarketMetric(symbol, value, previousValue = null) {
    const valueElement = document.getElementById(`${symbol}-value`);
    const changeElement = document.getElementById(`${symbol}-change`);
    
    if (valueElement) {
        valueElement.textContent = value.toFixed(2);
        valueElement.classList.add('data-update');
        setTimeout(() => valueElement.classList.remove('data-update'), 600);
    }
    
    if (changeElement && previousValue !== null) {
        const change = value - previousValue;
        const changePercent = previousValue > 0 ? ((change / previousValue) * 100) : 0;
        
        let changeText = '';
        let changeClass = '';
        
        if (Math.abs(change) < 0.01) {
            changeText = '→ 0.00%';
            changeClass = 'text-muted';
        } else if (change > 0) {
            changeText = `▲ +${changePercent.toFixed(2)}%`;
            changeClass = 'text-success';
        } else {
            changeText = `▼ ${changePercent.toFixed(2)}%`;
            changeClass = 'text-danger';
        }
        
        changeElement.textContent = changeText;
        changeElement.className = `small ${changeClass}`;
    }
}

// Update sentiment metrics with colored badges
function updateSentimentMetric(source, value) {
    const badgeElement = document.getElementById(`${source}-badge`);
    const valueElement = document.getElementById(`${source}-sentiment`);
    
    if (badgeElement && valueElement) {
        let sentiment = 'Neutral';
        let badgeClass = 'sentiment-neutral';
        
        if (value > 0.1) {
            sentiment = 'Positive';
            badgeClass = 'sentiment-positive';
        } else if (value < -0.1) {
            sentiment = 'Negative';
            badgeClass = 'sentiment-negative';
        }
        
        badgeElement.textContent = sentiment;
        badgeElement.className = `sentiment-badge ${badgeClass}`;
        valueElement.textContent = value.toFixed(3);
    }
}

// Update AI analysis section
function updateAIAnalysis(analysis) {
    if (!analysis) return;
    
    // Update narrative
    const narrativeElement = document.getElementById('market-narrative');
    if (narrativeElement && analysis.market_narrative) {
        narrativeElement.textContent = analysis.market_narrative;
    }
    
    // Update timestamp
    const timestampElement = document.getElementById('analysis-timestamp');
    if (timestampElement && analysis.timestamp) {
        const date = new Date(analysis.timestamp);
        timestampElement.textContent = `Updated ${date.toLocaleTimeString()}`;
    }
    
    // Update key concerns
    const concernsElement = document.getElementById('key-concerns');
    if (concernsElement && analysis.key_concerns) {
        concernsElement.innerHTML = analysis.key_concerns
            .map(concern => `<li>• ${concern}</li>`)
            .join('');
    }
    
    // Update recommendations
    const recommendationsElement = document.getElementById('recommendations');
    if (recommendationsElement && analysis.specific_recommendations) {
        recommendationsElement.innerHTML = analysis.specific_recommendations
            .map(rec => `<li>• ${rec}</li>`)
            .join('');
    }
}

// Load historical data with time range support
function loadHistoricalData(days = 30) {
    console.log('Starting to load historical data...');
    fetch(`/api/simple_historical`)
        .then(response => {
            console.log('Historical data response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Historical data response:', data);
            
            if (data && data.success === true && data.data && Array.isArray(data.data) && data.data.length > 0) {
                console.log('SUCCESS: Updating chart with', data.data.length, 'data points');
                updateHistoricalChart(data.data);
            }
        })
        .catch(error => {
            console.error('Error loading historical data:', error);
        });
}

// Update historical chart with enhanced features
function updateHistoricalChart(historicalData) {
    console.log('Processing', historicalData.length, 'records for chart');
    
    const labels = [];
    const scores = [];
    const movingAverage = [];
    
    // Process data
    historicalData.forEach((record, index) => {
        const date = new Date(record.timestamp);
        const label = date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric' 
        });
        
        labels.push(label);
        scores.push(record.score);
        
        // Calculate 7-day moving average
        if (index >= 6) {
            const sum = historicalData.slice(index - 6, index + 1)
                .reduce((acc, item) => acc + item.score, 0);
            movingAverage.push(sum / 7);
        } else {
            movingAverage.push(null);
        }
    });
    
    console.log('Chart labels (first 5):', labels.slice(0, 5));
    console.log('Chart scores (first 5):', scores.slice(0, 5));
    console.log('Total data points:', labels.length);
    
    // Update chart
    riskChart.data.labels = labels;
    riskChart.data.datasets[0].data = scores;
    riskChart.data.datasets[1].data = movingAverage;
    
    riskChart.update('none');
    
    console.log('Historical chart updated successfully with', labels.length, 'days of data');
}

// Show notification toast
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Update connection status
function updateConnectionStatus(status, type) {
    const statusElement = document.getElementById('connection-status');
    if (statusElement) {
        statusElement.textContent = status;
        statusElement.className = `badge bg-${type}`;
    }
}

// Request update from server
function requestUpdate() {
    if (socket && socket.connected) {
        socket.emit('request_update');
    } else {
        // Fallback to HTTP request
        loadInitialData();
    }
}

// Show error state
function showErrorState() {
    const elements = document.querySelectorAll('.skeleton');
    elements.forEach(el => {
        el.classList.remove('skeleton');
        el.textContent = 'Error';
        el.style.color = '#dc3545';
    });
    
    updateConnectionStatus('Error', 'danger');
}

// Component tooltip functionality
function showComponentTooltip(segment) {
    const value = segment.getAttribute('data-value');
    const percentage = segment.getAttribute('data-percentage');
    
    if (value && percentage) {
        const tooltip = `${value}% (${percentage}% of total risk)`;
        segment.setAttribute('title', tooltip);
    }
}