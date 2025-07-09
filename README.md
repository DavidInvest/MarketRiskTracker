# Strategic Risk Monitor

A cutting-edge real-time market risk monitoring system powered by machine learning, multi-source data integration, and generative AI. Provides comprehensive risk assessment through intelligent data processing and institutional-grade risk analysis.

## 🚀 Features

### Core Capabilities
- **Real-time Market Monitoring** - Live data from SPY, VIX, DXY, and 15+ market indicators
- **AI-Powered Risk Analysis** - Gemini 2.5 Flash integration for intelligent market insights
- **Machine Learning Predictions** - Multi-horizon crash probability models (1d, 7d, 30d)
- **Multi-Channel Alerts** - Email, Discord, Telegram notifications with contextual insights
- **Advanced Backtesting** - Historical strategy testing with comprehensive performance metrics
- **Professional Dashboard** - Real-time charts, risk scoring, and actionable recommendations

### Data Sources
- **Market Data**: yfinance (SPY, VIX, DXY, sector ETFs, bonds, commodities)
- **Economic Data**: Federal Reserve Economic Data (FRED API) - unlimited access
- **Sentiment Analysis**: Reddit, Google Trends, NewsAPI
- **Options Data**: Put/call ratios, volatility skew, options flow analysis
- **Credit Markets**: Treasury yield curve, corporate bond spreads

### Technical Architecture
- **Backend**: Flask with SQLAlchemy ORM, real-time WebSocket updates
- **Frontend**: Bootstrap 5 with Chart.js visualizations
- **ML Framework**: scikit-learn with advanced feature engineering
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Optimized for Replit with auto-scaling capabilities

## 📊 Risk Scoring System

The system uses an 8-factor risk model combining:
- **VIX (20%)** - Market volatility indicator
- **Sentiment (25%)** - Social media and news sentiment analysis
- **DXY (30%)** - US Dollar strength impact
- **Momentum (25%)** - Market trend analysis
- **Credit Spreads** - Corporate bond risk premiums
- **Yield Curve** - Treasury curve inversion detection
- **Options Flow** - Professional options market activity
- **Economic Indicators** - FRED macroeconomic data

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Required API keys (see Configuration section)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/strategic-risk-monitor.git
cd strategic-risk-monitor

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
python main.py
```

### Replit Deployment
1. Import this repository to Replit
2. Configure secrets in Replit Secrets manager
3. Run the application - it will auto-configure

## ⚙️ Configuration

### Required API Keys
- `GEMINI_API_KEY` - Google Gemini API for AI analysis
- `REDDIT_CLIENT_ID` & `REDDIT_CLIENT_SECRET` - Reddit sentiment analysis
- `NEWSAPI_KEY` - News sentiment analysis
- `FRED_API_KEY` - Federal Reserve economic data

### Optional Integrations
- `EMAIL_USERNAME` & `EMAIL_PASSWORD` - Email alerts
- `DISCORD_WEBHOOK_URL` - Discord notifications
- `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID` - Telegram alerts

### Database Configuration
- Development: SQLite (automatic)
- Production: Set `DATABASE_URL` for PostgreSQL

## 🔧 Usage

### Dashboard
- Real-time risk score (0-100 scale)
- Historical risk trends (30-day view)
- Market data visualization
- AI-generated risk insights
- ML prediction probabilities

### Backtesting
- Strategy performance testing
- Risk-adjusted returns analysis
- Maximum drawdown calculations
- Sharpe ratio optimization

### ML Management
- Model training interface
- Performance monitoring
- Feature importance analysis
- Multi-algorithm comparison

### Admin Panel
- System configuration
- Alert channel management
- System logs and monitoring
- Health status dashboard

## 📈 API Endpoints

### Data APIs
- `GET /api/quick_data` - Latest risk data and market conditions
- `GET /api/historical` - Historical risk scores and trends
- `GET /api/ml_predict` - ML-based risk predictions

### Management APIs
- `POST /api/train_model` - Train ML models
- `POST /api/run_backtest` - Execute backtesting
- `POST /api/update_alerts` - Configure alert settings

## 🏗️ Architecture

### Service Layer
- **DataCollector** - Multi-source market data aggregation
- **RiskCalculator** - Weighted risk score computation
- **MLRiskScorer** - Advanced ML-based predictions
- **AlertSystem** - Multi-channel notification management
- **LLMRiskAnalyzer** - AI-powered risk interpretation

### Data Flow
1. Real-time data collection from multiple sources
2. Risk calculation using weighted algorithms
3. ML model predictions and probability analysis
4. AI-generated insights and recommendations
5. Database persistence and caching
6. WebSocket broadcasting to connected clients
7. Threshold-based alert processing

## 🤖 Machine Learning

### Feature Engineering
- 25+ technical indicators (RSI, MACD, Bollinger Bands)
- Sentiment analysis scores from multiple sources
- Macroeconomic indicators from FRED API
- Options market metrics (put/call ratios, skew)
- Credit market conditions
- Currency and commodity correlations

### Model Types
- **Random Forest** - Feature importance and robustness
- **Gradient Boosting** - Non-linear pattern detection
- **Neural Networks** - Complex relationship modeling
- **Ensemble Methods** - Combined model predictions

### Prediction Horizons
- 1-day crash probability
- 3-day risk evolution
- 7-day market outlook
- 14-day trend analysis
- 30-day strategic positioning

## 📊 Performance

### Cost Optimization
- 75% cost reduction using Gemini vs OpenAI
- Free data sources (FRED, yfinance) for unlimited access
- Efficient caching and data persistence
- Optimized API call patterns

### Reliability
- Disaster recovery mechanisms
- Fallback data sources
- Automatic service restart
- Comprehensive error handling
- Health monitoring and alerts

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

- Create an issue for bug reports
- Use discussions for feature requests
- Check the wiki for detailed documentation

## 🏆 Acknowledgments

- Federal Reserve Economic Data (FRED) for comprehensive economic indicators
- Reddit API for sentiment analysis capabilities
- Google Trends for market sentiment insights
- yfinance for reliable market data access
- Gemini AI for intelligent risk analysis

---

**Built for institutional-grade risk monitoring with cost-effective AI integration.**