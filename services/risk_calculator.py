import numpy as np
import logging
from datetime import datetime

class RiskCalculator:
    def __init__(self):
        self.vix_baseline = 20.0  # Normal VIX level
        self.dxy_baseline = 100.0  # Normal DXY level
        self.spy_ma_period = 20  # Moving average period
        
    def calculate_risk_score(self, market_data, sentiment_data):
        """Calculate comprehensive risk score"""
        try:
            # VIX component (40% weight)
            vix_score = self._calculate_vix_score(market_data.get('vix', 20))
            
            # Sentiment component (30% weight)
            sentiment_score = self._calculate_sentiment_score(sentiment_data)
            
            # Dollar strength component (20% weight)
            dxy_score = self._calculate_dxy_score(market_data.get('dxy', 100))
            
            # Market momentum component (10% weight)
            momentum_score = self._calculate_momentum_score(market_data.get('spy', 440))
            
            # Weighted combination
            raw_score = (
                vix_score * 0.4 +
                sentiment_score * 0.3 +
                dxy_score * 0.2 +
                momentum_score * 0.1
            )
            
            # Normalize to 0-100 scale
            score = min(100, max(0, raw_score))
            
            # Determine risk level
            level = self._determine_risk_level(score)
            
            logging.info(f"Risk calculation: VIX={vix_score:.2f}, Sentiment={sentiment_score:.2f}, DXY={dxy_score:.2f}, Momentum={momentum_score:.2f}, Final={score:.2f}")
            
            return {
                'value': round(score, 2),
                'level': level,
                'components': {
                    'vix': round(vix_score, 2),
                    'sentiment': round(sentiment_score, 2),
                    'dxy': round(dxy_score, 2),
                    'momentum': round(momentum_score, 2)
                },
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error calculating risk score: {e}")
            return {
                'value': 50.0,
                'level': 'YELLOW',
                'components': {},
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _calculate_vix_score(self, vix_value):
        """Calculate VIX-based risk score"""
        if vix_value < 15:
            return 10  # Very low fear
        elif vix_value < 20:
            return 20  # Low fear
        elif vix_value < 25:
            return 40  # Normal fear
        elif vix_value < 30:
            return 60  # High fear
        elif vix_value < 35:
            return 80  # Very high fear
        else:
            return 100  # Extreme fear
    
    def _calculate_sentiment_score(self, sentiment_data):
        """Calculate sentiment-based risk score"""
        # Average sentiment across sources
        reddit_sentiment = sentiment_data.get('reddit', 0)
        twitter_sentiment = sentiment_data.get('twitter', 0)
        news_sentiment = sentiment_data.get('news', 0)
        
        avg_sentiment = (reddit_sentiment + twitter_sentiment + news_sentiment) / 3
        
        # Convert sentiment to risk score (negative sentiment = higher risk)
        if avg_sentiment >= 0.1:
            return 20  # Very positive sentiment
        elif avg_sentiment >= 0.05:
            return 30  # Positive sentiment
        elif avg_sentiment >= -0.05:
            return 50  # Neutral sentiment
        elif avg_sentiment >= -0.1:
            return 70  # Negative sentiment
        else:
            return 90  # Very negative sentiment
    
    def _calculate_dxy_score(self, dxy_value):
        """Calculate DXY-based risk score"""
        # Strong dollar can indicate flight to safety
        if dxy_value < 95:
            return 20  # Weak dollar
        elif dxy_value < 100:
            return 30  # Moderate dollar
        elif dxy_value < 105:
            return 40  # Normal dollar strength
        elif dxy_value < 110:
            return 60  # Strong dollar
        else:
            return 80  # Very strong dollar
    
    def _calculate_momentum_score(self, spy_value):
        """Calculate momentum-based risk score"""
        # For now, use a simple approach
        # In a real system, this would compare to moving averages
        if spy_value > 450:
            return 30  # Strong momentum
        elif spy_value > 430:
            return 40  # Moderate momentum
        elif spy_value > 410:
            return 50  # Neutral momentum
        elif spy_value > 390:
            return 60  # Weak momentum
        else:
            return 70  # Very weak momentum
    
    def _determine_risk_level(self, score):
        """Determine risk level based on score"""
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        elif score >= 20:
            return "LOW"
        else:
            return "MINIMAL"
    
    def calculate_portfolio_risk(self, portfolio_data, market_risk_score):
        """Calculate portfolio-specific risk assessment"""
        try:
            # Get portfolio beta, correlation, and concentration
            beta = portfolio_data.get('beta', 1.0)
            correlation = portfolio_data.get('correlation', 0.8)
            concentration = portfolio_data.get('concentration', 0.1)
            
            # Adjust market risk for portfolio characteristics
            portfolio_multiplier = (beta * 0.4) + (correlation * 0.3) + (concentration * 0.3)
            
            portfolio_risk = market_risk_score * portfolio_multiplier
            
            return {
                'portfolio_risk': round(portfolio_risk, 2),
                'market_risk': market_risk_score,
                'beta_impact': round(beta * market_risk_score * 0.4, 2),
                'correlation_impact': round(correlation * market_risk_score * 0.3, 2),
                'concentration_impact': round(concentration * market_risk_score * 0.3, 2)
            }
            
        except Exception as e:
            logging.error(f"Error calculating portfolio risk: {e}")
            return {'portfolio_risk': market_risk_score, 'market_risk': market_risk_score}
