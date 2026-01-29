"""
Simple Streamlit Demo - Student Learning Example
-------------------------------------------------

This is a basic Streamlit app demonstrating:
- Text display and formatting
- User input widgets (text, selectbox, slider)
- File upload
- Button interactions
- Charts

Run: streamlit run streamlit_demo.py
"""

import streamlit as st

# Title and introduction
st.title("Hello Streamlit 👋")
st.write("I am learning Streamlit as a student!")

st.markdown("---")

# Text input
st.subheader("📝 Text Input")
input_text = st.text_input("Input")
print("Text from user:", input_text)  # This prints to terminal
st.write("You entered:", input_text)

st.markdown("---")

# File uploader
st.subheader("📁 File Upload")
uploaded_file = st.file_uploader(
    "Upload a file",
    type=["csv", "txt", "jpg", "png", "pdf"]
)

st.markdown("---")

# Selectbox
st.subheader("👤 Select Gender")
gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])

st.markdown("---")

# Slider
st.subheader("⭐ Rate This App")
rating = st.slider("Rate this app (1-10):", 1, 10, 5)

st.markdown("---")

# Submit button
if st.button("Submit", type="primary"):
    st.success("✅ Form Submitted!")
    
    # Display uploaded file info
    if uploaded_file is not None:
        st.write("**Uploaded File:**")
        st.write(f"- Name: {uploaded_file.name}")
        st.write(f"- Size: {uploaded_file.size} bytes")
        st.write(f"- Type: {uploaded_file.type}")
    else:
        st.write("**Uploaded File:** None")
    
    # Display gender with warning
    st.warning(f"**Selected Gender:** {gender}")
    
    # Display rating
    st.write(f"**Rating:** {rating}/10")
    
    # Sample line chart
    st.write("**Sample Chart:**")
    st.line_chart([1, 2, 4, 5])

st.markdown("---")
st.info("💡 Try changing the inputs and clicking Submit again!")
