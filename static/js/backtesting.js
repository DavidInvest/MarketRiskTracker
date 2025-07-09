// Backtesting JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const backtestForm = document.getElementById('backtest-form');
    const riskThreshold = document.getElementById('risk-threshold');
    const thresholdValue = document.getElementById('threshold-value');
    
    // Update threshold display
    riskThreshold.addEventListener('input', function() {
        thresholdValue.textContent = this.value;
    });
    
    // Handle form submission
    backtestForm.addEventListener('submit', function(e) {
        e.preventDefault();
        runBacktest();
    });
});

function runBacktest() {
    const btn = document.getElementById('run-backtest-btn');
    btn.disabled = true;
    btn.innerHTML = '<i data-feather="loader"></i> Running...';
    
    // Get form data
    const formData = {
        name: document.getElementById('backtest-name').value,
        start_date: document.getElementById('start-date').value,
        end_date: document.getElementById('end-date').value,
        initial_capital: parseFloat(document.getElementById('initial-capital').value),
        risk_threshold: parseFloat(document.getElementById('risk-threshold').value)
    };
    
    // Send request
    fetch('/api/run_backtest', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayResults(data.results);
        } else {
            alert('Error running backtest: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error running backtest');
    })
    .finally(() => {
        btn.disabled = false;
        btn.innerHTML = '<i data-feather="play"></i> Run Backtest';
        feather.replace();
    });
}

function displayResults(results) {
    document.getElementById('total-return').textContent = results.total_return.toFixed(2) + '%';
    document.getElementById('sharpe-ratio').textContent = results.sharpe_ratio.toFixed(2);
    document.getElementById('max-drawdown').textContent = results.max_drawdown.toFixed(2) + '%';
    document.getElementById('num-trades').textContent = results.trades;
}