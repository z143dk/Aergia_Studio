from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

print("Testing 'models/gemini-1.5-flash'...")
try:
    response = client.models.generate_content(model="models/gemini-1.5-flash", contents="Hello")
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Error with prefix: {e}")

print("\nListing first 5 models:")
try:
    for i, m in enumerate(client.models.list()):
        print(f"Model: {m.name}")
        if i >= 4: break
except Exception as e:
    print(f"List Error: {e}")
