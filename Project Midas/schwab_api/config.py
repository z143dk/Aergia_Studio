import os
from dotenv import load_dotenv

# Load environment variables from Project Midas or root .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, '.env'))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

# Schwab API Credentials
APP_KEY = os.getenv('SCHWAB_APP_KEY')
APP_SECRET = os.getenv('SCHWAB_APP_SECRET')
REDIRECT_URI = 'https://127.0.0.1'

# API Base URL
BASE_URL = 'https://api.schwabapi.com/trader/v1/'

# Token File Path (to persist tokens locally)
TOKEN_FILE = os.path.join(BASE_DIR, 'schwab_tokens.json')
