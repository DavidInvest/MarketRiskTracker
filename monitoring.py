import schedule
import time
import logging
from threading import Thread
from app import app, db, socketio
from models import RiskScore, SystemLog
from services.data_collector import DataCollector
from services.risk_calculator import RiskCalculator
from services.ml_risk_scorer import MLRiskScorer
from services.alert_system import AlertSystem
from services.disaster_recovery import DisasterRecoveryManager
from services.llm_risk_analyzer import LLMRiskAnalyzer
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
            ml_scorer = MLRiskScorer()
            alerter = AlertSystem()
            llm_analyzer = LLMRiskAnalyzer()
            
            # Load existing ML models or train new ones
            if not ml_scorer.load_models():
                logging.info("Training initial ML models...")
            
            # Collect data
            market_data = collector.collect_market_data()
            sentiment_data = collector.collect_sentiment_data()
            
            # Calculate enhanced risk score with ML
            basic_risk_score = calculator.calculate_risk_score(market_data, sentiment_data)
            ml_predictions = ml_scorer.predict_market_risks(market_data, sentiment_data)
            
            # Combine basic and ML scores (weighted approach)
            combined_score = (basic_risk_score['value'] * 0.6) + (ml_predictions['ml_risk_score'] * 0.4)
            risk_score = {
                'value': combined_score,
                'level': basic_risk_score['level'],
                'components': basic_risk_score.get('components', {}),
                'ml_predictions': ml_predictions
            }
            
            # Generate LLM-powered risk analysis
            risk_components = risk_score.get('components', {})
            llm_analysis = llm_analyzer.analyze_market_risks(market_data, sentiment_data, risk_components)
            
            # Save to database with LLM analysis
            new_score = RiskScore(
                score=risk_score['value'],
                level=risk_score['level'],
                market_data=market_data,
                sentiment_data=sentiment_data
            )
            db.session.add(new_score)
            db.session.commit()
            
            # Send intelligent alerts with LLM insights
            if risk_score['value'] >= 40:
                alert_insights = llm_analyzer.generate_alert_insights(risk_score['value'], market_data, sentiment_data)
                # Enhanced alert with LLM insights
                enhanced_risk_score = {**risk_score, 'llm_insights': alert_insights}
                alerter.send_alert(enhanced_risk_score)
                log_system_event("WARNING", f"Intelligent risk alert sent: {risk_score['level']} ({risk_score['value']}) - {alert_insights.get('alert_title', 'Risk Alert')}")
            
            # Emit real-time update via WebSocket with LLM analysis
            socketio.emit('risk_update', {
                'risk_score': risk_score,
                'market_data': market_data,
                'sentiment_data': sentiment_data,
                'llm_analysis': llm_analysis,
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
