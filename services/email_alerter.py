import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

class EmailAlerter:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('EMAIL_PASSWORD')
        self.recipient_emails = [email.strip() for email in os.getenv('RECIPIENT_EMAILS', '').split(',') if email.strip()]
    
    def send_email(self, subject, body):
        """Send email alert"""
        if not self.sender_email or not self.sender_password:
            logging.error("❌ Email credentials not configured.")
            return False
        
        if not self.recipient_emails:
            logging.error("❌ No recipient emails configured.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_emails)
            
            # Create HTML version
            html_body = self._create_html_email(subject, body)
            
            # Attach both plain text and HTML versions
            text_part = MIMEText(body, 'plain')
            html_part = MIMEText(html_body, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logging.info("✅ Email alert sent successfully")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to send email: {e}")
            return False
    
    def _create_html_email(self, subject, body):
        """Create HTML formatted email"""
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #dc3545;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 0 0 8px 8px;
                    border: 1px solid #dee2e6;
                }}
                .alert-level {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #dc3545;
                    text-align: center;
                    margin: 20px 0;
                }}
                .metrics {{
                    background-color: white;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                    border-left: 4px solid #dc3545;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚨 Strategic Risk Monitor Alert</h1>
            </div>
            <div class="content">
                <pre>{body}</pre>
                <div class="footer">
                    <p>This is an automated alert from Strategic Risk Monitor</p>
                    <p>Please review your positions and risk management strategy</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_body
