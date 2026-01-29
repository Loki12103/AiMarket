"""
Rating-Based Sentiment Analysis
--------------------------------
Assigns sentiment labels based on rating column for Flipkart data only.
For other sources, keeps existing sentiment values.

Rating mapping:
- 1-2 → negative
- 3 → neutral
- 4-5 → positive
"""

import pandas as pd
import numpy as np

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("combined_cleaned_data.csv")

# -----------------------------
# Rating-based sentiment for Flipkart
# -----------------------------
def rating_sentiment(row):
    if str(row['source']).lower() == 'flipkart':
        try:
            rating = int(row['rating'])
        except:
            return "unknown"
        
        if rating in [1, 2]:
            return "negative"
        elif rating == 3:
            return "neutral"
        elif rating in [4, 5]:
            return "positive"
        else:
            return "unknown"
    else:
        return row.get('sentiment_label', None)  # keep previous value

df['sentiment_label'] = df.apply(rating_sentiment, axis=1)

# -----------------------------
# Add RANDOM review_date (2021-01-01 to 2025-01-01)
# -----------------------------
start_date = pd.to_datetime("2021-01-01")
end_date = pd.to_datetime("2025-01-01")
mask = df['review_date'].isna() | (df['review_date'] == "")
random_dates = pd.to_datetime(
    np.random.randint(
        start_date.value // 10**9,
        end_date.value // 10**9,
        size=mask.sum()
    ),
    unit='s'
)
df.loc[mask, 'review_date'] = random_dates.strftime("%Y-%m-%d")

# -----------------------------
# Save Output
# -----------------------------
df.to_csv("output_rating_sentiment.csv", index=False)
print("✅ Rating-based sentiment analysis completed. Saved as output_rating_sentiment.csv")

# -----------------------------
# Display Statistics
# -----------------------------
print("\n" + "=" * 60)
print("SENTIMENT DISTRIBUTION")
print("=" * 60)
print(df['sentiment_label'].value_counts())
print()
print(f"Total rows: {len(df)}")
print(f"Flipkart rows: {len(df[df['source'].str.lower() == 'flipkart'])}")
print(f"Non-Flipkart rows: {len(df[df['source'].str.lower() != 'flipkart'])}")
