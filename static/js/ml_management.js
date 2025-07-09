// ML Management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const trainingForm = document.getElementById('training-form');
    
    // Handle form submission
    trainingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        trainModel();
    });
});

function trainModel() {
    const btn = document.getElementById('train-model-btn');
    const progress = document.getElementById('training-progress');
    
    btn.disabled = true;
    btn.innerHTML = '<i data-feather="loader"></i> Training...';
    progress.style.display = 'block';
    
    // Get form data
    const formData = {
        model_name: document.getElementById('model-name').value,
        training_data: document.getElementById('training-data').value,
        model_type: document.getElementById('model-type').value
    };
    
    // Send request
    fetch('/api/train_model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayTrainingResults(data.results);
        } else {
            alert('Error training model: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error training model');
    })
    .finally(() => {
        btn.disabled = false;
        btn.innerHTML = '<i data-feather="play"></i> Train Model';
        progress.style.display = 'none';
        feather.replace();
    });
}

function displayTrainingResults(results) {
    document.getElementById('model-accuracy').textContent = results.accuracy.toFixed(1) + '%';
    document.getElementById('model-precision').textContent = results.validation_accuracy.toFixed(1) + '%';
    document.getElementById('model-recall').textContent = results.training_time.toFixed(1) + 's';
    
    // Show success message
    alert(`Model trained successfully!\nAccuracy: ${results.accuracy.toFixed(1)}%\nTraining Time: ${results.training_time.toFixed(1)}s`);
}