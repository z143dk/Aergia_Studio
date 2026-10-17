import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\.env")

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("Listing available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Model: {m.name}")
