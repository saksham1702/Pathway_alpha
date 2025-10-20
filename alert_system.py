# alert_system.py
import pathway as pw
from datetime import datetime
from typing import Dict, Any

class AlertSystem:
    def __init__(self, alert_threshold: float = 1.5):
        """
        Initialize Alert System
        
        Args:
            alert_threshold: Minimum signal strength to trigger alerts
        """
        self.alert_threshold = alert_threshold
    
    def generate_alerts(self, risk_adjusted_signals):
        """Generate alerts for approved signals"""
        # Filter for approved signals only
        approved_signals = risk_adjusted_signals.filter(
            pw.this.approved == True
        )
        
        # Generate alerts with timestamp
        alerts = approved_signals.select(
            pw.this.symbol,
            pw.this.price,
            pw.this.signal_type,
            pw.this.signal_strength,
            pw.this.position_size,
            pw.this.risk_score,
            alert_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            alert_message = pw.this.symbol + " " + pw.this.signal_type + " signal detected!"
        )
        
        return alerts