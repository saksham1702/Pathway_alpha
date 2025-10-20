## Stream Trader (Pathway Financial AI Agent)

Real-time financial AI agent built on the Pathway streaming engine. Ingests market data, detects signals, applies risk management, generates LLM-driven insights (Groq Llama), and emits alerts — all in one production-lean pipeline.

### Features
- Streaming market data ingestion (Polygon.io)
- Signal detection with thresholds (BUY/SELL/HOLD)
- Risk management: filtering, position sizing, approvals
- LLM insights via Groq Llama (explanations, recommendations)
- Alerts for approved opportunities

### Project Structure
```
market_data.py            # MarketDataConnector (Polygon.io)
signal_detector.py        # SignalDetector (rules via Pathway)
risk_manager.py           # Risk filters, sizing, approvals
alert_system.py           # Alert generation on approved signals
llm_reasoning.py          # Rule-based insights + Groq Llama calls
financial_ai_pipeline.py  # Orchestration (single run + monitoring)
test_connector.py         # Basic connector test
test_signal_detector.py   # Signals pipeline test
```

### Requirements
- Python 3.11+
- Pathway
- pandas, requests, python-dotenv
- Groq Python client or HTTP (we use HTTP via `requests`)

Install from `requirements.txt`:
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` in repo root:
```
POLYGON_API_KEY=your_polygon_api_key
GROQ_API_KEY=your_groq_api_key
```

### Quick Start
Run the full pipeline (single analysis):
```bash
source env/bin/activate
python financial_ai_pipeline.py
```
The script will:
- Fetch live/simulated previous-day data for symbols
- Build streaming tables in Pathway
- Detect signals and apply risk
- Generate AI insights and alerts
- Print results to console

### How Streaming Works (Pathway)
Pathway builds a lazy computation graph; `pw.run()` executes it. Tables (e.g., signals, risk-adjusted signals, insights) update as new data arrives in a streaming setup. We use `pw.debug.compute_and_print(table)` to display table contents after execution.

### LLM Integration (Groq Llama)
- Rule-based insights are computed inside Pathway for real-time speed
- Approved signals are exported post-run and sent to Groq Llama for natural-language analysis
- Update `.env` with `GROQ_API_KEY`

### Configuration
Edit symbols and thresholds in `financial_ai_pipeline.py` and `SignalDetector`/`RiskManager`:
```python
SignalDetector(buy_threshold=0.015, sell_threshold=-0.015)
RiskManager(max_position_size=0.1, max_portfolio_risk=0.05)
symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
```

### Testing Snippets
Connector test:
```bash
python test_connector.py
```
Signals test:
```bash
python test_signal_detector.py
```

### Common Issues
- Missing API key → ensure `.env` is in repo root and sourced by `python-dotenv`
- Pathway errors about `.to_pandas()` → use `pw.debug.compute_and_print` or export via non-streaming paths
- Groq 401 Unauthorized → verify `GROQ_API_KEY` and network access

### Roadmap / Next Steps
- Observability: metrics (latency, counts), structured JSON logs
- Scenario tests: late events, API timeouts, retries/backoff
- Dockerfile + launch scripts for one-command run
- Dashboard sink (DB/CSV/web) for signals and alerts

### License
Proprietary (update as needed).


