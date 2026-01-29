"""
News Data Collection Module
----------------------------
Automated news collection for market intelligence
Integrates with NewsAPI to fetch product and technology news
Uses FinBERT for sentiment analysis
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import notification
from notification import send_slack_notification
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

load_dotenv()

# -----------------------------
# API CONFIG
# -----------------------------
API_KEY = os.getenv("NEWS_API_KEY", "6bd01117d4b74c2f91e0ce5bdcbdef04")
BASE_URL = "https://newsapi.org/v2/everything"

# Collect data from the last week so that we have new data every week
FROM_DATE = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
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

# -----------------------------
# OUTPUT FILE CONFIG
# -----------------------------
OUTPUT_FILE = "datasets/final data/news_data_with_sentiment.csv"


# -----------------------------
# FETCH NEWS FUNCTION
# -----------------------------
def fetch_news(query, category):
    """
    Fetch news articles for a specific keyword and category
    
    Args:
        query (str): Keyword to search
        category (str): Category name for classification
    
    Returns:
        list: List of article dictionaries
    """
    params = {
        "q": query,
        "from": FROM_DATE,
        "language": LANGUAGE,
        "sortBy": "popularity",
        "pageSize": PAGE_SIZE,
        "apiKey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
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
# SENTIMENT PREDICTION FUNCTION
# -----------------------------
def get_sentiment(text):
    """
    Predict sentiment using FinBERT model
    
    Args:
        text (str): Text to analyze
    
    Returns:
        str: Sentiment label (Positive, Negative, Neutral)
    """
    MODEL_NAME = "ProsusAI/finbert"

    # Load model & tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    if pd.isna(text) or text.strip() == "":
        return "Neutral"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        sentiment_idx = torch.argmax(probs).item()

    label_map = {
        0: "Negative",
        1: "Neutral",
        2: "Positive"
    }

    return label_map[sentiment_idx]


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def get_news_data():
    """
    Main function to collect news data with sentiment analysis
    Called by scheduler for automated news collection
    """
    print(f"\n{'='*60}")
    print(f"NEWS DATA COLLECTION STARTED")
    print(f"Timestamp: {datetime.now()}")
    print(f"From Date: {FROM_DATE}")
    print(f"{'='*60}\n")
    
    try:
        all_articles = []

        # Fetch news for all categories
        for category, keywords in tqdm(CATEGORY_KEYWORDS.items(), desc="Categories"):
            for keyword in keywords:
                try:
                    articles = fetch_news(keyword, category)
                    all_articles.extend(articles)
                except Exception as e:
                    error_msg = f"Error fetching {keyword}: {e}"
                    print(error_msg)
                    send_slack_notification(
                        text=f"🚨 News Fetch Error\n\nKeyword: {keyword}\nCategory: {category}\nError: {e}"
                    )

        # -----------------------------
        # SAVE TO CSV
        # -----------------------------
        news_df = pd.DataFrame(all_articles)

        # Remove duplicates based on URL
        news_df.drop_duplicates(subset="url", inplace=True)

        # Save intermediate file
        news_df.to_csv("news_data_categorized.csv", index=False)
        print(f"\n✓ Saved {len(news_df)} articles to news_data_categorized.csv")

        # -----------------------------
        # COMBINE TEXT FIELDS
        # -----------------------------
        news_df["combined_text"] = (
            news_df["title"].fillna("") + ". " +
            news_df["description"].fillna("") + ". " +
            news_df["content"].fillna("")
        )

        # -----------------------------
        # APPLY SENTIMENT MODEL
        # -----------------------------
        print("\n🔍 Analyzing sentiment using FinBERT...")
        tqdm.pandas()
        news_df["sentiment_label"] = news_df["combined_text"].progress_apply(get_sentiment)

        # -----------------------------
        # SAVE OUTPUT
        # -----------------------------
        news_df.drop(columns=["combined_text"], inplace=True)
        
        if os.path.exists(OUTPUT_FILE):
            # Append without header
            news_df.to_csv(OUTPUT_FILE, mode="a", index=False, header=False)
            print(f"\n✓ Appended {len(news_df)} articles to {OUTPUT_FILE}")
        else:
            # Create file with header
            news_df.to_csv(OUTPUT_FILE, index=False)
            print(f"\n✓ Created {OUTPUT_FILE} with {len(news_df)} articles")

        # Send success notification
        notification.send_mail(
            f"""
News Data Collection Completed Successfully!

Total Articles Collected: {len(news_df)}
Categories Searched: {len(CATEGORY_KEYWORDS)}
Date Range: {FROM_DATE} to {datetime.today().strftime('%Y-%m-%d')}

Sentiment Analysis: FinBERT
Output File: {OUTPUT_FILE}

Sentiment Distribution:
{news_df['sentiment_label'].value_counts().to_dict()}

Timestamp: {datetime.now()}

---
AI Market Trend & Consumer Sentiment Forecaster
Weekly News Collection
""",
            "✓ News Data Extraction Successful"
        )
        
        print("✅ Sentiment analysis completed and saved successfully.")
        return news_df

    except Exception as e:
        print(f"\n✗ News collection failed: {str(e)}")
        
        error_msg = f"Failed to Extract News Data. Error: {e}\n\nTimestamp: {datetime.now()}"
        
        # Send error notifications
        notification.send_mail(
            error_msg,
            "✗ News Data Extraction Failed"
        )
        
        send_slack_notification(
            text=f"🚨 NEWS COLLECTION FAILED\n\n{error_msg}"
        )
        
        return None


# Test function for manual execution
def test_news_collection():
    """Test news collection manually"""
    print("\nTesting news collection...\n")
    result = get_news_data()
    
    if result is not None:
        print(f"\n✓ Test successful! Collected {len(result)} articles")
        print("\nSample data:")
        print(result.head())
    else:
        print("\n✗ Test failed - no data collected")


if __name__ == "__main__":
    # Run manual test
    test_news_collection()


# -----------------------------
# TEST FUNCTION
# -----------------------------
def test_news_collection():
    """Test news collection manually"""
    print("\n" + "="*60)
    print("TESTING NEWS COLLECTION")
    print("="*60 + "\n")
    
    result = get_news_data()
    
    if result is not None:
        print(f"\n✓ Test successful! Collected {len(result)} articles")
        print("\nSentiment Distribution:")
        print(result['sentiment_label'].value_counts())
        print("\nCategory Distribution:")
        print(result['category'].value_counts().head(10))
        print("\nSample data:")
        print(result[['title', 'category', 'sentiment_label']].head())
    else:
        print("\n✗ Test failed - no data collected")