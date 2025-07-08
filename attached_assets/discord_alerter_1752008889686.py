import requests
import os

class DiscordAlerter:
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    def send_alert(self, message):
        if not self.webhook_url:
            print("❌ Discord webhook URL not configured.")
            return
        payload = {'content': message}
        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 204:
                print("✅ Discord alert sent.")
            else:
                print(f"⚠️ Discord alert failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Discord alert exception: {e}")