# Strategic Risk Monitor

## Overview

The Strategic Risk Monitor is a real-time Flask-based web application that monitors U.S. market risk using machine learning and sentiment analysis. The system provides live risk scoring, multi-channel alerting, backtesting capabilities, and ML model management through a comprehensive web dashboard.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**January 8, 2025**
- ✅ Successfully deployed Strategic Risk Monitor with all core features
- ✅ Configured all API keys: Reddit, NewsAPI, Email, Discord, Telegram, Twitter
- ✅ Real-time market data collection working (SPY, VIX, DXY)
- ✅ Sentiment analysis operational (Reddit: 0.02, News: 0.01)
- ✅ Risk scoring system active (Current: 32.0 - Moderate Risk)
- ✅ Dashboard interface accessible and functional
- ✅ All notification channels configured and ready
- ✅ ML prediction system available for training
- ✅ Backtesting capabilities implemented
- ✅ Enhanced with comprehensive free data sources (FRED, Treasury, Options)
- ✅ Implemented 8-factor risk model with credit spreads, yield curve, options flow
- ✅ Added 15+ additional market indicators (REITs, bonds, commodities)
- ✅ Integrated Federal Reserve Economic Data (FRED) API for unlimited access
- ✅ Added options market analysis (put/call ratios, volatility skew)
- ✅ Implemented Treasury yield curve monitoring and inversion detection
- ✅ **Added LLM-powered risk analysis using OpenAI GPT-4o-mini for intelligent risk interpretation**
- ✅ **Implemented comprehensive risk insights with actionable recommendations**
- ✅ **Enhanced dashboard with AI Risk Analysis section showing market narrative, key concerns, and probability scenarios**
- ✅ **Upgraded alert system with LLM insights for contextualized risk notifications**
- ✅ **MAJOR: Implemented advanced machine learning-based risk scoring system with sophisticated feature engineering**
- ✅ **Created MLRiskScorer with 25+ technical indicators, sentiment analysis, and macro features**
- ✅ **Added multi-horizon crash prediction models (1d, 3d, 7d, 14d, 30d)**
- ✅ **Integrated Random Forest, Gradient Boosting, and Neural Network algorithms with automatic model selection**
- ✅ **Enhanced monitoring system to combine basic risk scoring (60%) with ML predictions (40%)**
- ✅ **Added advanced ML training API endpoint for continuous model improvement**
- ✅ **Integrated FRED API for real-time economic indicators in ML feature engineering**
- ✅ **Fixed ML prediction display system to show actual multi-horizon crash probabilities**
- ✅ **Enhanced dashboard with comprehensive ML metrics (1d, 7d, 30d predictions + ML risk score)**
- ✅ **MAJOR BREAKTHROUGH: Fixed frontend-backend data disconnection issue**
- ✅ **Dashboard now displays real-time market data: SPY=620.31, VIX=16.81, DXY=97.51**
- ✅ **Implemented intelligent data loading with database caching and fresh data fallback**
- ✅ **Real sentiment analysis working: Reddit=0.010, News=-0.040, Twitter=0.000**
- ✅ **All placeholder values replaced with authentic market data from live APIs**
- ✅ **System now provides true institutional-grade risk monitoring with real data**

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM for data persistence
- **Real-time Communication**: Flask-SocketIO for WebSocket connections
- **Database**: SQLite (development) with PostgreSQL support configured
- **Task Scheduling**: Schedule library for periodic monitoring cycles
- **ML Framework**: scikit-learn for risk prediction models

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **Real-time Updates**: Socket.IO client for live data streaming
- **Data Visualization**: Chart.js for interactive charts and graphs
- **Styling**: Custom CSS with Bootstrap dark theme integration

### Data Layer
- **ORM**: SQLAlchemy with declarative base
- **Models**: RiskScore, AlertConfig, SystemLog, BacktestResult, MLModel
- **Storage**: JSON columns for flexible data storage (market data, sentiment data, model parameters)

## Key Components

### Core Services
1. **DataCollector**: Aggregates market data from yfinance, Reddit, Twitter, and news APIs
2. **RiskCalculator**: Computes weighted risk scores from VIX, sentiment, DXY, and momentum indicators
3. **AlertSystem**: Multi-channel notifications via email, Discord, and Telegram
4. **MLIntegration**: Handles model loading, prediction, and crash probability assessment
5. **MLTrainer**: Manages model training with both synthetic and real historical data
6. **Backtester**: Performs historical strategy testing with portfolio simulation
7. **DisasterRecoveryManager**: Provides fallback mechanisms for service failures

### Web Interface
- **Dashboard**: Real-time risk monitoring with live charts and current market data
- **Admin Panel**: System configuration, alert management, and system logs
- **Backtesting**: Historical strategy testing with configurable parameters
- **ML Management**: Model training, performance monitoring, and deployment

### Monitoring System
- **Threaded Execution**: Separate monitoring thread for continuous data collection
- **Scheduled Tasks**: Regular risk calculation and alert processing
- **Error Handling**: Comprehensive logging and fallback mechanisms

## Data Flow

1. **Data Collection**: Services gather market data (VIX, SPY, DXY) and sentiment data (Reddit, Twitter, news)
2. **Risk Calculation**: Weighted algorithm combines indicators into unified risk score (0-100)
3. **Database Storage**: Risk scores, market data, and metadata persisted to SQLite/PostgreSQL
4. **Real-time Updates**: WebSocket broadcasts push updates to connected clients
5. **Alert Processing**: Threshold-based alerts sent through configured channels
6. **ML Integration**: Models provide crash probability predictions based on current conditions

## External Dependencies

### Required APIs
- **yfinance**: Market data collection (free, no API key required)
- **Reddit API**: Sentiment analysis from subreddits
- **Twitter API**: Social media sentiment tracking
- **News APIs**: NewsAPI and GNews for media sentiment

### Alert Channels
- **Email**: SMTP configuration for email alerts
- **Discord**: Webhook URL for Discord notifications
- **Telegram**: Bot token and chat ID for Telegram alerts

### Python Libraries
- Flask ecosystem (Flask, SQLAlchemy, SocketIO)
- Data science stack (numpy, pandas, scikit-learn)
- External APIs (yfinance, praw, tweepy, requests)
- ML persistence (joblib for model serialization)

## Deployment Strategy

### Development
- **Local Development**: Flask development server with debug mode
- **Database**: SQLite for quick setup and testing
- **Environment Variables**: Configurable through .env file or Replit Secrets

### Production Considerations
- **Database Migration**: Automatic table creation on startup
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxy
- **Connection Pooling**: SQLAlchemy engine options for production database connections
- **CORS**: Configured for cross-origin requests in Socket.IO

### Monitoring & Reliability
- **Logging**: Comprehensive logging system with database persistence
- **Fallback Mechanisms**: Disaster recovery manager handles service failures
- **Health Checks**: System status monitoring through admin interface
- **Auto-recovery**: Automatic restart capabilities for failed services

The application is designed to be deployed on Replit with minimal configuration, using environment variables for API keys and external service credentials. The modular architecture allows for easy extension and maintenance of individual components.