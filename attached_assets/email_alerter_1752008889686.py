import smtplib
from email.message import EmailMessage
import os

class EmailAlerter:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('EMAIL_PASSWORD')
        self.recipient_emails = os.getenv('RECIPIENT_EMAILS', '').split(',')

    def send_email(self, subject, body):
        if not self.sender_email or not self.sender_password:
            print("❌ Email credentials not configured.")
            return

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_emails
        msg.set_content(body)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.sender_email, self.sender_password)
                smtp.send_message(msg)
            print("✅ Email alert sent.")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")