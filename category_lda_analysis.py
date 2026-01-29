"""
Category-Wise LDA Topic Modeling
---------------------------------
Performs topic modeling separately for each product category to discover
category-specific themes and patterns.

Configuration Parameters Explained:
- NUM_TOPICS_PER_CATEGORY = 5  → Number of topics LDA will create per category
- MIN_DOCS_PER_CATEGORY = 20   → Minimum reviews required to run LDA
- MAX_DF = 0.8                 → Removes words in >80% of documents (too common)
- MIN_DF = 5                   → Keeps words in ≥5 documents (not too rare)
- TOP_WORDS = 10               → Number of keywords shown per topic
- RANDOM_STATE = 42            → Ensures reproducible results

Why Category-Wise LDA?
- Different categories have different aspects (e.g., battery for phones, comfort for shoes)
- More focused and relevant topics per category
- Easier to interpret and act upon

Example Output:
Category: Mobile_Accessories
  Topic 0: charging, cable, fast, adapter, port, usb, charger, speed
  Topic 1: battery, power, bank, capacity, mah, backup, portable
  Topic 2: case, cover, protection, drop, screen, protector, tempered
"""

import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("CATEGORY-WISE LDA TOPIC MODELING")
print("=" * 70)
print()

# -----------------------------
# CONFIG
# -----------------------------
INPUT_FILE = "sentiment_categorized_products.csv"
OUTPUT_FILE = "category_wise_lda_output.csv"
NUM_TOPICS_PER_CATEGORY = 5
MIN_DOCS_PER_CATEGORY = 20
MAX_DF = 0.8
MIN_DF = 5
TOP_WORDS = 10
RANDOM_STATE = 42

print("Configuration:")
print(f"  Input file: {INPUT_FILE}")
print(f"  Output file: {OUTPUT_FILE}")
print(f"  Topics per category: {NUM_TOPICS_PER_CATEGORY}")
print(f"  Min documents required: {MIN_DOCS_PER_CATEGORY}")
print(f"  Max document frequency: {MAX_DF} (removes very common words)")
print(f"  Min document frequency: {MIN_DF} (removes very rare words)")
print(f"  Top words per topic: {TOP_WORDS}")
print()

# -----------------------------
# Custom Stopwords
# (remove sentiment & generic review words)
# -----------------------------
CUSTOM_STOPWORDS = set([
    "good", "bad", "excellent", "poor", "amazing", "nice", "worst", "best",
    "love", "hate", "perfect", "terrible", "awesome", "waste",
    "money", "worth", "value", "price",
    "product", "products", "quality", "buy", "purchase",
    "using", "use", "used", "really", "very", "highly",
    "recommend", "recommended", "work", "works", "working"
])

print(f"Custom stopwords: {len(CUSTOM_STOPWORDS)} words removed")
print(f"  Examples: {list(CUSTOM_STOPWORDS)[:10]}")
print()

# -----------------------------
# Text Cleaning (Aspect Focused)
# -----------------------------
def clean_for_lda(text):
    """
    Clean text for LDA:
    - Convert to lowercase
    - Remove numbers, punctuation, symbols
    - Remove custom stopwords
    - Keep only words > 2 characters
    """
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)   # Remove numbers, punctuation, symbols
    tokens = text.split()
    tokens = [t for t in tokens if t not in CUSTOM_STOPWORDS and len(t) > 2]
    return " ".join(tokens)

# -----------------------------
# Load Data
# -----------------------------
print("=" * 70)
print("LOADING DATA")
print("=" * 70)

try:
    df = pd.read_csv(INPUT_FILE)
    print(f"✅ Loaded {len(df)} records from {INPUT_FILE}")
except FileNotFoundError:
    print(f"❌ ERROR: File '{INPUT_FILE}' not found!")
    print()
    print("Please ensure you have:")
    print("1. Run sentiment analysis on categorized products")
    print("2. File contains 'cleaned_text' and 'category' columns")
    exit(1)

# Clean and prepare data
df = df.dropna(subset=["cleaned_text", "category"])
df = df[df["cleaned_text"].str.strip() != ""]

print(f"✅ After removing empty rows: {len(df)} records")
print()

# Apply additional cleaning for LDA
print("Applying LDA-specific text cleaning...")
df["lda_text"] = df["cleaned_text"].apply(clean_for_lda)

# Remove rows where cleaning resulted in empty text
df = df[df["lda_text"].str.strip() != ""]
print(f"✅ Final dataset: {len(df)} records")
print()

# -----------------------------
# Category Distribution
# -----------------------------
print("=" * 70)
print("CATEGORY DISTRIBUTION")
print("=" * 70)

category_counts = df["category"].value_counts()
print(f"\nTotal categories: {len(category_counts)}")
print(f"\nTop 10 categories:")
for cat, count in category_counts.head(10).items():
    marker = "✓" if count >= MIN_DOCS_PER_CATEGORY else "✗"
    print(f"  {marker} {cat:<40} {count:>5} reviews")
print()

# -----------------------------
# Helper: Extract Topic Words
# -----------------------------
def get_topic_words(model, feature_names, top_n):
    """
    Extract top N words for each topic.
    
    How it works:
    - argsort() → sorts word weights
    - [-top_n:] → selects top N words
    - [::-1] → reverses to highest → lowest
    """
    topic_map = {}
    for idx, topic in enumerate(model.components_):
        top_indices = topic.argsort()[-top_n:][::-1]
        words = [feature_names[i] for i in top_indices]
        topic_map[idx] = ", ".join(words)
    return topic_map

