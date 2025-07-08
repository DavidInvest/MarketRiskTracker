#!/usr/bin/env python3
"""
Quick test script to debug sentiment collection
"""
import os
import sys
sys.path.append('.')

from services.data_collector import DataCollector
from services.disaster_recovery import DisasterRecoveryManager

def test_sentiment():
    recovery = DisasterRecoveryManager()
    collector = DataCollector(recovery)
    
    print("Testing sentiment collection...")
    print("="*50)
    
    # Test News sentiment
    print("1. Testing NewsAPI...")
    try:
        news_sentiment = collector._get_newsapi_sentiment()
        print(f"   News sentiment: {news_sentiment}")
    except Exception as e:
        print(f"   News error: {e}")
    
    # Test Twitter sentiment
    print("\n2. Testing Twitter API...")
    try:
        twitter_sentiment = collector._get_twitter_sentiment()
        print(f"   Twitter sentiment: {twitter_sentiment}")
    except Exception as e:
        print(f"   Twitter error: {e}")
    
    # Test Reddit sentiment
    print("\n3. Testing Reddit API...")
    try:
        reddit_sentiment = collector._get_reddit_sentiment()
        print(f"   Reddit sentiment: {reddit_sentiment}")
    except Exception as e:
        print(f"   Reddit error: {e}")
    
    print("\n" + "="*50)
    print("Test complete!")

if __name__ == "__main__":
    test_sentiment()