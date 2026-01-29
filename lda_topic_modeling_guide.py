"""
Topic Modeling with LDA - Complete Educational Guide
-----------------------------------------------------

WHAT IS TOPIC MODELING?
- Automatically discovers main themes in large text collections
- No manual reading required
- Finds patterns like "delivery issues", "camera quality", "battery problems"

WHY USE TOPIC MODELING?
1. Too much text - humans can't read everything (1000s of reviews)
2. Summarize massive datasets automatically
3. Understand customer pain points
4. Categorize text for further analysis
5. Useful for dashboards and business decisions
6. Unsupervised learning - discovers topics on its own
7. Converts messy text → structured insights

HOW LDA WORKS:
- Input: Collection of documents (reviews, articles, tweets)
- Process: Assumes each document is a mix of topics
- Output: Topics (word clusters) + Topic proportions per document

EXAMPLE OUTPUT:
Topic 1 (Battery Issues): battery, charging, power, drain
Topic 2 (Delivery): shipping, delivery, late, damaged
Topic 3 (Quality): quality, excellent, good, satisfied
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
import numpy as np

print("=" * 70)
print("TOPIC MODELING WITH LDA - EDUCATIONAL GUIDE")
print("=" * 70)
print()

# ============================================================================
# PART 1: SIMPLE EXAMPLE - Understanding the Basics
# ============================================================================

print("=" * 70)
print("PART 1: SIMPLE EXAMPLE - Step-by-Step Breakdown")
print("=" * 70)
print()

# -----------------------------
# STEP 1: Prepare Sample Documents
# -----------------------------
print("STEP 1: Sample Documents")
print("-" * 70)

documents = [
    "battery backup inverter power",
    "power inverter battery charging",
    "washing machine home appliance",
    "refrigerator cooling appliance",
    "mobile phone charger cable",
    "smartphone battery charging"
]

print("Our sample documents (product-related text):")
for i, doc in enumerate(documents):
    print(f"  Doc {i+1}: {doc}")
print()
print("Goal: Automatically group these into 2 main topics")
print()

# -----------------------------
# STEP 2: Convert Text to Numbers (Vectorization)
# -----------------------------
print("STEP 2: Convert Text to Numbers")
print("-" * 70)

vectorizer = CountVectorizer(stop_words="english")
doc_term_matrix = vectorizer.fit_transform(documents)

print("What CountVectorizer does:")
print("  ✓ Removes common English stopwords (is, the, and, etc.)")
print("  ✓ Builds vocabulary of important words")
print("  ✓ Creates Document-Term Matrix (counts word occurrences)")
print()

print(f"Vocabulary created: {vectorizer.get_feature_names_out()}")
print(f"Matrix shape: {doc_term_matrix.shape} (6 documents × {doc_term_matrix.shape[1]} words)")
print()

# Display the matrix
print("Document-Term Matrix (first 3 docs, first 5 words):")
df_matrix = pd.DataFrame(
    doc_term_matrix.toarray(),
    columns=vectorizer.get_feature_names_out()
)
print(df_matrix.iloc[:3, :5])
print()

# -----------------------------
# STEP 3: Create LDA Model
# -----------------------------
print("STEP 3: Create LDA Model")
print("-" * 70)

lda = LatentDirichletAllocation(
    n_components=2,   # number of topics to discover
    random_state=42   # ensures reproducible results
)

print("LDA Configuration:")
print(f"  n_components = 2  → We want to discover 2 topics")
print(f"  random_state = 42 → Ensures same output every time")
print()

# -----------------------------
# STEP 4: Train the Model
# -----------------------------
print("STEP 4: Train the LDA Model")
print("-" * 70)

lda.fit(doc_term_matrix)

print("Training complete! LDA has learned:")
print("  ✓ Which words frequently appear together")
print("  ✓ How to group documents into topics")
print("  ✓ Word importance for each topic")
print()

# -----------------------------
# STEP 5: Extract Topics
# -----------------------------
print("STEP 5: Extract and Display Topics")
print("-" * 70)

words = vectorizer.get_feature_names_out()

print("Discovered Topics:\n")
for topic_id, topic in enumerate(lda.components_):
    # Get indices of top 5 words
    top_indices = topic.argsort()[-5:][::-1]
    top_words = [words[i] for i in top_indices]
    top_scores = [topic[i] for i in top_indices]
    
    print(f"Topic {topic_id}:")
    print(f"  Keywords: {', '.join(top_words)}")
    print(f"  Scores:   {', '.join([f'{s:.3f}' for s in top_scores])}")
    print()

print("Interpretation:")
print("  Topic 0 likely represents: POWER/BATTERY PRODUCTS")
print("  Topic 1 likely represents: HOME APPLIANCES")
print()

# -----------------------------
# STEP 6: Document-Topic Distribution
# -----------------------------
print("STEP 6: Assign Topics to Documents")
print("-" * 70)

doc_topic_dist = lda.transform(doc_term_matrix)

print("Each document's topic distribution:\n")
for i, dist in enumerate(doc_topic_dist):
    dominant_topic = dist.argmax()
    confidence = dist.max()
    print(f"Doc {i+1}: {documents[i]}")
    print(f"  → Topic 0: {dist[0]:.2%} | Topic 1: {dist[1]:.2%}")
    print(f"  → Dominant Topic: {dominant_topic} (confidence: {confidence:.2%})")
    print()

print()

# ============================================================================
# PART 2: ADVANCED EXAMPLE - Real-World Application
# ============================================================================

print("=" * 70)
print("PART 2: ADVANCED EXAMPLE - Product Review Analysis")
print("=" * 70)
print()

# Larger, more realistic dataset
advanced_documents = [
    "excellent product good quality fast delivery very satisfied",
    "battery drains quickly charging issues power problem",
    "price too high expensive not worth money",
    "camera quality amazing photos clear beautiful pictures",
    "delivery delayed package arrived late damaged box",
    "screen broke easily poor build quality materials cheap",
    "customer service helpful responsive quick support excellent",
    "battery backup excellent lasts long time power",
    "sound quality poor audio disappointing speakers bad",
    "great value money affordable good features price",
    "heating issues overheating phone gets hot problem",
    "shipping fast arrived early well packaged perfect",
    "software buggy crashes frequently freezes often terrible",
    "display bright vibrant colors screen excellent beautiful",
    "build quality premium feels solid sturdy durable",
    "charger stopped working cable broke quickly poor",
    "performance smooth fast responsive good speed excellent",
    "design beautiful elegant looks premium attractive",
    "warranty claim easy replacement process smooth helpful",
    "fingerprint sensor works perfectly accurate fast reliable",
    "value disappointed waste money regret purchase bad",
    "arrived broken damaged shipping terrible package poor",
    "love product amazing best purchase ever excellent",
    "slow laggy performance terrible disappointing speed",
    "recommended friends family excellent product quality"
]

print(f"Analyzing {len(advanced_documents)} product reviews")
print()

# Vectorization with better parameters
print("Step 1: Vectorization with advanced settings")
print("-" * 70)

vectorizer_adv = CountVectorizer(
    stop_words="english",
    max_features=50,      # Keep top 50 words only
    min_df=2,             # Word must appear in at least 2 documents
    max_df=0.8            # Ignore words in >80% of documents
)

doc_term_matrix_adv = vectorizer_adv.fit_transform(advanced_documents)

print(f"✓ Vocabulary size: {len(vectorizer_adv.get_feature_names_out())} words")
print(f"✓ Matrix shape: {doc_term_matrix_adv.shape}")
print(f"✓ Top words: {list(vectorizer_adv.get_feature_names_out()[:10])}")
print()

# LDA with more topics
print("Step 2: LDA with 5 topics")
print("-" * 70)

n_topics = 5
lda_adv = LatentDirichletAllocation(
    n_components=n_topics,
    max_iter=30,
    learning_method='online',
    random_state=42
)

lda_adv.fit(doc_term_matrix_adv)
print("✓ Model trained successfully")
print()

# Display topics with interpretations
print("Step 3: Discovered Topics")
print("-" * 70)
print()

words_adv = vectorizer_adv.get_feature_names_out()

# Map to store topic interpretations
topic_names = []

for topic_id, topic in enumerate(lda_adv.components_):
    top_indices = topic.argsort()[-8:][::-1]
    top_words = [words_adv[i] for i in top_indices]
    
    print(f"Topic {topic_id + 1}:")
    print(f"  Keywords: {', '.join(top_words)}")
    
    # Auto-interpret topic
    if any(word in top_words for word in ['battery', 'charging', 'power']):
        interpretation = "Battery & Power Issues"
    elif any(word in top_words for word in ['delivery', 'shipping', 'arrived', 'package']):
        interpretation = "Delivery & Shipping"
    elif any(word in top_words for word in ['quality', 'excellent', 'good', 'premium']):
        interpretation = "Product Quality & Satisfaction"
    elif any(word in top_words for word in ['price', 'expensive', 'money', 'value']):
        interpretation = "Price & Value"
    elif any(word in top_words for word in ['poor', 'bad', 'terrible', 'disappointing']):
        interpretation = "Negative Experiences"
    else:
        interpretation = "General Features"
    
    topic_names.append(interpretation)
    print(f"  Interpretation: {interpretation}")
    print()

# Assign topics to documents
print("Step 4: Topic Assignment")
print("-" * 70)
print()

doc_topic_dist_adv = lda_adv.transform(doc_term_matrix_adv)

# Create results dataframe
results_df = pd.DataFrame({
    'review': advanced_documents,
    'dominant_topic': doc_topic_dist_adv.argmax(axis=1),
    'confidence': doc_topic_dist_adv.max(axis=1)
})

# Add topic name
results_df['topic_name'] = results_df['dominant_topic'].apply(lambda x: topic_names[x])

# Show sample results
print("Sample Topic Assignments:\n")
for idx, row in results_df.head(10).iterrows():
    print(f"Review: {row['review'][:60]}...")
    print(f"  → Topic: {row['topic_name']} (confidence: {row['confidence']:.2%})")
    print()

# Topic distribution
print("=" * 70)
print("TOPIC DISTRIBUTION SUMMARY")
print("=" * 70)
print()

topic_counts = results_df['topic_name'].value_counts()
for topic, count in topic_counts.items():
    percentage = (count / len(results_df)) * 100
    print(f"{topic:.<40} {count:>3} reviews ({percentage:>5.1f}%)")
print()

# Save results
output_file = "lda_topic_modeling_results.csv"
results_df.to_csv(output_file, index=False)
print(f"✅ Results saved to: {output_file}")
print()

# ============================================================================
# BUSINESS INSIGHTS
# ============================================================================

print("=" * 70)
print("💡 BUSINESS INSIGHTS & APPLICATIONS")
print("=" * 70)
print()

print("1. CUSTOMER PAIN POINTS:")
print("   - Identify topics with highest negative sentiment")
print("   - Track frequency of complaint topics")
print("   - Prioritize fixes for most-discussed issues")
print()

print("2. PRODUCT IMPROVEMENTS:")
print("   - Focus on topics customers care about most")
print("   - Understand feature satisfaction levels")
print("   - Guide product development roadmap")
print()

print("3. TREND ANALYSIS:")
print("   - Track topic popularity over time")
print("   - Detect emerging issues early")
print("   - Monitor seasonal patterns")
print()

print("4. MARKETING INSIGHTS:")
print("   - Highlight features customers praise")
print("   - Address common concerns in marketing")
print("   - Create targeted campaigns per topic")
print()

print("5. CUSTOMER SEGMENTATION:")
print("   - Group customers by topics they discuss")
print("   - Personalize responses per segment")
print("   - Tailor products to different groups")
print()

print("=" * 70)
print("🎯 NEXT STEPS")
print("=" * 70)
print()
print("1. Combine topic modeling with sentiment analysis")
print("2. Analyze topic trends over time (add timestamps)")
print("3. Create topic-based dashboards and visualizations")
print("4. Fine-tune number of topics (try 3, 5, 7, 10)")
print("5. Use for automated review categorization")
print("6. Build topic-based recommendation systems")
print()
print("=" * 70)
print("📚 KEY TAKEAWAYS")
print("=" * 70)
print()
print("✓ LDA automatically discovers hidden topics in text")
print("✓ No manual labeling required (unsupervised)")
print("✓ Converts unstructured text → structured insights")
print("✓ Essential for analyzing large text datasets")
print("✓ Perfect for customer feedback analysis")
print("=" * 70)
