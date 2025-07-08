from app import db
from datetime import datetime
from sqlalchemy import JSON

class RiskScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float, nullable=False)
    level = db.Column(db.String(20), nullable=False)
    market_data = db.Column(JSON)
    sentiment_data = db.Column(JSON)

class AlertConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String(50), nullable=False)  # email, discord, telegram
    enabled = db.Column(db.Boolean, default=True)
    threshold = db.Column(db.Float, default=40.0)
    config_data = db.Column(JSON)  # Store channel-specific config
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    component = db.Column(db.String(50))

class BacktestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)
    parameters = db.Column(JSON)
    results = db.Column(JSON)
    performance_metrics = db.Column(JSON)

class MLModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    accuracy = db.Column(db.Float)
    training_data_size = db.Column(db.Integer)
    model_path = db.Column(db.String(255))
