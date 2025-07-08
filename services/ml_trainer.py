import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import joblib
import logging
from datetime import datetime, timedelta

class MLTrainer:
    def __init__(self):
        self.model_dir = "models"
        self.model_path = os.path.join(self.model_dir, "risk_predictor.pkl")
        self.data_path = os.path.join(self.model_dir, "training_data.csv")
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
    
    def train_model(self, use_real_data=False):
        """Train the ML model"""
        try:
            if use_real_data:
                X, y = self._load_real_data()
            else:
                X, y = self._generate_training_data()
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
            
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X, y, cv=5)
            
            # Save model
            joblib.dump(model, self.model_path)
            
            logging.info(f"✅ Model trained successfully. Accuracy: {accuracy:.4f}")
            logging.info(f"Cross-validation scores: {cv_scores}")
            
            return self.model_path, accuracy, len(X)
            
        except Exception as e:
            logging.error(f"❌ Error training ML model: {e}")
            raise
    
    def _generate_training_data(self, n_samples=1000):
        """Generate synthetic training data"""
        np.random.seed(42)
        
        # Generate features
        vix = np.random.normal(20, 5, n_samples)
        dxy = np.random.normal(100, 10, n_samples)
        spy = np.random.normal(440, 50, n_samples)
        reddit_sentiment = np.random.normal(0, 0.1, n_samples)
        twitter_sentiment = np.random.normal(0, 0.1, n_samples)
        news_sentiment = np.random.normal(0, 0.1, n_samples)
        
        # Calculate risk score (simplified)
        risk_score = (vix - 15) * 2 + (1 - (reddit_sentiment + twitter_sentiment + news_sentiment) / 3) * 25
        risk_score = np.clip(risk_score, 0, 100)
        
        # Create features matrix
        X = np.column_stack([vix, dxy, spy, reddit_sentiment, twitter_sentiment, news_sentiment, risk_score])
        
        # Generate labels (crash = 1, no crash = 0)
        # Higher VIX and risk score increase crash probability
        crash_prob = (vix > 25) & (risk_score > 60)
        y = crash_prob.astype(int)
        
        # Add some noise to make it more realistic
        noise = np.random.random(n_samples) < 0.1
        y = y ^ noise  # XOR with noise
        
        return X, y
    
    def _load_real_data(self):
        """Load real historical data for training"""
        try:
            if os.path.exists(self.data_path):
                df = pd.read_csv(self.data_path)
                
                # Extract features and labels
                feature_columns = ['vix', 'dxy', 'spy', 'reddit_sentiment', 'twitter_sentiment', 'news_sentiment', 'risk_score']
                X = df[feature_columns].values
                y = df['crash_label'].values
                
                return X, y
            else:
                logging.warning("⚠️ Real data file not found. Using synthetic data.")
                return self._generate_training_data()
                
        except Exception as e:
            logging.error(f"❌ Error loading real data: {e}")
            return self._generate_training_data()
    
    def retrain_model(self, new_data):
        """Retrain model with new data"""
        try:
            # Load existing model
            if os.path.exists(self.model_path):
                model = joblib.load(self.model_path)
            else:
                model = RandomForestClassifier(n_estimators=100, random_state=42)
            
            # Prepare new data
            X_new = new_data['features']
            y_new = new_data['labels']
            
            # Retrain model
            model.fit(X_new, y_new)
            
            # Save updated model
            joblib.dump(model, self.model_path)
            
            logging.info("✅ Model retrained successfully")
            return True
            
        except Exception as e:
            logging.error(f"❌ Error retraining model: {e}")
            return False
    
    def evaluate_model(self):
        """Evaluate the current model"""
        try:
            if not os.path.exists(self.model_path):
                return {"error": "Model not found"}
            
            model = joblib.load(self.model_path)
            
            # Generate test data
            X_test, y_test = self._generate_training_data(n_samples=200)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            
            # Get classification report
            report = classification_report(y_test, y_pred, output_dict=True)
            
            return {
                'accuracy': accuracy,
                'precision': report['1']['precision'],
                'recall': report['1']['recall'],
                'f1_score': report['1']['f1-score'],
                'test_samples': len(X_test)
            }
            
        except Exception as e:
            logging.error(f"❌ Error evaluating model: {e}")
            return {"error": str(e)}
