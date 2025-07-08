import requests
import os
import logging
from datetime import datetime

class TelegramAlerter:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    def send_alert(self, message):
        """Send alert to Telegram chat"""
        if not self.token or not self.chat_id:
            logging.error("❌ Telegram credentials not configured.")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            
            # Format message with Markdown
            formatted_message = f"""
🚨 *MARKET RISK ALERT*

{message}

_Generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC_
            """
            
            data = {
                'chat_id': self.chat_id,
                'text': formatted_message.strip(),
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                logging.info("✅ Telegram alert sent successfully")
                return True
            else:
                logging.error(f"⚠️ Telegram alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Telegram alert exception: {e}")
            return False
    
    def send_test_alert(self):
        """Send test alert to Telegram"""
        test_message = "🧪 This is a test alert from Strategic Risk Monitor"
        return self.send_alert(test_message)
