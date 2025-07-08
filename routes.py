from flask import render_template, request, jsonify, redirect, url_for
from flask_socketio import emit
from app import app, db, socketio
from models import RiskScore, AlertConfig, SystemLog, BacktestResult, MLModel
from services.risk_calculator import RiskCalculator
from services.data_collector import DataCollector
from services.alert_system import AlertSystem
from services.backtesting import Backtester
from services.ml_integration import MLIntegration
from services.ml_trainer import MLTrainer
from services.disaster_recovery import DisasterRecoveryManager
from datetime import datetime, timedelta
import json
import logging

# Initialize services lazily
dr_manager = None
data_collector = None
risk_calculator = None
alert_system = None
backtester = None
ml_integration = None
ml_trainer = None

def init_services():
    global dr_manager, data_collector, risk_calculator, alert_system, backtester, ml_integration, ml_trainer
    try:
        if dr_manager is None:
            logging.info("Initializing services...")
            dr_manager = DisasterRecoveryManager()
            data_collector = DataCollector(dr_manager)
            risk_calculator = RiskCalculator()
            alert_system = AlertSystem()
            backtester = Backtester()
            ml_integration = MLIntegration()
            ml_trainer = MLTrainer()
            logging.info("All services initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing services: {e}")
        raise

@app.route('/')
def dashboard():
    """Main dashboard page"""
    try:
        init_services()
        
        # Get latest risk score
        latest_score = RiskScore.query.order_by(RiskScore.timestamp.desc()).first()
        
        # Get recent scores for chart
        recent_scores = RiskScore.query.order_by(RiskScore.timestamp.desc()).limit(50).all()
        
        return render_template('dashboard.html', 
                             latest_score=latest_score,
                             recent_scores=recent_scores)
    except Exception as e:
        logging.error(f"Error in dashboard route: {e}")
        return f"""
        <h1>Strategic Risk Monitor</h1>
        <p>System is initializing... Dashboard will be available shortly.</p>
        <p>Error: {str(e)}</p>
        <p><a href="/health">Health Check</a> | <a href="/admin">Admin Panel</a></p>
        """, 200

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.route('/admin')
def admin():
    """Admin panel for system configuration"""
    alert_configs = AlertConfig.query.all()
    system_logs = SystemLog.query.order_by(SystemLog.timestamp.desc()).limit(100).all()
    
    return render_template('admin.html', 
                         alert_configs=alert_configs,
                         system_logs=system_logs)

@app.route('/backtesting')
def backtesting():
    """Backtesting interface"""
    backtest_results = BacktestResult.query.order_by(BacktestResult.timestamp.desc()).all()
    return render_template('backtesting.html', backtest_results=backtest_results)

@app.route('/ml_management')
def ml_management():
    """ML model management interface"""
    ml_models = MLModel.query.order_by(MLModel.created_at.desc()).all()
    return render_template('ml_management.html', ml_models=ml_models)

