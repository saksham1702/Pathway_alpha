import pathway as pw
import requests
import pandas as pd
from typing import Dict, Any
from dotenv import load_dotenv
import os 
load_dotenv()

api_key = os.getenv("POLYGON_API_KEY")

class MarketDataConnector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"
    
    def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        # Polygon.io API endpoint for stock quotes
        url = f"{self.base_url}/v2/aggs/ticker/{symbol}/prev"
        params = {
            'apikey': self.api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check for API errors
        if "status" in data and data["status"] != "OK":
            raise Exception(f"API Error: {data.get('message', data)}")
        
        # Extract data from Polygon.io response
        if "results" not in data or not data["results"]:
            raise Exception("No stock data found")
        #print(data)
        result = data["results"][0]  # Get the first (and usually only) result
        current_price = float(result['c'])
        previous_price = float(result['o'])
        change_percent = ((current_price - previous_price) / previous_price) * 100
        return {
            'symbol': symbol,
            'price': float(result['c']),  # Close price
            'volume': int(result['v']),   # Volume
            'timestamp': result['t'],     # Timestamp
            'change_percent': change_percent  # We'll calculate this later
        }
    
    def create_streaming_table(self, symbols: list):
        # This will be the first Pathway streaming table
        data = []
        for symbol in symbols:
            try:
                stock_data = self.get_stock_data(symbol)
                data.append(stock_data)
            except Exception as e:
                print(f"Failed to get data for {symbol}: {e}")

            # Process and format the data
            # Add to data list
        df = pd.DataFrame(data)
        if len(df) == 0:
            df = pd.DataFrame(columns=["symbol", "price", "volume", "timestamp", "change_percent"])
        else:
            df = df.reset_index(drop=True)
        
        print(f"DataFrame shape: {df.shape}")
        print(f"DataFrame content:\n{df}")
        
        # Create Pathway table
        table = pw.debug.table_from_pandas(df)
        print(f"Pathway table created: {type(table)}")
        return table
    