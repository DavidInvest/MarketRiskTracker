#!/usr/bin/env python3
"""
Test Google Trends sentiment directly
"""
from pytrends.request import TrendReq
import pandas as pd

def test_google_trends():
    try:
        print("Testing Google Trends API...")
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Test simple keywords
        keywords = ['stock market', 'recession']
        pytrends.build_payload(keywords, cat=0, timeframe='now 1-d', geo='US', gprop='')
        
        interest_data = pytrends.interest_over_time()
        print(f"Retrieved {len(interest_data)} data points")
        
        if not interest_data.empty:
            print("Sample data:")
            print(interest_data.tail(3))
            print("\nGoogle Trends test successful!")
            return True
        else:
            print("No data retrieved from Google Trends")
            return False
            
    except Exception as e:
        print(f"Google Trends error: {e}")
        return False

if __name__ == "__main__":
    test_google_trends()