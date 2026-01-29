"""
Merge and Clean Flipkart + Amazon Datasets
-------------------------------------------
Combines two different data sources into one unified format
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

print("=" * 60)
print("MERGING FLIPKART + AMAZON DATASETS")
print("=" * 60)
print()

# --------------------------
# 1. Download stopwords
# --------------------------
print("Step 1: Loading stopwords...")
nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))
print(f"✓ Loaded {len(stop_words)} stopwords")
print()

# --------------------------
# CLEANING FUNCTIONS
# --------------------------
def clean_lowercase(text):
    if isinstance(text, str):
        return text.lower()
    return text

def clean_punctuation(text):
    if isinstance(text, str):
        return re.sub(r"[^\w\s]", "", text)
    return text

def clean_stopwords(text):
    if isinstance(text, str):
        return " ".join([w for w in text.split() if w not in stop_words])
    return text

def clean_whitespace(text):
    if isinstance(text, str):
        return re.sub(r"\s+", " ", text).strip()
    return text

def clean_text(text):
    text = clean_lowercase(text)
    text = clean_punctuation(text)
    text = clean_stopwords(text)
    text = clean_whitespace(text)
    return text

def clean_text_flip(t):
    """Special cleaning for Flipkart data"""
    t = str(t)
    # 1. Remove non-ASCII garbled characters
    t = re.sub(r"[^\x00-\x7F]", " ", t)
    # 2. Remove ALL special characters except letters/numbers/space
    t = re.sub(r"[^a-zA-Z0-9 ]", " ", t)
    # 3. Collapse multiple spaces into one
    t = re.sub(r"\s+", " ", t)
    return t.strip()

# --------------------------
# 2. LOAD FILES
# --------------------------
print("Step 2: Loading datasets...")
try:
    df_flip = pd.read_csv("datasets/flipkart_product.csv", encoding="latin1", engine="python")
    print(f"✓ Loaded Flipkart: {len(df_flip)} rows")
except FileNotFoundError:
    print("❌ Error: datasets/flipkart_product.csv not found!")
    df_flip = None

try:
    df_amazon = pd.read_excel("datasets/Amazon DataSheet - Pradeep.xlsx")
    print(f"✓ Loaded Amazon: {len(df_amazon)} rows")
except FileNotFoundError:
    print("❌ Error: datasets/Amazon DataSheet - Pradeep.xlsx not found!")
    df_amazon = None

if df_flip is None and df_amazon is None:
    print("\n❌ No data files found. Please add the required files.")
    exit()

print()

# --------------------------
# 3. PROCESS FLIPKART DATA
# --------------------------
if df_flip is not None:
    print("Step 3: Processing Flipkart data...")
    
    # Clean all text columns
    df_flip = df_flip.applymap(lambda x: clean_text_flip(x) if isinstance(x, str) else x)
    
    # Standardize column names
    df_flip = df_flip.rename(columns={
        "ProductName": "product",
        "Review": "review_title",
        "Summary": "review_text",
        "Rate": "rating"
    })
    
    # Add missing columns
    df_flip["source"] = "flipkart"
    df_flip["review_date"] = ""
    df_flip["sentiment_label"] = ""
    df_flip["category"] = ""
    
    print(f"✓ Processed Flipkart data")
    print()

# --------------------------
# 4. PROCESS AMAZON DATA
# --------------------------
if df_amazon is not None:
    print("Step 4: Processing Amazon data...")
    
    # Standardize column names
    df_amazon = df_amazon.rename(columns={
        "Product Name": "product",
        "Comment": "review_text",
        "Star Rating": "rating",
        "Date of Review": "review_date",
        "Category": "category",
        "Sentiment": "sentiment_label"
    })
    
    # Add missing columns
    df_amazon["source"] = "amazon"
    df_amazon["review_title"] = ""
    
    print(f"✓ Processed Amazon data")
    print()

# --------------------------
# 5. KEEP ONLY REQUIRED COLUMNS
# --------------------------
required = [
    "source",
    "product",
    "review_text",
    "review_title",
    "rating",
    "category",
    "review_date",
    "sentiment_label"
]

if df_flip is not None:
    df_flip = df_flip[required]

if df_amazon is not None:
    df_amazon = df_amazon[required]

# --------------------------
# 6. COMBINE BOTH
# --------------------------
print("Step 5: Combining datasets...")
dfs_to_combine = []
if df_flip is not None:
    dfs_to_combine.append(df_flip)
if df_amazon is not None:
    dfs_to_combine.append(df_amazon)

df = pd.concat(dfs_to_combine, ignore_index=True)
print(f"✓ Combined dataset: {len(df)} total rows")
print()

# --------------------------
# 7. CLEAN review_text & product
# --------------------------
print("Step 6: Cleaning text columns...")
df["cleaned_text"] = df["review_text"].astype(str).apply(clean_text)
df["product"] = df["product"].astype(str).apply(clean_text)
print(f"✓ Cleaned review_text and product columns")
print()

# --------------------------
# 8. ADD sentiment_score placeholder
# --------------------------
df["sentiment_score"] = ""

# --------------------------
# 9. SAVE OUTPUT
# --------------------------
print("Step 7: Saving combined dataset...")
output_file = "datasets/combined_cleaned_data.csv"
df.to_csv(output_file, index=False)
print(f"✓ Saved to: {output_file}")
print()

# --------------------------
# 10. SHOW SUMMARY
# --------------------------
print("=" * 60)
print("MERGE COMPLETED SUCCESSFULLY! ✅")
print("=" * 60)
print(f"Total rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print()
print("Column breakdown:")
for col in df.columns:
    non_empty = df[col].astype(str).str.strip().ne('').sum()
    print(f"  - {col}: {non_empty} non-empty values")
print()
print("Sample data (first 3 rows):")
print("-" * 60)
print(df[['source', 'product', 'cleaned_text', 'sentiment_label']].head(3))
print()
print("=" * 60)
