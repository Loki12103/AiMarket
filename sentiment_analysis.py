"""
Sentiment Analysis with Gemini
-------------------------------
Analyze cleaned Flipkart reviews using Google Gemini
"""

import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("=" * 60)
print("SENTIMENT ANALYSIS WITH GEMINI")
print("=" * 60)
print()

# Load cleaned data
try:
    df = pd.read_csv("sentimentdataset_cleaned.csv")
    print(f"✓ Loaded {len(df)} cleaned reviews")
    print()
except FileNotFoundError:
    print("❌ Error: Please run data_cleaning.py first!")
    exit()

# Take sample reviews for analysis
sample_reviews = df.head(5)

print("Analyzing sample reviews...")
print("-" * 60)

for idx, row in sample_reviews.iterrows():
    # Get the review text (adjust column name based on your CSV)
    review_text = str(row.get('Review', row.get('review', row.get('text', ''))))
    
    if not review_text or review_text == 'nan':
        continue
    
    prompt = f"""
    Analyze this product review and provide:
    1. Sentiment: Positive/Negative/Neutral
    2. Key points mentioned
    3. Overall rating (1-5 stars)
    
    Review: "{review_text}"
    
    Keep the analysis concise (2-3 sentences).
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3
        ),
    )
    
    print(f"\nReview {idx + 1}:")
    print(f"Original: {review_text[:100]}...")
    print(f"Analysis: {response.text}")
    print("-" * 60)

print("\n✅ Sentiment analysis completed!")
