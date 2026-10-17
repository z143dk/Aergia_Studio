
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Logic from director
MIDAS_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Project Midas", ".env.local")
load_dotenv(MIDAS_ENV_PATH)
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    MIDAS_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Project Midas", ".env")
    load_dotenv(MIDAS_ENV_PATH)
    API_KEY = os.getenv("GOOGLE_API_KEY")

print(f"API Key found: {'Yes' if API_KEY else 'No'}")
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        print("Listing models...")
        with open("models_list.txt", "w") as f:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    f.write(f"{m.name}\n")
                    print(m.name)
    except Exception as e:
        print(f"Error: {e}")
