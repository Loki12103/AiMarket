"""
Test RAG Queries Script
-----------------------
Tests multiple queries against the vector database to extract insights
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS index
vector_db = FAISS.load_local(
    "consumer_sentiment_faiss1",
    embeddings,
    allow_dangerous_deserialization=True
)

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("Gemini_Api_key"))


def query_rag(query, k=10):
    """
    Query the RAG system and get AI-generated response
    
    Args:
        query: The question to ask
        k: Number of similar documents to retrieve
    
    Returns:
        AI-generated answer based on retrieved context
    """
    print("\n" + "="*80)
    print(f"QUERY: {query}")
    print("="*80)
    
    # Similarity search
    results = vector_db.similarity_search(query, k=k)
    
    print(f"\nRetrieved {len(results)} relevant documents:")
    print("-"*80)
    
    # Collect retrieved documents
    retrieved_documents = []
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r.page_content[:200]}...")
        print(f"    Source: {r.metadata}")
        retrieved_documents.append(r.page_content)
    
    print("\n" + "-"*80)
    print("Generating AI response...")
    print("-"*80 + "\n")
    
    # Create prompt for Gemini
    prompt = f"""
You are a market intelligence analyst.

Using only the information from the provided context, give a response based on the question.

Do not use bullet points, headings, or sections.
Do not add external knowledge.

Context:
{retrieved_documents}

Question:
{query}

Answer:
"""
    
    # Get response from Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            temperature=0.2
        ),
    )
    
    print("ANSWER:")
    print(response.text)
    print("\n" + "="*80 + "\n")
    
    return response.text


# -----------------------------
# Test Queries
# -----------------------------
queries = [
    "why home appliance having good reviews",
    "Why are certain mobile accessory brands losing customer trust?",
    "Common complaints in mobile accessory reviews"
]

print("\n" + "="*80)
print("RAG QUERY TESTING - AI MARKET SENTIMENT ANALYSIS")
print("="*80)
print(f"Vector Database: consumer_sentiment_faiss1")
print(f"Total Queries: {len(queries)}")
print("="*80)

results = {}

for query in queries:
    try:
        answer = query_rag(query)
        results[query] = answer
    except Exception as e:
        print(f"❌ Error processing query '{query}': {e}\n")
        results[query] = f"Error: {e}"

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

for i, (query, answer) in enumerate(results.items(), 1):
    print(f"\n{i}. {query}")
    if answer.startswith("Error"):
        print(f"   ❌ {answer}")
    else:
        print(f"   ✅ Response generated successfully")

print("\n" + "="*80)
print("Testing complete!")
print("="*80)
