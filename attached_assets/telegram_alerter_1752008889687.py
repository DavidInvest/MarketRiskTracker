import requests
import os

class TelegramAlerter:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def send_alert(self, message):
        if not self.token or not self.chat_id:
            print("❌ Telegram credentials not configured.")
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {'chat_id': self.chat_id, 'text': message}
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("✅ Telegram alert sent.")
            else:
                print(f"⚠️ Telegram alert failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Telegram alert exception: {e}")