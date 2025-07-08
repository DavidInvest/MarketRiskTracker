import os
import requests
import logging
from datetime import datetime
import yfinance as yf
import praw
import tweepy

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
        self.twitter_bearer = os.getenv('TWITTER_BEARER')
        
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
            if self.twitter_bearer:
                self.twitter_client = tweepy.Client(bearer_token=self.twitter_bearer)
                
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