# -----------------------------
# Store Results
# -----------------------------
final_results = []
skipped_categories = []
processed_categories = []

# -----------------------------
# Category-wise LDA
# -----------------------------
print("=" * 70)
print("RUNNING LDA FOR EACH CATEGORY")
print("=" * 70)
print()

for category, df_cat in df.groupby("category"):
    print(f"Category: {category}")
    print(f"  Reviews: {len(df_cat)}")
    
    # Check minimum document requirement
    if len(df_cat) < MIN_DOCS_PER_CATEGORY:
        print(f"  ✗ SKIPPED (need at least {MIN_DOCS_PER_CATEGORY} reviews)")
        skipped_categories.append((category, len(df_cat)))
        print()
        continue
    
    # Create document-term matrix
    vectorizer = CountVectorizer(
        stop_words="english",
        max_df=MAX_DF,         # Ignore words in >80% of docs
        min_df=MIN_DF,         # Ignore words in <5 docs
        ngram_range=(1, 2)     # Capture phrases like "battery life"
    )
    
    doc_term_matrix = vectorizer.fit_transform(df_cat["lda_text"])
    
    print(f"  Vocabulary: {doc_term_matrix.shape[1]} unique terms")
    
    # Check if enough terms for topics
    if doc_term_matrix.shape[1] < NUM_TOPICS_PER_CATEGORY:
        print(f"  ✗ SKIPPED (not enough unique terms)")
        skipped_categories.append((category, len(df_cat)))
        print()
        continue
    
    # Train LDA model
    lda = LatentDirichletAllocation(
        n_components=NUM_TOPICS_PER_CATEGORY,
        random_state=RANDOM_STATE,
        learning_method="batch",
        max_iter=20
    )
    
    lda.fit(doc_term_matrix)
    
    # Extract topics
    feature_names = vectorizer.get_feature_names_out()
    topic_word_map = get_topic_words(lda, feature_names, TOP_WORDS)
    
    print(f"  ✓ Discovered {NUM_TOPICS_PER_CATEGORY} topics:")
    for topic_id, keywords in topic_word_map.items():
        print(f"    Topic {topic_id}: {keywords}")
    
    # Assign topics to documents
    topic_dist = lda.transform(doc_term_matrix)
    
    df_cat = df_cat.copy()
    df_cat["lda_topic"] = topic_dist.argmax(axis=1)
    df_cat["lda_topic_confidence"] = topic_dist.max(axis=1)
    df_cat["lda_topic_keywords"] = df_cat["lda_topic"].map(topic_word_map)
    
    final_results.append(df_cat)
    processed_categories.append(category)
    print()

# -----------------------------
# Summary
# -----------------------------
print("=" * 70)
print("PROCESSING SUMMARY")
print("=" * 70)
print()

print(f"✓ Successfully processed: {len(processed_categories)} categories")
print(f"✗ Skipped: {len(skipped_categories)} categories")
print()

if skipped_categories:
    print("Skipped categories:")
    for cat, count in skipped_categories:
        print(f"  • {cat} ({count} reviews)")
    print()

# -----------------------------
# Combine & Save
# -----------------------------
if final_results:
    final_df = pd.concat(final_results, ignore_index=True)
    final_df.to_csv(OUTPUT_FILE, index=False)
    
    print("=" * 70)
    print("RESULTS SAVED")
    print("=" * 70)
    print(f"✅ Saved {len(final_df)} records to: {OUTPUT_FILE}")
    print()
    
    # Show column info
    print("Output columns:")
    for col in final_df.columns:
        print(f"  • {col}")
    print()
    
    # Topic distribution statistics
    print("=" * 70)
    print("TOPIC ASSIGNMENT STATISTICS")
    print("=" * 70)
    print()
    
    print(f"Average topic confidence: {final_df['lda_topic_confidence'].mean():.3f}")
    print(f"Min topic confidence: {final_df['lda_topic_confidence'].min():.3f}")
    print(f"Max topic confidence: {final_df['lda_topic_confidence'].max():.3f}")
    print()
    
    # Sample results
    print("=" * 70)
    print("SAMPLE RESULTS")
    print("=" * 70)
    print()
    
    for idx, row in final_df.head(5).iterrows():
        print(f"Review {idx + 1}:")
        print(f"  Category: {row['category']}")
        print(f"  Text: {str(row['cleaned_text'])[:80]}...")
        print(f"  Topic: {row['lda_topic']}")
        print(f"  Keywords: {row['lda_topic_keywords']}")
        print(f"  Confidence: {row['lda_topic_confidence']:.3f}")
        print()
    
else:
    print("=" * 70)
    print("NO RESULTS")
    print("=" * 70)
    print("❌ No category had enough data for LDA.")
    print()
    print("Suggestions:")
    print(f"1. Lower MIN_DOCS_PER_CATEGORY (currently {MIN_DOCS_PER_CATEGORY})")
    print(f"2. Lower MIN_DF (currently {MIN_DF})")
    print(f"3. Ensure you have more review data")

# -----------------------------
# Next Steps
# -----------------------------
print("=" * 70)
print("💡 NEXT STEPS")
print("=" * 70)
print()
print("1. Run 'category_topic_summary.py' to extract keyword summaries")
print("2. Combine topics with sentiment analysis")
print("3. Analyze topic trends over time")
print("4. Create category-topic dashboards")
print("5. Identify category-specific pain points")
print()
print("=" * 70)
