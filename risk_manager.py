import pathway as pw
from typing import Dict, Any

class RiskManager:
    def __init__(self, max_position_size: float = 0.1, max_portfolio_risk: float = 0.05):
        """ initializing risk manager with max position size and max portfolio risk
        max_position_size : maximum percentage of portfolio allowed for a single position
        max_portfolio_risk : maximum percentage of portfolio allowed for risk"""
        self.max_position_size = max_position_size
        self.max_portfolio_risk = max_portfolio_risk
    
    def calculate_position_size(self, signal_strength: float, portfolio_value: float):
        """ Calculate the risk of the portfolio """

        position_multiplier= min(signal_strength/5.0,1.0)
        max_position_value = portfolio_value * self.max_position_size
        return max_position_value * position_multiplier


    def apply_risk_filters(self, signals_table):
        filtered_signals = signals_table.filter(
            pw.this.signal_strength > 1.0 
        )

        risk_adjusted_signals = filtered_signals.select(
            pw.this.symbol,
            pw.this.price,
            pw.this.volume,
            pw.this.timestamp,
            pw.this.signal_strength,
            pw.this.signal_type,
            
            position_size = pw.this.signal_strength*1000,
            risk_score = pw.this.signal_strength/5.0,
            approved = pw.this.signal_strength > 1.5
        )
        return risk_adjusted_signals