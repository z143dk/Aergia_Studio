# main.py
import os
import json
import logging
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()

# Setup local logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("aergia_os.log"),
        logging.StreamHandler()
    ]
)

# Configuration
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "market_data")
POLYGON_API_BASE_URL = "https://api.polygon.io"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# --- Market Data Fetcher Function ---
def fetch_and_save_market_data():
    """
    Fetches daily OHLCV data for a list of tickers and saves to local JSON files.
    """
    logging.info("Starting market data fetch...")

    if not POLYGON_API_KEY:
        logging.error("POLYGON_API_KEY not found in environment variables.")
        return

    # Define tickers
    tickers = ["AAPL", "MSFT", "GOOG"]

    # Calculate yesterday's date
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Check if it's the weekend
    if today.weekday() in [5, 6]:
        logging.info("It's the weekend. Skipping market data fetch.")
        return

    headers = {"Authorization": f"Bearer {POLYGON_API_KEY}"}
    
    for ticker in tickers:
        logging.info(f"Fetching data for {ticker} on {yesterday}...")
        
        url = f"{POLYGON_API_BASE_URL}/v2/aggs/ticker/{ticker}/range/1/day/{yesterday}/{yesterday}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data and data.get('results'):
                # Prepare the record
                record = {
                    'ticker': ticker,
                    'date': yesterday,
                    'fetched_at': datetime.now().isoformat(),
                    'data': data['results']
                }
                
                # Save to local file
                filename = f"{ticker}_{yesterday}.json"
                filepath = os.path.join(DATA_DIR, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(record, f, indent=2)
                
                logging.info(f"Saved data for {ticker} to {filepath}")
            else:
                logging.info(f"No results found for {ticker} on {yesterday}.")

        except Exception as e:
            logging.error(f"Error fetching/saving data for {ticker}: {e}")

    logging.info("Market data fetch completed.")

if __name__ == "__main__":
    fetch_and_save_market_data()