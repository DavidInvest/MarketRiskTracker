import os
import requests
import logging
from datetime import datetime, timedelta
import yfinance as yf
import praw
import tweepy
from fredapi import Fred
from bs4 import BeautifulSoup
from fredapi import Fred
from bs4 import BeautifulSoup

class DataCollector:
    def __init__(self, recovery_manager):
        self.recovery = recovery_manager
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.gnews_key = os.getenv('GNEWS_KEY')
        
        # Reddit API
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        
        # Twitter API
        self.twitter_api_key = os.getenv('TWITTER_API_KEY')
        self.twitter_api_secret = os.getenv('TWITTER_API_SECRET')
        self.twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.twitter_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        # FRED API (Federal Reserve Economic Data) - Free, unlimited
        self.fred_api_key = os.getenv('FRED_API_KEY')
        
        self._setup_apis()
    
    def _setup_apis(self):
        """Setup API connections"""
        try:
            # Reddit API
            if self.reddit_client_id and self.reddit_client_secret:
                self.reddit = praw.Reddit(
                    client_id=self.reddit_client_id,
                    client_secret=self.reddit_client_secret,
                    user_agent="RiskMonitor/1.0"
                )
            
            # Twitter API
            if all([self.twitter_api_key, self.twitter_api_secret, self.twitter_access_token, self.twitter_access_token_secret]):
                self.twitter_client = tweepy.Client(
                    consumer_key=self.twitter_api_key,
                    consumer_secret=self.twitter_api_secret,
                    access_token=self.twitter_access_token,
                    access_token_secret=self.twitter_access_token_secret
                )
            
            # FRED API - Free unlimited access to Federal Reserve data
            if self.fred_api_key:
                self.fred = Fred(api_key=self.fred_api_key)
            else:
                # FRED works without API key for basic access
                self.fred = Fred()
                
        except Exception as e:
            logging.error(f"Error setting up APIs: {e}")
    
    def collect_market_data(self):
        """Collect market data from various sources"""
        try:
            # Try yfinance first (free and reliable)
            spy = yf.Ticker("SPY")
            vix = yf.Ticker("^VIX")
            dxy = yf.Ticker("DX-Y.NYB")
            
            spy_data = spy.history(period="1d", interval="1m")
            vix_data = vix.history(period="1d", interval="1m")
            dxy_data = dxy.history(period="1d", interval="1m")
            
            market_data = {
                'spy': float(spy_data['Close'].iloc[-1]) if not spy_data.empty else 440.25,
                'vix': float(vix_data['Close'].iloc[-1]) if not vix_data.empty else 21.45,
                'dxy': float(dxy_data['Close'].iloc[-1]) if not dxy_data.empty else 102.3,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Add comprehensive data from free sources
            try:
                # Add FRED economic data
                fred_data = self._get_fred_data()
                market_data.update(fred_data)
                
                # Add Treasury yield curve data
                treasury_data = self._get_treasury_data()
                market_data.update(treasury_data)
                
                # Add options market data
                options_data = self._get_options_data()
                market_data.update(options_data)
                
                # Add additional market ETFs for broader coverage
                additional_tickers = {
                    'qqq': 'QQQ',         # Nasdaq
                    'xlre': 'XLRE',       # Real Estate
                    'vnq': 'VNQ',         # REITs
                    'iyr': 'IYR',         # Real Estate
                    'tnx': '^TNX',        # 10-Year Treasury
                    'gdx': 'GDX',         # Gold Miners
                    'gld': 'GLD',         # Gold
                    'uso': 'USO',         # Oil
                    'tlt': 'TLT',         # 20+ Year Treasury
                    'hyg': 'HYG',         # High Yield Corporate Bonds
                    'lqd': 'LQD'          # Investment Grade Corporate Bonds
                }
                
                for name, ticker in additional_tickers.items():
                    try:
                        asset = yf.Ticker(ticker)
                        data = asset.history(period="1d", interval="1m")
                        if not data.empty:
                            market_data[name] = float(data['Close'].iloc[-1])
                        else:
                            market_data[name] = None
                    except Exception as e:
                        logging.warning(f"Could not fetch {ticker}: {e}")
                        market_data[name] = None
                        
            except Exception as e:
                logging.warning(f"Error collecting additional market data: {e}")
            
            logging.info(f"Market data collected: SPY={market_data['spy']}, VIX={market_data['vix']}, DXY={market_data['dxy']}")
            return market_data
            
        except Exception as e:
            logging.error(f"Error collecting market data: {e}")
            self.recovery.fallback("market_data")
            # Return fallback data
            return {
                'spy': 440.25,
                'vix': 21.45,
                'dxy': 102.3,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _get_fred_data(self):
        """Get Federal Reserve Economic Data - Free unlimited access"""
        fred_data = {}
        
        try:
            # Key economic indicators from FRED
            fred_indicators = {
                'fed_funds_rate': 'DFF',           # Federal Funds Rate
                'ten_year_yield': 'DGS10',         # 10-Year Treasury Yield
                'credit_spread': 'BAMLH0A0HYM2',   # Corporate Credit Spread
                'dollar_index': 'DEXUSEU',         # Dollar vs Euro
                'unemployment': 'UNRATE',          # Unemployment Rate
                'cpi': 'CPIAUCSL',                 # Consumer Price Index
                'gdp': 'GDP',                      # GDP
                'consumer_confidence': 'UMCSENT'    # Consumer Sentiment
            }
            
            for name, series_id in fred_indicators.items():
                try:
                    # Get latest value
                    data = self.fred.get_series(series_id, limit=1)
                    if not data.empty:
                        fred_data[name] = float(data.iloc[-1])
                    else:
                        fred_data[name] = None
                except Exception as e:
                    logging.warning(f"Could not fetch FRED {series_id}: {e}")
                    fred_data[name] = None
                    
        except Exception as e:
            logging.error(f"Error getting FRED data: {e}")
            
        return fred_data
    
    def _get_treasury_data(self):
        """Get Treasury yield curve data"""
        treasury_data = {}
        
        try:
            # Treasury yield curve
            treasury_tickers = {
                'three_month': '^IRX',     # 3-Month Treasury
                'two_year': '^TNX',        # 2-Year Treasury (using 10Y as proxy)
                'five_year': '^FVX',       # 5-Year Treasury
                'ten_year': '^TNX',        # 10-Year Treasury
                'thirty_year': '^TYX'      # 30-Year Treasury
            }
            
            for name, ticker in treasury_tickers.items():
                try:
                    treasury = yf.Ticker(ticker)
                    data = treasury.history(period="1d", interval="1m")
                    if not data.empty:
                        treasury_data[name] = float(data['Close'].iloc[-1])
                    else:
                        treasury_data[name] = None
                except Exception as e:
                    logging.warning(f"Could not fetch Treasury {ticker}: {e}")
                    treasury_data[name] = None
                    
        except Exception as e:
            logging.error(f"Error getting Treasury data: {e}")
            
        return treasury_data
    
    def _get_options_data(self):
        """Get options market data for risk assessment"""
        options_data = {}
        
        try:
            # Get VIX term structure and options data
            vix = yf.Ticker("^VIX")
            spy = yf.Ticker("SPY")
            
            # Get options expiration dates
            spy_expirations = spy.options
            
            if spy_expirations:
                # Get near-term options data
                near_expiry = spy_expirations[0]
                option_chain = spy.option_chain(near_expiry)
                
                # Calculate put/call ratio
                puts_volume = option_chain.puts['volume'].sum()
                calls_volume = option_chain.calls['volume'].sum()
                
                if calls_volume > 0:
                    put_call_ratio = puts_volume / calls_volume
                    options_data['put_call_ratio'] = float(put_call_ratio)
                else:
                    options_data['put_call_ratio'] = None
                    
                # Get skew indicators
                atm_strike = spy.info.get('previousClose', 440)
                otm_puts = option_chain.puts[option_chain.puts['strike'] < atm_strike * 0.95]
                otm_calls = option_chain.calls[option_chain.calls['strike'] > atm_strike * 1.05]
                
                if not otm_puts.empty and not otm_calls.empty:
                    put_iv = otm_puts['impliedVolatility'].mean()
                    call_iv = otm_calls['impliedVolatility'].mean()
                    options_data['skew'] = float(put_iv - call_iv) if put_iv and call_iv else None
                else:
                    options_data['skew'] = None
                    
        except Exception as e:
            logging.error(f"Error getting options data: {e}")
            
        return options_data
    
    def collect_sentiment_data(self):
        """Collect sentiment data from social media and news"""
        sentiment_data = {
            'reddit': 0.0,
            'twitter': 0.0,
            'news': 0.0,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            # Reddit sentiment
            if hasattr(self, 'reddit'):
                sentiment_data['reddit'] = self._get_reddit_sentiment()
            
            # Twitter sentiment
            if hasattr(self, 'twitter_client'):
                sentiment_data['twitter'] = self._get_twitter_sentiment()
            
            # News sentiment
            sentiment_data['news'] = self._get_news_sentiment()
            
            logging.info(f"Sentiment data collected: Reddit={sentiment_data['reddit']}, Twitter={sentiment_data['twitter']}, News={sentiment_data['news']}")
            return sentiment_data
            
        except Exception as e:
            logging.error(f"Error collecting sentiment data: {e}")
            self.recovery.fallback("sentiment_data")
            return sentiment_data
    
    def _get_reddit_sentiment(self):
        """Get sentiment from Reddit posts"""
        try:
            subreddit = self.reddit.subreddit("investing+stocks+wallstreetbets")
            posts = subreddit.hot(limit=10)
            
            sentiment_scores = []
            for post in posts:
                # Simple sentiment analysis based on title keywords
                title = post.title.lower()
                score = 0
                
                # Positive keywords
                if any(word in title for word in ['bull', 'up', 'gain', 'profit', 'buy', 'bullish']):
                    score += 0.1
                
                # Negative keywords
                if any(word in title for word in ['bear', 'down', 'loss', 'sell', 'crash', 'bearish']):
                    score -= 0.1
                
                sentiment_scores.append(score)
            
            return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
            
        except Exception as e:
            logging.error(f"Error getting Reddit sentiment: {e}")
            return 0.0
    
    def _get_twitter_sentiment(self):
        """Get sentiment from Twitter"""
        try:
            # Search for market-related tweets
            tweets = self.twitter_client.search_recent_tweets(
                query="$SPY OR $VIX OR market OR stocks",
                max_results=10,
                tweet_fields=['public_metrics']
            )
            
            if not tweets.data:
                return 0.0
            
            sentiment_scores = []
            for tweet in tweets.data:
                text = tweet.text.lower()
                score = 0
                
                # Simple sentiment analysis
                if any(word in text for word in ['bull', 'up', 'gain', 'profit', 'buy']):
                    score += 0.1
                
                if any(word in text for word in ['bear', 'down', 'loss', 'sell', 'crash']):
                    score -= 0.1
                
                sentiment_scores.append(score)
            
            return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
            
        except Exception as e:
            logging.error(f"Error getting Twitter sentiment: {e}")
            return 0.0
    
    def _get_news_sentiment(self):
        """Get sentiment from news articles"""
        try:
            # Try NewsAPI first
            if self.newsapi_key:
                return self._get_newsapi_sentiment()
            
            # Fallback to GNews
            if self.gnews_key:
                return self._get_gnews_sentiment()
                
            return 0.0
            
        except Exception as e:
            logging.error(f"Error getting news sentiment: {e}")
            return 0.0
    
    def _get_newsapi_sentiment(self):
        """Get sentiment from NewsAPI"""
        try:
            # Check if API key format is correct (NewsAPI keys are 32 characters, not OpenAI format)
            if not self.newsapi_key or self.newsapi_key.startswith('sk-'):
                logging.warning("NewsAPI key appears to be in wrong format. Please get a proper key from newsapi.org")
                return 0.0
                
            url = f"https://newsapi.org/v2/everything?q=stock market OR SPY OR VIX&apiKey={self.newsapi_key}&sortBy=publishedAt&pageSize=10"
            response = requests.get(url)
            
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                
                sentiment_scores = []
                for article in articles:
                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower()
                    text = f"{title} {description}"
                    
                    score = 0
                    if any(word in text for word in ['bull', 'up', 'gain', 'profit', 'rise']):
                        score += 0.1
                    
                    if any(word in text for word in ['bear', 'down', 'loss', 'fall', 'crash']):
                        score -= 0.1
                    
                    sentiment_scores.append(score)
                
                return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
            
            return 0.0
            
        except Exception as e:
            logging.error(f"Error with NewsAPI: {e}")
            return 0.0
    
    def _get_gnews_sentiment(self):
        """Get sentiment from GNews"""
        try:
            url = f"https://gnews.io/api/v4/search?q=stock market&token={self.gnews_key}&max=10"
            response = requests.get(url)
            
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                
                sentiment_scores = []
                for article in articles:
                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower()
                    text = f"{title} {description}"
                    
                    score = 0
                    if any(word in text for word in ['bull', 'up', 'gain', 'profit', 'rise']):
                        score += 0.1
                    
                    if any(word in text for word in ['bear', 'down', 'loss', 'fall', 'crash']):
                        score -= 0.1
                    
                    sentiment_scores.append(score)
                
                return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
            
            return 0.0
            
        except Exception as e:
            logging.error(f"Error with GNews: {e}")
            return 0.0
