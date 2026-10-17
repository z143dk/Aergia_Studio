from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

print("Listing models with new SDK...")
try:
    for m in client.models.list():
        if "generateContent" in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"List Error: {e}")

print("\nTesting 'gemini-1.5-flash'...")
try:
    response = client.models.generate_content(model="gemini-1.5-flash", contents="Hello")
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Gen Error: {e}")
