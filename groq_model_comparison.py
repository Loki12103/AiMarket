

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


prompt = "Write a creative tagline for an AI-powered review analysis tool in one sentence."


models = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

print("=" * 70)
print("COMPARING DIFFERENT OPEN SOURCE MODELS")
print("=" * 70)
print(f"Prompt: {prompt}")
print("=" * 70)
print()

for model in models:
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            temperature=0.7,  
            max_tokens=100,
        )
        
        print(f"Model: {model}")
        print(f"Response: {response.choices[0].message.content}")
        print(f"Tokens: {response.usage.total_tokens}")
        print("-" * 70)
        print()
        
    except Exception as e:
        print(f"Error with {model}: {str(e)}")
        print("-" * 70)
        print()
