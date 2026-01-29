import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


prompt = "Explain the difference between open-source and proprietary LLMs in simple terms."

print("=" * 60)
print("Testing Multiple Open Source Models via Groq")
print("=" * 60)
print()

models = [
    "llama-3.3-70b-versatile",      
    "llama-3.1-8b-instant",         
    "mixtral-8x7b-32768",          
    "gemma2-9b-it",                
]


print(f"Model: {models[0]}")
print("-" * 60)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model=models[0],
    temperature=0.5,
    max_tokens=1024,
)

print(chat_completion.choices[0].message.content)
print("\n" + "=" * 60)
print(f"Model used: {chat_completion.model}")
print(f"Tokens used: {chat_completion.usage.total_tokens}")
print("=" * 60)
