import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import logging
from datetime import datetime, timedelta
import yfinance as yf
import requests

class MLRiskScorer:
    def __init__(self):
        self.models = {
            'crash_predictor_1d': None,
            'crash_predictor_3d': None,
            'crash_predictor_7d': None,
            'crash_predictor_14d': None,
            'crash_predictor_30d': None,
            'risk_scorer': None,
            'sentiment_analyzer': None
        }
        self.scalers = {}
        self.feature_importance = {}
        self.performance_metrics = {}
        try:
            from fredapi import Fred
            self.fred = Fred()  # No API key needed for basic access
        except ImportError:
            self.fred = None
            logging.warning("FRED API not available, using fallback economic data")
        
    def engineer_features(self, market_data, sentiment_data, lookback_days=252):
        """Create sophisticated features for ML models"""
        try:
            features = {}
            
            # Basic market features
            features['spy_price'] = market_data.get('spy', 440)
            features['vix'] = market_data.get('vix', 20)
            features['dxy'] = market_data.get('dxy', 100)
            features['ten_year'] = market_data.get('ten_year', 4.5)
            
            # Technical indicators (calculated from historical data)
            spy_data = self._get_historical_data('SPY', lookback_days)
            if len(spy_data) > 20:
                # RSI
                features['rsi_14'] = self._calculate_rsi(spy_data['Close'], 14)
                features['rsi_30'] = self._calculate_rsi(spy_data['Close'], 30)
                
                # Moving averages
                features['sma_20'] = spy_data['Close'].rolling(20).mean().iloc[-1]
                features['sma_50'] = spy_data['Close'].rolling(50).mean().iloc[-1]
                features['sma_200'] = spy_data['Close'].rolling(200).mean().iloc[-1]
                
                # Price position relative to MAs
                current_price = spy_data['Close'].iloc[-1]
                features['price_vs_sma20'] = (current_price - features['sma_20']) / features['sma_20']
                features['price_vs_sma50'] = (current_price - features['sma_50']) / features['sma_50']
                features['price_vs_sma200'] = (current_price - features['sma_200']) / features['sma_200']
                
                # Volatility features
                features['volatility_20d'] = spy_data['Close'].pct_change().rolling(20).std() * np.sqrt(252)
                features['volatility_60d'] = spy_data['Close'].pct_change().rolling(60).std() * np.sqrt(252)
                
                # Volume analysis
                if 'Volume' in spy_data.columns:
                    features['volume_ratio'] = spy_data['Volume'].iloc[-1] / spy_data['Volume'].rolling(20).mean().iloc[-1]
                    features['volume_trend'] = spy_data['Volume'].rolling(5).mean().iloc[-1] / spy_data['Volume'].rolling(20).mean().iloc[-1]
                
                # Momentum indicators
                features['momentum_1d'] = spy_data['Close'].pct_change(1).iloc[-1]
                features['momentum_5d'] = spy_data['Close'].pct_change(5).iloc[-1]
                features['momentum_20d'] = spy_data['Close'].pct_change(20).iloc[-1]
                
                # Bollinger Bands
                bb_middle = spy_data['Close'].rolling(20).mean()
                bb_std = spy_data['Close'].rolling(20).std()
                bb_upper = bb_middle + (bb_std * 2)
                bb_lower = bb_middle - (bb_std * 2)
                features['bb_position'] = (current_price - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])
                
            # Sentiment features
            features['reddit_sentiment'] = sentiment_data.get('reddit', 0)
            features['news_sentiment'] = sentiment_data.get('news', 0)
            features['twitter_sentiment'] = sentiment_data.get('twitter', 0)
            features['avg_sentiment'] = (features['reddit_sentiment'] + features['news_sentiment'] + features['twitter_sentiment']) / 3
            
            # Market structure features
            sector_data = self._get_sector_performance()
            features.update(sector_data)
            
            # Economic indicators from FRED
            economic_features = self._get_fred_features()
            features.update(economic_features)
            
            # Interaction features (key insight from the PDF)
            features['vix_yield_interaction'] = features['vix'] * features['ten_year']
            features['sentiment_volatility_interaction'] = features['avg_sentiment'] * features.get('volatility_20d', 1)
            features['dxy_vix_interaction'] = features['dxy'] * features['vix']
            
            # Market breadth features
            breadth_data = self._get_market_breadth()
            features.update(breadth_data)
            
            # Options market features
            options_features = self._get_options_features()
            features.update(options_features)
            
            return pd.Series(features).fillna(0)
            
        except Exception as e:
            logging.error(f"Error engineering features: {e}")
            # Return basic features if advanced feature engineering fails
            return pd.Series({
                'spy_price': market_data.get('spy', 440),
                'vix': market_data.get('vix', 20),
                'dxy': market_data.get('dxy', 100),
                'ten_year': market_data.get('ten_year', 4.5),
                'reddit_sentiment': sentiment_data.get('reddit', 0),
                'news_sentiment': sentiment_data.get('news', 0),
                'twitter_sentiment': sentiment_data.get('twitter', 0)
            })
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 50
    
    def _get_historical_data(self, symbol, days):
        """Get historical data using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            data = ticker.history(start=start_date, end=end_date)
            return data
        except Exception as e:
            logging.error(f"Error getting historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _get_sector_performance(self):
        """Get sector ETF performance"""
        try:
            sectors = ['XLF', 'XLK', 'XLV', 'XLE', 'XLI', 'XLU', 'XLB', 'XLRE', 'XLP', 'XLY']
            sector_features = {}
            
            for sector in sectors[:5]:  # Limit to avoid API limits
                try:
                    ticker = yf.Ticker(sector)
                    hist = ticker.history(period='5d')
                    if not hist.empty:
                        sector_features[f'{sector.lower()}_5d_return'] = hist['Close'].pct_change(4).iloc[-1]
                except:
                    sector_features[f'{sector.lower()}_5d_return'] = 0
            
            return sector_features
        except Exception as e:
            logging.error(f"Error getting sector performance: {e}")
            return {}
    
    def _get_fred_features(self):
        """Get economic indicators from FRED API"""
        try:
            fred_features = {}
            
            if self.fred is not None:
                # Key economic indicators (free access)
                fred_series = {
                    'fed_funds_rate': 'DFF',
                    'unemployment_rate': 'UNRATE',
                    'cpi_yoy': 'CPIAUCSL',
                    'real_gdp_growth': 'GDPC1'
                }
                
                for name, series_id in fred_series.items():
                    try:
                        # Get latest available data
                        data = self.fred.get_series(series_id, limit=1)
                        if not data.empty:
                            fred_features[name] = data.iloc[-1]
                        else:
                            fred_features[name] = 0
                    except:
                        fred_features[name] = 0
            else:
                # Fallback values when FRED API is not available
                fred_features = {
                    'fed_funds_rate': 5.0,
                    'unemployment_rate': 4.0,
                    'cpi_yoy': 3.0,
                    'real_gdp_growth': 2.0
                }
                    
            return fred_features
            
        except Exception as e:
            logging.error(f"Error getting FRED features: {e}")
            return {
                'fed_funds_rate': 5.0,
                'unemployment_rate': 4.0,
                'cpi_yoy': 3.0,
                'real_gdp_growth': 2.0
            }
    
    def _get_market_breadth(self):
        """Calculate market breadth indicators"""
        try:
            # Use free market breadth approximation
            breadth_features = {}
            
            # Get Russell 2000 vs S&P 500 ratio (small cap vs large cap)
            spy_data = yf.Ticker('SPY').history(period='20d')
            iwm_data = yf.Ticker('IWM').history(period='20d')
            
            if not spy_data.empty and not iwm_data.empty:
                spy_return = spy_data['Close'].pct_change(19).iloc[-1]
                iwm_return = iwm_data['Close'].pct_change(19).iloc[-1]
                breadth_features['small_large_ratio'] = iwm_return / spy_return if spy_return != 0 else 1
            else:
                breadth_features['small_large_ratio'] = 1
                
            return breadth_features
            
        except Exception as e:
            logging.error(f"Error calculating market breadth: {e}")
            return {'small_large_ratio': 1}
    
    def _get_options_features(self):
        """Get options market indicators"""
        try:
            options_features = {}
            
            # VIX term structure (free from CBOE)
            vix_data = yf.Ticker('^VIX').history(period='5d')
            vix9d_data = yf.Ticker('^VIX9D').history(period='5d')
            
            if not vix_data.empty:
                current_vix = vix_data['Close'].iloc[-1]
                options_features['vix_level'] = current_vix
                
                if not vix9d_data.empty:
                    vix9d = vix9d_data['Close'].iloc[-1]
                    options_features['vix_term_structure'] = current_vix / vix9d if vix9d != 0 else 1
                else:
                    options_features['vix_term_structure'] = 1
            else:
                options_features['vix_level'] = 20
                options_features['vix_term_structure'] = 1
                
            return options_features
            
        except Exception as e:
            logging.error(f"Error getting options features: {e}")
            return {'vix_level': 20, 'vix_term_structure': 1}
    
    def train_models(self, training_data, retrain=False):
        """Train all ML models with comprehensive feature engineering"""
        try:
            logging.info("Starting ML model training with advanced features...")
            
            if len(training_data) < 100:
                logging.warning("Insufficient training data, using synthetic data generation")
                training_data = self._generate_synthetic_training_data()
            
            # Prepare features and targets
            X = []
            y_crash_1d, y_crash_3d, y_crash_7d, y_crash_14d, y_crash_30d = [], [], [], [], []
            y_risk_score, y_sentiment = [], []
            
            for i, row in training_data.iterrows():
                # Engineer features for this data point
                features = self.engineer_features(row.get('market_data', {}), row.get('sentiment_data', {}))
                X.append(features.values)
                
                # Create target variables
                y_crash_1d.append(self._calculate_crash_probability(row, 1))
                y_crash_3d.append(self._calculate_crash_probability(row, 3))
                y_crash_7d.append(self._calculate_crash_probability(row, 7))
                y_crash_14d.append(self._calculate_crash_probability(row, 14))
                y_crash_30d.append(self._calculate_crash_probability(row, 30))
                
                y_risk_score.append(row.get('risk_score', 50))
                y_sentiment.append(row.get('market_direction', 0))
            
            X = np.array(X)
            feature_names = features.index.tolist()
            
            # Scale features
            scaler = RobustScaler()  # More robust to outliers than StandardScaler
            X_scaled = scaler.fit_transform(X)
            self.scalers['features'] = scaler
            
            # Train models for each prediction horizon
            models_to_train = {
                'crash_predictor_1d': y_crash_1d,
                'crash_predictor_3d': y_crash_3d,
                'crash_predictor_7d': y_crash_7d,
                'crash_predictor_14d': y_crash_14d,
                'crash_predictor_30d': y_crash_30d,
                'risk_scorer': y_risk_score,
                'sentiment_analyzer': y_sentiment
            }
            
            for model_name, y_target in models_to_train.items():
                logging.info(f"Training {model_name}...")
                
                # Try multiple algorithms and select best
                algorithms = [
                    ('RandomForest', RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)),
                    ('GradientBoosting', GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=6)),
                    ('NeuralNetwork', MLPRegressor(hidden_layer_sizes=(100, 50), random_state=42, max_iter=500))
                ]
                
                best_score = -np.inf
                best_model = None
                best_algorithm = None
                
                # Time series cross-validation
                tscv = TimeSeriesSplit(n_splits=5)
                
                for algo_name, algorithm in algorithms:
                    try:
                        scores = cross_val_score(algorithm, X_scaled, y_target, cv=tscv, scoring='r2')
                        avg_score = np.mean(scores)
                        
                        if avg_score > best_score:
                            best_score = avg_score
                            best_model = algorithm
                            best_algorithm = algo_name
                            
                    except Exception as e:
                        logging.warning(f"Failed to train {algo_name} for {model_name}: {e}")
                        continue
                
                if best_model is not None:
                    # Train final model on all data
                    best_model.fit(X_scaled, y_target)
                    self.models[model_name] = best_model
                    
                    # Calculate feature importance
                    if hasattr(best_model, 'feature_importances_'):
                        importance = dict(zip(feature_names, best_model.feature_importances_))
                        self.feature_importance[model_name] = importance
                    
                    # Store performance metrics
                    self.performance_metrics[model_name] = {
                        'algorithm': best_algorithm,
                        'cv_score': best_score,
                        'trained_at': datetime.now().isoformat()
                    }
                    
                    logging.info(f"{model_name} trained successfully with {best_algorithm} (R² = {best_score:.3f})")
                else:
                    logging.error(f"Failed to train {model_name}")
            
            # Save models
            self._save_models()
            logging.info("ML model training completed successfully")
            
            return True
            
        except Exception as e:
            logging.error(f"Error training ML models: {e}")
            return False
    
    def _calculate_crash_probability(self, row, days_ahead):
        """Calculate crash probability for given time horizon"""
        # Simplified crash probability based on risk components
        vix = row.get('market_data', {}).get('vix', 20)
        sentiment = row.get('sentiment_data', {}).get('reddit', 0)
        
        # Higher VIX and negative sentiment increase crash probability
        base_prob = min(0.9, max(0.1, (vix - 10) / 50))
        sentiment_adj = max(-0.3, min(0.3, sentiment * -10))  # Negative sentiment increases risk
        
        # Adjust for time horizon (longer periods have higher probability)
        time_factor = min(2.0, 1 + (days_ahead - 1) * 0.1)
        
        crash_prob = min(0.95, max(0.05, (base_prob + sentiment_adj) * time_factor))
        return crash_prob
    
    def _generate_synthetic_training_data(self, n_samples=1000):
        """Generate synthetic training data for initial model training"""
        np.random.seed(42)
        training_data = []
        
        for i in range(n_samples):
            # Generate realistic market conditions
            vix = np.random.normal(20, 8)
            vix = max(10, min(50, vix))
            
            spy = np.random.normal(440, 50)
            dxy = np.random.normal(100, 5)
            ten_year = np.random.normal(4.5, 1)
            
            reddit_sentiment = np.random.normal(0, 0.1)
            news_sentiment = np.random.normal(0, 0.1)
            
            # Calculate corresponding risk score
            risk_score = min(100, max(0, vix * 2 + abs(reddit_sentiment) * 100 + (ten_year - 2) * 10))
            
            training_data.append({
                'market_data': {
                    'spy': spy,
                    'vix': vix,
                    'dxy': dxy,
                    'ten_year': ten_year
                },
                'sentiment_data': {
                    'reddit': reddit_sentiment,
                    'news': news_sentiment,
                    'twitter': 0
                },
                'risk_score': risk_score,
                'market_direction': reddit_sentiment
            })
        
        return pd.DataFrame(training_data)
    
    def predict_market_risks(self, market_data, sentiment_data):
        """Generate ML-based risk predictions"""
        try:
            # Engineer features
            features = self.engineer_features(market_data, sentiment_data)
            
            if 'features' not in self.scalers:
                logging.warning("Models not trained yet, using fallback scoring")
                return self._fallback_predictions(market_data, sentiment_data)
            
            # Scale features
            X = self.scalers['features'].transform([features.values])
            
            predictions = {}
            
            # Generate predictions from each model
            for model_name, model in self.models.items():
                if model is not None:
                    try:
                        pred = model.predict(X)[0]
                        predictions[model_name] = max(0, min(1 if 'crash' in model_name else 100, pred))
                    except Exception as e:
                        logging.error(f"Error predicting with {model_name}: {e}")
                        predictions[model_name] = 0.5 if 'crash' in model_name else 50
            
            # Calculate composite risk score
            crash_scores = [v for k, v in predictions.items() if 'crash' in k]
            ml_risk_score = predictions.get('risk_scorer', 50)
            
            # Weight recent predictions more heavily
            weighted_crash_prob = (
                predictions.get('crash_predictor_1d', 0.5) * 0.4 +
                predictions.get('crash_predictor_3d', 0.5) * 0.3 +
                predictions.get('crash_predictor_7d', 0.5) * 0.2 +
                predictions.get('crash_predictor_14d', 0.5) * 0.1
            )
            
            return {
                'ml_risk_score': ml_risk_score,
                'crash_probability_1d': predictions.get('crash_predictor_1d', 0.5),
                'crash_probability_3d': predictions.get('crash_predictor_3d', 0.5),
                'crash_probability_7d': predictions.get('crash_predictor_7d', 0.5),
                'crash_probability_14d': predictions.get('crash_predictor_14d', 0.5),
                'crash_probability_30d': predictions.get('crash_predictor_30d', 0.5),
                'weighted_crash_probability': weighted_crash_prob,
                'market_sentiment_prediction': predictions.get('sentiment_analyzer', 0),
                'confidence_score': self._calculate_prediction_confidence(features),
                'feature_contributions': self._get_feature_contributions(features, model_name='risk_scorer')
            }
            
        except Exception as e:
            logging.error(f"Error in ML risk prediction: {e}")
            return self._fallback_predictions(market_data, sentiment_data)
    
    def _fallback_predictions(self, market_data, sentiment_data):
        """Fallback predictions when ML models aren't available"""
        vix = market_data.get('vix', 20)
        sentiment = sentiment_data.get('reddit', 0)
        
        # Simple rule-based fallback
        base_risk = min(100, max(0, vix * 2.5))
        sentiment_adj = abs(sentiment) * 50
        
        return {
            'ml_risk_score': min(100, base_risk + sentiment_adj),
            'crash_probability_1d': min(0.8, vix / 50),
            'crash_probability_3d': min(0.85, vix / 45),
            'crash_probability_7d': min(0.9, vix / 40),
            'crash_probability_14d': min(0.95, vix / 35),
            'crash_probability_30d': min(0.95, vix / 30),
            'weighted_crash_probability': min(0.8, vix / 50),
            'market_sentiment_prediction': sentiment,
            'confidence_score': 0.3,
            'feature_contributions': {}
        }
    
    def _calculate_prediction_confidence(self, features):
        """Calculate confidence in predictions based on feature quality"""
        try:
            # Simple confidence calculation based on data completeness
            non_zero_features = sum(1 for x in features.values if x != 0)
            total_features = len(features)
            return min(1.0, non_zero_features / total_features)
        except:
            return 0.5
    
    def _get_feature_contributions(self, features, model_name):
        """Get feature contributions to the prediction"""
        try:
            if model_name in self.feature_importance:
                importance = self.feature_importance[model_name]
                contributions = {}
                for i, feature_name in enumerate(features.index):
                    if feature_name in importance:
                        contributions[feature_name] = importance[feature_name] * features.values[i]
                return contributions
            return {}
        except:
            return {}
    
    def _save_models(self):
        """Save trained models and scalers"""
        try:
            model_dir = 'models'
            os.makedirs(model_dir, exist_ok=True)
            
            # Save models
            for name, model in self.models.items():
                if model is not None:
                    joblib.dump(model, f'{model_dir}/{name}.pkl')
            
            # Save scalers
            for name, scaler in self.scalers.items():
                joblib.dump(scaler, f'{model_dir}/scaler_{name}.pkl')
            
            # Save metadata
            metadata = {
                'feature_importance': self.feature_importance,
                'performance_metrics': self.performance_metrics,
                'trained_at': datetime.now().isoformat()
            }
            joblib.dump(metadata, f'{model_dir}/metadata.pkl')
            
            logging.info("Models saved successfully")
            
        except Exception as e:
            logging.error(f"Error saving models: {e}")
    
    def load_models(self):
        """Load trained models and scalers"""
        try:
            model_dir = 'models'
            
            # Load models
            for name in self.models.keys():
                model_path = f'{model_dir}/{name}.pkl'
                if os.path.exists(model_path):
                    self.models[name] = joblib.load(model_path)
            
            # Load scalers
            scaler_path = f'{model_dir}/scaler_features.pkl'
            if os.path.exists(scaler_path):
                self.scalers['features'] = joblib.load(scaler_path)
            
            # Load metadata
            metadata_path = f'{model_dir}/metadata.pkl'
            if os.path.exists(metadata_path):
                metadata = joblib.load(metadata_path)
                self.feature_importance = metadata.get('feature_importance', {})
                self.performance_metrics = metadata.get('performance_metrics', {})
            
            logging.info("Models loaded successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error loading models: {e}")
            return False
    
    def retrain_models(self, new_data):
        """Retrain models with new data"""
        logging.info("Starting model retraining...")
        return self.train_models(new_data, retrain=True)
    
    def get_model_performance(self):
        """Get current model performance metrics"""
        return self.performance_metrics
    
    def get_feature_importance(self):
        """Get feature importance for all models"""
        return self.feature_importance