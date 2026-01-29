"""
Basic Gemini Example
--------------------
Simple example showing how to use Google's Gemini API
"""

from google import genai

client = genai.Client(api_key="your_api_key_here")

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Explain how AI works in a few words"
)

print(response.text)
