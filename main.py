from app import app, socketio
from monitoring import start_monitoring_system
import threading
import logging
import os

if __name__ == "__main__":
    # Start the monitoring system in a separate thread
    monitoring_thread = threading.Thread(target=start_monitoring_system, daemon=True)
    monitoring_thread.start()
    
    logging.info("🚀 Starting Strategic Risk Monitoring System")
    
    # Run the Flask-SocketIO server
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, use_reloader=False)
