"""
AI Market Trend & Consumer Sentiment Dashboard
-----------------------------------------------

Interactive dashboard for analyzing:
- Product review sentiment
- Topic trends across categories
- Social media insights (Reddit)
- News sentiment analysis

Features:
- Multi-source filtering
- Category-based analysis
- Sentiment distribution & trends
- Time-based visualizations

Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="AI Market Trend & Consumer Sentiment Forecaster",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<h1 class="main-title">📊 AI-Powered Market Trend & Consumer Sentiment Dashboard</h1>', unsafe_allow_html=True)
st.markdown("##### 📈 Consumer sentiment, topic trends, and social insights from reviews, news, and Reddit data")
st.markdown("---")

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    """Load and preprocess all datasets"""
    try:
        # Load reviews data
        reviews = pd.read_csv("final data/category_wise_lda_output_with_topic_labels.csv")
        st.sidebar.success("✅ Reviews data loaded")
    except FileNotFoundError:
        st.sidebar.error("❌ Reviews data not found")
        reviews = pd.DataFrame()
    
    try:
        # Load Reddit data
        reddit = pd.read_excel("final data/reddit_category_trend_data.xlsx")
        st.sidebar.success("✅ Reddit data loaded")
    except FileNotFoundError:
        st.sidebar.warning("⚠️ Reddit data not found")
        reddit = pd.DataFrame()
    
    try:
        # Load news data
        news = pd.read_csv("final data/news_data_with_sentiment.csv")
        st.sidebar.success("✅ News data loaded")
    except FileNotFoundError:
        st.sidebar.warning("⚠️ News data not found")
        news = pd.DataFrame()
    
    # Convert date columns
    if "review_date" in reviews.columns:
        reviews["review_date"] = pd.to_datetime(
            reviews["review_date"], errors="coerce"  # Convert invalid dates to NaT
        )
    
    if "published_at" in news.columns:
        news["published_at"] = pd.to_datetime(
            news["published_at"], errors="coerce"  # Convert invalid dates to NaT
        )
    
    if "created_date" in reddit.columns:
        reddit["created_date"] = pd.to_datetime(
            reddit["created_date"], errors="coerce"  # Convert invalid dates to NaT
        )
    
    return reviews, reddit, news

# Load data with error handling
with st.spinner("Loading data..."):
    reviews_df, reddit_df, news_df = load_data()

# Check if data loaded successfully
if reviews_df.empty:
    st.error("❌ Unable to load reviews data. Please ensure 'final data/category_wise_lda_output_with_topic_labels.csv' exists.")
    st.stop()

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.title("⚙️ Filters")
st.sidebar.markdown("---")

# Source filter
if "source" in reviews_df.columns:
    source_options = reviews_df["source"].unique().tolist()
    source_filter = st.sidebar.multiselect(
        "📦 Select Source",
        options=source_options,
        default=source_options
    )
else:
    source_filter = []
    st.sidebar.warning("⚠️ No 'source' column found")

# Category filter
if "category" in reviews_df.columns:
    category_options = reviews_df["category"].unique().tolist()
    category_filter = st.sidebar.multiselect(
        "🏷️ Select Category",
        options=category_options,
        default=category_options[:5] if len(category_options) > 5 else category_options
    )
else:
    category_filter = []
    st.sidebar.warning("⚠️ No 'category' column found")

# Date range filter (if available)
if "review_date" in reviews_df.columns and reviews_df["review_date"].notna().any():
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Date Range")
    
    min_date = reviews_df["review_date"].min()
    max_date = reviews_df["review_date"].max()
    
    date_range = st.sidebar.date_input(
        "Select date range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        date_filter_enabled = True
        start_date, end_date = date_range
    else:
        date_filter_enabled = False
else:
    date_filter_enabled = False

st.sidebar.markdown("---")

# Apply filters
filtered_reviews = reviews_df.copy()

if source_filter and "source" in reviews_df.columns:
    filtered_reviews = filtered_reviews[filtered_reviews["source"].isin(source_filter)]

if category_filter and "category" in reviews_df.columns:
    filtered_reviews = filtered_reviews[filtered_reviews["category"].isin(category_filter)]

if date_filter_enabled and "review_date" in filtered_reviews.columns:
    filtered_reviews = filtered_reviews[
        (filtered_reviews["review_date"] >= pd.Timestamp(start_date)) &
        (filtered_reviews["review_date"] <= pd.Timestamp(end_date))
    ]

st.sidebar.metric("🔍 Filtered Reviews", f"{len(filtered_reviews):,}")

# ============================================================================
# KPI METRICS
# ============================================================================
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

# Total reviews
col1.metric(
    "📝 Total Reviews",
    f"{len(filtered_reviews):,}",
    delta=f"{len(filtered_reviews) - len(reviews_df):+,}" if len(filtered_reviews) != len(reviews_df) else None
)

# Sentiment percentages
if "sentiment_label" in filtered_reviews.columns:
    positive_pct = (filtered_reviews["sentiment_label"].str.lower() == "positive").mean() * 100
    negative_pct = (filtered_reviews["sentiment_label"].str.lower() == "negative").mean() * 100
    neutral_pct = (filtered_reviews["sentiment_label"].str.lower() == "neutral").mean() * 100
    
    col2.metric("😊 Positive", f"{positive_pct:.1f}%")
    col3.metric("😞 Negative", f"{negative_pct:.1f}%")
    col4.metric("😐 Neutral", f"{neutral_pct:.1f}%")
else:
    col2.metric("😊 Positive", "N/A")
    col3.metric("😞 Negative", "N/A")
    col4.metric("😐 Neutral", "N/A")

st.markdown("---")

# ============================================================================
# SENTIMENT DISTRIBUTION & CATEGORY ANALYSIS
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("😊 Overall Sentiment Distribution")
    
    if "sentiment_label" in reviews_df.columns:
        sentiment_dist = reviews_df["sentiment_label"].value_counts().reset_index()
        sentiment_dist.columns = ["Sentiment", "Count"]
        
        fig = px.pie(
            sentiment_dist,
            names="Sentiment",
            values="Count",
            title="Sentiment Breakdown",
            hole=0.4,
            color="Sentiment",
            color_discrete_map={
                "Positive": "#2ecc71",
                "positive": "#2ecc71",
                "Negative": "#e74c3c",
                "negative": "#e74c3c",
                "Neutral": "#95a5a6",
                "neutral": "#95a5a6"
            }
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Sentiment data not available")

with col2:
    st.subheader("📦 Category-wise Sentiment Comparison")
    
    if "category" in reviews_df.columns and "sentiment_label" in reviews_df.columns:
        category_sentiment = (
            reviews_df.groupby(["category", "sentiment_label"])
            .size()
            .reset_index(name="count")
        )
        
        fig = px.bar(
            category_sentiment,
            x="category",
            y="count",
            color="sentiment_label",
            title="Sentiment Distribution by Category",
            barmode="group",
            color_discrete_map={
                "Positive": "#2ecc71",
                "positive": "#2ecc71",
                "Negative": "#e74c3c",
                "negative": "#e74c3c",
                "Neutral": "#95a5a6",
                "neutral": "#95a5a6"
            }
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Category/Sentiment data not available")

st.markdown("---")

# ============================================================================
# SENTIMENT TREND OVER TIME
# ============================================================================
st.subheader("📈 Sentiment Trend Over Time")

if "review_date" in filtered_reviews.columns and "sentiment_label" in filtered_reviews.columns:
    # Remove NaT values
    trend_df = filtered_reviews.dropna(subset=["review_date"])
    
    if len(trend_df) > 0:
        sentiment_trend = (
            trend_df.groupby([pd.Grouper(key="review_date", freq="W"), "sentiment_label"])
            .size()
            .reset_index(name="count")
        )
        
        fig_trend = px.line(
            sentiment_trend,
            x="review_date",
            y="count",
            color="sentiment_label",
            title="Weekly Sentiment Trend",
            labels={"review_date": "Date", "count": "Number of Reviews", "sentiment_label": "Sentiment"},
            color_discrete_map={
                "Positive": "#2ecc71",
                "positive": "#2ecc71",
                "Negative": "#e74c3c",
                "negative": "#e74c3c",
                "Neutral": "#95a5a6",
                "neutral": "#95a5a6"
            }
        )
        fig_trend.update_layout(hovermode='x unified')
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("ℹ️ No date information available for trend analysis")
else:
    st.warning("⚠️ Date or sentiment data not available for trend analysis")

st.markdown("---")

# ============================================================================
# TOPIC ANALYSIS (if available)
# ============================================================================
if "lda_topic_label" in filtered_reviews.columns or "topic" in filtered_reviews.columns:
    st.subheader("💬 Topic Analysis")
    
    topic_col = "lda_topic_label" if "lda_topic_label" in filtered_reviews.columns else "topic"
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top topics
        topic_counts = filtered_reviews[topic_col].value_counts().head(10)
        
        fig_topics = px.bar(
            x=topic_counts.values,
            y=topic_counts.index,
            orientation='h',
            title="Top 10 Discussion Topics",
            labels={"x": "Number of Reviews", "y": "Topic"},
            color=topic_counts.values,
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_topics, use_container_width=True)
    
    with col2:
        # Topic sentiment
        if "sentiment_label" in filtered_reviews.columns:
            topic_sentiment = (
                filtered_reviews.groupby([topic_col, "sentiment_label"])
                .size()
                .reset_index(name="count")
            )
            
            # Filter to top 10 topics
            top_topics = topic_counts.head(10).index.tolist()
            topic_sentiment = topic_sentiment[topic_sentiment[topic_col].isin(top_topics)]
            
            fig_topic_sent = px.bar(
                topic_sentiment,
                x=topic_col,
                y="count",
                color="sentiment_label",
                title="Sentiment by Topic (Top 10)",
                barmode="stack",
                color_discrete_map={
                    "Positive": "#2ecc71",
                    "positive": "#2ecc71",
                    "Negative": "#e74c3c",
                    "negative": "#e74c3c",
                    "Neutral": "#95a5a6",
                    "neutral": "#95a5a6"
                }
            )
            fig_topic_sent.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_topic_sent, use_container_width=True)

    st.markdown("---")

# ============================================================================
# DATA TABLE
# ============================================================================
st.subheader("📋 Detailed Review Data")

# Display controls
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    available_cols = filtered_reviews.columns.tolist()
    default_cols = []
    for col in ["product", "category", "rating", "sentiment_label", "review_date"]:
        if col in available_cols:
            default_cols.append(col)
    
    show_columns = st.multiselect(
        "Select columns to display:",
        options=available_cols,
        default=default_cols if default_cols else available_cols[:5]
    )

with col2:
    rows_to_show = st.selectbox("Rows:", [10, 25, 50, 100], index=1)

with col3:
    if st.button("📥 Download"):
        csv = filtered_reviews.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_reviews.csv",
            mime="text/csv"
        )

# Display table
if show_columns:
    st.dataframe(
        filtered_reviews[show_columns].head(rows_to_show),
        use_container_width=True,
        height=400
    )
else:
    st.info("ℹ️ Please select at least one column to display")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>AI-Powered Market Trend & Consumer Sentiment Forecaster</strong></p>
    <p>Built with ❤️ using Streamlit & Plotly | 📊 Real-time Analytics & Insights</p>
</div>
""", unsafe_allow_html=True)
