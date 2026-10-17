import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

sys.path.append(os.getcwd())
try:
    load_dotenv(".env.local", override=True)
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key present: {bool(api_key)}")
    genai.configure(api_key=api_key)
    print("Listing models...")
    for m in genai.list_models():
        print(f"Model: {m.name}")
    print("Done listing.")
except Exception as e:
    print(f"Error: {e}")
