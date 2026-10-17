import requests
from . import config, auth

class SchwabClient:
    def __init__(self):
        self.tokens = auth.load_tokens()
        if not self.tokens:
            raise Exception("No tokens found. Please run setup_schwab.py first.")
        
        # Simple check if token is expired could go here (omitted for brevity, good to add later)
        self.access_token = self.tokens.get('access_token')

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json'
        }

    def get_account_numbers(self):
        """
        Retrieves account numbers linked to the user.
        """
        url = f'{config.BASE_URL}/accounts/accountNumbers'
        response = requests.get(url, headers=self.get_headers())
        
        if response.status_code == 401:
            print("Token expired. Refreshing...")
            self.tokens = auth.refresh_access_token()
            self.access_token = self.tokens.get('access_token')
            # Retry
            response = requests.get(url, headers=self.get_headers())

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching accounts: {response.text}")

    def get_account_balance(self, account_hash):
        """
        Retrieves detailed balance/position info for a specific account.
        """
        url = f'{config.BASE_URL}/accounts/{account_hash}'
        response = requests.get(url, headers=self.get_headers())
        
        if response.status_code == 401:
            self.tokens = auth.refresh_access_token()
            self.access_token = self.tokens.get('access_token')
            response = requests.get(url, headers=self.get_headers())

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching balance: {response.text}")


    def get_quote(self, symbol):
        """
        Retrieves a quote for a specific symbol.
        """
        # Note: Market Data API might have a different base URL or endpoint structure
        # ensuring we use the correct one for quotes if different.
        # Often it is https://api.schwabapi.com/marketdata/v1/quotes
        market_data_url = 'https://api.schwabapi.com/marketdata/v1/quotes'
        params = {'symbols': symbol, 'fields': 'quote,reference'}
        response = requests.get(market_data_url, headers=self.get_headers(), params=params)
        
        if response.status_code == 401:
            self.tokens = auth.refresh_access_token()
            self.access_token = self.tokens.get('access_token')
            response = requests.get(market_data_url, headers=self.get_headers(), params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching quote for {symbol}: {response.status_code} {response.text}")

    def get_price_history(self, symbol, period_type='year', period=1, frequency_type='daily', frequency=1):
        """
        Get price history for a symbol.
        Useful for technical analysis (Daily candles, etc.)
        """
        url = 'https://api.schwabapi.com/marketdata/v1/pricehistory'
        params = {
            'symbol': symbol,
            'periodType': period_type,
            'period': period,
            'frequencyType': frequency_type,
            'frequency': frequency
        }
        # Include Close, High, Low, Open, Volume
        
        response = requests.get(url, headers=self.get_headers(), params=params)
        
        if response.status_code == 401:
            self.tokens = auth.refresh_access_token()
            self.access_token = self.tokens.get('access_token')
            response = requests.get(url, headers=self.get_headers(), params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching price history: {response.status_code} {response.text}")

    def get_option_chain(self, symbol, contract_type='ALL', strike_count=10, from_date=None, to_date=None):
        """
        Get option chain for a symbol.
        contract_type: CALL, PUT, ALL
        """
        url = 'https://api.schwabapi.com/marketdata/v1/chains'
        params = {
            'symbol': symbol,
            'contractType': contract_type,
            'strikeCount': strike_count,
            'includeUnderlyingQuote': 'true',
            'strategy': 'SINGLE'
        }
        if from_date:
            params['fromDate'] = from_date # Format: YYYY-MM-DD
        if to_date:
            params['toDate'] = to_date

        response = requests.get(url, headers=self.get_headers(), params=params)
        
        if response.status_code == 401:
            self.tokens = auth.refresh_access_token()
            self.access_token = self.tokens.get('access_token')
            response = requests.get(url, headers=self.get_headers(), params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching option chain: {response.status_code} {response.text}")

    def place_order(self, account_hash, order_spec):
        """
        Places an order for a specific account.
        order_spec: Dictionary containing the order JSON payload.
        """
        url = f'{config.BASE_URL}/accounts/{account_hash}/orders'
        
        # Schwab requires specific headers for orders
        headers = self.get_headers()
        headers['Content-Type'] = 'application/json'
        
        response = requests.post(url, headers=headers, json=order_spec)
        
        if response.status_code == 401:
            self.tokens = auth.refresh_access_token()
            self.access_token = self.tokens.get('access_token')
            # Refresh headers with new token
            headers = self.get_headers()
            headers['Content-Type'] = 'application/json'
            response = requests.post(url, headers=headers, json=order_spec)
            
        if response.status_code == 201:
            # 201 Created is the standard success response for orders
            # Schwab usually returns the Location header with the Order ID
            location = response.headers.get('Location', '')
            order_id = location.split('/')[-1] if location else 'Unknown'
            return {"status": "SUBMITTED", "order_id": order_id}
        else:
            raise Exception(f"Error placing order: {response.status_code} {response.text}")
