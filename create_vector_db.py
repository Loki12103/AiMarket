"""
Create FAISS Vector Database for AI Insight Panel
--------------------------------------------------
Builds vector database from reviews, news, and Reddit data
"""

import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

print("="*60)
print("CREATING FAISS VECTOR DATABASE")
print("="*60)
print()

# Load data
print("1. Loading data...")
reviews = pd.read_csv("datasets/final data/category_wise_lda_output_with_topic_labels.csv")
news = pd.read_csv("datasets/final data/news_data_with_sentiment.csv")
reddit = pd.read_excel("datasets/final data/reddit_category_trend_data.xlsx")

print(f"   ✓ Reviews: {len(reviews)} records")
print(f"   ✓ News: {len(news)} records")
print(f"   ✓ Reddit: {len(reddit)} records")
print()

# Create documents
print("2. Creating documents...")
documents = []

# Add reviews
for _, row in reviews.iterrows():
    text = f"""
Category: {row.get('category', 'Unknown')}
Source: {row.get('source', 'Review')}
Sentiment: {row.get('sentiment_label', 'Unknown')}
Topic: {row.get('topic_label', 'Unknown')}
Review: {row.get('review_text', '')}
"""
    documents.append(Document(page_content=text.strip()))

# Add news
for _, row in news.iterrows():
    text = f"""
Category: {row.get('category', 'Unknown')}
Source: News - {row.get('source', 'Unknown')}
Sentiment: {row.get('sentiment_label', 'Unknown')}
Title: {row.get('title', '')}
Description: {row.get('description', '')}
"""
    documents.append(Document(page_content=text.strip()))

# Add Reddit posts
for _, row in reddit.iterrows():
    text = f"""
Category: {row.get('category_label', 'Unknown')}
Source: Reddit
Title: {row.get('title', '')}
Text: {row.get('selftext', '')}
"""
    documents.append(Document(page_content=text.strip()))

print(f"   ✓ Created {len(documents)} documents")
print()

# Create embeddings
print("3. Loading embedding model (this may take a while)...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print("   ✓ Model loaded")
print()

# Create FAISS index
print("4. Building FAISS vector database...")
print("   (This may take several minutes depending on data size)")
vector_db = FAISS.from_documents(documents, embeddings)
print("   ✓ Vector database created")
print()

# Save to disk
print("5. Saving vector database...")
vector_db.save_local("consumer_sentiment_faiss1")
print("   ✓ Saved to: consumer_sentiment_faiss1/")
print()

print("="*60)
print("✅ VECTOR DATABASE CREATED SUCCESSFULLY!")
print("="*60)
print()
print("You can now use the AI Insight Panel in the dashboard.")
print("Run: streamlit run dashboard_with_dual_scheduler.py")
