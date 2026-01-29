import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

reviews = """
1. "This product is amazing! Best purchase ever. 5/5 stars!"
2. "Terrible quality. Broke after 2 days. Very disappointed."
3. "Good value for money. Works as expected."
4. "Outstanding customer service and great product quality."
5. "Not what I expected. The description was misleading."
"""

prompt = f"""
Analyze the following customer reviews:

{reviews}

Please provide:
1. Overall sentiment (Positive/Negative/Mixed)
2. Key trends or common themes
3. Percentage breakdown of positive vs negative reviews
4. Recommendations for improvement

Keep the analysis concise and actionable.
"""

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=prompt,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0),
        temperature=0.3  # Lower temperature for more consistent analysis
    ),
)

print("=" * 60)
print("REVIEW ANALYSIS")
print("=" * 60)
print(response.text)
