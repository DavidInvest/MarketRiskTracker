import requests
import os
import logging
import json
from datetime import datetime

class DiscordAlerter:
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    def send_alert(self, message):
        """Send alert to Discord channel"""
        if not self.webhook_url:
            logging.error("❌ Discord webhook URL not configured.")
            return False
        
        try:
            # Create rich embed
            embed = {
                "title": "🚨 Market Risk Alert",
                "description": message,
                "color": 0xdc3545,  # Red color
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": "Strategic Risk Monitor",
                    "icon_url": "https://cdn.jsdelivr.net/npm/feather-icons@4.28.0/dist/feather-sprite.svg"
                },
                "fields": [
                    {
                        "name": "⚠️ Action Required",
                        "value": "Please review your positions and risk management strategy",
                        "inline": False
                    }
                ]
            }
            
            payload = {
                "content": "📊 **Market Risk Alert**",
                "embeds": [embed]
            }
            
            response = requests.post(self.webhook_url, json=payload)
            
            if response.status_code == 204:
                logging.info("✅ Discord alert sent successfully")
                return True
            else:
                logging.error(f"⚠️ Discord alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Discord alert exception: {e}")
            return False
    
    def send_test_alert(self):
        """Send test alert to Discord"""
        test_message = "🧪 This is a test alert from Strategic Risk Monitor"
        return self.send_alert(test_message)
