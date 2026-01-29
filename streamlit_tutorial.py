"""
Streamlit Basics - Complete Tutorial
-------------------------------------

What is Streamlit?
- Open-source Python framework for building interactive web apps
- No HTML, CSS, or JavaScript required - just Python!
- Perfect for data science, ML, and analytics projects
- Runs in the browser (local or deployed)

Setup:
1. Install: pip install streamlit
2. Run this app: streamlit run streamlit_tutorial.py
3. View documentation: streamlit hello

Official docs: https://docs.streamlit.io/
"""

import streamlit as st
import pandas as pd
import numpy as np

# ============================================================================
# PAGE CONFIGURATION (Must be first Streamlit command)
# ============================================================================
st.set_page_config(
    page_title="Streamlit Tutorial",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.title("📚 Navigation")
st.sidebar.write("Use this sidebar to navigate between sections")

section = st.sidebar.radio(
    "Choose a section:",
    [
        "Introduction",
        "Text & Formatting",
        "Data Display",
        "Charts & Visualizations",
        "User Input Widgets",
        "Interactive Example"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Streamlit reruns the entire script on every interaction!")

# ============================================================================
# MAIN CONTENT
# ============================================================================

if section == "Introduction":
    st.title("🎉 Welcome to Streamlit!")
    
    st.markdown("""
    ## What You'll Learn
    
    This tutorial covers:
    - Text and formatting options
    - Displaying data (tables, dataframes)
    - Creating charts and visualizations
    - User input widgets (buttons, sliders, text inputs)
    - Building interactive applications
    
    ### Why Streamlit?
    ✅ **Easy** - Just Python, no web dev experience needed  
    ✅ **Fast** - Build apps in minutes, not hours  
    ✅ **Interactive** - Automatic updates on user input  
    ✅ **Beautiful** - Clean, modern UI out of the box
    
    ### Quick Start
    ```python
    import streamlit as st
    
    st.title("My First App")
    st.write("Hello, World!")
    ```
    
    **Navigate using the sidebar to explore different features!**
    """)

elif section == "Text & Formatting":
    st.title("📝 Text & Formatting")
    
    st.header("Header Text")
    st.subheader("Subheader Text")
    st.text("Plain text - simple and direct")
    
    st.markdown("---")
    
    st.subheader("Markdown Support")
    st.markdown("""
    **Bold Text**  
    *Italic Text*  
    ***Bold and Italic***  
    
    - Bullet point 1
    - Bullet point 2
    - Bullet point 3
    
    1. Numbered item 1
    2. Numbered item 2
    3. Numbered item 3
    
    [Link to Streamlit Docs](https://docs.streamlit.io/)
    
    `Inline code`
    
    ```python
    # Code block
    def hello():
        return "Hello, Streamlit!"
    ```
    """)
    
    st.markdown("---")
    
    st.subheader("Special Messages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ Success message")
        st.info("ℹ️ Info message")
    
    with col2:
        st.warning("⚠️ Warning message")
        st.error("❌ Error message")
    
    st.markdown("---")
    
    st.subheader("Code Display")
    code = '''def hello_world():
    print("Hello, Streamlit!")'''
    st.code(code, language='python')

elif section == "Data Display":
    st.title("📊 Data Display")
    
    # Create sample data
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Age": [24, 27, 22, 32, 29],
        "City": ["New York", "London", "Paris", "Tokyo", "Sydney"],
        "Score": [85, 92, 78, 95, 88]
    })
    
    st.subheader("Sample Dataset")
    st.write("Here's a sample pandas DataFrame:")
    
    st.write(df)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("st.dataframe()")
        st.write("Interactive, scrollable table")
        st.dataframe(df, use_container_width=True)
    
    with col2:
        st.subheader("st.table()")
        st.write("Static table")
        st.table(df)
    
    st.markdown("---")
    
    st.subheader("Metrics Display")
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Users", "5", "+2")
    col2.metric("Average Age", "26.8", "-1.2")
    col3.metric("Average Score", "87.6", "+3.4")
    
    st.markdown("---")
    
    st.subheader("JSON Display")
    data = {
        "name": "John Doe",
        "age": 30,
        "skills": ["Python", "Streamlit", "Data Science"]
    }
    st.json(data)

elif section == "Charts & Visualizations":
    st.title("📈 Charts & Visualizations")
    
    # Generate sample data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Product A', 'Product B', 'Product C']
    )
    
    st.subheader("Line Chart")
    st.line_chart(chart_data)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bar Chart")
        st.bar_chart(chart_data)
    
    with col2:
        st.subheader("Area Chart")
        st.area_chart(chart_data)
    
    st.markdown("---")
    
    st.subheader("More Advanced Charts")
    st.info("💡 For more complex visualizations, use matplotlib, plotly, or altair!")
    
    # Example with matplotlib
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots()
    ax.plot(chart_data.index, chart_data['Product A'], label='Product A')
    ax.plot(chart_data.index, chart_data['Product B'], label='Product B')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Product Performance')
    ax.legend()
    
    st.pyplot(fig)

