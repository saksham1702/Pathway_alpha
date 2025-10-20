import pathway as pw
from market_data import MarketDataConnector
from signal_detector import SignalDetector
from typing import Dict, List, Any
import time
from datetime import datetime
from dotenv import load_dotenv
import os
from risk_manager import RiskManager
from alert_system import AlertSystem
from llm_reasoning import LLMReasoningEngine
load_dotenv()

class FinancialAIpipeline:
    def __init__(self,  api_key: str,symbols: List[str]):
        self.symbols = symbols
        self.connector = MarketDataConnector(api_key= api_key)
        self.signal_detector = SignalDetector(
            buy_threshold= 0.015,
            sell_threshold= -0.015
        )
        self.risk_manager = RiskManager(
            max_position_size= 0.1,
            max_portfolio_risk= 0.05
        )
        self.alert_system = AlertSystem(
            alert_threshold= 1.5
        )
        self.llm_engine = LLMReasoningEngine(groq_api_key=os.getenv("GROQ_API_KEY"))

    def run_signal_analysis(self):
        """ Run the signal analysis pipeline """
        print(f"\n{'='*50}")
        print(f"Financial AI Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")

        market_table = self.connector.create_streaming_table(self.symbols)
        signals_table = self.signal_detector.detect_signals(market_table)
        risk_signals_table = self.risk_manager.apply_risk_filters(signals_table)
        insights_table = self.llm_engine.generate_trading_insights(risk_signals_table)
        alerts = self.alert_system.generate_alerts(risk_signals_table)

        filtered_table = risk_signals_table.filter(pw.this.approved == True)
        pw.run() 
        approved_df = pw.debug.table_to_pandas(filtered_table)

        approved_signals_data = []
        try:

            for _ , row in approved_df.iterrows():
                approved_signals_data.append(row.to_dict())

            if approved_signals_data:
                llm_signals = self.llm_engine.generate_llm_insights(approved_signals_data)
                print("\n🤖 LLM-Powered Trading Insights:")
                for insight in llm_signals:
                    print(f"\nStock: {insight['symbol']}")
                    print(f"Analysis: {insight['analysis']}")
        except Exception as e:
            print(f"Error generating LLM insights: {e}")


        print("Signal analysis completed successfully")
        print("Market table:")
        pw.debug.compute_and_print(market_table, include_id=False)

        print("\n Trading Signals:")
        pw.debug.compute_and_print(signals_table, include_id=False)

        print("\n Risk-Adjusted signals")
        pw.debug.compute_and_print(risk_signals_table, include_id=False)
        
        print("\n🤖 AI Trading Insights:")
        pw.debug.compute_and_print(insights_table, include_id=False)
        
        print("\n🚨 Trading Alerts:")
        pw.debug.compute_and_print(alerts, include_id=False)
        
        return insights_table


    def run_continuous_monitoring(self, interval_seconds: int = 300):
        """ Run the continuous monitoring pipeline """
        print(f" Starting continuous monitoring of {self.symbols}")
        print(f" Update interval: {interval_seconds} seconds")

        while True:
            try:
                self.run_signal_analysis()
                print(f"\n⏳ Waiting {interval_seconds} seconds for next update...")
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                print("\n🛑 Monitoring interrupted by user")
                break
            except Exception as e:
                print(f"Error: {e}")
                print("Retrying in 60 seconds...")
                time.sleep(60)
    

if __name__ == "__main__":
    api_key = os.getenv("POLYGON_API_KEY")
    
    # Define stocks to monitor
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    
    # Create and run the pipeline
    pipeline = FinancialAIpipeline(api_key, symbols)
    
    # Run a single analysis
    print("Running Financial AI Analysis...")
    pipeline.run_signal_analysis()