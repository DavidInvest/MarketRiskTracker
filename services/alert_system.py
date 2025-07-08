import logging
from app import db
from models import AlertConfig
from services.email_alerter import EmailAlerter
from services.discord_alerter import DiscordAlerter
from services.telegram_alerter import TelegramAlerter

class AlertSystem:
    def __init__(self):
        self.email_alerter = EmailAlerter()
        self.discord_alerter = DiscordAlerter()
        self.telegram_alerter = TelegramAlerter()
    
    def send_alert(self, risk_score):
        """Send alerts through configured channels"""
        try:
            # Get alert configurations
            alert_configs = AlertConfig.query.filter_by(enabled=True).all()
            
            # Prepare alert message
            message = self._format_alert_message(risk_score)
            subject = f"🚨 Market Risk Alert: {risk_score['level']}"
            
            for config in alert_configs:
                if risk_score['value'] >= config.threshold:
                    self._send_channel_alert(config.channel, subject, message, risk_score)
            
            logging.info(f"Alerts sent for risk level: {risk_score['level']} ({risk_score['value']})")
            
        except Exception as e:
            logging.error(f"Error sending alerts: {e}")
    
    def _format_alert_message(self, risk_score):
        """Format alert message with LLM insights"""
        components = risk_score.get('components', {})
        llm_insights = risk_score.get('llm_insights', {})
        
        # Base alert message
        message = f"""
🚨 MARKET RISK ALERT 🚨

Current Risk Score: {risk_score['value']}
Risk Level: {risk_score['level']}

Risk Components:
• VIX Impact: {components.get('vix', 'N/A')}
• Sentiment Impact: {components.get('sentiment', 'N/A')}
• Dollar Strength: {components.get('dxy', 'N/A')}
• Market Momentum: {components.get('momentum', 'N/A')}
• Credit Risk: {components.get('credit', 'N/A')}
• Yield Curve: {components.get('yield_curve', 'N/A')}
• Options Flow: {components.get('options', 'N/A')}
• Economic Indicators: {components.get('economic', 'N/A')}"""

        # Add LLM insights if available
        if llm_insights:
            message += f"""

🤖 AI RISK INSIGHTS:
Alert: {llm_insights.get('alert_title', 'Risk Alert')}
Context: {llm_insights.get('alert_message', 'Risk threshold exceeded')}
Recommended Action: {llm_insights.get('immediate_action', 'Monitor positions closely')}
Urgency Level: {llm_insights.get('urgency_level', 3)}/5"""

        message += f"""

Timestamp: {risk_score.get('timestamp', 'N/A')}

⚠️ Please review your positions and risk management strategy.
        """
        
        return message.strip()
    
    def _send_channel_alert(self, channel, subject, message, risk_score):
        """Send alert to specific channel"""
        try:
            if channel == 'email':
                self.email_alerter.send_email(subject, message)
            elif channel == 'discord':
                self.discord_alerter.send_alert(f"**{subject}**\n```\n{message}\n```")
            elif channel == 'telegram':
                self.telegram_alerter.send_alert(f"{subject}\n\n{message}")
            else:
                logging.warning(f"Unknown alert channel: {channel}")
                
        except Exception as e:
            logging.error(f"Error sending {channel} alert: {e}")
    
    def test_alert_channel(self, channel):
        """Test alert channel functionality"""
        try:
            test_message = f"🧪 Test alert from Strategic Risk Monitor - {channel.upper()}"
            
            if channel == 'email':
                self.email_alerter.send_email("Test Alert", test_message)
            elif channel == 'discord':
                self.discord_alerter.send_alert(test_message)
            elif channel == 'telegram':
                self.telegram_alerter.send_alert(test_message)
            
            return True
            
        except Exception as e:
            logging.error(f"Error testing {channel} alert: {e}")
            return False
