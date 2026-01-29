"""
AI Market Dashboard - Sentiment & Topic Analysis
-------------------------------------------------

Interactive Streamlit dashboard for the AI-Powered Market Trend & Sentiment Forecaster project.

Features:
- Upload and analyze product review data
- View sentiment distribution
- Explore topic modeling results
- Filter by category and sentiment
- Visualize trends and patterns

Run: streamlit run market_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="AI Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<h1 class="main-header">🤖 AI Market Trend & Sentiment Analyzer</h1>', unsafe_allow_html=True)
st.markdown("### Discover insights from product reviews and market trends")

st.markdown("---")

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.title("⚙️ Dashboard Controls")
st.sidebar.markdown("---")

# File upload
st.sidebar.subheader("📁 Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload review dataset (CSV)",
    type=["csv"],
    help="Upload a CSV file with product reviews"
)

# Sample data option
use_sample_data = st.sidebar.checkbox("Use Sample Data", value=True)

# Load data
@st.cache_data
def load_data(file=None):
    if file is not None:
        df = pd.read_csv(file)
    else:
        # Generate sample data
        categories = ["Mobile_Accessories", "Kitchen_Appliances", "Home_Appliances", 
                     "Electronics", "Fashion", "Beauty_Personal_Care"]
        sentiments = ["positive", "negative", "neutral"]
        
        np.random.seed(42)
        n_samples = 500
        
        df = pd.DataFrame({
            "product": [f"Product {i}" for i in range(n_samples)],
            "category": np.random.choice(categories, n_samples),
            "rating": np.random.randint(1, 6, n_samples),
            "sentiment_label": np.random.choice(sentiments, n_samples, p=[0.6, 0.25, 0.15]),
            "review_text": ["Sample review text"] * n_samples,
            "review_date": pd.date_range(start="2024-01-01", periods=n_samples, freq="D"),
            "sentiment_score": np.random.uniform(-1, 1, n_samples)
        })
    
    return df

# Load data
if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success(f"✅ Loaded {len(df)} reviews")
elif use_sample_data:
    df = load_data()
    st.sidebar.info(f"📊 Using {len(df)} sample reviews")
else:
    df = None
    st.sidebar.warning("⚠️ Please upload a file or enable sample data")

# Filters (only show if data is loaded)
if df is not None:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filters")
    
    # Category filter
    categories = ["All"] + sorted(df["category"].unique().tolist())
    selected_category = st.sidebar.selectbox("Category:", categories)
    
    # Sentiment filter
    sentiments = ["All"] + sorted(df["sentiment_label"].unique().tolist())
    selected_sentiment = st.sidebar.selectbox("Sentiment:", sentiments)
    
    # Rating filter
    min_rating, max_rating = st.sidebar.slider(
        "Rating Range:",
        min_value=1,
        max_value=5,
        value=(1, 5)
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    
    if selected_sentiment != "All":
        filtered_df = filtered_df[filtered_df["sentiment_label"] == selected_sentiment]
    
    filtered_df = filtered_df[
        (filtered_df["rating"] >= min_rating) & 
        (filtered_df["rating"] <= max_rating)
    ]
    
    st.sidebar.markdown("---")
    st.sidebar.metric("Filtered Reviews", len(filtered_df))

# ============================================================================
# MAIN CONTENT
# ============================================================================

if df is not None:
    # Top metrics
    st.subheader("📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Reviews",
            f"{len(filtered_df):,}",
            f"{len(filtered_df) - len(df):+,}" if selected_category != "All" or selected_sentiment != "All" else None
        )
    
    with col2:
        avg_rating = filtered_df["rating"].mean()
        st.metric("Average Rating", f"{avg_rating:.2f}⭐")
    
    with col3:
        positive_pct = (filtered_df["sentiment_label"] == "positive").sum() / len(filtered_df) * 100
        st.metric("Positive Reviews", f"{positive_pct:.1f}%")
    
    with col4:
        categories_count = filtered_df["category"].nunique()
        st.metric("Categories", categories_count)
    
    st.markdown("---")
    
    # Two-column layout
    col_left, col_right = st.columns(2)
    
    # ========================================================================
    # LEFT COLUMN
    # ========================================================================
    with col_left:
        st.subheader("😊 Sentiment Distribution")
        
        sentiment_counts = filtered_df["sentiment_label"].value_counts()
        
        fig_sentiment = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Sentiment Breakdown",
            color=sentiment_counts.index,
            color_discrete_map={
                "positive": "#2ecc71",
                "negative": "#e74c3c",
                "neutral": "#95a5a6"
            }
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("⭐ Rating Distribution")
        
        rating_counts = filtered_df["rating"].value_counts().sort_index()
        
        fig_rating = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            labels={"x": "Rating", "y": "Count"},
            title="Review Ratings",
            color=rating_counts.values,
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_rating, use_container_width=True)
    
    # ========================================================================
    # RIGHT COLUMN
    # ========================================================================
    with col_right:
        st.subheader("📦 Category Breakdown")
        
        category_counts = filtered_df["category"].value_counts().head(10)
        
        fig_category = px.bar(
            x=category_counts.values,
            y=category_counts.index,
            orientation='h',
            labels={"x": "Number of Reviews", "y": "Category"},
            title="Top Categories",
            color=category_counts.values,
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_category, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("📈 Sentiment by Category")
        
        sentiment_by_category = pd.crosstab(
            filtered_df["category"],
            filtered_df["sentiment_label"]
        ).head(10)
        
        fig_sent_cat = px.bar(
            sentiment_by_category,
            title="Sentiment Distribution Across Categories",
            labels={"value": "Count", "variable": "Sentiment"},
            color_discrete_map={
                "positive": "#2ecc71",
                "negative": "#e74c3c",
                "neutral": "#95a5a6"
            }
        )
        st.plotly_chart(fig_sent_cat, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # FULL WIDTH SECTIONS
    # ========================================================================
    
    st.subheader("📅 Trend Over Time")
    
    if "review_date" in filtered_df.columns:
        filtered_df["review_date"] = pd.to_datetime(filtered_df["review_date"])
        
        daily_sentiment = filtered_df.groupby([
            filtered_df["review_date"].dt.date,
            "sentiment_label"
        ]).size().reset_index(name="count")
        
        fig_trend = px.line(
            daily_sentiment,
            x="review_date",
            y="count",
            color="sentiment_label",
            title="Sentiment Trends Over Time",
            labels={"review_date": "Date", "count": "Number of Reviews"},
            color_discrete_map={
                "positive": "#2ecc71",
                "negative": "#e74c3c",
                "neutral": "#95a5a6"
            }
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # DATA TABLE
    # ========================================================================
    
    st.subheader("📋 Review Data")
    
    # Display options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        show_columns = st.multiselect(
            "Select columns to display:",
            options=filtered_df.columns.tolist(),
            default=["product", "category", "rating", "sentiment_label"][:min(4, len(filtered_df.columns))]
        )
    
    with col2:
        rows_to_show = st.selectbox("Rows to display:", [10, 25, 50, 100], index=1)
    
    with col3:
        if st.button("📥 Download CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download Filtered Data",
                data=csv,
                file_name=f"filtered_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Display table
    if show_columns:
        st.dataframe(
            filtered_df[show_columns].head(rows_to_show),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("⚠️ Please select at least one column to display")

else:
    # No data loaded
    st.info("👈 Please upload a dataset or enable sample data from the sidebar to get started!")
    
    st.markdown("### 📖 How to Use This Dashboard")
    st.markdown("""
    1. **Upload your data** using the sidebar file uploader, or enable sample data
    2. **Apply filters** to focus on specific categories, sentiments, or ratings
    3. **Explore visualizations** to understand trends and patterns
    4. **Download filtered data** for further analysis
    
    ### 📊 Supported Data Format
    Your CSV file should contain columns like:
    - `product` - Product name
    - `category` - Product category
    - `rating` - Rating (1-5)
    - `sentiment_label` - Sentiment (positive/negative/neutral)
    - `review_text` - Review content
    - `review_date` - Date of review
    """)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>AI-Powered Market Trend & Sentiment Forecaster</strong></p>
    <p>Built with ❤️ using Streamlit | 📊 Data Science & Analytics</p>
</div>
""", unsafe_allow_html=True)
