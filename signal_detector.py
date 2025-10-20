import pathway as pw 
from typing import Dict, Any

class SignalDetector:
    def __init__(self,buy_threshold: float = 0.02, sell_threshold: float = -0.02):
        """ initializing signal detector with threshold parameters
        buy threshold : maximum price increase around ~2% to trigger the buying
        sell threshold : maximum price decrease around ~2% to trigger the selling """
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def detect_signals(self, market_data_table):
        """ Analyse market and generate trading signals 
        Args:
        market_data_table : pathway table with stock data
        Returns:
        pathway table with trading signals"""
        signals = market_data_table.select(
            pw.this.symbol,
            pw.this.price,
            pw.this.change_percent,
            pw.this.volume,
            pw.this.timestamp,
            signal_type = pw.if_else(
                pw.this.change_percent > self.buy_threshold,
                "BUY",
                pw.if_else(
                    pw.this.change_percent < self.sell_threshold,
                    "SELL",
                    "HOLD"
                )
            ),
            signal_strength = pw.this.change_percent
        )
        return signals