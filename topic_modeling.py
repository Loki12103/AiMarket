"""
Topic Modeling with LDA (Latent Dirichlet Allocation)
------------------------------------------------------
Automatically discovers main themes/topics in text data without manual labeling.

What is Topic Modeling?
- Unsupervised learning technique
- Finds hidden patterns in large text collections
- Groups words that frequently appear together

Why Use Topic Modeling?
1. Analyze massive text datasets automatically
2. Discover customer pain points and preferences
3. Categorize text for further analysis
4. Convert unstructured text → structured insights
5. Track trends and emerging topics over time

How LDA Works:
- Assumes each document is a mixture of topics
- Each topic is a mixture of words
- Mathematically finds word-topic relationships

Example Output:
Topic 1 (Battery Issues): battery, charging, power, drain, overheating
Topic 2 (Delivery): shipping, delivery, late, damaged, package
Topic 3 (Quality): quality, excellent, good, satisfied, recommend
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
import numpy as np

print("=" * 60)
print("TOPIC MODELING WITH LDA")
print("=" * 60)
print()

# -----------------------------
# EXAMPLE 1: Simple Topic Modeling
# -----------------------------
print("=" * 60)
print("EXAMPLE 1: Basic Topic Discovery")
print("=" * 60)
print()

# Sample documents
documents = [
    "battery backup inverter power",
    "power inverter battery charging",
    "washing machine home appliance",
    "refrigerator cooling appliance",
    "mobile phone charger cable",
    "smartphone battery charging"
]

print("Sample Documents:")
for i, doc in enumerate(documents, 1):
    print(f"{i}. {doc}")
print()

# Convert text to numbers (Bag of Words)
vectorizer = CountVectorizer(stop_words="english")
doc_term_matrix = vectorizer.fit_transform(documents)

print(f"Document-Term Matrix Shape: {doc_term_matrix.shape}")
print(f"Vocabulary Size: {len(vectorizer.get_feature_names_out())}")
print()

# LDA Model
lda = LatentDirichletAllocation(
    n_components=2,   # number of topics
    random_state=42,
    max_iter=20
)
lda.fit(doc_term_matrix)

print("Discovered Topics:")
print("-" * 60)

words = vectorizer.get_feature_names_out()
for topic_id, topic in enumerate(lda.components_):
    top_words = [words[i] for i in topic.argsort()[-5:]]
    print(f"Topic {topic_id}: {', '.join(top_words)}")
print()

# -----------------------------
# EXAMPLE 2: Topic Modeling on Real Data
# -----------------------------
print("=" * 60)
print("EXAMPLE 2: Product Review Topic Modeling")
print("=" * 60)
print()

# Try to load actual review data
try:
    # Attempt to load cleaned review data
    df = pd.read_csv("combined_cleaned_data.csv").head(500)  # Use first 500 reviews
    text_column = "cleaned_text"
    
    print(f"✅ Loaded {len(df)} reviews")
    print()
    
except FileNotFoundError:
    # Fallback to sample data
    print("⚠️ No review data found. Using sample data.")
    print()
    
    df = pd.DataFrame({
        "cleaned_text": [
            "excellent product good quality fast delivery very satisfied",
            "battery drains quickly charging issues power problem",
            "price too high expensive not worth money",
            "camera quality amazing photos clear beautiful pictures",
            "delivery delayed package arrived late damaged box",
            "screen broke easily poor build quality materials",
            "customer service helpful responsive quick support",
            "battery backup excellent lasts long time",
            "sound quality poor audio disappointing speakers",
            "great value money affordable good features",
            "heating issues overheating phone gets hot",
            "shipping fast arrived early well packaged",
            "software buggy crashes frequently freezes often",
            "display bright vibrant colors screen excellent",
            "build quality premium feels solid sturdy",
            "charger stopped working cable broke quickly",
            "performance smooth fast responsive good speed",
            "design beautiful elegant looks premium",
            "warranty claim easy replacement process smooth",
            "fingerprint sensor works perfectly accurate fast"
        ] * 25  # Repeat to get 500 samples
    })
    text_column = "cleaned_text"

# Clean and prepare text
df[text_column] = df[text_column].fillna("").astype(str)

# Remove very short reviews
df = df[df[text_column].str.len() > 10]

print(f"Reviews to analyze: {len(df)}")
print()

# -----------------------------
# Vectorization
# -----------------------------
print("Creating document-term matrix...")
vectorizer_real = CountVectorizer(
    max_features=1000,      # Top 1000 words
    stop_words="english",   # Remove common words
    min_df=2,               # Word must appear in at least 2 documents
    max_df=0.8              # Ignore words in >80% of documents
)

doc_term_matrix_real = vectorizer_real.fit_transform(df[text_column])
print(f"✅ Matrix shape: {doc_term_matrix_real.shape}")
print()

# -----------------------------
# LDA Topic Modeling
# -----------------------------
print("Running LDA topic modeling...")
n_topics = 5  # Adjust based on your needs

lda_real = LatentDirichletAllocation(
    n_components=n_topics,
    random_state=42,
    max_iter=30,
    learning_method='online',
    n_jobs=-1  # Use all CPU cores
)

lda_real.fit(doc_term_matrix_real)
print("✅ LDA model trained")
print()

# -----------------------------
# Display Discovered Topics
# -----------------------------
print("=" * 60)
print("DISCOVERED TOPICS")
print("=" * 60)
print()

feature_names = vectorizer_real.get_feature_names_out()

for topic_idx, topic in enumerate(lda_real.components_):
    top_word_indices = topic.argsort()[-10:][::-1]  # Top 10 words
    top_words = [feature_names[i] for i in top_word_indices]
    
    print(f"Topic {topic_idx + 1}:")
    print(f"  Keywords: {', '.join(top_words)}")
    print()

# -----------------------------
# Assign Topics to Documents
# -----------------------------
print("=" * 60)
print("TOPIC DISTRIBUTION IN DOCUMENTS")
print("=" * 60)
print()

# Transform documents to topic space
doc_topic_dist = lda_real.transform(doc_term_matrix_real)

# Assign dominant topic to each document
df['dominant_topic'] = doc_topic_dist.argmax(axis=1)
df['topic_confidence'] = doc_topic_dist.max(axis=1)

# Show distribution
print("Topic Distribution:")
print(df['dominant_topic'].value_counts().sort_index())
print()

# -----------------------------
# Show Sample Documents per Topic
# -----------------------------
print("=" * 60)
print("SAMPLE DOCUMENTS PER TOPIC")
print("=" * 60)
print()

for topic_id in range(n_topics):
    topic_docs = df[df['dominant_topic'] == topic_id].head(3)
    
    if len(topic_docs) > 0:
        print(f"\nTopic {topic_id + 1} Examples:")
        print("-" * 60)
        for idx, row in topic_docs.iterrows():
            print(f"  • {row[text_column][:100]}...")
            print(f"    Confidence: {row['topic_confidence']:.3f}")
        print()

# -----------------------------
# Topic Statistics
# -----------------------------
print("=" * 60)
print("TOPIC STATISTICS")
print("=" * 60)
print()

for topic_id in range(n_topics):
    topic_docs = df[df['dominant_topic'] == topic_id]
    avg_confidence = topic_docs['topic_confidence'].mean() if len(topic_docs) > 0 else 0
    
    print(f"Topic {topic_id + 1}:")
    print(f"  Documents: {len(topic_docs)}")
    print(f"  Avg Confidence: {avg_confidence:.3f}")
    print()

# -----------------------------
# Save Results
# -----------------------------
output_file = "topic_modeling_results.csv"
df.to_csv(output_file, index=False)
print(f"✅ Results saved to: {output_file}")
print()

# -----------------------------
# Business Insights
# -----------------------------
print("=" * 60)
print("💡 HOW TO USE THESE TOPICS")
print("=" * 60)
print()
print("1. Customer Pain Points Analysis:")
print("   - Identify topics with negative sentiment")
print("   - Track which issues appear most frequently")
print()
print("2. Product Feature Insights:")
print("   - See what features customers discuss most")
print("   - Understand what drives satisfaction")
print()
print("3. Trend Analysis:")
print("   - Track topic popularity over time")
print("   - Detect emerging issues or trends")
print()
print("4. Targeted Improvements:")
print("   - Focus on high-frequency problem topics")
print("   - Prioritize features customers care about")
print()
print("5. Content Categorization:")
print("   - Automatically tag reviews by topic")
print("   - Create topic-specific dashboards")
print("=" * 60)
print()
print("💡 NEXT STEPS:")
print("=" * 60)
print("1. Combine with sentiment analysis per topic")
print("2. Analyze topic trends over time")
print("3. Create visualizations (word clouds, topic networks)")
print("4. Tune number of topics (try 3, 5, 7, 10)")
print("5. Use for customer feedback prioritization")
print("=" * 60)
