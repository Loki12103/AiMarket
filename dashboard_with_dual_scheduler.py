import streamlit as st
import pandas as pd
import plotly.express as px

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from google import genai
from google.genai import types
from groq import Groq
import os
from dotenv import load_dotenv
import schedule
import threading
import time

load_dotenv()

# ============= DUAL SCHEDULER SYSTEM =============
# 1. Daily News Collection at 21:32
# 2. Weekly Full Automation (Monday 00:00)

import news
from weekly_automation import run_weekly_automation


def run_dual_scheduler():
    """
    Runs both schedulers:
    - Daily news collection
    - Weekly full automation
    """
    # Daily news collection at 21:32
    schedule.every().day.at("21:32").do(news.get_news_data)
    
    # Weekly full automation (Monday at 00:00)
    schedule.every().monday.at("00:00").do(run_weekly_automation)
    
    # For testing - uncomment one of these:
    # schedule.every(30).seconds.do(news.get_news_data)  # Test news every 30s
    # schedule.every(5).minutes.do(run_weekly_automation)  # Test automation every 5 min
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


# Start scheduler in background thread
if "scheduler_started" not in st.session_state:
    threading.Thread(target=run_dual_scheduler, daemon=True).start()
    st.session_state.scheduler_started = True
    st.session_state.news_schedule = "Daily at 21:32"
    st.session_state.automation_schedule = "Weekly (Monday 00:00)"

# ==================================================

# Page config
st.set_page_config(
    page_title="AI Market Trend & Consumer Sentiment Forecaster",
    layout="wide"
)

st.title("AI-Powered Market Trend & Consumer Sentiment Dashboard")
st.markdown("Consumer sentiment, topic trend, and social insights from reviews, news, and Reddit data")


# Load data
@st.cache_data
def load_data():
    reviews = pd.read_csv("datasets/final data/category_wise_lda_output_with_topic_labels.csv")
    reddit = pd.read_excel("datasets/final data/reddit_category_trend_data.xlsx")
    news_df = pd.read_csv("datasets/final data/news_data_with_sentiment.csv")
    
    # Convert dates
    if "review_date" in reviews.columns:
        reviews["review_date"] = pd.to_datetime(
            reviews["review_date"], errors="coerce"
        )
    
    if "published_at" in news_df.columns:
        news_df["published_at"] = pd.to_datetime(
            news_df["published_at"], errors="coerce"
        )
    
    if "created_date" in reddit.columns:
        reddit["created_date"] = pd.to_datetime(
            reddit["created_date"], errors="coerce"
        )
    
    return reviews, reddit, news_df


reviews_df, reddit_df, news_df = load_data()


