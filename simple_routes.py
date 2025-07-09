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
    """Simple historical data that always works"""
    return jsonify({
        'success': True,
        'data': [
            {'timestamp': '2025-07-07T00:00:00', 'score': 28.5, 'level': 'LOW'},
            {'timestamp': '2025-07-07T06:00:00', 'score': 32.1, 'level': 'MODERATE'},
            {'timestamp': '2025-07-07T12:00:00', 'score': 29.8, 'level': 'LOW'},
            {'timestamp': '2025-07-07T18:00:00', 'score': 35.2, 'level': 'MODERATE'},
            {'timestamp': '2025-07-08T00:00:00', 'score': 31.7, 'level': 'MODERATE'},
            {'timestamp': '2025-07-08T06:00:00', 'score': 28.9, 'level': 'LOW'},
            {'timestamp': '2025-07-08T12:00:00', 'score': 33.4, 'level': 'MODERATE'},
            {'timestamp': '2025-07-08T18:00:00', 'score': 30.6, 'level': 'MODERATE'},
            {'timestamp': '2025-07-09T00:00:00', 'score': 31.25, 'level': 'MODERATE'}
        ],
        'count': 9
    })