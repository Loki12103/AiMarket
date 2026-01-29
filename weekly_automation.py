"""
Weekly Automated Data Collection & Monitoring Pipeline
-------------------------------------------------------
Complete automation:
1. Collect data from all sources
2. Perform sentiment analysis
3. Run topic modeling
4. Detect sentiment spikes & trend shifts
5. Send real-time notifications
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from notification import send_mail


class WeeklyAutomation:
    """Complete weekly automation pipeline"""
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.data_dir = "final data"
        self.collection_results = {}
        self.monitoring_results = {}
        
    def collect_review_data(self):
        """
        Collect product review data
        In production: Replace with actual API calls or web scraping
        """
        print("\n1. Collecting Product Review Data...")
        
        try:
            # Placeholder: Load existing data
            # In production: Call scraping.collect_reviews()
            reviews = pd.read_csv(f"{self.data_dir}/category_wise_lda_output_with_topic_labels.csv")
            
            self.collection_results["reviews"] = {
                "status": "success",
                "count": len(reviews),
                "source": "Amazon/Flipkart"
            }
            
            print(f"   ✓ Collected {len(reviews)} product reviews")
            return reviews
            
        except Exception as e:
            self.collection_results["reviews"] = {
                "status": "failed",
                "error": str(e)
            }
            print(f"   ✗ Failed to collect reviews: {str(e)}")
            return None
    
    def collect_news_data(self):
        """
        Collect news articles
        In production: Call News API
        """
        print("\n2. Collecting News Data...")
        
        try:
            # Placeholder: Load existing data
            # In production: Call news_api_collector.collect_news()
            news = pd.read_csv(f"{self.data_dir}/news_data_with_sentiment.csv")
            
            self.collection_results["news"] = {
                "status": "success",
                "count": len(news),
                "source": "NewsAPI"
            }
            
            print(f"   ✓ Collected {len(news)} news articles")
            return news
            
        except Exception as e:
            self.collection_results["news"] = {
                "status": "failed",
                "error": str(e)
            }
            print(f"   ✗ Failed to collect news: {str(e)}")
            return None
    
    def collect_reddit_data(self):
        """
        Collect Reddit posts
        In production: Call Reddit API
        """
        print("\n3. Collecting Reddit Data...")
        
        try:
            # Placeholder: Load existing data
            # In production: Call reddit_data_collector.collect_posts()
            reddit = pd.read_excel(f"{self.data_dir}/reddit_category_trend_data.xlsx")
            
            self.collection_results["reddit"] = {
                "status": "success",
                "count": len(reddit),
                "source": "Reddit API"
            }
            
            print(f"   ✓ Collected {len(reddit)} Reddit posts")
            return reddit
            
        except Exception as e:
            self.collection_results["reddit"] = {
                "status": "failed",
                "error": str(e)
            }
            print(f"   ✗ Failed to collect Reddit data: {str(e)}")
            return None
    
    def analyze_sentiment_spikes(self, current_data, historical_data):
        """Detect sentiment spikes"""
        print("\n4. Analyzing Sentiment Spikes...")
        
        spikes = []
        threshold = 0.15  # 15% change
        
        try:
            # Calculate sentiment by category
            current_sentiment = (
                current_data.groupby("category")["sentiment_label"]
                .apply(lambda x: (x == "Positive").mean())
            )
            
            historical_sentiment = (
                historical_data.groupby("category")["sentiment_label"]
                .apply(lambda x: (x == "Positive").mean())
            )
            
            # Compare
            for category in current_sentiment.index:
                if category in historical_sentiment.index:
                    old_score = historical_sentiment[category]
                    new_score = current_sentiment[category]
                    change = abs(new_score - old_score)
                    
                    if change >= threshold:
                        direction = "POSITIVE" if new_score > old_score else "NEGATIVE"
                        
                        spike = {
                            "category": category,
                            "old_sentiment": old_score,
                            "new_sentiment": new_score,
                            "change": change,
                            "direction": direction
                        }
                        
                        spikes.append(spike)
                        
                        # Send alert
                        self.send_sentiment_spike_alert(spike)
                        
                        print(f"   ⚠️ {direction} spike in {category}: {change*100:.1f}% change")
            
            if not spikes:
                print("   ✓ No significant sentiment spikes detected")
            
            return spikes
            
        except Exception as e:
            print(f"   ✗ Sentiment analysis failed: {str(e)}")
            self.send_pipeline_error("Sentiment Spike Detection", str(e))
            return []
    
    def analyze_trend_shifts(self, current_data, historical_data):
        """Detect trend shifts in category mentions"""
        print("\n5. Analyzing Trend Shifts...")
        
        shifts = []
        threshold = 0.20  # 20% change
        
        try:
            current_counts = current_data["category"].value_counts()
            historical_counts = historical_data["category"].value_counts()
            
            # Compare
            for category in current_counts.index:
                if category in historical_counts.index:
                    old_count = historical_counts[category]
                    new_count = current_counts[category]
                    pct_change = (new_count - old_count) / old_count
                    
                    if abs(pct_change) >= threshold:
                        direction = "UP" if pct_change > 0 else "DOWN"
                        
                        shift = {
                            "category": category,
                            "old_count": old_count,
                            "new_count": new_count,
                            "pct_change": pct_change,
                            "direction": direction
                        }
                        
                        shifts.append(shift)
                        
                        # Send alert
                        self.send_trend_shift_alert(shift)
                        
                        print(f"   📈 Trend {direction} in {category}: {pct_change*100:+.1f}%")
            
            if not shifts:
                print("   ✓ No significant trend shifts detected")
            
            return shifts
            
        except Exception as e:
            print(f"   ✗ Trend analysis failed: {str(e)}")
            self.send_pipeline_error("Trend Shift Detection", str(e))
            return []
    
    def send_sentiment_spike_alert(self, spike):
        """Send email alert for sentiment spike"""
        change_pct = spike["change"] * 100
        
        message = f"""
