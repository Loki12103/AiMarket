"""
Automated Scheduler for Weekly Data Collection & Monitoring
------------------------------------------------------------
Runs data collection, sentiment analysis, and sends notifications
"""

import schedule
import time
from datetime import datetime
import pandas as pd
from notification import send_mail, send_slack_notification
from weekly_automation import run_weekly_automation
import news
import subprocess


def collect_weekly_data():
    """
    Run complete weekly automation pipeline
    Calls weekly_automation.py for comprehensive processing
    """
    print(f"\n{'='*60}")
    print(f"Weekly Automation Triggered by Scheduler")
    print(f"Timestamp: {datetime.now()}")
    print(f"{'='*60}\n")
    
    try:
        # Run complete automation pipeline
        results = run_weekly_automation()
        
        print(f"\n{'='*60}")
        print("Scheduler: Weekly automation completed successfully")
        print(f"{'='*60}\n")
        
        return results
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"Scheduler: Weekly automation failed - {str(e)}")
        print(f"{'='*60}\n")
        
        error_msg = f"""
CRITICAL ERROR in Scheduled Weekly Automation!

Error: {str(e)}

The scheduled weekly data collection and monitoring pipeline has failed.
Immediate technical investigation required.

Timestamp: {datetime.now()}"""
        
        # Send critical error notifications
        send_mail(
            text=error_msg,
            subject="✗ CRITICAL: Scheduled Automation Failed"
        )
        
        send_slack_notification(
            text=f"🚨 CRITICAL ERROR in Weekly Automation\n\nError: {str(e)}\nTimestamp: {datetime.now()}"
        )
        
        return None

---
AI Market Trend & Consumer Sentiment Forecaster
Automated Scheduler
""",
            subject="✗ CRITICAL: Scheduled Automation Failed"
        )
        
        return None


def collect_news_data():
    """Run news data collection"""
    print(f"\n[{datetime.now()}] Starting news data collection...")
    try:
        news.get_news_data()
        print(f"[{datetime.now()}] News collection completed ✓")
    except Exception as e:
        error_msg = f"News data collection failed: {str(e)}"
        print(f"❌ {error_msg}")
        send_slack_notification(
            text=f"🚨 NEWS COLLECTION ERROR\n\n{error_msg}\nTimestamp: {datetime.now()}"
        )


def collect_reddit_data():
    """Run Reddit data collection"""
    print(f"\n[{datetime.now()}] Starting Reddit data collection...")
    try:
        subprocess.run(["python", "reddit_data_collector.py"], check=True)
        print(f"[{datetime.now()}] Reddit collection completed ✓")
    except Exception as e:
        error_msg = f"Reddit data collection failed: {str(e)}"
        print(f"❌ {error_msg}")
        send_slack_notification(
            text=f"🚨 REDDIT COLLECTION ERROR\n\n{error_msg}\nTimestamp: {datetime.now()}"
        )


def test_scheduler():
    """Test function for scheduler verification"""
    print(f"[{datetime.now()}] Scheduler is running correctly ✓")
    
    send_mail(
        text=f"Scheduler test completed successfully at {datetime.now()}",
        subject="Scheduler Test - Running"
    )


def run_scheduler():
    """
    Main scheduler function
    Runs in background thread
    """
    print("\n" + "="*60)
    print("AI Market Scheduler Started")
    print("="*60)
    print(f"Start Time: {datetime.now()}")
    print("\nScheduled Jobs:")
    print("- Weekly Data Collection: Every Monday at 12:00 AM")
    print("- News Collection: Every Sunday at 02:00 AM")
    print("- Reddit Collection: Every Sunday at 03:00 AM")
    print("- Status: Running in background\n")
    print("="*60 + "\n")
    
    # Schedule weekly data collection every Monday at midnight
    schedule.every().monday.at("00:00").do(collect_weekly_data)
    
    # Schedule news and reddit data collection (every 10th Sunday)
    schedule.every(10).sunday.at("02:00").do(collect_news_data)
    schedule.every(10).sunday.at("03:00").do(collect_reddit_data)
    
    # For testing: uncomment one of these and comment the line above
    # schedule.every(30).seconds.do(test_scheduler)  # Test every 30 seconds
    # schedule.every(5).minutes.do(collect_weekly_data)  # Test every 5 minutes
    # schedule.every().day.at("09:00").do(collect_weekly_data)  # Daily at 9 AM
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every 60 seconds


if __name__ == "__main__":
    # Run scheduler directly (for testing)
    print("Starting scheduler in foreground mode...")
    print("Press Ctrl+C to stop\n")
    
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")
