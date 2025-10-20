from market_data import MarketDataConnector
from dotenv import load_dotenv
import os
import pathway as pw
import pandas as pd
load_dotenv()

api_key = os.getenv("POLYGON_API_KEY")
def test_market_data_connector():
    connector = MarketDataConnector(api_key= api_key)
    symbols = ["AAPL", "GOOGL"] 
    try:
        print("Testing individual stock data..")
        stock_data = connector.get_stock_data("AAPL")
        print(f"Stock data for AAPL: {stock_data}")

        print("Testing streaming table..")
        table = connector.create_streaming_table(symbols)
        print("Table created successfully")
        print(f"Table type: {type(table)}")
        
        pw.run()
        print("Pipeline executed successfully")
        
        # Try to display the table data using Pathway's built-in method
        try:
            print("\nTable data:")
            pw.debug.compute_and_print(table, include_id=False)
        except Exception as e:
            print(f"Error displaying table: {e}")
            print("Table created successfully but cannot display data")
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    test_market_data_connector()