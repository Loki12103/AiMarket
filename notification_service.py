"""
Notification Service Module
----------------------------
Send alerts via Email (SMTP) and Slack
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
from notification_config import (
    EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS,
    SMTP_SERVER, SMTP_PORT,
    SLACK_WEBHOOK_URL, SLACK_BOT_NAME, SLACK_BOT_EMOJI,
    ALERT_TYPES
)


class NotificationService:
    """Handle email and Slack notifications"""
    
    def __init__(self):
        self.email_sender = EMAIL_SENDER
        self.email_password = EMAIL_PASSWORD
        self.email_receivers = EMAIL_RECEIVERS
        self.slack_webhook = SLACK_WEBHOOK_URL
    
    def send_email_alert(self, subject, message_body, alert_type="INFO"):
        """
        Send email alert via SMTP
        
        Args:
            subject (str): Email subject
            message_body (str): Email content
            alert_type (str): Type of alert (INFO, WARNING, ERROR)
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg["Subject"] = f"[{alert_type}] {subject}"
            msg["From"] = self.email_sender
            msg["To"] = ", ".join(self.email_receivers)
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_message = f"""
{message_body}

---
Alert Type: {alert_type}
Timestamp: {timestamp}
AI Market Trend & Consumer Sentiment Forecaster
"""
            
            msg.attach(MIMEText(full_message, "plain"))
            
            # Connect to Gmail SMTP server
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  # Start TLS encryption
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)
            
            print(f"✓ Email sent successfully to {len(self.email_receivers)} recipients")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email: {str(e)}")
            return False
    
    def send_slack_alert(self, message, alert_type="INFO", color=None):
        """
        Send alert to Slack channel
        
        Args:
            message (str): Alert message
            alert_type (str): Type of alert
            color (str): Message color (good, warning, danger)
        """
        try:
            # Determine color based on alert type
            if color is None:
                if "ERROR" in alert_type or "FAILURE" in alert_type:
                    color = "danger"
                elif "WARNING" in alert_type:
                    color = "warning"
                else:
                    color = "good"
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            payload = {
                "text": f"*{alert_type}*",
                "username": SLACK_BOT_NAME,
                "icon_emoji": SLACK_BOT_EMOJI,
                "attachments": [
                    {
                        "color": color,
                        "text": message,
                        "footer": "AI Market Intelligence System",
                        "ts": int(datetime.now().timestamp())
                    }
                ]
            }
            
            response = requests.post(self.slack_webhook, json=payload)
            
            if response.status_code == 200:
                print(f"✓ Slack alert sent successfully")
                return True
            else:
                print(f"✗ Slack alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Failed to send Slack alert: {str(e)}")
            return False
    
    def send_alert(self, alert_type, message, email=True, slack=True):
        """
        Send alert via both email and Slack
        
        Args:
            alert_type (str): Type of alert from ALERT_TYPES
            message (str): Alert message
            email (bool): Send via email
            slack (bool): Send via Slack
        """
        subject = ALERT_TYPES.get(alert_type, "Market Intelligence Alert")
        
        results = {}
        
        if email:
            results["email"] = self.send_email_alert(subject, message, alert_type)
        
        if slack:
            results["slack"] = self.send_slack_alert(message, alert_type)
        
        return results


# Convenience functions
def send_sentiment_spike_alert(category, old_sentiment, new_sentiment, direction):
    """Send alert for sentiment spike"""
    notifier = NotificationService()
    
    change_pct = abs(new_sentiment - old_sentiment) * 100
    
    alert_type = f"SENTIMENT_SPIKE_{direction.upper()}"
    
    message = f"""
Sentiment Spike Detected in {category}!

Direction: {direction.upper()}
Previous Sentiment Score: {old_sentiment:.2%}
Current Sentiment Score: {new_sentiment:.2%}
Change: {change_pct:.1f}%

This requires immediate attention from the market intelligence team.
"""
    
    notifier.send_alert(alert_type, message)


def send_trend_shift_alert(category, old_count, new_count, direction):
    """Send alert for trend shift"""
    notifier = NotificationService()
    
    change_pct = ((new_count - old_count) / old_count) * 100
    
    alert_type = f"TREND_SHIFT_{direction.upper()}"
    
    message = f"""
Trend Shift Detected in {category}!

Direction: {direction.upper()}
Previous Mentions: {old_count}
Current Mentions: {new_count}
Change: {change_pct:+.1f}%

Consumer interest is shifting. Review category strategy.
"""
    
    notifier.send_alert(alert_type, message)


def send_data_ingestion_alert(source, status, record_count=0, error_message=""):
    """Send alert for data ingestion"""
    notifier = NotificationService()
    
    if status == "success":
        alert_type = "DATA_INGESTION_SUCCESS"
        message = f"""
Data Successfully Fetched from {source}

Records Fetched: {record_count}
Status: SUCCESS

Weekly data ingestion completed successfully.
"""
    else:
        alert_type = "DATA_INGESTION_FAILURE"
        message = f"""
Data Fetch Failed from {source}!

Status: FAILED
Error: {error_message}

Please check data source connection and credentials.
"""
    
    notifier.send_alert(alert_type, message)


def send_pipeline_error_alert(pipeline_name, error_message):
    """Send alert for pipeline errors"""
    notifier = NotificationService()
    
    message = f"""
Pipeline Processing Error!

Pipeline: {pipeline_name}
Error: {error_message}

Immediate technical investigation required.
"""
    
    notifier.send_alert("PIPELINE_ERROR", message)


if __name__ == "__main__":
    # Test notifications
    print("Testing Notification Service...")
    
    notifier = NotificationService()
    
    # Test email
    print("\n1. Testing Email Alert...")
    notifier.send_email_alert(
        "Test Alert", 
        "This is a test email from the Market Intelligence System.",
        "INFO"
    )
    
    # Test Slack
    print("\n2. Testing Slack Alert...")
    notifier.send_slack_alert(
        "This is a test Slack message from the Market Intelligence System.",
        "INFO"
    )
    
    print("\nNotification tests completed!")