@app.route('/api/risk_data')
def get_risk_data():
    """API endpoint to get latest risk data"""
    try:
        # Ensure services are initialized
        init_services()
        
        market_data = data_collector.collect_market_data()
        sentiment_data = data_collector.collect_sentiment_data()
        risk_score = risk_calculator.calculate_risk_score(market_data, sentiment_data)
        
        # Save to database
        new_score = RiskScore(
            score=risk_score['value'],
            level=risk_score['level'],
            market_data=market_data,
            sentiment_data=sentiment_data
        )
        db.session.add(new_score)
        db.session.commit()
        
        # Format response with proper structure for frontend
        response = {
            'success': True,
            'risk_score': {
                'value': risk_score['value'],
                'level': risk_score['level'],
                'components': risk_score.get('components', {})
            },
            'market_data': market_data,
            'sentiment_data': sentiment_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error getting risk data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/quick_data')
def quick_data():
    """Quick data endpoint for dashboard - only essential data"""
    try:
        init_services()
        
        # Get only the latest database record instead of collecting new data
        latest_score = RiskScore.query.order_by(RiskScore.timestamp.desc()).first()
        
        if latest_score:
            # Ensure proper data structure
            market_data = latest_score.market_data or {}
            sentiment_data = latest_score.sentiment_data or {}
            
            # Extract the essential values safely
            spy_value = market_data.get('spy', 0)
            vix_value = market_data.get('vix', 0)
            dxy_value = market_data.get('dxy', 0)
            
            reddit_sentiment = sentiment_data.get('reddit', 0)
            twitter_sentiment = sentiment_data.get('twitter', 0)
            news_sentiment = sentiment_data.get('news', 0)
            
            response = {
                'success': True,
                'risk_score': {
                    'value': float(latest_score.score),
                    'level': latest_score.level,
                    'components': {}
                },
                'market_data': {
                    'spy': float(spy_value),
                    'vix': float(vix_value),
                    'dxy': float(dxy_value),
                    'timestamp': latest_score.timestamp.isoformat()
                },
                'sentiment_data': {
                    'reddit': float(reddit_sentiment),
                    'twitter': float(twitter_sentiment),
                    'news': float(news_sentiment)
                },
                'timestamp': latest_score.timestamp.isoformat(),
                'source': 'database'
            }
            
            return jsonify(response)
        else:
            # If no database records, collect fresh data
            market_data = data_collector.collect_market_data()
            sentiment_data = data_collector.collect_sentiment_data()
            risk_score = risk_calculator.calculate_risk_score(market_data, sentiment_data)
            
            return jsonify({
                'success': True,
                'risk_score': {
                    'value': risk_score['value'],
                    'level': risk_score['level'],
                    'components': risk_score.get('components', {})
                },
                'market_data': market_data,
                'sentiment_data': sentiment_data,
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'fresh'
            })
    except Exception as e:
        logging.error(f"Error in quick_data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test_data')
def test_data():
    """Simple test endpoint to verify data collection"""
    try:
        init_services()
        market_data = data_collector.collect_market_data()
        return jsonify({
            'success': True,
            'market_data': market_data,
            'message': 'Data collection working'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/historical_data')
def get_historical_data():
    """API endpoint to get historical risk data"""
    try:
        days = request.args.get('days', 7, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        scores = RiskScore.query.filter(
            RiskScore.timestamp >= start_date
        ).order_by(RiskScore.timestamp.asc()).all()
        
        data = [{
            'timestamp': score.timestamp.isoformat(),
            'score': score.score,
            'level': score.level,
            'market_data': score.market_data,
            'sentiment_data': score.sentiment_data
        } for score in scores]
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        logging.error(f"Error getting historical data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/update_alert_config', methods=['POST'])
def update_alert_config():
    """API endpoint to update alert configuration"""
    try:
        data = request.get_json()
        config_id = data.get('id')
        
        if config_id:
            config = AlertConfig.query.get(config_id)
        else:
            config = AlertConfig(channel=data.get('channel'))
            db.session.add(config)
        
        config.enabled = data.get('enabled', True)
        config.threshold = data.get('threshold', 40.0)
        config.config_data = data.get('config_data', {})
        config.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error updating alert config: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/run_backtest', methods=['POST'])
def run_backtest():
    """API endpoint to run backtesting"""
    try:
        data = request.get_json()
        name = data.get('name', 'Backtest')
        parameters = data.get('parameters', {})
        
        # Run backtest
        results = backtester.run_backtest(parameters)
        
        # Save results
        backtest_result = BacktestResult(
            name=name,
            parameters=parameters,
            results=results,
            performance_metrics=backtester.calculate_performance_metrics(results)
        )
        db.session.add(backtest_result)
        db.session.commit()
        
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        logging.error(f"Error running backtest: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/train_ml_model', methods=['POST'])
def train_ml_model():
    """API endpoint to train ML model"""
    try:
        data = request.get_json()
        model_name = data.get('name', 'Risk Predictor')
        
        # Train model
        model_path, accuracy, training_size = ml_trainer.train_model()
        
        # Save model info
        ml_model = MLModel(
            name=model_name,
            version="1.0",
            accuracy=accuracy,
            training_data_size=training_size,
            model_path=model_path
        )
        db.session.add(ml_model)
        db.session.commit()
        
        return jsonify({'success': True, 'accuracy': accuracy})
    except Exception as e:
        logging.error(f"Error training ML model: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ml_predict', methods=['POST'])
def ml_predict():
    """API endpoint for ML predictions"""
    try:
        from services.ml_risk_scorer import MLRiskScorer
        
        data = request.get_json()
        market_data = data.get('market_data', {})
        sentiment_data = data.get('sentiment_data', {})
        
        # Initialize ML scorer and try to load models
        ml_scorer = MLRiskScorer()
        if not ml_scorer.load_models():
            # If no models exist, train them quickly with synthetic data
            logging.info("No ML models found, training new models...")
            training_data = ml_scorer._generate_synthetic_training_data(200)
            success = ml_scorer.train_models(training_data)
            if not success:
                return jsonify({'success': False, 'error': 'Failed to train ML models'})
        
        # Get ML predictions
        predictions = ml_scorer.predict_market_risks(market_data, sentiment_data)
        
        return jsonify({
            'success': True,
            'predictions': predictions
        })
        
    except Exception as e:
        logging.error(f"Error making ML prediction: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('connected', {'message': 'Connected to risk monitoring system'})

@socketio.on('request_update')
def handle_update_request():
    """Handle request for real-time updates"""
    try:
        market_data = data_collector.collect_market_data()
        sentiment_data = data_collector.collect_sentiment_data()
        risk_score = risk_calculator.calculate_risk_score(market_data, sentiment_data)
        
        emit('risk_update', {
            'risk_score': risk_score,
            'market_data': market_data,
            'sentiment_data': sentiment_data,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logging.error(f"Error sending update: {e}")
        emit('error', {'message': str(e)})

@app.route('/api/train_advanced_ml', methods=['POST'])
def train_advanced_ml():
    """API endpoint to train advanced ML models"""
    try:
        from services.ml_risk_scorer import MLRiskScorer
        import pandas as pd
        
        ml_scorer = MLRiskScorer()
        
        # Get historical data for training
        historical_scores = RiskScore.query.order_by(RiskScore.timestamp.desc()).limit(1000).all()
        
        if len(historical_scores) < 10:
            # Generate synthetic training data if insufficient real data
            logging.info("Insufficient historical data, generating synthetic training data")
            training_data = ml_scorer._generate_synthetic_training_data(500)
        else:
            # Convert historical scores to training format
            training_data = []
            for score in historical_scores:
                training_data.append({
                    'market_data': score.market_data or {},
                    'sentiment_data': score.sentiment_data or {},
                    'risk_score': score.score,
                    'timestamp': score.timestamp
                })
            training_data = pd.DataFrame(training_data)
        
        # Train the models
        success = ml_scorer.train_models(training_data)
        
        if success:
            performance = ml_scorer.get_model_performance()
            feature_importance = ml_scorer.get_feature_importance()
            
            return jsonify({
                'success': True, 
                'message': 'Advanced ML models trained successfully',
                'performance': performance,
                'feature_importance': feature_importance
            })
        else:
            return jsonify({'success': False, 'error': 'Training failed'})
            
    except Exception as e:
        logging.error(f"Error training advanced ML models: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
