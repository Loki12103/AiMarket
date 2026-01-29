"""
Reddit API - Product Discussion Scraper
----------------------------------------
Fetches product discussions and reviews from Reddit
No API key required for public data!
"""

import requests
import pandas as pd
import json
from datetime import datetime

print("=" * 60)
print("REDDIT API - PRODUCT DISCUSSION SCRAPER")
print("=" * 60)
print()

def fetch_reddit_posts(query, limit=50):
    """
    Fetch Reddit posts for a given search query
    
    Parameters:
    - query: Search term (e.g., "iPhone 15", "Samsung Galaxy")
    - limit: Number of posts to fetch (max 100)
    """
    base_url = "https://www.reddit.com/search.json"
    
    params = {
        "q": query,
        "limit": limit,
        "sort": "relevance"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"Searching Reddit for: '{query}'")
    print(f"Fetching up to {limit} posts...")
    print()
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        return None
    
    return response.json()

def parse_reddit_data(json_data):
    """
    Parse Reddit JSON response into clean DataFrame
    """
    posts = []
    
    if not json_data or "data" not in json_data:
        return pd.DataFrame()
    
    for post in json_data["data"]["children"]:
        data = post["data"]
        
        posts.append({
            "title": data.get("title", ""),
            "text": data.get("selftext", ""),
            "subreddit": data.get("subreddit", ""),
            "author": data.get("author", ""),
            "score": data.get("score", 0),
            "num_comments": data.get("num_comments", 0),
            "created_utc": datetime.fromtimestamp(data.get("created_utc", 0)),
            "url": data.get("url", ""),
            "permalink": f"https://reddit.com{data.get('permalink', '')}"
        })
    
    return pd.DataFrame(posts)

# Search queries for different products
search_queries = [
    "iPhone 15 review",
    "Samsung Galaxy S24",
    "laptop recommendations",
]

print("=" * 60)
print("COLLECTING REDDIT DATA")
print("=" * 60)
print()

all_data = []

for query in search_queries:
    # Fetch data
    json_data = fetch_reddit_posts(query, limit=50)
    
    if json_data:
        # Parse into DataFrame
        df = parse_reddit_data(json_data)
        
        if not df.empty:
            print(f"✅ Found {len(df)} posts for '{query}'")
            print(f"   Top subreddit: {df['subreddit'].mode()[0] if not df.empty else 'N/A'}")
            print(f"   Avg score: {df['score'].mean():.1f}")
            print()
            
            # Add query column
            df["search_query"] = query
            all_data.append(df)
    else:
        print(f"❌ Failed to fetch data for '{query}'")
        print()

# Combine all data
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    
    print("=" * 60)
    print("DATA COLLECTION SUMMARY")
    print("=" * 60)
    print(f"Total posts collected: {len(combined_df)}")
    print(f"Date range: {combined_df['created_utc'].min()} to {combined_df['created_utc'].max()}")
    print()
    
    print("Top 5 subreddits:")
    print(combined_df['subreddit'].value_counts().head(5))
    print()
    
    # Save to CSV
    output_csv = "datasets/reddit_product_discussions.csv"
    combined_df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"✅ Data saved to: {output_csv}")
    
    # Also save raw JSON
    output_json = "datasets/reddit_raw_data.json"
    combined_df.to_json(output_json, orient="records", indent=4)
    print(f"✅ Raw JSON saved to: {output_json}")
    
    # Show sample
    print()
    print("=" * 60)
    print("SAMPLE POSTS (First 3)")
    print("=" * 60)
    for idx, row in combined_df.head(3).iterrows():
        print(f"\n{idx+1}. {row['title'][:70]}...")
        print(f"   Subreddit: r/{row['subreddit']}")
        print(f"   Score: {row['score']} | Comments: {row['num_comments']}")
        print(f"   Date: {row['created_utc']}")
    print()
else:
    print("❌ No data collected!")

print("=" * 60)
