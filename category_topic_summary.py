"""
Category-Topic Keyword Summary Extractor
-----------------------------------------
Extracts and summarizes topic keywords for each category-topic combination.

Purpose:
- Creates a clean summary of all discovered topics
- Maps each category to its topics and keywords
- Useful for dashboards, reports, and analysis

Input: category_wise_lda_output.csv (from category_lda_analysis.py)
Output: category_topic_keywords.csv

Output Format:
category              | lda_topic | lda_topic_keywords
---------------------|-----------|-------------------------------------------
Mobile_Accessories   | 0         | charging, cable, fast, adapter, port, usb
Mobile_Accessories   | 1         | battery, power, bank, capacity, backup
Kitchen_Appliances   | 0         | mixer, grinder, blade, jar, motor, speed
...
"""

import pandas as pd

print("=" * 70)
print("CATEGORY-TOPIC KEYWORD SUMMARY")
print("=" * 70)
print()

# -----------------------------
# Configuration
# -----------------------------
INPUT_FILE = "category_wise_lda_output.csv"
OUTPUT_FILE = "category_topic_keywords.csv"

# -----------------------------
# Load Data
# -----------------------------
print("Loading data...")
try:
    df = pd.read_csv(INPUT_FILE)
    print(f"✅ Loaded {len(df)} records from {INPUT_FILE}")
    print()
except FileNotFoundError:
    print(f"❌ ERROR: File '{INPUT_FILE}' not found!")
    print()
    print("Please run 'category_lda_analysis.py' first to generate the data.")
    exit(1)

# Check required columns
required_cols = ["category", "lda_topic", "lda_topic_keywords"]
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    print(f"❌ ERROR: Missing required columns: {missing_cols}")
    print(f"Available columns: {list(df.columns)}")
    exit(1)

# -----------------------------
# Extract Unique Category-Topic Keywords
# -----------------------------
print("Extracting unique category-topic combinations...")

category_topic_keywords = (
    df.groupby(["category", "lda_topic"])["lda_topic_keywords"]
    .first()  # Get first instance (all same topic should have same keywords)
    .reset_index()
)

print(f"✅ Extracted {len(category_topic_keywords)} category-topic combinations")
print()

# -----------------------------
# Statistics
# -----------------------------
print("=" * 70)
print("SUMMARY STATISTICS")
print("=" * 70)
print()

num_categories = category_topic_keywords["category"].nunique()
topics_per_category = category_topic_keywords.groupby("category").size()

print(f"Total categories: {num_categories}")
print(f"Total category-topic pairs: {len(category_topic_keywords)}")
print(f"Average topics per category: {topics_per_category.mean():.1f}")
print()

# -----------------------------
# Display Sample Results
# -----------------------------
print("=" * 70)
print("SAMPLE CATEGORY-TOPIC MAPPINGS")
print("=" * 70)
print()

# Show topics for first 3 categories
for category in category_topic_keywords["category"].unique()[:3]:
    cat_topics = category_topic_keywords[
        category_topic_keywords["category"] == category
    ]
    
    print(f"Category: {category}")
    print(f"Topics discovered: {len(cat_topics)}")
    print()
    
    for _, row in cat_topics.iterrows():
        print(f"  Topic {row['lda_topic']}: {row['lda_topic_keywords']}")
    print()

# -----------------------------
# Category-wise Topic Count
# -----------------------------
print("=" * 70)
print("TOPICS PER CATEGORY")
print("=" * 70)
print()

category_topic_count = (
    category_topic_keywords.groupby("category")
    .size()
    .sort_values(ascending=False)
)

for category, count in category_topic_count.items():
    print(f"{category:<40} {count} topics")
print()

# -----------------------------
# Save Results
# -----------------------------
category_topic_keywords.to_csv(OUTPUT_FILE, index=False)

print("=" * 70)
print("RESULTS SAVED")
print("=" * 70)
print(f"✅ File saved as: {OUTPUT_FILE}")
print()

print("Output columns:")
print("  • category - Product category")
print("  • lda_topic - Topic ID (0 to N)")
print("  • lda_topic_keywords - Top keywords for this topic")
print()

# -----------------------------
# Full Dataset Preview
# -----------------------------
print("=" * 70)
print("FULL DATASET PREVIEW (First 15 rows)")
print("=" * 70)
print()

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 80)

print(category_topic_keywords.head(15).to_string(index=False))
print()

if len(category_topic_keywords) > 15:
    print(f"... and {len(category_topic_keywords) - 15} more rows")
    print()

# -----------------------------
# Use Cases
# -----------------------------
print("=" * 70)
print("💡 HOW TO USE THIS DATA")
print("=" * 70)
print()

print("1. Dashboard Creation:")
print("   - Display topics for each category")
print("   - Create interactive topic browsers")
print("   - Show keyword clouds per category")
print()

print("2. Customer Insights:")
print("   - Identify what customers discuss per category")
print("   - Find category-specific pain points")
print("   - Discover feature preferences")
print()

print("3. Product Strategy:")
print("   - Guide product development priorities")
print("   - Understand competitive landscape")
print("   - Track emerging trends per category")
print()

print("4. Content Analysis:")
print("   - Filter reviews by topic")
print("   - Analyze sentiment per topic")
print("   - Track topic evolution over time")
print()

print("5. Quality Assurance:")
print("   - Identify recurring issues (topics)")
print("   - Monitor quality-related topics")
print("   - Prioritize fixes by topic frequency")
print()

# -----------------------------
# Next Steps
# -----------------------------
print("=" * 70)
print("🎯 NEXT STEPS")
print("=" * 70)
print()

print("1. Combine with sentiment analysis:")
print("   - Analyze sentiment per category-topic")
print("   - Identify positive vs negative topics")
print()

print("2. Temporal analysis:")
print("   - Track topic trends over time")
print("   - Detect emerging or declining topics")
print()

print("3. Visualization:")
print("   - Create word clouds per topic")
print("   - Build interactive topic explorer")
print("   - Generate category-topic heatmaps")
print()

print("4. Advanced analysis:")
print("   - Correlate topics with ratings")
print("   - Build topic-based recommendation system")
print("   - Predict trending topics")
print()

print("=" * 70)
