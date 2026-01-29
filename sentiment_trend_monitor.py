"""
Sentiment and Trend Monitoring System
--------------------------------------
Detects sentiment spikes and trend shifts, sends real-time alerts
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from notification_service import (
    send_sentiment_spike_alert,
    send_trend_shift_alert,
    send_data_ingestion_alert,
    send_pipeline_error_alert
)
from notification_config import (
    SENTIMENT_SPIKE_THRESHOLD,
    TREND_SHIFT_THRESHOLD,
    MINIMUM_DATA_POINTS
)


class SentimentTrendMonitor:
    """Monitor sentiment spikes and trend shifts"""
    
    def __init__(self, current_data_path, historical_data_path=None):
        """
        Initialize monitor
        
        Args:
            current_data_path (str): Path to current week's data
            historical_data_path (str): Path to previous week's data
        """
        self.current_data_path = current_data_path
        self.historical_data_path = historical_data_path
        self.alerts_sent = []
    
    def load_data(self):
        """Load current and historical data"""
        try:
            self.current_data = pd.read_csv(self.current_data_path)
            
            if self.historical_data_path:
                self.historical_data = pd.read_csv(self.historical_data_path)
            else:
                # If no historical data, use previous week from current data
                self.split_data_by_week()
            
            send_data_ingestion_alert(
                source="Product Reviews",
                status="success",
                record_count=len(self.current_data)
            )
            return True
            
        except Exception as e:
            send_data_ingestion_alert(
                source="Product Reviews",
                status="failed",
                error_message=str(e)
            )
            return False
    
    def split_data_by_week(self):
        """Split data into current and previous week"""
        if "review_date" in self.current_data.columns:
            self.current_data["review_date"] = pd.to_datetime(
                self.current_data["review_date"], errors="coerce"
            )
            
            # Get last 2 weeks
            cutoff_date = datetime.now() - timedelta(days=7)
            
            self.historical_data = self.current_data[
                self.current_data["review_date"] < cutoff_date
            ]
            self.current_data = self.current_data[
                self.current_data["review_date"] >= cutoff_date
            ]
    
    def detect_sentiment_spikes(self):
        """Detect sudden sentiment changes by category"""
        if len(self.current_data) < MINIMUM_DATA_POINTS:
            print("Insufficient data for sentiment analysis")
            return []
        
        spikes = []
        
        try:
            # Calculate sentiment scores by category
            current_sentiment = self.calculate_sentiment_by_category(self.current_data)
            historical_sentiment = self.calculate_sentiment_by_category(self.historical_data)
            
            # Compare sentiments
            for category in current_sentiment.index:
                if category in historical_sentiment.index:
                    old_score = historical_sentiment[category]
                    new_score = current_sentiment[category]
                    
                    change = abs(new_score - old_score)
                    
                    if change >= SENTIMENT_SPIKE_THRESHOLD:
                        direction = "positive" if new_score > old_score else "negative"
                        
                        spike_info = {
                            "category": category,
                            "old_sentiment": old_score,
                            "new_sentiment": new_score,
                            "change": change,
                            "direction": direction
                        }
                        
                        spikes.append(spike_info)
                        
                        # Send alert
                        send_sentiment_spike_alert(
                            category=category,
                            old_sentiment=old_score,
                            new_sentiment=new_score,
                            direction=direction
                        )
                        
                        print(f"⚠️ Sentiment spike detected in {category}: {direction.upper()}")
            
            return spikes
            
        except Exception as e:
            send_pipeline_error_alert(
                pipeline_name="Sentiment Spike Detection",
                error_message=str(e)
            )
            return []
    
    def calculate_sentiment_by_category(self, data):
        """Calculate positive sentiment percentage by category"""
        if "sentiment_label" not in data.columns or "category" not in data.columns:
            return pd.Series()
        
        sentiment_scores = (
            data.groupby("category")["sentiment_label"]
            .apply(lambda x: (x == "Positive").mean())
        )
        
        return sentiment_scores
    
    def detect_trend_shifts(self):
        """Detect sudden changes in category mentions"""
        if len(self.current_data) < MINIMUM_DATA_POINTS:
            print("Insufficient data for trend analysis")
            return []
        
        shifts = []
        
        try:
            # Count mentions by category
            current_counts = self.current_data["category"].value_counts()
            historical_counts = self.historical_data["category"].value_counts()
            
            # Compare counts
            for category in current_counts.index:
                if category in historical_counts.index:
                    old_count = historical_counts[category]
                    new_count = current_counts[category]
                    
                    # Calculate percentage change
                    pct_change = (new_count - old_count) / old_count
                    
                    if abs(pct_change) >= TREND_SHIFT_THRESHOLD:
                        direction = "up" if pct_change > 0 else "down"
                        
                        shift_info = {
                            "category": category,
                            "old_count": old_count,
                            "new_count": new_count,
                            "pct_change": pct_change,
                            "direction": direction
                        }
                        
                        shifts.append(shift_info)
                        
                        # Send alert
                        send_trend_shift_alert(
                            category=category,
                            old_count=old_count,
                            new_count=new_count,
                            direction=direction
                        )
                        
                        print(f"📈 Trend shift detected in {category}: {direction.upper()}")
            
            return shifts
            
        except Exception as e:
            send_pipeline_error_alert(
                pipeline_name="Trend Shift Detection",
                error_message=str(e)
            )
            return []
    
    def run_monitoring(self):
        """Run complete monitoring pipeline"""
        print("="*60)
        print("AI Market Trend Monitoring System")
        print("="*60)
        print(f"Timestamp: {datetime.now()}\n")
        
        # Load data
        if not self.load_data():
            print("✗ Failed to load data. Monitoring aborted.")
            return
        
        print(f"✓ Loaded {len(self.current_data)} current records")
        print(f"✓ Loaded {len(self.historical_data)} historical records\n")
        
        # Detect sentiment spikes
        print("Analyzing sentiment spikes...")
        sentiment_spikes = self.detect_sentiment_spikes()
        print(f"Found {len(sentiment_spikes)} sentiment spikes\n")
        
        # Detect trend shifts
        print("Analyzing trend shifts...")
        trend_shifts = self.detect_trend_shifts()
        print(f"Found {len(trend_shifts)} trend shifts\n")
        
        # Summary
        print("="*60)
        print("Monitoring Summary")
        print("="*60)
        print(f"Total Alerts Sent: {len(sentiment_spikes) + len(trend_shifts)}")
        print(f"Sentiment Spikes: {len(sentiment_spikes)}")
        print(f"Trend Shifts: {len(trend_shifts)}")
        print("="*60)
        
        return {
            "sentiment_spikes": sentiment_spikes,
            "trend_shifts": trend_shifts,
            "total_alerts": len(sentiment_spikes) + len(trend_shifts)
        }


def run_weekly_monitoring():
    """Run weekly monitoring job"""
    try:
        monitor = SentimentTrendMonitor(
            current_data_path="final data/category_wise_lda_output_with_topic_labels.csv"
        )
        
        results = monitor.run_monitoring()
        
        return results
        
    except Exception as e:
        send_pipeline_error_alert(
            pipeline_name="Weekly Monitoring Job",
            error_message=str(e)
        )
        print(f"✗ Monitoring failed: {str(e)}")
        return None


if __name__ == "__main__":
    # Run monitoring
    results = run_weekly_monitoring()
    
    if results:
        print("\n✓ Weekly monitoring completed successfully!")
    else:
        print("\n✗ Weekly monitoring failed!")
