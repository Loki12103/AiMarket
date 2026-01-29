"""
NewsAPI - Product & Tech News Fetcher
--------------------------------------
Fetches latest news articles about products and technology
Requires FREE API key from newsapi.org
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta

print("=" * 60)
print("NEWSAPI - PRODUCT NEWS COLLECTOR")
print("=" * 60)
print()

# ==========================================
# SETUP INSTRUCTIONS
# ==========================================
print("📌 NewsAPI Setup:")
print("-" * 60)
print("1. Go to: https://newsapi.org/register")
print("2. Sign up for FREE account (500 requests/day)")
print("3. Copy your API key")
print("4. Add to .env file: NEWS_API_KEY=your_key_here")
print()
print("=" * 60)
print()

# Load API key from environment
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_API_KEY_HERE")

if NEWS_API_KEY == "YOUR_API_KEY_HERE":
    print("⚠️ WARNING: Using placeholder API key!")
    print("Please add your actual key to .env file")
    print()

def fetch_product_news(query, days_back=7, language="en"):
    """
    Fetch news articles about a product
    
    Parameters:
    - query: Product name or keyword
    - days_back: How many days back to search
    - language: Language code (en, hi, etc.)
    """
    base_url = "https://newsapi.org/v2/everything"
    
    # Calculate date range
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days_back)
    
    params = {
        "q": query,
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "language": language,
        "sortBy": "relevancy",
        "apiKey": NEWS_API_KEY
    }
    
    print(f"Searching news for: '{query}'")
    print(f"Date range: {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}")
    print()
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()

def parse_news_data(json_data):
    """Parse NewsAPI JSON into clean DataFrame"""
    if not json_data or json_data.get("status") != "ok":
        return pd.DataFrame()
    
    articles = []
    
    for article in json_data.get("articles", []):
        articles.append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "source": article.get("source", {}).get("name", ""),
            "author": article.get("author", ""),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
            "image_url": article.get("urlToImage", "")
        })
    
    return pd.DataFrame(articles)

# ==========================================
# EXAMPLE USAGE
# ==========================================

# Product queries to search
product_queries = [
    "iPhone 15 Pro review",
    "Samsung Galaxy S24",
    "Tesla Model 3",
]

print("=" * 60)
print("COLLECTING NEWS DATA")
print("=" * 60)
print()

all_news = []

for query in product_queries:
    # Fetch news
    json_data = fetch_product_news(query, days_back=7)
    
    if json_data and json_data.get("status") == "ok":
        # Parse into DataFrame
        df = parse_news_data(json_data)
        
        if not df.empty:
            total_results = json_data.get("totalResults", 0)
            print(f"✅ Found {len(df)} articles for '{query}' (Total: {total_results})")
            print(f"   Top source: {df['source'].mode()[0] if not df.empty else 'N/A'}")
            print()
            
            # Add query column
            df["search_query"] = query
            all_news.append(df)
        else:
            print(f"⚠️ No articles found for '{query}'")
            print()
    else:
        print(f"❌ Failed to fetch news for '{query}'")
        print()

# ==========================================
# SAVE RESULTS
# ==========================================

if all_news:
    combined_df = pd.concat(all_news, ignore_index=True)
    
    print("=" * 60)
    print("NEWS COLLECTION SUMMARY")
    print("=" * 60)
    print(f"Total articles: {len(combined_df)}")
    print(f"Date range: {combined_df['published_at'].min()} to {combined_df['published_at'].max()}")
    print()
    
    print("Top 5 news sources:")
    print(combined_df['source'].value_counts().head(5))
    print()
    
    # Save to CSV
    output_csv = "datasets/news_product_articles.csv"
    combined_df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"✅ Data saved to: {output_csv}")
    
    # Also save raw JSON
    output_json = "datasets/news_raw_data.json"
    combined_df.to_json(output_json, orient="records", indent=4)
    print(f"✅ Raw JSON saved to: {output_json}")
    
    # Show sample
    print()
    print("=" * 60)
    print("SAMPLE ARTICLES (First 3)")
    print("=" * 60)
    for idx, row in combined_df.head(3).iterrows():
        print(f"\n{idx+1}. {row['title']}")
        print(f"   Source: {row['source']}")
        print(f"   Published: {row['published_at']}")
        print(f"   {row['description'][:100]}...")
    print()
else:
    print("❌ No news data collected!")
    print("Make sure you have added NEWS_API_KEY to .env file")

print("=" * 60)