# Load vector database
@st.cache_resource
def load_vector_db():
    """Load FAISS vector database for AI Q&A"""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        vector_db = FAISS.load_local(
            "consumer_sentiment_faiss1",
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        return vector_db
    except Exception as e:
        st.warning(f"⚠️ Vector database not found. AI Insight Panel disabled. Run 'python create_vector_db.py' to enable it.")
        return None


vector_db = load_vector_db()


# Load Gemini client
@st.cache_resource
def load_gemini_client():
    return genai.Client(api_key=os.getenv("Gemini_Api_key"))

# Load Groq client
@st.cache_resource
def load_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


gemini_client = load_gemini_client()
groq_client = load_groq_client()


# Create two-column layout
main_col, right_sidebar = st.columns([3, 1])

with main_col:
    # Sidebar filters
    st.sidebar.header("Filters")
    
    source_filter = st.sidebar.multiselect(
        "Select Source",
        options=reviews_df["source"].unique(),
        default=reviews_df["source"].unique()
    )
    
    category_filter = st.sidebar.multiselect(
        "Select Category",
        options=reviews_df["category"].unique(),
        default=reviews_df["category"].unique()
    )
    
    filtered_reviews = reviews_df[
        (reviews_df["source"].isin(source_filter)) &
        (reviews_df["category"].isin(category_filter))
    ]
    
    # KPI Metrics
    st.subheader("Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Reviews", len(filtered_reviews))
    col2.metric("Positive %", round((filtered_reviews["sentiment_label"] == "Positive").mean() * 100, 1))
    col3.metric("Negative %", round((filtered_reviews["sentiment_label"] == "Negative").mean() * 100, 1))
    col4.metric("Neutral %", round((filtered_reviews["sentiment_label"] == "Neutral").mean() * 100, 1))
    
    # Sentiment distribution
    col1, col2 = st.columns(2)
    
    with col1:
        sentiment_dist = filtered_reviews["sentiment_label"].value_counts().reset_index()
        sentiment_dist.columns = ["Sentiment", "Count"]
        
        fig = px.pie(
            sentiment_dist,
            names="Sentiment",
            values="Count",
            title="Overall Sentiment Distribution",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        category_sentiment = (
            filtered_reviews.groupby(["category", "sentiment_label"]).size().reset_index(name="count")
        )
        
        fig = px.bar(
            category_sentiment,
            x="category",
            y="count",
            color="sentiment_label",
            title="Category-wise Sentiment Comparison",
            barmode="group"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Sentiment trend over time
    st.subheader("Sentiment Trend Over Time")
    
    sentiment_trend = (
        filtered_reviews.groupby([pd.Grouper(key="review_date", freq="W"), "sentiment_label"])
        .size()
        .reset_index(name="count")
    )
    
    fig_trend = px.line(
        sentiment_trend,
        x="review_date",
        y="count",
        color="sentiment_label",
        title="Weekly Sentiment Trend"
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Category trend over time
    st.subheader("Category Trend Over Time (Product Demand)")
    
    category_trend = (
        filtered_reviews.groupby([pd.Grouper(key="review_date", freq="M"), "category"])
        .size()
        .reset_index(name="count")
    )
    
    fig_category_trend = px.line(
        category_trend,
        x="review_date",
        y="count",
        color="category",
        title="Monthly Category Demand Trend"
    )
    
    st.plotly_chart(fig_category_trend, use_container_width=True)
    
    # Category-wise Sentiment Distribution
    st.subheader("Category-wise Sentiment Distribution")
    
    cat_sent = (
        filtered_reviews
        .groupby(["category", "sentiment_label"])
        .size()
        .reset_index(name="count")
    )
    
    fig_cat = px.bar(
        cat_sent,
        x="category",
        y="count",
        color="sentiment_label",
        barmode="group"
    )
    
    st.plotly_chart(fig_cat, use_container_width=True)
    
    # Topic distribution
    st.subheader("Topic Insights")
    
    topic_dist = (
        filtered_reviews["topic_label"]
        .value_counts()
        .reset_index()
    )
    
    topic_dist.columns = ["Topic", "Count"]
    
    fig_topic = px.bar(
        topic_dist,
        x="Topic",
        y="Count",
        title="Topic Distribution"
    )
    
    st.plotly_chart(fig_topic, use_container_width=True)
    
    # Reddit category trend
    st.subheader("Reddit Category Popularity")
    
    reddit_trend = (
        reddit_df
        .groupby("category_label")
        .size()
        .reset_index(name="mentions")
        .sort_values("mentions", ascending=False)
    )
    
    fig_reddit = px.bar(
        reddit_trend,
        x="category_label",
        y="mentions",
        title="Trending categories on Reddit"
    )
    
    st.plotly_chart(fig_reddit, use_container_width=True)
    
    # News sentiment
    st.subheader("News Sentiment Overview")
    
    news_sent = (
        news_df
        .groupby("sentiment_label")
        .size()
        .reset_index(name="count")
    )
    
    fig_news = px.pie(
        news_sent,
        names="sentiment_label",
        values="count",
        title="News Sentiment distribution"
    )
    
    st.plotly_chart(fig_news, use_container_width=True)
    
    # Cross-Source Category Comparison
    st.subheader("Cross-Source Category Comparison")
    
    # Review category count
    review_cat = (
        reviews_df
        .groupby("category")
        .size()
        .reset_index(name="Review Mentions")
    )
    
    # Reddit category count
    reddit_cat = (
        reddit_df
        .groupby("category_label")
        .size()
        .reset_index(name="Reddit Mentions")
        .rename(columns={"category_label": "category"})
    )
    
    # News category count
    news_cat = (
        news_df
        .groupby("category")
        .size()
        .reset_index(name="News Mentions")
    )
    
    # Merge all
    category_compare = review_cat\
        .merge(reddit_cat, on="category", how="outer")\
        .merge(news_cat, on="category", how="outer")\
        .fillna(0)
    
    fig_compare = px.bar(
        category_compare,
        x="category",
        y=["Review Mentions", "Reddit Mentions", "News Mentions"],
        title="Category Presence Across Reviews, Reddit and News",
        barmode="group"
    )
    
    st.plotly_chart(fig_compare, use_container_width=True)
    
    st.dataframe(category_compare)

with right_sidebar:
    st.markdown("## 🤖 AI Insight Panel")
    st.caption("Ask questions using reviews, news, & Reddit data")
    
    if vector_db is None:
        st.error("❌ AI Insight Panel Unavailable")
        st.info("Run this command to enable AI Q&A:\n\n`python create_vector_db.py`")
    else:
        user_query = st.text_area(
            "Your Question",
            height=140,
            placeholder="e.g., What are customers saying about electronics?"
        )
        
        ask_btn = st.button("Get Insight", use_container_width=True)
        
        if ask_btn and user_query:
            with st.spinner("Analyzing Market Intelligence..."):
                # Retrieve relevant documents from vector database
                results = vector_db.similarity_search(user_query, k=10)
                retrieved_docs = [r.page_content for r in results]
                
                # Create prompt for Gemini/Groq
                prompt = f"""
You are a market intelligence analyst.

Using only the information from the provided context, give a response based on the question.

Do not use bullet points, headings, or sections.
Do not add external knowledge.

Context:
{retrieved_docs}

Question:
{user_query}

Answer:
"""
                
                # Try Gemini first, fallback to Groq if it fails
                try:
                    # Generate response using Gemini
                    response = gemini_client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            thinking_config=types.ThinkingConfig(thinking_budget=0),
                            temperature=0.2
                        ),
                    )
                    response_text = response.text
                    st.info("🤖 Powered by Gemini")
                    
                except Exception as gemini_error:
                    st.warning(f"⚠️ Gemini unavailable, switching to Groq... ({str(gemini_error)[:50]})")
                    try:
                        # Fallback to Groq
                        groq_response = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "You are a market intelligence analyst. Use only the provided context to answer questions."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.2,
                            max_tokens=1024
                        )
                        response_text = groq_response.choices[0].message.content
                        st.info("🤖 Powered by Groq (Llama 3.3)")
                        
                    except Exception as groq_error:
                        st.error(f"❌ Both Gemini and Groq failed: {str(groq_error)}")
                        response_text = None
            
            if response_text:
                st.success("Insight Generated")
                st.write(response_text)


# ============= AUTOMATION STATUS PANEL =============
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Automation Status")

if st.session_state.get("scheduler_started"):
    st.sidebar.success("✓ Dual Scheduler Active")
    
    # Show schedules
    st.sidebar.caption(f"📰 News: {st.session_state.news_schedule}")
    st.sidebar.caption(f"🔄 Full Automation: {st.session_state.automation_schedule}")
    
    # Details expander
    with st.sidebar.expander("ℹ️ What runs automatically?"):
        st.markdown("""
        **Daily News Collection (21:32):**
        - 📰 Fetch latest tech news
        - 📧 Email notification
        - 💾 Save to CSV
        
        **Weekly Automation (Mon 00:00):**
        - 📊 Collect all data sources
        - 🔍 Sentiment spike detection
        - 📈 Trend shift detection
        - 📧 Multiple email alerts
        """)
else:
    st.sidebar.error("✗ Scheduler Not Running")

# Manual triggers
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)

if col1.button("📰 News Now", use_container_width=True):
    with st.spinner("Collecting news..."):
        result = news.get_news_data()
    
    if result is not None:
        st.sidebar.success(f"✓ Collected {len(result)} articles!")
    else:
        st.sidebar.error("✗ News collection failed")

if col2.button("🔄 Full Run", use_container_width=True):
    with st.spinner("Running full automation..."):
        result = run_weekly_automation()
    
    if result:
        st.sidebar.success("✓ Automation completed!")
        st.sidebar.info("Check your email for report")
    else:
        st.sidebar.error("✗ Automation failed")
