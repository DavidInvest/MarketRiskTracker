import numpy as np
import pandas as pd
import logging
from datetime import datetime, timedelta
from services.risk_calculator import RiskCalculator

class Backtester:
    def __init__(self):
        self.risk_calculator = RiskCalculator()
        
    def run_backtest(self, parameters):
        """Run backtesting with given parameters"""
        try:
            # Extract parameters
            start_date = parameters.get('start_date', '2020-01-01')
            end_date = parameters.get('end_date', '2023-12-31')
            initial_capital = parameters.get('initial_capital', 100000)
            risk_threshold = parameters.get('risk_threshold', 60)
            
            # Generate synthetic historical data
            historical_data = self._generate_historical_data(start_date, end_date)
            
            # Run backtest
            results = self._execute_backtest(historical_data, initial_capital, risk_threshold)
            
            logging.info(f"✅ Backtest completed. Final portfolio value: ${results['final_value']:,.2f}")
            
            return results
            
        except Exception as e:
            logging.error(f"❌ Error running backtest: {e}")
            raise
    
    def _generate_historical_data(self, start_date, end_date):
        """Generate synthetic historical market data"""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Generate daily data
        dates = pd.date_range(start=start, end=end, freq='D')
        n_days = len(dates)
        
        # Generate market data with realistic patterns
        np.random.seed(42)
        
        # SPY prices (with trend and volatility)
        spy_returns = np.random.normal(0.0005, 0.015, n_days)  # Daily returns
        spy_prices = 400 * np.exp(np.cumsum(spy_returns))
        
        # VIX (mean-reverting)
        vix_base = 20
        vix_values = []
        current_vix = vix_base
        
        for i in range(n_days):
            # Mean reversion
            vix_change = np.random.normal(0, 2) - 0.1 * (current_vix - vix_base)
            current_vix = max(10, min(80, current_vix + vix_change))
            vix_values.append(current_vix)
        
        # DXY (dollar index)
        dxy_returns = np.random.normal(0, 0.005, n_days)
        dxy_prices = 100 * np.exp(np.cumsum(dxy_returns))
        
        # Sentiment data
        reddit_sentiment = np.random.normal(0, 0.1, n_days)
        twitter_sentiment = np.random.normal(0, 0.1, n_days)
        news_sentiment = np.random.normal(0, 0.1, n_days)
        
        # Create DataFrame
        data = pd.DataFrame({
            'date': dates,
            'spy': spy_prices,
            'vix': vix_values,
            'dxy': dxy_prices,
            'reddit_sentiment': reddit_sentiment,
            'twitter_sentiment': twitter_sentiment,
            'news_sentiment': news_sentiment
        })
        
        return data
    
    def _execute_backtest(self, data, initial_capital, risk_threshold):
        """Execute backtesting logic"""
        portfolio_value = initial_capital
        cash = initial_capital
        positions = 0
        
        portfolio_history = []
        trades = []
        
        for i, row in data.iterrows():
            # Calculate risk score
            market_data = {
                'spy': row['spy'],
                'vix': row['vix'],
                'dxy': row['dxy']
            }
            
            sentiment_data = {
                'reddit': row['reddit_sentiment'],
                'twitter': row['twitter_sentiment'],
                'news': row['news_sentiment']
            }
            
            risk_score = self.risk_calculator.calculate_risk_score(market_data, sentiment_data)
            
            # Trading logic
            if risk_score['value'] > risk_threshold and positions > 0:
                # Sell positions (risk too high)
                cash = positions * row['spy']
                positions = 0
                trades.append({
                    'date': row['date'],
                    'action': 'SELL',
                    'price': row['spy'],
                    'risk_score': risk_score['value']
                })
            elif risk_score['value'] < risk_threshold * 0.7 and positions == 0:
                # Buy positions (risk acceptable)
                positions = cash / row['spy']
                cash = 0
                trades.append({
                    'date': row['date'],
                    'action': 'BUY',
                    'price': row['spy'],
                    'risk_score': risk_score['value']
                })
            
            # Calculate portfolio value
            current_value = cash + (positions * row['spy'])
            portfolio_history.append({
                'date': row['date'],
                'value': current_value,
                'risk_score': risk_score['value'],
                'spy_price': row['spy'],
                'vix': row['vix']
            })
        
        # Calculate final results
        final_value = cash + (positions * data.iloc[-1]['spy'])
        total_return = (final_value - initial_capital) / initial_capital
        
        # Calculate performance metrics
        portfolio_df = pd.DataFrame(portfolio_history)
        daily_returns = portfolio_df['value'].pct_change().dropna()
        
        volatility = daily_returns.std() * np.sqrt(252)  # Annualized
        sharpe_ratio = (daily_returns.mean() * 252) / volatility if volatility > 0 else 0
        
        max_drawdown = self._calculate_max_drawdown(portfolio_df['value'])
        
        return {
            'initial_capital': initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'num_trades': len(trades),
            'portfolio_history': portfolio_history,
            'trades': trades
        }
    
    def _calculate_max_drawdown(self, portfolio_values):
        """Calculate maximum drawdown"""
        peak = portfolio_values.expanding().max()
        drawdown = (portfolio_values - peak) / peak
        return drawdown.min()
    
    def calculate_performance_metrics(self, results):
        """Calculate additional performance metrics"""
        try:
            portfolio_history = results['portfolio_history']
            
            if not portfolio_history:
                return {}
            
            df = pd.DataFrame(portfolio_history)
            
            # Calculate metrics
            total_days = len(df)
            profitable_days = len(df[df['value'] > results['initial_capital']])
            
            metrics = {
                'win_rate': profitable_days / total_days if total_days > 0 else 0,
                'average_daily_return': df['value'].pct_change().mean(),
                'best_day': df['value'].pct_change().max(),
                'worst_day': df['value'].pct_change().min(),
                'total_trading_days': total_days
            }
            
            return metrics
            
        except Exception as e:
            logging.error(f"❌ Error calculating performance metrics: {e}")
            return {}
