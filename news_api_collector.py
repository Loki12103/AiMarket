"""
News API Data Collector
------------------------
Collects news articles from NewsAPI.org for product categories.
Requires API key from https://newsapi.org/

Features:
- Fetches news for multiple product categories
- Removes duplicate articles
- Progress tracking with tqdm
- Exports to CSV for analysis

Setup:
1. Get free API key from https://newsapi.org/
2. Create .env file with: NEWS_API_KEY=your_api_key_here
3. Install: pip install requests pandas python-dotenv tqdm
"""

import requests
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------
# API CONFIG
# -----------------------------
API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"
FROM_DATE = "2025-12-25"
LANGUAGE = "en"
PAGE_SIZE = 50

# -----------------------------
# CATEGORY KEYWORDS
# -----------------------------
CATEGORY_KEYWORDS = {
    "Electricals_Power_Backup": ["inverter", "ups", "power backup", "generator"],
    "Home_Appliances": ["air conditioner", "refrigerator", "washing machine", "air cooler"],
    "Kitchen_Appliances": ["mixer", "grinder", "microwave", "oven", "juicer"],
    "Furniture": ["sofa", "bed", "table", "chair"],
    "Home_Storage_Organization": ["storage box", "wardrobe", "organizer"],
    "Computers_Tablets": ["laptop", "tablet", "desktop"],
    "Mobile_Accessories": ["charger", "earphones", "power bank"],
    "Wearables": ["smartwatch", "fitness band"],
    "TV_Audio_Entertainment": ["smart tv", "speaker", "soundbar"],
    "Networking_Devices": ["router", "wifi modem"],
    "Toys_Kids": ["kids toys", "children games"],
    "Gardening_Outdoor": ["gardening", "lawn tools"],
    "Kitchen_Dining": ["cookware", "utensils"],
    "Mens_Clothing": ["mens clothing", "mens fashion"],
    "Footwear": ["shoes", "sneakers"],
    "Beauty_Personal_Care": ["skincare", "beauty products"],
    "Security_Surveillance": ["cctv", "security camera"],
    "Office_Printer_Supplies": ["printer", "scanner"],
    "Software": ["software", "saas"],
    "Fashion_Accessories": ["handbag", "watch", "wallet"]
}

print("=" * 60)
print("NEWS API DATA COLLECTOR")
print("=" * 60)
print()

# -----------------------------
# Validate API Key
# -----------------------------
if not API_KEY:
    print("❌ ERROR: NEWS_API_KEY not found!")
    print()
    print("Setup instructions:")
    print("1. Get free API key from https://newsapi.org/")
    print("2. Create a .env file in this directory")
    print("3. Add line: NEWS_API_KEY=your_api_key_here")
    print()
    exit(1)

print(f"✅ API Key loaded")
print(f"📅 From Date: {FROM_DATE}")
print(f"🌐 Language: {LANGUAGE}")
print(f"📄 Page Size: {PAGE_SIZE}")
print(f"📋 Categories: {len(CATEGORY_KEYWORDS)}")
print()

# -----------------------------
# FETCH NEWS FUNCTION
# -----------------------------
def fetch_news(query, category):
    """Fetch news articles for a specific query and category"""
    params = {
        "q": query,
        "from": FROM_DATE,
        "language": LANGUAGE,
        "sortBy": "popularity",
        "pageSize": PAGE_SIZE,
        "apiKey": API_KEY
    }
    
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    articles = []
    for a in data.get("articles", []):
        articles.append({
            "source": a["source"]["name"],
            "author": a.get("author"),
            "title": a.get("title"),
            "description": a.get("description"),
            "content": a.get("content"),
            "url": a.get("url"),
            "image_url": a.get("urlToImage"),
            "published_at": a.get("publishedAt"),
            "category": category,
            "query_used": query,
            "collected_at": datetime.utcnow()
        })
    
    return articles

# -----------------------------
# MAIN PIPELINE
# -----------------------------
print("=" * 60)
print("COLLECTING NEWS ARTICLES")
print("=" * 60)
print()

all_articles = []
total_queries = sum(len(keywords) for keywords in CATEGORY_KEYWORDS.values())
failed_queries = []

with tqdm(total=total_queries, desc="Fetching articles") as pbar:
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            try:
                articles = fetch_news(keyword, category)
                all_articles.extend(articles)
                pbar.set_postfix({"Category": category, "Articles": len(all_articles)})
            except Exception as e:
                failed_queries.append({"keyword": keyword, "error": str(e)[:50]})
                pbar.set_postfix({"Category": category, "Error": "Failed"})
            
            pbar.update(1)

print()
print("=" * 60)

# -----------------------------
# SAVE TO CSV
# -----------------------------
news_df = pd.DataFrame(all_articles)

# Remove duplicates based on URL
initial_count = len(news_df)
news_df.drop_duplicates(subset="url", inplace=True)
duplicates_removed = initial_count - len(news_df)

output_file = "news_data_categorized.csv"
news_df.to_csv(output_file, index=False)

print(f"✅ Saved {len(news_df)} articles to {output_file}")
print(f"📊 Total collected: {initial_count}")
print(f"🔄 Duplicates removed: {duplicates_removed}")
print(f"❌ Failed queries: {len(failed_queries)}")
print()

# -----------------------------
# Display Statistics
# -----------------------------
if len(news_df) > 0:
    print("=" * 60)
    print("CATEGORY DISTRIBUTION")
    print("=" * 60)
    print(news_df['category'].value_counts().head(10))
    print()
    
    print("=" * 60)
    print("TOP NEWS SOURCES")
    print("=" * 60)
    print(news_df['source'].value_counts().head(10))
    print()
    
    print("=" * 60)
    print("SAMPLE ARTICLES")
    print("=" * 60)
    for idx, row in news_df.head(3).iterrows():
        print(f"\nArticle {idx + 1}:")
        print(f"Category: {row['category']}")
        print(f"Source: {row['source']}")
        print(f"Title: {row['title']}")
        print(f"Published: {row['published_at']}")
        print(f"URL: {row['url']}")
        print("-" * 60)
    print()

# -----------------------------
# Display Failed Queries
# -----------------------------
if failed_queries:
    print("=" * 60)
    print("FAILED QUERIES")
    print("=" * 60)
    for fq in failed_queries[:5]:
        print(f"❌ {fq['keyword']}: {fq['error']}")
    if len(failed_queries) > 5:
        print(f"... and {len(failed_queries) - 5} more")
    print()

print("=" * 60)
print("💡 NEXT STEPS:")
print("=" * 60)
print("1. Clean and preprocess article text")
print("2. Apply sentiment analysis")
print("3. Analyze trends over time")
print("4. Compare with product review data")
print("=" * 60)
