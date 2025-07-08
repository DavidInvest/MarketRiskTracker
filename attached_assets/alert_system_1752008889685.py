from modules.email_alerter import EmailAlerter

class AlertSystem:
    def __init__(self):
        self.email = EmailAlerter()

    def send_alert(self, risk_score):
        subject = f"🚨 Market Risk Alert: {risk_score['level']}"
        body = f"Risk score is {risk_score['value']}.
Level: {risk_score['level']}
Please review your positions."
        self.email.send_email(subject, body)