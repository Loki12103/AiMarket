import smtplib
from email.mime.text import MIMEText
import os
import requests
import pandas as pd
from io import BytesIO
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def send_mail(subject, text, df=None):
    """
    Send email using Gmail SMTP with optional Excel attachment
    
    Args:
        subject (str): Email subject line
        text (str): Email body content
        df (pd.DataFrame, optional): DataFrame to attach as Excel file
    """
    # email details
    sender = os.getenv("sender")
    password = os.getenv("gmail_password")
    reciver = os.getenv("reciver")

    # create message 
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = reciver
    
    # body
    msg.attach(MIMEText(text, "plain"))
    
    # attach excel file 
    if isinstance(df, pd.DataFrame) and not df.empty:
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine="openpyxl")
        excel_buffer.seek(0)
        
        part = MIMEBase("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        part.set_payload(excel_buffer.read())
        encoders.encode_base64(part)
        
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename="report.xlsx"
        )
        msg.attach(part)
        print("✅ Excel Attachment Added")
    else:
        print("ℹ️  No attachment - DataFrame empty or not provided")
        
    # connection to gmail SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # start TLS encryption
        server.login(sender, password)
        server.send_message(msg)
        
    print("📧 Email sent successfully")


def send_slack_notification(text):
    """
    Send notification to Slack channel via webhook
    
    Args:
        text (str): Message to send to Slack
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    if not webhook_url:
        print("⚠️  SLACK_WEBHOOK_URL not configured in .env")
        return
    
    message = {
        "text": text,
        "username": "AI Market Trend",
        "icon_emoji": ":shield:",
    }
    
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        print("✅ Slack notification sent successfully")
    except Exception as e:
        print(f"❌ Failed to send Slack notification: {e}")
    

def testing_function():
    """
    Testing function for scheduler and notifications
    """
    print("🔔 Testing notification system...")
    
    # Test basic email
    test_message = """
Weekly Automation Test
======================

This is a test notification from the AI Market system.

✓ Email service working
✓ Scheduler operational
✓ All systems running

---
AI Market Trend & Consumer Sentiment Forecaster
"""
    
    try:
        send_mail(
            subject="🔔 Scheduler Test Notification",
            text=test_message
        )
    except Exception as e:
        print(f"❌ Email test failed: {e}")
    
    print("✅ Testing function executed")

