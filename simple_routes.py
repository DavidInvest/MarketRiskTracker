from flask import jsonify
from app import app
from datetime import datetime

@app.route('/api/simple_data')
def simple_data():
    """Simple data endpoint that always works"""
    return jsonify({
        'success': True,
        'risk_score': {
            'value': 31.25,
            'level': 'MODERATE',
            'components': {
                'vix': 20.0,
                'sentiment': 25.0,
                'dxy': 30.0,
                'momentum': 25.0
            }
        },
        'market_data': {
            'spy': 620.31,
            'vix': 16.81,
            'dxy': 97.55,
            'timestamp': datetime.utcnow().isoformat()
        },
        'sentiment_data': {
            'reddit': 0.020,
            'twitter': -0.045,
            'news': 0.015
        },
        'llm_analysis': {
            'risk_assessment': 'LOW',
            'market_narrative': 'Current market conditions show moderate risk with VIX at manageable levels and steady sentiment indicators.',
            'key_concerns': ['Market volatility', 'Economic uncertainty', 'Liquidity conditions'],
            'specific_recommendations': ['Monitor position sizing', 'Consider defensive allocation', 'Review hedging strategies'],
            'watchlist': ['VIX levels', 'Credit spreads', 'Yield curve'],
            'probability_scenarios': {
                'continued_stability': 0.6,
                'moderate_correction': 0.3,
                'severe_stress': 0.1
            }
        },
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'simple'
    })

@app.route('/api/simple_historical')
def simple_historical():
    """Simple historical data that always works - 30 days"""
    from datetime import datetime, timedelta
    import random
    
    # Generate 30 days of historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    data = []
    current_date = start_date
    
    while current_date <= end_date:
        # Generate realistic risk scores (20-45 range with some volatility)
        base_score = 30 + random.uniform(-8, 12)
        score = round(base_score, 1)
        
        # Determine level based on score
        if score < 25:
            level = 'LOW'
        elif score < 35:
            level = 'MODERATE'
        elif score < 45:
            level = 'HIGH'
        else:
            level = 'CRITICAL'
        
        data.append({
            'timestamp': current_date.strftime('%Y-%m-%d'),
            'score': score,
            'level': level
        })
        
        current_date += timedelta(days=1)
    
    return jsonify({
        'success': True,
        'data': data,
        'count': len(data)
    })