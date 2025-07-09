# Strategic Risk Monitor

A cutting-edge Strategic Risk Monitor powered by machine learning, multi-source data integration, and generative AI, delivering comprehensive risk assessment through intelligent data processing.

## Features

- **Real-time Market Monitoring** - Live data from SPY, VIX, DXY
- **AI-Powered Risk Analysis** - OpenAI GPT-4o-mini for intelligent insights
- **Machine Learning Predictions** - Advanced ML models for crash probability
- **Multi-Channel Alerts** - Email, Discord, Telegram notifications
- **Professional Dashboard** - Clean, institutional-grade interface
- **Sentiment Analysis** - Reddit, Google Trends, and news sentiment
- **Historical Backtesting** - Strategy performance analysis
- **Comprehensive Data Sources** - 15+ free economic indicators

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-SocketIO
- **Frontend**: Bootstrap 5, Chart.js, Vanilla JavaScript
- **Machine Learning**: scikit-learn, pandas, numpy
- **AI Integration**: OpenAI GPT-4o-mini (cost-optimized)
- **Data Sources**: yfinance, Reddit API, NewsAPI, Google Trends
- **Database**: SQLite (development), PostgreSQL (production)

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables for API keys
4. Run: `python main.py`

## Current Status

✅ **Fully Functional Dashboard** - Real-time data display working
✅ **All Navigation Sections** - Dashboard, Backtesting, ML Management, Admin
✅ **API Integration** - Live market data and sentiment analysis
✅ **AI Risk Analysis** - OpenAI-powered market insights
✅ **Machine Learning** - Crash prediction models operational
✅ **Multi-Channel Alerts** - Email, Discord, Telegram configured

## API Requirements

- OpenAI API Key (for AI analysis)
- Reddit API credentials
- NewsAPI key
- Email SMTP settings
- Discord/Telegram webhooks (optional)

## Architecture

The system uses a modular architecture with separate services for data collection, risk calculation, machine learning, and alerting. Real-time updates are handled via WebSocket connections, and the dashboard provides institutional-grade monitoring capabilities.

For detailed technical documentation, see `replit.md`.