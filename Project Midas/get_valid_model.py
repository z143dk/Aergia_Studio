import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv('.env')
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

valid_model = None
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Authorized Model: {m.name}")
            # Prefer 1.5 Flash or Pro
            if 'gemini-1.5-flash' in m.name:
                valid_model = m.name
                break
            if 'gemini-1.5-pro' in m.name and valid_model is None:
                valid_model = m.name
    
    if valid_model:
        print(f"CHOSEN_MODEL: {valid_model}")
        with open('valid_model.txt', 'w') as f:
            f.write(valid_model)
    else:
        print("NO_VALID_GEMINI_MODEL_FOUND")
        
except Exception as e:
    print(f"ERROR: {e}")
