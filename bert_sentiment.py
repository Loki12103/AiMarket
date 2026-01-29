"""
BERT Sentiment Analysis
-----------------------
BERT (Bidirectional Encoder Representations from Transformers) is a 
pre-trained deep learning language model developed by Google.

Advantages:
✔ Understands context and meaning
✔ Handles negation and complex sentences
✔ High accuracy in sentiment analysis
✔ Pre-trained on large datasets (Wikipedia, Books)
⚠ Uses high computation power

Model: nlptown/bert-base-multilingual-uncased-sentiment
Output: 1-5 star ratings
"""

import pandas as pd
from transformers import pipeline

# -----------------------------
# Load Data
# -----------------------------
print("Loading data...")
df = pd.read_csv("combined_cleaned_data.csv").head(100)  # Process first 100 rows (remove .head() for all data)
print(f"✅ Loaded {len(df)} rows")
print()

# -----------------------------
# Load BERT Sentiment Model
# -----------------------------
print("Loading BERT sentiment model (this may take a minute)...")
print("Model: nlptown/bert-base-multilingual-uncased-sentiment")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)
print("✅ BERT model loaded successfully")
print()

# -----------------------------
# Apply Sentiment Analysis
# -----------------------------
def get_sentiment(text):
    if pd.isna(text) or str(text).strip() == "":
        return "Neutral", 0, 0
    
    try:
        result = sentiment_pipeline(str(text)[:512])  # BERT max token limit
        label = result[0]["label"]
        score = result[0]["score"]
        
        # Convert star rating to sentiment
        if label in ["1 star", "2 stars"]:
            sentiment = "negative"
        elif label == "3 stars":
            sentiment = "neutral"
        else:  # 4-5 stars
            sentiment = "positive"
        
        return sentiment, label, score
    except Exception as e:
        print(f"Error processing text: {str(e)[:50]}")
        return "Neutral", "error", 0

print("Analyzing sentiment...")
results = df["review_text"].apply(get_sentiment)

df["sentiment_bert"] = results.apply(lambda x: x[0])
df["sentiment_star_rating"] = results.apply(lambda x: x[1])
df["sentiment_confidence"] = results.apply(lambda x: x[2])

# -----------------------------
# Save Output
# -----------------------------
df.to_csv("bert_sentiment_output.csv", index=False)
print()
print("✅ BERT sentiment analysis completed. Saved as bert_sentiment_output.csv")
print()

# -----------------------------
# Display Statistics
# -----------------------------
print("=" * 60)
print("BERT SENTIMENT DISTRIBUTION")
print("=" * 60)
print(df['sentiment_bert'].value_counts())
print()

print("=" * 60)
print("STAR RATING DISTRIBUTION")
print("=" * 60)
print(df['sentiment_star_rating'].value_counts())
print()

print("=" * 60)
print("CONFIDENCE STATISTICS")
print("=" * 60)
print(f"Mean confidence: {df['sentiment_confidence'].mean():.4f}")
print(f"Min confidence: {df['sentiment_confidence'].min():.4f}")
print(f"Max confidence: {df['sentiment_confidence'].max():.4f}")
print()

# -----------------------------
# Sample Results
# -----------------------------
print("=" * 60)
print("SAMPLE RESULTS (First 5 rows)")
print("=" * 60)
for idx, row in df.head(5).iterrows():
    print(f"\nReview {idx + 1}:")
    print(f"Text: {str(row['review_text'])[:100]}...")
    print(f"Star Rating: {row['sentiment_star_rating']}")
    print(f"Sentiment: {row['sentiment_bert']}")
    print(f"Confidence: {row['sentiment_confidence']:.4f}")
    print("-" * 60)

print()
print("💡 NOTE: Processing stopped at 100 rows. Remove .head(100) to process all data.")
