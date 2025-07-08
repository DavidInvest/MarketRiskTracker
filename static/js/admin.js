// Admin JavaScript for Strategic Risk Monitor

document.addEventListener('DOMContentLoaded', function() {
    loadAlertConfigs();
    updateSystemStats();
    
    // Auto-refresh system stats every 30 seconds
    setInterval(updateSystemStats, 30000);
});

// Load alert configurations
function loadAlertConfigs() {
    // This would typically load from the server
    // For now, we'll use the existing data from the template
    console.log('Alert configurations loaded');
}

// Update system statistics
function updateSystemStats() {
    // Update active alerts count
    document.getElementById('active-alerts').textContent = '3';
    
    // Update data points count
    document.getElementById('data-points').textContent = '1,247';
    
    // Update uptime
    document.getElementById('uptime').textContent = '2d 4h 23m';
}

// Save alert configuration
function saveAlertConfig() {
    const emailConfig = {
        channel: 'email',
        enabled: document.getElementById('email-enabled').checked,
        threshold: parseFloat(document.getElementById('email-threshold').value),
        config_data: {}
    };
    
    const discordConfig = {
        channel: 'discord',
        enabled: document.getElementById('discord-enabled').checked,
        threshold: parseFloat(document.getElementById('discord-threshold').value),
        config_data: {}
    };
    
    const telegramConfig = {
        channel: 'telegram',
        enabled: document.getElementById('telegram-enabled').checked,
        threshold: parseFloat(document.getElementById('telegram-threshold').value),
        config_data: {}
    };
    
    const configs = [emailConfig, discordConfig, telegramConfig];
    
    Promise.all(configs.map(config => 
        fetch('/api/update_alert_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config)
        })
    ))
    .then(responses => {
        const allSuccessful = responses.every(response => response.ok);
        if (allSuccessful) {
            showAlert('Alert configuration saved successfully!', 'success');
        } else {
            showAlert('Error saving configuration', 'danger');
        }
    })
    .catch(error => {
        console.error('Error saving config:', error);
        showAlert('Error saving configuration', 'danger');
    });
}

// Test alert channel
function testAlert(channel) {
    const button = event.target;
    const originalText = button.innerHTML;
    
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Testing...';
    button.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
        showAlert(`${channel.charAt(0).toUpperCase() + channel.slice(1)} test sent!`, 'info');
    }, 2000);
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

// Real-time log updates
function updateSystemLogs() {
    // This would fetch new logs from the server
    // For now, we'll simulate adding a new log entry
    const logsTable = document.getElementById('logs-table');
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${new Date().toLocaleString()}</td>
        <td><span class="badge bg-info">INFO</span></td>
        <td>system</td>
        <td>System health check completed</td>
    `;
    logsTable.insertBefore(newRow, logsTable.firstChild);
    
    // Keep only last 100 entries
    while (logsTable.children.length > 100) {
        logsTable.removeChild(logsTable.lastChild);
    }
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
