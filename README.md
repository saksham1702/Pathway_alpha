# Stream Trader (Pathway Financial AI Agent)

Real-time financial AI agent built on the Pathway streaming engine. Ingests market data, detects signals, applies risk management, generates LLM-driven insights (Groq Llama), and emits alerts — all in one production-lean pipeline.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker Desktop installed
- GitHub account (to clone the repository)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
# Copy the example and add your API keys
cp .env.example .env
# Edit .env with your actual API keys
```

Add your API keys to `.env`:
```env
POLYGON_API_KEY=your_polygon_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run with Docker
```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f financial-ai

# Stop the container
docker-compose down
```

### 4. Monitor the Pipeline
```bash
# Check container status
docker ps

# View resource usage
docker stats financial-ai-pipeline

# Get a shell inside the container
docker exec -it financial-ai-pipeline bash
```

## 🏗️ Manual Setup (Without Docker)

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
```env
POLYGON_API_KEY=your_polygon_api_key
GROQ_API_KEY=your_groq_api_key
```

### Run the Pipeline
```bash
source env/bin/activate
python financial_ai_pipeline.py
```

## ✨ Features
- **Streaming market data ingestion** (Polygon.io)
- **Signal detection** with configurable thresholds (BUY/SELL/HOLD)
- **Risk management**: filtering, position sizing, approvals
- **LLM insights** via Groq Llama (explanations, recommendations)
- **Real-time alerts** for approved opportunities
- **Docker deployment** for easy setup and scaling
- **Modular architecture** for easy extension

## 📁 Project Structure
```
src/
├── connectors/
│   └── market_data.py          # MarketDataConnector (Polygon.io)
├── signal_detector.py           # SignalDetector (rules via Pathway)
├── risk_manager.py             # Risk filters, sizing, approvals
├── alert_system.py             # Alert generation on approved signals
├── llm_reasoning.py            # Rule-based insights + Groq Llama calls
└── financial_ai_pipeline.py   # Orchestration (single run + monitoring)

# Docker files
Dockerfile                      # Container configuration
docker-compose.yaml            # Orchestration
requirements.txt               # Python dependencies
.dockerignore                  # Docker ignore patterns
.env.example                   # Environment template

# Testing
test_connector.py              # Basic connector test
test_signal_detector.py        # Signals pipeline test

# Documentation
README.md                      # This file
docker_deployment_guide.md     # Detailed Docker setup
fraud_monitor_plan.md          # Future fraud detection system
```

## 🔧 How It Works

### Streaming Architecture (Pathway)
Pathway builds a lazy computation graph; `pw.run()` executes it. Tables (e.g., signals, risk-adjusted signals, insights) update as new data arrives in a streaming setup. We use `pw.debug.compute_and_print(table)` to display table contents after execution.

### LLM Integration (Groq Llama)
- **Rule-based insights** are computed inside Pathway for real-time speed
- **Approved signals** are exported post-run and sent to Groq Llama for natural-language analysis
- **Hybrid approach**: Fast streaming + Deep LLM analysis for approved signals

### Configuration
Edit symbols and thresholds in `financial_ai_pipeline.py` and `SignalDetector`/`RiskManager`:
```python
SignalDetector(buy_threshold=0.015, sell_threshold=-0.015)
RiskManager(max_position_size=0.1, max_portfolio_risk=0.05)
symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
```

## 🧪 Testing

### Individual Components
```bash
# Test market data connector
python test_connector.py

# Test signal detection
python test_signal_detector.py
```

### Docker Testing
```bash
# Test Docker build
docker build -t financial-ai .

# Test with docker-compose
docker-compose up -d
docker-compose logs -f financial-ai
```

## 🐛 Troubleshooting

### Common Issues
- **Missing API key** → ensure `.env` is in repo root and sourced by `python-dotenv`
- **Pathway errors** about `.to_pandas()` → use `pw.debug.compute_and_print` or export via non-streaming paths
- **Groq 401 Unauthorized** → verify `GROQ_API_KEY` and network access
- **Docker build fails** → check Docker Desktop is running and you have internet connection
- **Container won't start** → check API keys in `.env` file

### Docker Debugging
```bash
# Check container status
docker ps

# View detailed logs
docker-compose logs financial-ai

# Get shell access
docker exec -it financial-ai-pipeline bash

# Check resource usage
docker stats financial-ai-pipeline
```

## 🚀 Deployment Options

### Local Development
- Use Docker Compose for easy local development
- Mount volumes for data persistence
- Hot-reload with volume mounts

### Production Deployment
- Push to container registry (Docker Hub, AWS ECR)
- Deploy to cloud services (AWS ECS, Google Cloud Run, Azure Container Instances)
- Set up monitoring and health checks
- Configure auto-scaling

## 📈 Roadmap

### ✅ Completed
- [x] Core streaming pipeline with Pathway
- [x] Market data ingestion (Polygon.io)
- [x] Signal detection and risk management
- [x] LLM integration (Groq Llama)
- [x] Docker deployment
- [x] Real-time alerts

### 🔄 In Progress
- [ ] Observability dashboard with metrics and traces
- [ ] Testing framework with scenario tests
- [ ] Comprehensive documentation

### 📋 Future Features
- [ ] Fraud detection system (see `fraud_monitor_plan.md`)
- [ ] Web dashboard for monitoring
- [ ] Backtesting capabilities
- [ ] Multi-asset support (crypto, forex)
- [ ] Advanced ML models integration

## 📄 License
Proprietary (update as needed).

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## 📞 Support
- Check the troubleshooting section above
- Review `docker_deployment_guide.md` for detailed Docker setup
- See `fraud_monitor_plan.md` for future fraud detection system


