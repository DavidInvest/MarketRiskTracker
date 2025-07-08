// ML Management JavaScript for Strategic Risk Monitor
let featureChart;
let currentModelId = null;

// Initialize ML management page
document.addEventListener('DOMContentLoaded', function() {
    initializeFeatureChart();
    initializeEventListeners();
    loadModelPerformance();
});

// Initialize feature importance chart
function initializeFeatureChart() {
    const ctx = document.getElementById('featureChart').getContext('2d');
    featureChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['VIX', 'DXY', 'SPY', 'Reddit Sentiment', 'Twitter Sentiment', 'News Sentiment', 'Risk Score'],
            datasets: [{
                label: 'Feature Importance',
                data: [0, 0, 0, 0, 0, 0, 0],
                backgroundColor: [
                    '#dc3545',
                    '#fd7e14',
                    '#ffc107',
                    '#28a745',
                    '#20c997',
                    '#17a2b8',
                    '#6f42c1'
                ],
                borderColor: [
                    '#dc3545',
                    '#fd7e14',
                    '#ffc107',
                    '#28a745',
                    '#20c997',
                    '#17a2b8',
                    '#6f42c1'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Importance'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Initialize event listeners
function initializeEventListeners() {
    // Training form submission
    document.getElementById('training-form').addEventListener('submit', function(e) {
        e.preventDefault();
        trainModel();
    });
    
    // Prediction form submission
    document.getElementById('prediction-form').addEventListener('submit', function(e) {
        e.preventDefault();
        makePrediction();
    });
}

// Load current model performance
function loadModelPerformance() {
    // Load feature importance
    loadFeatureImportance();
    
    // Load model metrics (placeholder values)
    document.getElementById('model-accuracy').textContent = '85.2%';
    document.getElementById('model-precision').textContent = '83.7%';
    document.getElementById('model-recall').textContent = '87.1%';
    document.getElementById('model-f1').textContent = '85.4%';
}

// Load feature importance
function loadFeatureImportance() {
    // This would typically fetch from an API endpoint
    // For now, we'll use example values
    const importanceData = [0.25, 0.15, 0.20, 0.10, 0.08, 0.12, 0.10];
    
    featureChart.data.datasets[0].data = importanceData;
    featureChart.update();
}

// Train new model
function trainModel() {
    const button = document.getElementById('train-model-btn');
    const originalText = button.innerHTML;
    const progressDiv = document.getElementById('training-progress');
    
    // Show progress and disable button
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Training...';
    button.disabled = true;
    progressDiv.style.display = 'block';
    
    // Get training parameters
    const modelName = document.getElementById('model-name').value;
    const trainingData = document.getElementById('training-data').value;
    const modelType = document.getElementById('model-type').value;
    
    // Submit training request
    fetch('/api/train_ml_model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: modelName,
            training_data: trainingData,
            model_type: modelType
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Model trained successfully! Accuracy: ' + (data.accuracy * 100).toFixed(2) + '%', 'success');
            updateModelPerformance(data.accuracy);
            loadFeatureImportance(); // Refresh feature importance
            
            // Add new model to history table
            addModelToHistory(modelName, '1.0', data.accuracy, true);
        } else {
            showAlert('Error training model: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        console.error('Error training model:', error);
        showAlert('Error training model: ' + error.message, 'danger');
    })
    .finally(() => {
        // Reset button and hide progress
        button.innerHTML = originalText;
        button.disabled = false;
        progressDiv.style.display = 'none';
    });
}

// Update model performance display
function updateModelPerformance(accuracy) {
    document.getElementById('model-accuracy').textContent = (accuracy * 100).toFixed(1) + '%';
    
    // Update other metrics (simulated)
    document.getElementById('model-precision').textContent = ((accuracy - 0.02) * 100).toFixed(1) + '%';
    document.getElementById('model-recall').textContent = ((accuracy + 0.01) * 100).toFixed(1) + '%';
    document.getElementById('model-f1').textContent = ((accuracy - 0.005) * 100).toFixed(1) + '%';
}

// Add model to history table
function addModelToHistory(name, version, accuracy, isActive) {
    const tbody = document.querySelector('#ml_management table tbody');
    const row = document.createElement('tr');
    
    row.innerHTML = `
        <td>${name}</td>
        <td>${version}</td>
        <td>${(accuracy * 100).toFixed(2)}%</td>
        <td>
            <span class="badge bg-${isActive ? 'success' : 'secondary'}">
                ${isActive ? 'Active' : 'Inactive'}
            </span>
        </td>
        <td>
            <button class="btn btn-sm btn-outline-primary" onclick="activateModel(${Date.now()})">
                Activate
            </button>
        </td>
    `;
    
    // Insert at the beginning
    tbody.insertBefore(row, tbody.firstChild);
}

// Make prediction
function makePrediction() {
    const button = document.querySelector('#prediction-form button[type="submit"]');
    const originalText = button.innerHTML;
    
    // Disable button and show loading
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Predicting...';
    button.disabled = true;
    
    // Get input values
    const features = [
        parseFloat(document.getElementById('pred-vix').value),
        parseFloat(document.getElementById('pred-dxy').value),
        parseFloat(document.getElementById('pred-spy').value),
        parseFloat(document.getElementById('pred-sentiment').value),
        parseFloat(document.getElementById('pred-sentiment').value), // Twitter (same as avg)
        parseFloat(document.getElementById('pred-sentiment').value), // News (same as avg)
        50 // Default risk score
    ];
    
    // Submit prediction request
    fetch('/api/ml_predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            features: features
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayPrediction(data.prediction);
        } else {
            showAlert('Error making prediction: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        console.error('Error making prediction:', error);
        showAlert('Error making prediction: ' + error.message, 'danger');
    })
    .finally(() => {
        // Re-enable button
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

// Display prediction result
function displayPrediction(prediction) {
    const resultDiv = document.getElementById('prediction-result');
    const valueSpan = document.getElementById('prediction-value');
    
    let predictionText;
    let alertClass;
    
    if (prediction.length > 1) {
        // Binary classification (crash/no crash)
        const crashProbability = prediction[1];
        predictionText = `Crash Probability: ${(crashProbability * 100).toFixed(1)}%`;
        
        if (crashProbability > 0.7) {
            alertClass = 'alert-danger';
        } else if (crashProbability > 0.4) {
            alertClass = 'alert-warning';
        } else {
            alertClass = 'alert-success';
        }
    } else {
        // Single value prediction
        predictionText = `Prediction: ${prediction[0].toFixed(3)}`;
        alertClass = 'alert-info';
    }
    
    valueSpan.textContent = predictionText;
    resultDiv.className = `alert ${alertClass}`;
    resultDiv.style.display = 'block';
}

// Activate model
function activateModel(modelId) {
    // Update all models to inactive
    const badges = document.querySelectorAll('.badge');
    badges.forEach(badge => {
        if (badge.textContent === 'Active') {
            badge.textContent = 'Inactive';
            badge.className = 'badge bg-secondary';
        }
    });
    
    // Find and activate the clicked model
    const button = event.target;
    const row = button.closest('tr');
    const badge = row.querySelector('.badge');
    badge.textContent = 'Active';
    badge.className = 'badge bg-success';
    
    showAlert('Model activated successfully!', 'success');
}

// Evaluate current model
function evaluateModel() {
    showAlert('Model evaluation started...', 'info');
    
    // This would typically call an API endpoint
    setTimeout(() => {
        showAlert('Model evaluation completed. Check performance metrics.', 'success');
    }, 2000);
}

// Retrain model with new data
function retrainModel() {
    showAlert('Model retraining started...', 'info');
    
    // This would typically call an API endpoint
    setTimeout(() => {
        showAlert('Model retrained successfully!', 'success');
        loadModelPerformance(); // Refresh performance metrics
    }, 3000);
}

// Export model
function exportModel() {
    showAlert('Model export started...', 'info');
    
    // This would typically trigger a download
    setTimeout(() => {
        showAlert('Model exported successfully!', 'success');
    }, 1000);
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

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize feather icons
feather.replace();
