import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv('.env')
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

with open('gemini3_name.txt', 'w') as f:
    for m in genai.list_models():
        if 'gemini-3' in m.name:
            f.write(m.name.replace('models/', ''))
            print(f"FOUND: {m.name}")
            break
