import numpy as np
import logging
from datetime import datetime

class RiskCalculator:
    def __init__(self):
        self.vix_baseline = 20.0  # Normal VIX level
        self.dxy_baseline = 100.0  # Normal DXY level
        self.spy_ma_period = 20  # Moving average period
        
    def calculate_risk_score(self, market_data, sentiment_data):
        """Calculate comprehensive risk score using enhanced data sources"""
        try:
            # Core risk components
            vix_score = self._calculate_vix_score(market_data.get('vix', 20))
            sentiment_score = self._calculate_sentiment_score(sentiment_data)
            dxy_score = self._calculate_dxy_score(market_data.get('dxy', 100))
            momentum_score = self._calculate_momentum_score(market_data.get('spy', 440))
            
            # Enhanced risk components from comprehensive data
            credit_score = self._calculate_credit_risk_score(market_data)
            yield_curve_score = self._calculate_yield_curve_score(market_data)
            options_score = self._calculate_options_risk_score(market_data)
            economic_score = self._calculate_economic_risk_score(market_data)
            
            # Enhanced weighted combination
            raw_score = (
                vix_score * 0.20 +           # VIX gets 20% weight
                sentiment_score * 0.15 +     # Sentiment gets 15% weight
                dxy_score * 0.15 +          # Dollar strength gets 15% weight
                momentum_score * 0.15 +      # Momentum gets 15% weight
                credit_score * 0.15 +        # Credit spreads get 15% weight
                yield_curve_score * 0.10 +   # Yield curve gets 10% weight
                options_score * 0.05 +       # Options flow gets 5% weight
                economic_score * 0.05        # Economic indicators get 5% weight
            )
            
            # Normalize to 0-100 scale
            score = min(100, max(0, raw_score))
            
            # Determine risk level
            level = self._determine_risk_level(score)
            
            logging.info(f"Enhanced risk calculation: VIX={vix_score:.2f}, Sentiment={sentiment_score:.2f}, DXY={dxy_score:.2f}, Momentum={momentum_score:.2f}, Credit={credit_score:.2f}, YieldCurve={yield_curve_score:.2f}, Final={score:.2f}")
            
            return {
                'value': round(score, 2),
                'level': level,
                'components': {
                    'vix': round(vix_score, 2),
                    'sentiment': round(sentiment_score, 2),
                    'dxy': round(dxy_score, 2),
                    'momentum': round(momentum_score, 2),
                    'credit': round(credit_score, 2),
                    'yield_curve': round(yield_curve_score, 2),
                    'options': round(options_score, 2),
                    'economic': round(economic_score, 2)
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
    
    def _calculate_credit_risk_score(self, market_data):
        """Calculate credit risk score from spreads and bond ETFs"""
        try:
            # Get credit spread data from FRED
            credit_spread = market_data.get('credit_spread', 200)  # Default to 200bps
            
            # Get bond ETF data
            hyg_price = market_data.get('hyg', 80)  # High yield corporate bonds
            lqd_price = market_data.get('lqd', 120)  # Investment grade corporate bonds
            tlt_price = market_data.get('tlt', 90)   # Long-term treasuries
            
            # Calculate credit stress from spread
            if credit_spread > 500:
                spread_score = 80
            elif credit_spread > 350:
                spread_score = 60
            elif credit_spread > 250:
                spread_score = 40
            else:
                spread_score = 20
            
            # Calculate bond performance stress
            bond_stress = 0
            if hyg_price and lqd_price and tlt_price:
                # High yield underperformance vs treasuries indicates credit stress
                hy_vs_treasury = (hyg_price / tlt_price) * 100
                if hy_vs_treasury < 85:
                    bond_stress = 30
                elif hy_vs_treasury < 90:
                    bond_stress = 20
                else:
                    bond_stress = 10
            
            return min(100, spread_score + bond_stress)
            
        except Exception as e:
            logging.error(f"Error calculating credit risk: {e}")
            return 25
    
    def _calculate_yield_curve_score(self, market_data):
        """Calculate yield curve risk score"""
        try:
            # Get yield curve data
            three_month = market_data.get('three_month', 5.0)
            two_year = market_data.get('two_year', 4.5)
            ten_year = market_data.get('ten_year', 4.2)
            thirty_year = market_data.get('thirty_year', 4.4)
            
            # Calculate curve slope (10Y - 2Y)
            curve_slope = ten_year - two_year
            
            # Calculate inversion risk
            if curve_slope < -0.5:
                inversion_score = 80  # Deeply inverted
            elif curve_slope < -0.1:
                inversion_score = 60  # Inverted
            elif curve_slope < 0.5:
                inversion_score = 40  # Flat
            else:
                inversion_score = 20  # Normal
            
            # Calculate absolute yield level risk
            if ten_year > 6.0:
                yield_level_score = 60  # Very high rates
            elif ten_year > 5.0:
                yield_level_score = 40  # High rates
            elif ten_year < 2.0:
                yield_level_score = 30  # Very low rates
            else:
                yield_level_score = 10  # Normal rates
            
            return min(100, (inversion_score * 0.7) + (yield_level_score * 0.3))
            
        except Exception as e:
            logging.error(f"Error calculating yield curve risk: {e}")
            return 25
    
    def _calculate_options_risk_score(self, market_data):
        """Calculate options market risk score"""
        try:
            # Get options data
            put_call_ratio = market_data.get('put_call_ratio', 0.8)
            vix_skew = market_data.get('skew', 0.05)
            
            # Analyze put/call ratio
            if put_call_ratio > 1.5:
                pc_score = 70  # Excessive fear
            elif put_call_ratio > 1.2:
                pc_score = 50  # High fear
            elif put_call_ratio < 0.5:
                pc_score = 60  # Excessive complacency
            else:
                pc_score = 20  # Normal
            
            # Analyze skew
            if vix_skew and vix_skew > 0.1:
                skew_score = 40  # High skew indicates fear
            elif vix_skew and vix_skew < -0.05:
                skew_score = 30  # Negative skew unusual
            else:
                skew_score = 10  # Normal skew
            
            return min(100, (pc_score * 0.6) + (skew_score * 0.4))
            
        except Exception as e:
            logging.error(f"Error calculating options risk: {e}")
            return 25
    
    def _calculate_economic_risk_score(self, market_data):
        """Calculate economic indicators risk score"""
        try:
            # Get economic data
            unemployment = market_data.get('unemployment', 4.0)
            cpi = market_data.get('cpi', 3.0)
            consumer_confidence = market_data.get('consumer_confidence', 100)
            fed_funds_rate = market_data.get('fed_funds_rate', 5.0)
            
            risk_score = 0
            
            # Unemployment risk
            if unemployment > 6.0:
                risk_score += 30
            elif unemployment > 4.5:
                risk_score += 15
            elif unemployment < 3.5:
                risk_score += 10  # Too low can indicate overheating
            
            # Inflation risk
            if cpi > 5.0:
                risk_score += 25
            elif cpi > 3.5:
                risk_score += 15
            elif cpi < 1.0:
                risk_score += 20  # Deflation risk
            
            # Consumer confidence
            if consumer_confidence < 80:
                risk_score += 20
            elif consumer_confidence > 130:
                risk_score += 10  # Excessive optimism
            
            # Fed funds rate
            if fed_funds_rate > 6.0:
                risk_score += 15  # Very restrictive
            elif fed_funds_rate < 1.0:
                risk_score += 10  # Very accommodative
            
            return min(100, risk_score)
            
        except Exception as e:
            logging.error(f"Error calculating economic risk: {e}")
            return 25
