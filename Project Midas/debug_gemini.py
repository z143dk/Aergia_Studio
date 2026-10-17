import google.generativeai as genai
import os
from dotenv import load_dotenv

# Explicitly load from current directory to be sure
load_dotenv('.env')

api_key = os.getenv('GOOGLE_API_KEY')
print(f"DEBUG: Loaded API Key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("ERROR: API Key not found!")
    exit(1)

genai.configure(api_key=api_key)

print("\nAttempting to list models...")
try:
    for m in genai.list_models():
        print(f"- {m.name}")
except Exception as e:
    print(f"ERROR Listing Models: {e}")

print("\nAttempting basic generation with 'gemini-1.5-flash-001'...")
try:
    model = genai.GenerativeModel('gemini-1.5-flash-001')
    response = model.generate_content("Hello")
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"ERROR Generating: {e}")
