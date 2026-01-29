"""
Email and Slack Notification Configuration
------------------------------------------
Store your credentials and webhook URLs here
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration (SMTP)
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password")
EMAIL_RECEIVERS = [
    os.getenv("EMAIL_RECEIVER", "recipient@gmail.com"),
    # Add more recipients here
]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Slack Configuration
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
SLACK_CHANNEL = "#market-alerts"
SLACK_BOT_NAME = "MarketIntelligenceBot"
SLACK_BOT_EMOJI = ":chart_with_upwards_trend:"

# Notification Thresholds
SENTIMENT_SPIKE_THRESHOLD = 0.15  # 15% change in sentiment
TREND_SHIFT_THRESHOLD = 0.20  # 20% change in category mentions
MINIMUM_DATA_POINTS = 10  # Minimum records to trigger analysis

# Alert Types
ALERT_TYPES = {
    "SENTIMENT_SPIKE_POSITIVE": "Positive Sentiment Spike Detected",
    "SENTIMENT_SPIKE_NEGATIVE": "Negative Sentiment Spike Detected",
    "TREND_SHIFT_UP": "Trending Up - Category Demand Increase",
    "TREND_SHIFT_DOWN": "Trending Down - Category Demand Decrease",
    "DATA_INGESTION_SUCCESS": "Data Successfully Fetched",
    "DATA_INGESTION_FAILURE": "Data Fetch Failed",
    "PIPELINE_ERROR": "Pipeline Processing Error",
    "INCOMPLETE_DATA": "Incomplete Data Warning"
}
