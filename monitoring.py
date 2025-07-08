import schedule
import time
import logging
from threading import Thread
from app import app, db, socketio
from models import RiskScore, SystemLog
from services.data_collector import DataCollector
from services.risk_calculator import RiskCalculator
from services.alert_system import AlertSystem
from services.disaster_recovery import DisasterRecoveryManager
from datetime import datetime

def log_system_event(level, message, component="monitoring"):
    """Log system events to database"""
    try:
        with app.app_context():
            log_entry = SystemLog(
                level=level,
                message=message,
                component=component
            )
            db.session.add(log_entry)
            db.session.commit()
    except Exception as e:
        logging.error(f"Failed to log system event: {e}")

def run_monitoring_cycle():
    """Run a single monitoring cycle"""
    try:
        with app.app_context():
            # Initialize services
            dr_manager = DisasterRecoveryManager()
            collector = DataCollector(dr_manager)
            calculator = RiskCalculator()
            alerter = AlertSystem()
            
            # Collect data
            market_data = collector.collect_market_data()
            sentiment_data = collector.collect_sentiment_data()
            
            # Calculate risk score
            risk_score = calculator.calculate_risk_score(market_data, sentiment_data)
            
            # Save to database
            new_score = RiskScore(
                score=risk_score['value'],
                level=risk_score['level'],
                market_data=market_data,
                sentiment_data=sentiment_data
            )
            db.session.add(new_score)
            db.session.commit()
            
            # Send alerts if threshold exceeded
            if risk_score['value'] >= 40:
                alerter.send_alert(risk_score)
                log_system_event("WARNING", f"Risk alert sent: {risk_score['level']} ({risk_score['value']})")
            
            # Emit real-time update via WebSocket
            socketio.emit('risk_update', {
                'risk_score': risk_score,
                'market_data': market_data,
                'sentiment_data': sentiment_data,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            log_system_event("INFO", "✅ Monitoring cycle complete")
            
    except Exception as e:
        logging.error(f"Error in monitoring cycle: {e}")
        log_system_event("ERROR", f"Monitoring cycle failed: {str(e)}")

def start_monitoring_system():
    """Start the monitoring system with scheduled tasks"""
    logging.info("🚀 Starting monitoring system background tasks")
    
    # Schedule monitoring cycle every minute
    schedule.every(1).minutes.do(run_monitoring_cycle)
    
    # Run continuously
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"Error in monitoring scheduler: {e}")
            time.sleep(5)  # Wait before retrying