SENTIMENT SPIKE DETECTED!

Category: {spike["category"]}
Direction: {spike["direction"]}

Previous Sentiment Score: {spike["old_sentiment"]:.1%}
Current Sentiment Score: {spike["new_sentiment"]:.1%}
Change: {change_pct:.1f}%

This requires immediate attention from the market intelligence team.

Timestamp: {self.timestamp}

---
AI Market Trend & Consumer Sentiment Forecaster
Automated Weekly Monitoring System
"""
        
        send_mail(
            text=message,
            subject=f"⚠️ {spike['direction']} Sentiment Spike - {spike['category']}"
        )
    
    def send_trend_shift_alert(self, shift):
        """Send email alert for trend shift"""
        change_pct = shift["pct_change"] * 100
        
        message = f"""
TREND SHIFT DETECTED!

Category: {shift["category"]}
Direction: {shift["direction"]}

Previous Mentions: {shift["old_count"]}
Current Mentions: {shift["new_count"]}
Change: {change_pct:+.1f}%

Consumer interest is shifting. Review category strategy.

Timestamp: {self.timestamp}

---
AI Market Trend & Consumer Sentiment Forecaster
Automated Weekly Monitoring System
"""
        
        send_mail(
            text=message,
            subject=f"📈 Trend Shift {shift['direction']} - {shift['category']}"
        )
    
    def send_data_collection_summary(self):
        """Send summary email of data collection"""
        print("\n6. Sending Data Collection Summary...")
        
        total_success = sum(1 for r in self.collection_results.values() if r["status"] == "success")
        total_sources = len(self.collection_results)
        total_records = sum(r.get("count", 0) for r in self.collection_results.values() if r["status"] == "success")
        
        # Build message
        message = f"""
WEEKLY DATA COLLECTION COMPLETED

Summary:
---------
Total Sources: {total_sources}
Successful: {total_success}
Failed: {total_sources - total_success}
Total Records Collected: {total_records}

Details:
---------
"""
        
        for source, result in self.collection_results.items():
            if result["status"] == "success":
                message += f"\n✓ {source.upper()}: {result['count']} records from {result['source']}"
            else:
                message += f"\n✗ {source.upper()}: FAILED - {result.get('error', 'Unknown error')}"
        
        # Add monitoring summary
        total_alerts = len(self.monitoring_results.get("sentiment_spikes", [])) + \
                      len(self.monitoring_results.get("trend_shifts", []))
        
        message += f"""

