"""
Reddit API Data Collector
--------------------------
Collects consumer discussion data from Reddit for product categories.
Uses Reddit's public JSON API without authentication.

Features:
- Fetches posts for multiple product categories
- Rate-limiting to avoid API blocks
- Filters empty/low-quality posts
- Exports to CSV for analysis
"""

import requests
import pandas as pd
from datetime import datetime
import time
from notification import send_slack_notification

# -----------------------------
# Labels (Categories)
# -----------------------------
labels = [
    "Electricals_Power_Backup",
    "Home_Appliances",
    "Kitchen_Appliances",
    "Furniture",
    "Home_Storage_Organization",
    "Computers_Tablets",
    "Mobile_Accessories",
    "Wearables",
    "TV_Audio_Entertainment",
    "Networking_Devices",
    "Toys_Kids",
    "Gardening_Outdoor",
    "Kitchen_Dining",
    "Mens_Clothing",
    "Footwear",
    "Beauty_Personal_Care",
    "Security_Surveillance",
    "Office_Printer_Supplies",
    "Software",
    "Fashion_Accessories",
]

# -----------------------------
# Reddit API Setup
# -----------------------------
url = "https://www.reddit.com/search.json"
headers = {
    "User-Agent": "Mozilla/5.0 (ConsumerTrendAnalysisBot)"
}
all_rows = []

print("=" * 60)
print("REDDIT DATA COLLECTION")
print("=" * 60)
print(f"Categories to fetch: {len(labels)}")
print()

# -----------------------------
# Loop through labels
# -----------------------------
for idx, label in enumerate(labels, 1):
    print(f"[{idx}/{len(labels)}] Fetching data for: {label}")
    
    params = {
        "q": label.replace("_", " "),
        "limit": 100
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"   ❌ Failed (Status {response.status_code})")
            continue
        
        data = response.json()
        posts_found = 0
        
        for post in data["data"]["children"]:
            post_data = post["data"]
            all_rows.append({
                "source": "Reddit",
                "category_label": label,
                "query": label.replace("_", " "),
                "title": post_data.get("title", ""),
                "selftext": post_data.get("selftext", ""),
                "subreddit": post_data.get("subreddit", ""),
                "score": post_data.get("score", 0),
                "num_comments": post_data.get("num_comments", 0),
                "created_date": datetime.utcfromtimestamp(
                    post_data.get("created_utc", 0)
                )
            })
            posts_found += 1
        
        print(f"   ✅ Collected {posts_found} posts")
        
    except Exception as e:
        error_msg = f"   ❌ Error: {str(e)[:50]}"
        print(error_msg)
        send_slack_notification(
            text=f"🚨 Reddit Data Collection Error\\n\\nLabel: {label}\\nError: {str(e)}"
        )
    
    # Polite delay to avoid rate-limiting
    time.sleep(2)

print()
print("=" * 60)

# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame(all_rows)

# Remove empty text rows
initial_count = len(df)
df = df[df["selftext"].str.strip() != ""].reset_index(drop=True)
removed_count = initial_count - len(df)

print(f"Total records collected: {initial_count}")
print(f"Empty posts removed: {removed_count}")
print(f"Final records: {len(df)}")
print()

# -----------------------------
# Display Sample Data
# -----------------------------
if len(df) > 0:
    print("=" * 60)
    print("SAMPLE DATA (First 3 posts)")
    print("=" * 60)
    for idx, row in df.head(3).iterrows():
        print(f"\nPost {idx + 1}:")
        print(f"Category: {row['category_label']}")
        print(f"Subreddit: r/{row['subreddit']}")
        print(f"Title: {row['title'][:80]}...")
        print(f"Score: {row['score']} | Comments: {row['num_comments']}")
        print(f"Date: {row['created_date']}")
        print("-" * 60)
    print()

# -----------------------------
# Category Distribution
# -----------------------------
if len(df) > 0:
    print("=" * 60)
    print("CATEGORY DISTRIBUTION")
    print("=" * 60)
    print(df['category_label'].value_counts().head(10))
    print()

# -----------------------------
# Save to CSV
# -----------------------------
output_file = "reddit_mixed_consumer_data.csv"
df.to_csv(output_file, index=False)
print(f"✅ Dataset saved to: {output_file}")
print()

# -----------------------------
# Statistics
# -----------------------------
if len(df) > 0:
    print("=" * 60)
    print("STATISTICS")
    print("=" * 60)
    print(f"Total posts: {len(df)}")
    print(f"Unique subreddits: {df['subreddit'].nunique()}")
    print(f"Average score: {df['score'].mean():.2f}")
    print(f"Average comments: {df['num_comments'].mean():.2f}")
    print(f"Date range: {df['created_date'].min()} to {df['created_date'].max()}")
    print()

print("=" * 60)
print("💡 NEXT STEPS:")
print("=" * 60)
print("1. Clean and preprocess the text data")
print("2. Apply sentiment analysis (VADER or BERT)")
print("3. Merge with other data sources (Flipkart, Amazon)")
print("4. Analyze trends and patterns")
print("=" * 60)
