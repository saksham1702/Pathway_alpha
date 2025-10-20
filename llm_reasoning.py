import pathway as pw 
from typing import Dict, Any, List 
import json 
from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq
import requests
api_key = os.getenv("GROQ_API_KEY")

class LLMReasoningEngine:
    def __init__(self, groq_api_key: str = None):
        self.groq_api_key = groq_api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model_name = "llama-3.1-8b-instant"

    def generate_trading_insights(self, signals_table):
        """ Generate trading insights using LLM """
        insights = signals_table.select(
            pw.this.symbol,
            pw.this.signal_type,
            pw.this.signal_strength,
            pw.this.price,
            pw.this.volume,
            pw.this.timestamp,
            pw.this.position_size,
            pw.this.risk_score,
            pw.this.approved,
            
            market_sentiment = pw.if_else(
            pw.this.signal_strength > 2.0,
            "Strong Bullish Momentum",
            pw.if_else(
                pw.this.signal_strength >1.0,
                "Moderate Positive Movement",
                "Weak Signal - Monitor Closely"
            )
        ),
        risk_assessment = pw.if_else(
            pw.this.risk_score > 0.5,
            "High Risk - Hold Position",
            pw.if_else(
                pw.this.risk_score > 0.2,
                "Moderate Risk - Monitor Closely",
                "Low Risk - Consider Entry"
            )
        ),

            trading_recommendation = pw.if_else(
                pw.this.approved == True,
                pw.if_else(
                    pw.this.signal_strength > 2.5,
                    "Strong BUY - High Confidence",
                    "BUY - Good Opportunity"
                ),
                "HOLD - Wait for Better Entry"
            ),

            confidence_score = pw.this.signal_strength * (pw.this.volume / 1000000)
)
        return insights

    def generate_portfolio_summary(self, insights_table):
        """ Generate portfolio summary using LLM """
        approved_signals = insights_table.filter(pw.this.approved == True)

        #create portfolio summary table
        portfolio_summary = approved_signals.select(
            pw.this.symbol,
            pw.this.trading_recommendation,
            pw.this.confidence_score,
            pw.this.market_sentiment,
            pw.this.risk_assessment,
            pw.this.position_size,

            portfolio_allocation = pw.if_else(
                pw.this.confidence_score > 1000,
                "Allocate 5-10% of portfolio",
                pw.if_else(
                    pw.this.confidence_score > 500,
                    "Allocate 2-5% of portfolio",
                    "Allocate 1-2% of portfolio"
                )
            )
        )
        return portfolio_summary

    def call_groq_llama(self, prompt: str)->str:
        """ Call the Groq LLama API for advanced reasoning"""
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional financial analyst. You are given a prompt and you need to reason about the prompt and provide a detailed analysis of the prompt."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000, 
            "temperature": 0.3
        }
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error calling Groq LLama API: {e}"

    def generate_llm_insights(self , approved_signals_data):
        """ genrate LLM-powered insights from approved signals"""

        llm_insights = []
        for signal in approved_signals_data:
            prompt = f"""
        Analyze this trading signal:
        - Stock: {signal['symbol']}
        - Price: ${signal['price']}
        - Signal Strength: {signal['signal_strength']}%
        - Volume: {signal['volume']}
        - Risk Score: {signal['risk_score']}

        Provide a brief analysis and recommendation.
        """ 
        llm_response = self.call_groq_llama(prompt)
        llm_insights.append(
            {
                'symbol': signal['symbol'],
                'analysis': llm_response,
                'original_signal': signal
            }
        )
        return llm_insights
        