Monitoring Results:
-------------------
Sentiment Spikes Detected: {len(self.monitoring_results.get("sentiment_spikes", []))}
Trend Shifts Detected: {len(self.monitoring_results.get("trend_shifts", []))}
Total Alerts Sent: {total_alerts}

Timestamp: {self.timestamp}

---
AI Market Trend & Consumer Sentiment Forecaster
Automated Weekly Monitoring System
"""
        
        # Determine subject based on results
        if total_success == total_sources:
            subject = "✓ Weekly Data Collection - All Sources Successful"
        elif total_success > 0:
            subject = f"⚠️ Weekly Data Collection - {total_success}/{total_sources} Sources Successful"
        else:
            subject = "✗ Weekly Data Collection - All Sources Failed"
        
        send_mail(text=message, subject=subject)
        print("   ✓ Summary email sent")
    
    def send_pipeline_error(self, pipeline_name, error_message):
        """Send pipeline error alert"""
        message = f"""
PIPELINE ERROR!

Pipeline: {pipeline_name}
Error: {error_message}

Immediate technical investigation required.

Timestamp: {self.timestamp}

---
AI Market Trend & Consumer Sentiment Forecaster
Automated Weekly Monitoring System
"""
        
        send_mail(
            text=message,
            subject=f"✗ Pipeline Error - {pipeline_name}"
        )
    
    def run_weekly_pipeline(self):
        """Run complete weekly automation pipeline"""
        print("="*70)
        print("AI MARKET WEEKLY AUTOMATION PIPELINE")
        print("="*70)
        print(f"Start Time: {self.timestamp}\n")
        
        # Step 1-3: Collect data from all sources
        print("="*70)
        print("PHASE 1: DATA COLLECTION")
        print("="*70)
        
        reviews = self.collect_review_data()
        news = self.collect_news_data()
        reddit = self.collect_reddit_data()
        
        # Step 4-5: Monitoring (if reviews data available)
        if reviews is not None and len(reviews) > 0:
            print("\n" + "="*70)
            print("PHASE 2: SENTIMENT & TREND MONITORING")
            print("="*70)
            
            # Split data into current week vs previous week
            # For demo: use all data as current, simulate historical
            current_reviews = reviews.tail(int(len(reviews) * 0.6))
            historical_reviews = reviews.head(int(len(reviews) * 0.4))
            
            sentiment_spikes = self.analyze_sentiment_spikes(current_reviews, historical_reviews)
            trend_shifts = self.analyze_trend_shifts(current_reviews, historical_reviews)
            
            self.monitoring_results = {
                "sentiment_spikes": sentiment_spikes,
                "trend_shifts": trend_shifts
            }
        else:
            print("\n✗ Skipping monitoring due to missing review data")
            self.monitoring_results = {
                "sentiment_spikes": [],
                "trend_shifts": []
            }
        
        # Step 6: Send summary
        print("\n" + "="*70)
        print("PHASE 3: NOTIFICATION")
        print("="*70)
        
        self.send_data_collection_summary()
        
        # Final summary
        print("\n" + "="*70)
        print("PIPELINE EXECUTION SUMMARY")
        print("="*70)
        print(f"End Time: {datetime.now()}")
        print(f"Duration: {datetime.now() - self.timestamp}")
        print(f"Total Alerts Sent: {len(self.monitoring_results.get('sentiment_spikes', [])) + len(self.monitoring_results.get('trend_shifts', [])) + 1}")
        print("="*70 + "\n")
        
        return {
            "collection_results": self.collection_results,
            "monitoring_results": self.monitoring_results,
            "timestamp": self.timestamp
        }


def run_weekly_automation():
    """Main entry point for weekly automation"""
    automation = WeeklyAutomation()
    results = automation.run_weekly_pipeline()
    return results


if __name__ == "__main__":
    # Run weekly automation
    print("Starting Weekly Automation Pipeline...\n")
    
    try:
        results = run_weekly_automation()
        print("\n✓ Weekly automation completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Weekly automation failed: {str(e)}")
        
        # Send critical error email
        from notification import send_mail
        send_mail(
            text=f"Critical error in weekly automation pipeline:\n\n{str(e)}\n\nTimestamp: {datetime.now()}",
            subject="✗ CRITICAL: Weekly Automation Failed"
        )
