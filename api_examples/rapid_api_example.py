"""
RapidAPI Example - Amazon Product Data
---------------------------------------
Shows how to use RapidAPI for product data collection
NOTE: Requires RapidAPI key (sign up at rapidapi.com)
"""

import requests
import json

print("=" * 60)
print("RAPIDAPI - AMAZON PRODUCT DATA")
print("=" * 60)
print()

def fetch_amazon_products_rapidapi(query, api_key):
    """
    Fetch Amazon product data using RapidAPI
    
    Parameters:
    - query: Product search term
    - api_key: Your RapidAPI key
    """
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    
    querystring = {
        "query": query,
        "page": "1",
        "country": "IN"  # India
    }
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }
    
    print(f"Searching for: {query}")
    print()
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()

# DEMO MODE - Shows structure without actual API call
print("📌 RapidAPI Setup Instructions:")
print("-" * 60)
print("1. Go to: https://rapidapi.com/")
print("2. Sign up for free account")
print("3. Subscribe to 'Real-Time Amazon Data' API (free tier available)")
print("4. Copy your API key")
print("5. Replace 'YOUR_RAPIDAPI_KEY' below with your actual key")
print()
print("=" * 60)
print()

# Example code structure (won't run without real key)
API_KEY = "YOUR_RAPIDAPI_KEY"  # Replace with your key

print("Example usage:")
print("-" * 60)
print(f"api_key = '{API_KEY}'")
print("data = fetch_amazon_products_rapidapi('iPhone 15', api_key)")
print()

# Show expected response structure
example_response = {
    "status": "OK",
    "request_id": "abc123",
    "data": {
        "products": [
            {
                "asin": "B09X5XXXX",
                "product_title": "Apple iPhone 15 Pro (256GB) - Natural Titanium",
                "product_price": "₹1,34,900",
                "product_star_rating": "4.5",
                "product_num_ratings": 1234,
                "product_url": "https://amazon.in/...",
                "product_photo": "https://m.media-amazon.com/images/...",
                "is_prime": True
            }
        ]
    }
}

print("Expected Response Structure:")
print("-" * 60)
print(json.dumps(example_response, indent=4))
print()

# Example of how to parse the data
print("=" * 60)
print("DATA PARSING EXAMPLE")
print("=" * 60)
print()

demo_products = [
    {"title": "iPhone 15 Pro", "price": "₹1,34,900", "rating": 4.5, "reviews": 1234},
    {"title": "Samsung Galaxy S24", "price": "₹89,999", "rating": 4.3, "reviews": 892},
    {"title": "OnePlus 12", "price": "₹64,999", "rating": 4.6, "reviews": 567},
]

print("Sample products:")
for i, product in enumerate(demo_products, 1):
    print(f"{i}. {product['title']}")
    print(f"   Price: {product['price']}")
    print(f"   Rating: {product['rating']} ⭐ ({product['reviews']} reviews)")
    print()

print("=" * 60)
print("✅ Setup guide completed!")
print("=" * 60)
