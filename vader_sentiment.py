"""
VADER Sentiment Analysis
------------------------
VADER (Valence Aware Dictionary and sEntiment Reasoner) is a rule-based
sentiment analysis model designed specifically for:
- Social media posts
- Product reviews
- Short informal text
- Text with emojis, slang, and punctuation

Advantages:
✔ Works well on short texts
✔ Fast (runs only on CPU)
✔ No training needed
✔ Understands emojis, slang, and intensifiers
✔ Good for large datasets

Compound Score Interpretation:
- ≥ 0.05  → Positive
- ≤ -0.05 → Negative
- Between → Neutral
"""

import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# -----------------------------
# Load Data
# -----------------------------
print("Loading data...")
df = pd.read_csv("combined_cleaned_data.csv")
print(f"✅ Loaded {len(df)} rows")
print()

# -----------------------------
# VADER Sentiment Setup
# -----------------------------
print("Downloading VADER lexicon...")
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()
print("✅ VADER initialized")
print()

# -----------------------------
# Sentiment Score Calculation
# -----------------------------
print("Analyzing sentiment...")
df['sentiment_score_vader'] = df['cleaned_text'].apply(
    lambda x: sia.polarity_scores(str(x))['compound']
)

# -----------------------------
# Label Function
# -----------------------------
def label(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

df['sentiment_vader'] = df['sentiment_score_vader'].apply(label)

# -----------------------------
# Save Output
# -----------------------------
df.to_csv("output_vader_sentiment.csv", index=False)
print("✅ VADER sentiment analysis completed. Saved as output_vader_sentiment.csv")
print()

# -----------------------------
# Display Statistics
# -----------------------------
print("=" * 60)
print("VADER SENTIMENT DISTRIBUTION")
print("=" * 60)
print(df['sentiment_vader'].value_counts())
print()

print("=" * 60)
print("SENTIMENT SCORE STATISTICS")
print("=" * 60)
print(f"Mean score: {df['sentiment_score_vader'].mean():.4f}")
print(f"Min score: {df['sentiment_score_vader'].min():.4f}")
print(f"Max score: {df['sentiment_score_vader'].max():.4f}")
print(f"Median score: {df['sentiment_score_vader'].median():.4f}")
print()

# -----------------------------
# Sample Results
# -----------------------------
print("=" * 60)
print("SAMPLE RESULTS (First 5 rows)")
print("=" * 60)
for idx, row in df.head(5).iterrows():
    print(f"\nReview {idx + 1}:")
    print(f"Text: {str(row['cleaned_text'])[:100]}...")
    print(f"Score: {row['sentiment_score_vader']:.4f}")
    print(f"Sentiment: {row['sentiment_vader']}")
    print("-" * 60)
