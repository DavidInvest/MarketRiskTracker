import os
import json
import logging
from datetime import datetime
from openai import OpenAI

class LLMRiskAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        # Using gpt-4o-mini as requested by user
        self.model = "gpt-4o-mini"
        
    def analyze_market_risks(self, market_data, sentiment_data, risk_components):
        """Generate comprehensive risk analysis with actionable insights"""
        try:
            # Prepare data summary for LLM
            data_summary = self._prepare_data_summary(market_data, sentiment_data, risk_components)
            
            prompt = f"""
            As a professional risk analyst, analyze this comprehensive market data and provide actionable insights:

            MARKET DATA:
            {data_summary}

            CURRENT RISK COMPONENTS:
            - VIX Score: {risk_components.get('vix', 0)}/100
            - Sentiment Score: {risk_components.get('sentiment', 0)}/100
            - Dollar Strength: {risk_components.get('dxy', 0)}/100
            - Momentum: {risk_components.get('momentum', 0)}/100
            - Credit Risk: {risk_components.get('credit', 0)}/100
            - Yield Curve: {risk_components.get('yield_curve', 0)}/100
            - Options Flow: {risk_components.get('options', 0)}/100
            - Economic Indicators: {risk_components.get('economic', 0)}/100

            Provide a comprehensive analysis in JSON format with:
            1. "risk_assessment": Overall risk evaluation (LOW/MODERATE/HIGH/EXTREME)
            2. "key_concerns": Top 3 immediate risk factors
            3. "market_narrative": 2-3 sentence explanation of current market conditions
            4. "specific_recommendations": Actionable hedging strategies
            5. "watchlist": Key indicators to monitor closely
            6. "probability_scenarios": Likelihood of different market outcomes
            7. "time_horizon": Risk timeline (immediate/short-term/medium-term)
            
            Focus on actionable insights, not just descriptions. Be specific about dollar amounts, percentages, and timeframes.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional risk analyst providing actionable market insights. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=1500,
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            analysis['timestamp'] = datetime.now().isoformat()
            
            logging.info("LLM risk analysis completed successfully")
            return analysis
            
        except Exception as e:
            logging.error(f"Error in LLM risk analysis: {e}")
            return self._fallback_analysis(risk_components)
    
    def generate_alert_insights(self, risk_score, market_data, sentiment_data):
        """Generate intelligent alert messages with context"""
        try:
            risk_level = self._determine_risk_level(risk_score)
            
            prompt = f"""
            Generate a concise alert message for a risk monitoring system:
            
            CURRENT SITUATION:
            - Risk Score: {risk_score}/100 ({risk_level})
            - SPY: ${market_data.get('spy', 'N/A')}
            - VIX: {market_data.get('vix', 'N/A')}
            - DXY: {market_data.get('dxy', 'N/A')}
            - Reddit Sentiment: {sentiment_data.get('reddit', 0)}
            - News Sentiment: {sentiment_data.get('news', 0)}
            
            Provide a JSON response with:
            1. "alert_title": Concise headline (max 50 chars)
            2. "alert_message": Brief explanation (max 200 chars)
            3. "immediate_action": Specific recommendation
            4. "urgency_level": 1-5 scale
            
            Focus on what users should DO, not just what's happening.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a risk analyst creating actionable alerts. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=300,
                temperature=0.2
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logging.error(f"Error generating alert insights: {e}")
            return {
                "alert_title": f"Risk Level: {risk_level}",
                "alert_message": f"Market risk score is {risk_score}/100. Monitor positions closely.",
                "immediate_action": "Review portfolio allocation and consider hedging.",
                "urgency_level": 3
            }
    
    def analyze_portfolio_exposure(self, portfolio_data, market_risk_analysis):
        """Analyze portfolio-specific risks with LLM insights"""
        try:
            prompt = f"""
            Analyze portfolio exposure given current market conditions:
            
            PORTFOLIO DATA:
            {json.dumps(portfolio_data, indent=2)}
            
            MARKET RISK ANALYSIS:
            {json.dumps(market_risk_analysis, indent=2)}
            
            Provide JSON response with:
            1. "portfolio_risk_level": Overall portfolio risk assessment
            2. "vulnerable_positions": Specific assets at risk
            3. "hedging_recommendations": Exact hedging strategies with instruments
            4. "position_sizing": Recommended allocation changes
            5. "stress_scenarios": How portfolio performs in different market scenarios
            6. "immediate_actions": Specific trades to consider today
            
            Be specific about percentages, strike prices, and expiration dates for options.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a portfolio risk analyst. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=1000,
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logging.error(f"Error analyzing portfolio exposure: {e}")
            return {"portfolio_risk_level": "MODERATE", "vulnerable_positions": [], "hedging_recommendations": []}
    
    def interpret_market_patterns(self, historical_data, current_conditions):
        """Identify market patterns and correlations with LLM analysis"""
        try:
            prompt = f"""
            Analyze market patterns and identify emerging risks:
            
            HISTORICAL PATTERNS:
            {json.dumps(historical_data[-10:], indent=2) if historical_data else "No historical data available"}
            
            CURRENT CONDITIONS:
            {json.dumps(current_conditions, indent=2)}
            
            Provide JSON response with:
            1. "pattern_identification": Key patterns detected
            2. "correlation_analysis": Important correlations breaking down
            3. "regime_change_probability": Likelihood of market regime shift
            4. "leading_indicators": Indicators suggesting future moves
            5. "risk_catalysts": Potential triggers for market stress
            6. "positioning_insights": How smart money is positioned
            
            Focus on patterns that predict future moves, not just describe current state.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a market pattern analyst. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=1000,
                temperature=0.4
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logging.error(f"Error interpreting market patterns: {e}")
            return {"pattern_identification": "Analysis unavailable", "correlation_analysis": "No patterns detected"}
    
    def _prepare_data_summary(self, market_data, sentiment_data, risk_components):
        """Prepare comprehensive data summary for LLM analysis"""
        return f"""
        MARKET INDICATORS:
        - SPY: ${market_data.get('spy', 'N/A')} | VIX: {market_data.get('vix', 'N/A')} | DXY: {market_data.get('dxy', 'N/A')}
        - 10Y Treasury: {market_data.get('ten_year', 'N/A')}% | Credit Spread: {market_data.get('credit_spread', 'N/A')}bps
        - REITs (VNQ): ${market_data.get('vnq', 'N/A')} | High Yield (HYG): ${market_data.get('hyg', 'N/A')}
        - Gold (GLD): ${market_data.get('gld', 'N/A')} | Oil (USO): ${market_data.get('uso', 'N/A')}
        - Put/Call Ratio: {market_data.get('put_call_ratio', 'N/A')}
        
        ECONOMIC DATA:
        - Fed Funds Rate: {market_data.get('fed_funds_rate', 'N/A')}%
        - Unemployment: {market_data.get('unemployment', 'N/A')}%
        - CPI: {market_data.get('cpi', 'N/A')}%
        - Consumer Confidence: {market_data.get('consumer_confidence', 'N/A')}
        
        SENTIMENT INDICATORS:
        - Reddit Sentiment: {sentiment_data.get('reddit', 0)}
        - News Sentiment: {sentiment_data.get('news', 0)}
        - Twitter Sentiment: {sentiment_data.get('twitter', 0)}
        """
    
    def _determine_risk_level(self, risk_score):
        """Determine risk level from numerical score"""
        if risk_score >= 70:
            return "EXTREME"
        elif risk_score >= 50:
            return "HIGH"
        elif risk_score >= 30:
            return "MODERATE"
        else:
            return "LOW"
    
    def _fallback_analysis(self, risk_components):
        """Provide fallback analysis when LLM fails"""
        total_score = sum(risk_components.values()) / len(risk_components)
        risk_level = self._determine_risk_level(total_score)
        
        return {
            "risk_assessment": risk_level,
            "key_concerns": ["Market volatility", "Economic uncertainty", "Liquidity conditions"],
            "market_narrative": f"Current risk score of {total_score:.1f}/100 indicates {risk_level.lower()} market risk conditions.",
            "specific_recommendations": ["Monitor position sizing", "Consider defensive allocation", "Review hedging strategies"],
            "watchlist": ["VIX levels", "Credit spreads", "Yield curve"],
            "probability_scenarios": {"continued_stability": 0.6, "moderate_correction": 0.3, "severe_stress": 0.1},
            "time_horizon": "short-term",
            "timestamp": datetime.now().isoformat()
        }