// Backtesting JavaScript for Strategic Risk Monitor
let portfolioChart;
let currentBacktestResults = null;

// Initialize backtesting page
document.addEventListener('DOMContentLoaded', function() {
    initializePortfolioChart();
    initializeEventListeners();
    updateThresholdDisplay();
});

// Initialize portfolio performance chart
function initializePortfolioChart() {
    const ctx = document.getElementById('portfolioChart').getContext('2d');
    portfolioChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Portfolio Value',
                data: [],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                fill: true,
                tension: 0.4
            }, {
                label: 'SPY Benchmark',
                data: [],
                borderColor: '#17a2b8',
                backgroundColor: 'rgba(23, 162, 184, 0.1)',
                fill: false,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Portfolio Value ($)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': $' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// Initialize event listeners
function initializeEventListeners() {
    // Backtest form submission
    document.getElementById('backtest-form').addEventListener('submit', function(e) {
        e.preventDefault();
        runBacktest();
    });
    
    // Risk threshold slider
    document.getElementById('risk-threshold').addEventListener('input', updateThresholdDisplay);
    
    // Set default dates
    const today = new Date();
    const threeYearsAgo = new Date();
    threeYearsAgo.setFullYear(today.getFullYear() - 3);
    
    document.getElementById('start-date').value = threeYearsAgo.toISOString().split('T')[0];
    document.getElementById('end-date').value = today.toISOString().split('T')[0];
}

// Update threshold display
function updateThresholdDisplay() {
    const threshold = document.getElementById('risk-threshold').value;
    document.getElementById('threshold-value').textContent = threshold;
}

// Run backtest
function runBacktest() {
    const button = document.getElementById('run-backtest-btn');
    const originalText = button.innerHTML;
    
    // Disable button and show loading
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Running...';
    button.disabled = true;
    
    // Clear previous results
    clearResults();
    
    // Prepare parameters
    const parameters = {
        start_date: document.getElementById('start-date').value,
        end_date: document.getElementById('end-date').value,
        initial_capital: parseFloat(document.getElementById('initial-capital').value),
        risk_threshold: parseFloat(document.getElementById('risk-threshold').value)
    };
    
    const backtestName = document.getElementById('backtest-name').value;
    
    // Submit backtest
    fetch('/api/run_backtest', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: backtestName,
            parameters: parameters
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentBacktestResults = data.results;
            displayResults(data.results);
            showAlert('Backtest completed successfully!', 'success');
        } else {
            showAlert('Error running backtest: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        console.error('Error running backtest:', error);
        showAlert('Error running backtest: ' + error.message, 'danger');
    })
    .finally(() => {
        // Re-enable button
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

// Display backtest results
function displayResults(results) {
    // Update performance summary
    document.getElementById('total-return').textContent = (results.total_return * 100).toFixed(2) + '%';
    document.getElementById('sharpe-ratio').textContent = results.sharpe_ratio.toFixed(2);
    document.getElementById('max-drawdown').textContent = (results.max_drawdown * 100).toFixed(2) + '%';
    document.getElementById('num-trades').textContent = results.num_trades;
    
    // Update portfolio chart
    updatePortfolioChart(results.portfolio_history);
    
    // Update trades table
    updateTradesTable(results.trades);
    
    // Color code performance metrics
    colorCodeMetrics(results);
}

// Update portfolio chart
function updatePortfolioChart(portfolioHistory) {
    const labels = portfolioHistory.map(item => new Date(item.date).toLocaleDateString());
    const portfolioValues = portfolioHistory.map(item => item.value);
    
    // Calculate benchmark (SPY buy and hold)
    const initialSpy = portfolioHistory[0].spy_price;
    const benchmarkValues = portfolioHistory.map(item => {
        const spyReturn = item.spy_price / initialSpy;
        return currentBacktestResults.initial_capital * spyReturn;
    });
    
    portfolioChart.data.labels = labels;
    portfolioChart.data.datasets[0].data = portfolioValues;
    portfolioChart.data.datasets[1].data = benchmarkValues;
    portfolioChart.update();
}

// Update trades table
function updateTradesTable(trades) {
    const tbody = document.getElementById('trades-table');
    tbody.innerHTML = '';
    
    trades.forEach(trade => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${new Date(trade.date).toLocaleDateString()}</td>
            <td>
                <span class="badge bg-${trade.action === 'BUY' ? 'success' : 'danger'}">
                    ${trade.action}
                </span>
            </td>
            <td>$${trade.price.toFixed(2)}</td>
            <td>${trade.risk_score.toFixed(1)}</td>
        `;
        tbody.appendChild(row);
    });
}

// Color code performance metrics
function colorCodeMetrics(results) {
    const returnElement = document.getElementById('total-return');
    const sharpeElement = document.getElementById('sharpe-ratio');
    const drawdownElement = document.getElementById('max-drawdown');
    
    // Color code total return
    if (results.total_return > 0) {
        returnElement.classList.add('text-success');
    } else {
        returnElement.classList.add('text-danger');
    }
    
    // Color code Sharpe ratio
    if (results.sharpe_ratio > 1) {
        sharpeElement.classList.add('text-success');
    } else if (results.sharpe_ratio > 0.5) {
        sharpeElement.classList.add('text-warning');
    } else {
        sharpeElement.classList.add('text-danger');
    }
    
    // Color code max drawdown
    if (Math.abs(results.max_drawdown) < 0.1) {
        drawdownElement.classList.add('text-success');
    } else if (Math.abs(results.max_drawdown) < 0.2) {
        drawdownElement.classList.add('text-warning');
    } else {
        drawdownElement.classList.add('text-danger');
    }
}

// Clear previous results
function clearResults() {
    document.getElementById('total-return').textContent = '--';
    document.getElementById('sharpe-ratio').textContent = '--';
    document.getElementById('max-drawdown').textContent = '--';
    document.getElementById('num-trades').textContent = '--';
    
    // Clear color classes
    const metrics = ['total-return', 'sharpe-ratio', 'max-drawdown'];
    metrics.forEach(id => {
        const element = document.getElementById(id);
        element.classList.remove('text-success', 'text-warning', 'text-danger');
    });
    
    // Clear chart
    portfolioChart.data.labels = [];
    portfolioChart.data.datasets[0].data = [];
    portfolioChart.data.datasets[1].data = [];
    portfolioChart.update();
    
    // Clear trades table
    document.getElementById('trades-table').innerHTML = '';
}

// Load previous backtest
function loadBacktest(backtestId) {
    // This would fetch the backtest results from the server
    // For now, we'll show a placeholder
    showAlert('Loading backtest #' + backtestId, 'info');
}

// Show alert message
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main content
    const mainContent = document.querySelector('main');
    mainContent.insertBefore(alertDiv, mainContent.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Export results to CSV
function exportResults() {
    if (!currentBacktestResults) {
        showAlert('No backtest results to export', 'warning');
        return;
    }
    
    const csvContent = generateCSV(currentBacktestResults);
    downloadCSV(csvContent, 'backtest_results.csv');
}

// Generate CSV content
function generateCSV(results) {
    let csv = 'Date,Portfolio Value,SPY Price,Risk Score\n';
    
    results.portfolio_history.forEach(item => {
        csv += `${item.date},${item.value},${item.spy_price},${item.risk_score}\n`;
    });
    
    return csv;
}

// Download CSV file
function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Initialize feather icons
feather.replace();
