from market_data import MarketDataConnector
from signal_detector import SignalDetector
from dotenv import load_dotenv
import os
import pathway as pw
import pandas as pd
load_dotenv()

api_key = os.getenv("POLYGON_API_KEY")
def test_signal_detector():
    connector = MarketDataConnector(api_key= api_key)
    detector = SignalDetector()
    symbols = ["AAPL", "GOOGL"]
    market_table = connector.create_streaming_table(symbols)
    signals_table = detector.detect_signals(market_table)
    pw.run()
    print("Signal detection completed successfully")
    print("Market table:")
    pw.debug.compute_and_print(market_table, include_id=False)
    print("\n Trading Signals:")
    pw.debug.compute_and_print(signals_table, include_id=False)
    
if __name__ == "__main__":
    test_signal_detector()