elif section == "User Input Widgets":
    st.title("🎛️ User Input Widgets")
    
    st.subheader("Text Input")
    name = st.text_input("Enter your name:", placeholder="John Doe")
    if name:
        st.write(f"Hello, {name}! 👋")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Button")
        if st.button("Click Me!"):
            st.success("Button clicked! 🎉")
        
        st.subheader("Checkbox")
        agree = st.checkbox("I agree to the terms")
        if agree:
            st.write("✅ Thank you for agreeing!")
    
    with col2:
        st.subheader("Radio Buttons")
        choice = st.radio("Choose an option:", ["Option A", "Option B", "Option C"])
        st.write(f"You selected: {choice}")
        
        st.subheader("Selectbox")
        option = st.selectbox(
            "Pick your favorite:",
            ["Python", "JavaScript", "Java", "C++"]
        )
        st.write(f"You picked: {option}")
    
    st.markdown("---")
    
    st.subheader("Slider")
    age = st.slider("Select your age:", 0, 100, 25)
    st.write(f"Age: {age}")
    
    st.subheader("Range Slider")
    values = st.slider("Select a range:", 0, 100, (25, 75))
    st.write(f"Range: {values[0]} - {values[1]}")
    
    st.markdown("---")
    
    st.subheader("Number Input")
    number = st.number_input("Enter a number:", min_value=0, max_value=100, value=50)
    st.write(f"Number: {number}")
    
    st.markdown("---")
    
    st.subheader("Text Area")
    text = st.text_area("Enter your feedback:", placeholder="Type here...")
    if text:
        st.write(f"Character count: {len(text)}")
    
    st.markdown("---")
    
    st.subheader("Date & Time Input")
    from datetime import datetime, date
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_date = st.date_input("Select a date:", date.today())
        st.write(f"Date: {selected_date}")
    
    with col2:
        selected_time = st.time_input("Select a time:")
        st.write(f"Time: {selected_time}")
    
    st.markdown("---")
    
    st.subheader("File Upload")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "txt", "jpg", "png", "pdf"]
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size} bytes")
        st.write(f"File type: {uploaded_file.type}")

elif section == "Interactive Example":
    st.title("🎮 Interactive Example")
    st.write("Let's build a mini product rating app!")
    
    st.markdown("---")
    
    # User inputs
    st.subheader("📝 Enter Your Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_name = st.text_input("Your Name:", placeholder="Enter your name")
        gender = st.selectbox("Gender:", ["Male", "Female", "Other", "Prefer not to say"])
    
    with col2:
        email = st.text_input("Email:", placeholder="your@email.com")
        age_group = st.selectbox("Age Group:", ["18-25", "26-35", "36-45", "46+"])
    
    st.markdown("---")
    
    st.subheader("⭐ Rate Our Products")
    
    product1_rating = st.slider("Product A - Smart Watch:", 1, 10, 5)
    product2_rating = st.slider("Product B - Wireless Earbuds:", 1, 10, 5)
    product3_rating = st.slider("Product C - Fitness Tracker:", 1, 10, 5)
    
    st.markdown("---")
    
    st.subheader("📁 Upload Supporting Documents (Optional)")
    uploaded_file = st.file_uploader(
        "Upload a file (image, document, etc.)",
        type=["csv", "txt", "jpg", "png", "pdf"]
    )
    
    st.markdown("---")
    
    st.subheader("💭 Additional Feedback")
    feedback = st.text_area(
        "Share your thoughts:",
        placeholder="Tell us about your experience...",
        height=150
    )
    
    st.markdown("---")
    
    # Submit button
    if st.button("🚀 Submit Feedback", type="primary"):
        if not user_name:
            st.error("❌ Please enter your name!")
        elif not email:
            st.error("❌ Please enter your email!")
        else:
            st.success("✅ Thank you for your feedback!")
            
            # Display summary
            st.subheader("📊 Feedback Summary")
            
            summary_df = pd.DataFrame({
                "Field": ["Name", "Email", "Gender", "Age Group"],
                "Value": [user_name, email, gender, age_group]
            })
            
            st.table(summary_df)
            
            # Display ratings
            st.subheader("⭐ Your Ratings")
            
            ratings_df = pd.DataFrame({
                "Product": ["Smart Watch", "Wireless Earbuds", "Fitness Tracker"],
                "Rating": [product1_rating, product2_rating, product3_rating]
            })
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(ratings_df, use_container_width=True)
            
            with col2:
                st.bar_chart(ratings_df.set_index("Product"))
            
            # Calculate average
            avg_rating = (product1_rating + product2_rating + product3_rating) / 3
            st.metric("Average Rating", f"{avg_rating:.1f}/10")
            
            # Show uploaded file info
            if uploaded_file:
                st.info(f"📎 Attached file: {uploaded_file.name}")
            
            # Show feedback
            if feedback:
                st.subheader("💭 Your Feedback")
                st.write(feedback)
            
            # Visualization
            st.subheader("📈 Rating Visualization")
            chart_data = pd.DataFrame({
                "Rating": [product1_rating, product2_rating, product3_rating]
            }, index=["Product A", "Product B", "Product C"])
            st.line_chart(chart_data)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using Streamlit</p>
    <p>📚 <a href='https://docs.streamlit.io/'>Documentation</a> | 
    💬 <a href='https://discuss.streamlit.io/'>Community</a> | 
    🐙 <a href='https://github.com/streamlit/streamlit'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
