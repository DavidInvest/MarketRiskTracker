# Deployment Guide - Strategic Risk Monitor

## Quick Deployment Options

### 1. Replit Deployment (Recommended)
The easiest way to deploy the Strategic Risk Monitor.

1. **Import to Replit**
   - Go to [Replit](https://replit.com)
   - Click "Create Repl" → "Import from GitHub"
   - Enter your repository URL
   - Click "Import from GitHub"

2. **Configure Secrets**
   - Click on "Secrets" tab in Replit
   - Add all required API keys from `.env.example`:
     ```
     GEMINI_API_KEY=your_actual_key
     REDDIT_CLIENT_ID=your_actual_id
     REDDIT_CLIENT_SECRET=your_actual_secret
     NEWSAPI_KEY=your_actual_key
     FRED_API_KEY=your_actual_key
     SESSION_SECRET=random_secret_string
     ```

3. **Run the Application**
   - Click the "Run" button
   - The app will start automatically on port 5000
   - Access your deployment at the provided Replit URL

### 2. Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/yourusername/strategic-risk-monitor.git
   cd strategic-risk-monitor
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```
   - Access at http://localhost:5000

### 3. Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
   ```

2. **Build and Run**
   ```bash
   docker build -t risk-monitor .
   docker run -p 5000:5000 --env-file .env risk-monitor
   ```

### 4. Heroku Deployment

1. **Create Heroku App**
   ```bash
   heroku create your-risk-monitor
   ```

2. **Configure Environment Variables**
   ```bash
   heroku config:set GEMINI_API_KEY=your_key
   heroku config:set REDDIT_CLIENT_ID=your_id
   # ... add all other keys
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

### 5. DigitalOcean App Platform

1. **Create app.yaml**
   ```yaml
   name: strategic-risk-monitor
   services:
   - name: web
     source_dir: /
     github:
       repo: yourusername/strategic-risk-monitor
       branch: main
     run_command: gunicorn --bind 0.0.0.0:$PORT main:app
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: GEMINI_API_KEY
       value: your_key
       type: SECRET
   ```

2. **Deploy via CLI or Web Interface**

## Required API Keys

### Essential APIs (Free)
1. **Google Gemini API** - AI risk analysis
   - Visit: https://ai.google.dev/
   - Free tier: 1500 requests/day

2. **Reddit API** - Sentiment analysis
   - Visit: https://www.reddit.com/prefs/apps
   - Completely free

3. **NewsAPI** - News sentiment
   - Visit: https://newsapi.org/
   - Free tier: 1000 requests/day

4. **FRED API** - Economic data
   - Visit: https://fred.stlouisfed.org/docs/api/api_key.html
   - Completely free, unlimited

### Optional APIs
- Email alerts (Gmail)
- Discord webhooks
- Telegram bot
- Twitter API (alternative to Google Trends)

## Performance Optimization

### 1. Database Optimization
```python
# For production, use PostgreSQL
DATABASE_URL=postgresql://user:pass@host:port/db
```

### 2. Caching Configuration
```python
# Redis for production caching
REDIS_URL=redis://localhost:6379/0
```

### 3. Gunicorn Production Settings
```bash
gunicorn --workers 4 --timeout 300 --bind 0.0.0.0:5000 main:app
```

## Monitoring and Maintenance

### 1. Health Checks
- Dashboard: `/admin` - System status
- API: `/health` - Health check endpoint
- Logs: Available in admin panel

### 2. Automated Alerts
Configure alert thresholds in admin panel:
- Low risk: < 25
- Moderate risk: 25-50
- High risk: 50-75
- Critical risk: > 75

### 3. Backup Strategy
- Database: Automatic SQLite backups
- Models: ML models saved to filesystem
- Logs: Configurable retention period

## Troubleshooting

### Common Issues

1. **API Rate Limits**
   - Solution: Implement caching, reduce polling frequency
   - Check: Admin panel for API status

2. **Database Connection**
   - Solution: Verify DATABASE_URL format
   - Fallback: System uses SQLite by default

3. **Missing API Keys**
   - Solution: Check all required keys in .env
   - Fallback: System provides mock data when APIs unavailable

4. **Memory Issues**
   - Solution: Increase instance size
   - Check: ML model loading settings

### Support
- Create GitHub issues for bugs
- Use discussions for deployment questions
- Check logs in admin panel for errors

## Security Considerations

1. **API Key Protection**
   - Never commit keys to repository
   - Use environment variables only
   - Rotate keys regularly

2. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

3. **Network Security**
   - Use HTTPS in production
   - Configure proper CORS settings
   - Implement rate limiting

## Scaling Options

### Horizontal Scaling
- Multiple app instances
- Load balancer
- Shared database

### Vertical Scaling
- Increase memory/CPU
- Optimize database queries
- Cache frequently accessed data

### Cost Optimization
- Use free tier APIs effectively
- Implement intelligent caching
- Monitor usage patterns
- Scale down during off-hours