"""
Test Notification System
-------------------------
Quick test to verify email and Slack alerts are working
"""

from notification_service import NotificationService

def test_basic_notifications():
    """Test basic email and Slack notifications"""
    print("="*60)
    print("Testing Notification System")
    print("="*60)
    
    notifier = NotificationService()
    
    # Test 1: Email
    print("\n1. Testing Email Alert...")
    email_result = notifier.send_email_alert(
        subject="Test Email - Market Intelligence System",
        message_body="This is a test email to verify SMTP configuration.",
        alert_type="INFO"
    )
    
    if email_result:
        print("   Email test: PASSED ✓")
    else:
        print("   Email test: FAILED ✗")
    
    # Test 2: Slack
    print("\n2. Testing Slack Alert...")
    slack_result = notifier.send_slack_alert(
        message="This is a test Slack message to verify webhook configuration.",
        alert_type="INFO"
    )
    
    if slack_result:
        print("   Slack test: PASSED ✓")
    else:
        print("   Slack test: FAILED ✗")
    
    # Test 3: Combined Alert
    print("\n3. Testing Combined Alert...")
    combined_result = notifier.send_alert(
        alert_type="DATA_INGESTION_SUCCESS",
        message="Successfully fetched 1,500 product reviews from Amazon.",
        email=True,
        slack=True
    )
    
    print(f"   Combined test: {combined_result}")
    
    print("\n" + "="*60)
    print("Notification Test Complete")
    print("="*60)


def test_alert_scenarios():
    """Test different alert scenarios"""
    from notification_service import (
        send_sentiment_spike_alert,
        send_trend_shift_alert,
        send_data_ingestion_alert,
        send_pipeline_error_alert
    )
    
    print("\n" + "="*60)
    print("Testing Alert Scenarios")
    print("="*60)
    
    # Scenario 1: Sentiment Spike
    print("\n1. Sentiment Spike Alert...")
    send_sentiment_spike_alert(
        category="Mobile Accessories",
        old_sentiment=0.65,
        new_sentiment=0.85,
        direction="positive"
    )
    
    # Scenario 2: Trend Shift
    print("\n2. Trend Shift Alert...")
    send_trend_shift_alert(
        category="Home Appliances",
        old_count=450,
        new_count=650,
        direction="up"
    )
    
    # Scenario 3: Data Ingestion Success
    print("\n3. Data Ingestion Success Alert...")
    send_data_ingestion_alert(
        source="Reddit API",
        status="success",
        record_count=850
    )
    
    # Scenario 4: Data Ingestion Failure
    print("\n4. Data Ingestion Failure Alert...")
    send_data_ingestion_alert(
        source="News API",
        status="failed",
        error_message="API key expired or rate limit exceeded"
    )
    
    # Scenario 5: Pipeline Error
    print("\n5. Pipeline Error Alert...")
    send_pipeline_error_alert(
        pipeline_name="Sentiment Analysis Pipeline",
        error_message="BERT model failed to load - out of memory"
    )
    
    print("\n" + "="*60)
    print("Alert Scenario Tests Complete")
    print("="*60)


if __name__ == "__main__":
    # Run basic tests
    test_basic_notifications()
    
    # Ask user if they want to test scenarios
    print("\n")
    response = input("Do you want to test alert scenarios? (y/n): ")
    
    if response.lower() == 'y':
        test_alert_scenarios()
    
    print("\nAll tests completed!")
