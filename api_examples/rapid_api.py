import requests
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import os
import time
from dotenv import load_dotenv
import sys
sys.path.append('..')
from notification import send_slack_notification

load_dotenv()

# -----------------------------
# API CONFIG
# -----------------------------
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "9a5b8fc451msha257f028da4dc41p16d9c5jsn3bcaf16566be")

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
}

SEARCH_URL = "https://real-time-amazon-data.p.rapidapi.com/search"
REVIEW_URL = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"

COUNTRY = "US"
SEARCH_PAGE = 1
REVIEW_PAGE = 1
REQUEST_DELAY = 1  # seconds between requests to avoid rate limiting

# -----------------------------
# CATEGORY KEYWORDS
# -----------------------------
CATEGORY_KEYWORDS = {
    "Electricals_Power_Backup": ["inverter", "ups", "power backup", "generator"],
    "Home_Appliances": ["air conditioner", "refrigerator", "washing machine"],
    "Kitchen_Appliances": ["mixer", "grinder", "microwave"],
    "Computers_Tablets": ["laptop", "tablet"],
    "Mobile_Accessories": ["charger", "earphones", "power bank"],
    "Wearables": ["smartwatch", "fitness band"],
    "TV_Audio_Entertainment": ["smart tv", "speaker"],
}

# -----------------------------
# SEARCH AMAZON PRODUCTS
# -----------------------------
def search_products(query):
    """Search for products on Amazon using RapidAPI"""
    params = {
        "query": query,
        "page": SEARCH_PAGE,
        "country": COUNTRY,
        "sort_by": "RELEVANCE",
        "product_condition": "ALL",
        "is_prime": "false",
        "deals_and_discounts": "NONE"
    }

    try:
        response = requests.get(SEARCH_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY)  # Rate limiting
        return response.json().get("data", {}).get("products", [])
    except requests.exceptions.RequestException as e:
        error_msg = f"Error searching for '{query}': {e}"
        print(error_msg)
        send_slack_notification(
            text=f"🚨 RapidAPI Search Error\n\n{error_msg}"
        )
        return []

# -----------------------------
# FETCH REVIEWS BY ASIN
# -----------------------------
def fetch_reviews(asin):
    """Fetch product reviews by ASIN using RapidAPI"""
    params = {
        "asin": asin,
        "country": COUNTRY,
        "page": REVIEW_PAGE,
        "sort_by": "TOP_REVIEWS",
        "star_rating": "ALL",
        "verified_purchases_only": "false",
        "images_or_videos_only": "false",
        "current_format_only": "false"
    }

    try:
        response = requests.get(REVIEW_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY)  # Rate limiting
        return response.json().get("data", {}).get("reviews", [])
    except requests.exceptions.RequestException as e:
        error_msg = f"Error fetching reviews for ASIN '{asin}': {e}"
        print(error_msg)
        send_slack_notification(
            text=f"🚨 RapidAPI Review Fetch Error\n\n{error_msg}"
        )
        return []

# -----------------------------
# MAIN PIPELINE
# -----------------------------
def collect_amazon_reviews(products_per_keyword=5):
    """
    Collect Amazon product reviews across multiple categories
    
    Args:
        products_per_keyword: Number of products to fetch per keyword (default: 5)
    
    Returns:
        pandas.DataFrame: DataFrame containing all collected reviews
    """
    all_reviews = []
    
    print(f"🚀 Starting Amazon reviews collection...")
    print(f"📊 Categories: {len(CATEGORY_KEYWORDS)}")
    print(f"🔑 Keywords: {sum(len(keywords) for keywords in CATEGORY_KEYWORDS.values())}")
    print(f"⏱️  Request delay: {REQUEST_DELAY}s\n")

    for category, keywords in tqdm(CATEGORY_KEYWORDS.items(), desc="Categories"):
        for keyword in keywords:
            try:
                products = search_products(keyword)

                for product in products[:products_per_keyword]:
                    asin = product.get("asin")
                    if not asin:
                        continue

                    reviews = fetch_reviews(asin)

                    for r in reviews:
                        all_reviews.append({
                            "category": category,
                            "keyword_used": keyword,
                            "asin": asin,
                            "product_title": product.get("title"),
                            "brand": product.get("brand"),
                            "price": product.get("price"),
                            "rating": r.get("rating"),
                            "review_title": r.get("review_title"),
                            "review_text": r.get("review_text"),
                            "review_date": r.get("review_date"),
                            "reviewer": r.get("reviewer_name"),
                            "verified_purchase": r.get("verified_purchase"),
                            "collected_at": datetime.utcnow()
                        })

            except Exception as e:
                error_msg = f"❌ Error for keyword '{keyword}': {e}"
                print(error_msg)
                send_slack_notification(
                    text=f"🚨 RapidAPI Collection Error\n\nKeyword: {keyword}\nError: {e}"
                )

    return pd.DataFrame(all_reviews)

# -----------------------------
# SAVE DATA
# -----------------------------
def save_reviews(df, filename="amazon_reviews_categorized.csv"):
    """Save reviews to CSV with deduplication"""
    
    # Remove duplicates
    original_count = len(df)
    df.drop_duplicates(
        subset=["asin", "review_text"],
        inplace=True
    )
    duplicates_removed = original_count - len(df)
    
    # Save to datasets folder
    output_path = os.path.join("datasets", filename)
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Collection Complete!")
    print(f"📝 Total reviews collected: {original_count}")
    print(f"🗑️  Duplicates removed: {duplicates_removed}")
    print(f"💾 Saved {len(df)} unique reviews to {output_path}")
    
    return output_path

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    # Collect reviews
    df = collect_amazon_reviews(products_per_keyword=5)
    
    # Check if data was collected
    if df.empty:
        print("⚠️  No reviews were collected. Please check your API key and connection.")
    else:
        # Save to CSV
        save_reviews(df)
        
        # Display summary statistics
        print("\n📊 Summary Statistics:")
        print(f"Categories: {df['category'].nunique()}")
        print(f"Products (ASINs): {df['asin'].nunique()}")
        print(f"Date range: {df['review_date'].min()} to {df['review_date'].max()}")
        print("\nReviews per category:")
        print(df['category'].value_counts())
