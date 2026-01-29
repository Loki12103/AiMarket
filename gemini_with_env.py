import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Define temperature in LLM in 2-3 lines",
    config=types.GenerateContentConfig(
        temperature=0.3  
    ),
)

print("=" * 50)
print("Response with temperature=0.3 (More focused)")
print("=" * 50)
print(response.text)
print()


response2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Define temperature in LLM in 2-3 lines",
    config=types.GenerateContentConfig(
        temperature=0.9  
    ),
)

print("=" * 50)
print("Response with temperature=0.9 (More creative)")
print("=" * 50)
print(response2.text)
