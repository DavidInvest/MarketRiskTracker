import os
import numpy as np
import joblib
import logging
from datetime import datetime

class MLIntegration:
    def __init__(self):
        self.model_path = "models/risk_predictor.pkl"
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained ML model"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logging.info("✅ ML model loaded successfully")
            else:
                logging.warning("⚠️ ML model not found. Please train a model first.")
        except Exception as e:
            logging.error(f"❌ Error loading ML model: {e}")
    
    def predict(self, features):
        """Make prediction using the ML model"""
        try:
            if self.model is None:
                logging.warning("⚠️ ML model not loaded")
                return np.array([0.5, 0.5])  # Default prediction
            
            # Ensure features is a numpy array with correct shape
            features = np.array(features).reshape(1, -1)
            
            # Make prediction
            prediction = self.model.predict_proba(features)
            
            logging.info(f"ML prediction made: {prediction[0]}")
            return prediction[0]
            
        except Exception as e:
            logging.error(f"❌ Error making ML prediction: {e}")
            return np.array([0.5, 0.5])  # Default prediction
    
    def predict_crash_probability(self, market_data, sentiment_data, risk_score):
        """Predict market crash probability based on current conditions"""
        try:
            # Prepare features for ML model
            features = self._prepare_features(market_data, sentiment_data, risk_score)
            
            # Get prediction
            prediction = self.predict(features)
            
            # Return crash probability (assuming binary classification)
            crash_probability = prediction[1] if len(prediction) > 1 else prediction[0]
            
            return {
                'crash_probability': float(crash_probability),
                'confidence': float(max(prediction)),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"❌ Error predicting crash probability: {e}")
            return {
                'crash_probability': 0.5,
                'confidence': 0.5,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _prepare_features(self, market_data, sentiment_data, risk_score):
        """Prepare features for ML model"""
        features = [
            market_data.get('vix', 20),
            market_data.get('dxy', 100),
            market_data.get('spy', 440),
            sentiment_data.get('reddit', 0),
            sentiment_data.get('twitter', 0),
            sentiment_data.get('news', 0),
            risk_score.get('value', 50)
        ]
        
        return features
    
    def get_feature_importance(self):
        """Get feature importance from the model"""
        try:
            if self.model is None or not hasattr(self.model, 'feature_importances_'):
                return {}
            
            feature_names = ['VIX', 'DXY', 'SPY', 'Reddit Sentiment', 'Twitter Sentiment', 'News Sentiment', 'Risk Score']
            importance = self.model.feature_importances_
            
            return {
                name: float(imp) for name, imp in zip(feature_names, importance)
            }
            
        except Exception as e:
            logging.error(f"❌ Error getting feature importance: {e}")
            return {}
