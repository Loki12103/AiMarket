"""
Amazon Product Scraper - Mixed Reviews Collector
-------------------------------------------------
Collects both positive and negative product reviews
Uses multiple data sources
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

print("=" * 60)
print("MIXED REVIEWS COLLECTOR - MULTIPLE SOURCES")
print("=" * 60)
print()

# ==========================================
# METHOD 1: Reddit API (Real reviews)
# ==========================================

def fetch_mixed_reviews_reddit(product_name, limit=100):
    """
    Fetch mixed reviews from Reddit discussions
    Reddit naturally has both positive and negative opinions
    """
    print(f"📌 Searching Reddit for: {product_name}")
    
    url = "https://www.reddit.com/search.json"
    params = {
        "q": f"{product_name} review OR opinion OR experience",
        "limit": limit,
        "sort": "relevance"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed: {response.status_code}")
        return []
    
    data = response.json()
    reviews = []
    
    for post in data.get("data", {}).get("children", []):
        p = post["data"]
        
        # Combine title and text
        full_text = f"{p.get('title', '')} {p.get('selftext', '')}"
        
        if len(full_text.strip()) > 20:  # Only substantial posts
            reviews.append({
                "source": "Reddit",
                "product": product_name,
                "text": full_text[:500],
                "score": p.get("score", 0),
                "comments": p.get("num_comments", 0),
                "subreddit": p.get("subreddit", ""),
                "created": p.get("created_utc", 0)
            })
    
    print(f"✅ Found {len(reviews)} Reddit posts")
    return reviews

# ==========================================
# METHOD 2: Best Buy API (Real product reviews)
# ==========================================

def fetch_best_buy_reviews(product_keyword):
    """
    Fetch reviews from Best Buy API
    NOTE: This is a demo - actual implementation requires API key
    """
    print(f"📌 Best Buy reviews for: {product_keyword}")
    
    # Demo structure - shows what real API would return
    demo_reviews = [
        {
            "source": "BestBuy",
            "product": product_keyword,
            "text": "Amazing product! Works perfectly. Highly recommend.",
            "rating": 5,
            "helpful_count": 45
        },
        {
            "source": "BestBuy",
            "product": product_keyword,
            "text": "Disappointed with battery life. Overpriced for what you get.",
            "rating": 2,
            "helpful_count": 32
        },
        {
            "source": "BestBuy",
            "product": product_keyword,
            "text": "Good but not great. Has some issues with connectivity.",
            "rating": 3,
            "helpful_count": 18
        }
    ]
    
    print(f"✅ Demo: {len(demo_reviews)} sample reviews")
    return demo_reviews

# ==========================================
# METHOD 3: Twitter/X Search (Public opinions)
# ==========================================

def fetch_twitter_mentions(product_name):
    """
    Fetch Twitter/X mentions about product
    NOTE: Requires Twitter API key for production use
    """
    print(f"📌 Twitter mentions for: {product_name}")
    
    # Demo structure
    demo_tweets = [
        {
            "source": "Twitter",
            "product": product_name,
            "text": f"Just got my {product_name} and I'm blown away! Best purchase ever! 🔥",
            "likes": 234,
            "retweets": 45
        },
        {
            "source": "Twitter",
            "product": product_name,
            "text": f"Really disappointed with {product_name}. Not worth the hype at all 😞",
            "likes": 89,
            "retweets": 12
        },
        {
            "source": "Twitter",
            "product": product_name,
            "text": f"{product_name} is okay. Nothing special but does the job.",
            "likes": 23,
            "retweets": 3
        }
    ]
    
    print(f"✅ Demo: {len(demo_tweets)} sample tweets")
    return demo_tweets

# ==========================================
# COLLECT REVIEWS FROM ALL SOURCES
# ==========================================

products_to_analyze = [
    "iPhone 15 Pro",
    "Samsung Galaxy S24",
    "AirPods Pro"
]

print("=" * 60)
print("COLLECTING MIXED REVIEWS FROM MULTIPLE SOURCES")
print("=" * 60)
print()

all_reviews = []

for product in products_to_analyze:
    print(f"\n{'='*60}")
    print(f"Product: {product}")
    print('='*60)
    
    # Collect from Reddit (REAL API - works without key)
    reddit_reviews = fetch_mixed_reviews_reddit(product, limit=50)
    all_reviews.extend(reddit_reviews)
    
    # Demo: Best Buy reviews
    bestbuy_reviews = fetch_best_buy_reviews(product)
    all_reviews.extend(bestbuy_reviews)
    
    # Demo: Twitter mentions
    twitter_reviews = fetch_twitter_mentions(product)
    all_reviews.extend(twitter_reviews)
    
    time.sleep(1)  # Be nice to servers

# ==========================================
# SAVE & ANALYZE
# ==========================================

if all_reviews:
    df = pd.DataFrame(all_reviews)
    
    print("\n" + "=" * 60)
    print("COLLECTION SUMMARY")
    print("=" * 60)
    print(f"Total reviews: {len(df)}")
    print(f"\nReviews by source:")
    print(df['source'].value_counts())
    print(f"\nReviews by product:")
    print(df['product'].value_counts())
    print()
    
    # Save data
    output_csv = "datasets/mixed_product_reviews.csv"
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"✅ Saved to: {output_csv}")
    
    output_json = "datasets/mixed_reviews_raw.json"
    df.to_json(output_json, orient="records", indent=4)
    print(f"✅ Raw JSON: {output_json}")
    
    # Show samples
    print("\n" + "=" * 60)
    print("SAMPLE REVIEWS (First 5)")
    print("=" * 60)
    for idx, row in df.head(5).iterrows():
        print(f"\n{idx+1}. [{row['source']}] {row['product']}")
        print(f"   {row['text'][:100]}...")
    
    print("\n" + "=" * 60)
    print("✅ Mixed reviews collected successfully!")
    print("💡 Tip: Use sentiment_analysis.py to analyze positive/negative sentiment")
    print("=" * 60)

else:
    print("❌ No reviews collected!")
