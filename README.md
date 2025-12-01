# Samani Financial Analyst

A comprehensive financial analysis application with advanced income statement, balance sheet, and cash flow analysis powered by FinBERT sentiment analysis and GPU acceleration via Modal.

# Hugging Face Space
[![Hugging Face Space](https://img.shields.io/badge/🤗%20Hugging%20Face-Samani%20Fin%20Analyst-blue)](https://huggingface.co/spaces/smainye/samani-fin-analyst)


## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app locally
python src/main.py
```

The Gradio UI will launch at `http://localhost:7860`

## 📊 Features

- **Financial Statement Parsing**: Automated extraction from Excel files (IAS-compliant)
- **Advanced Ratio Analysis**: 20+ financial metrics (profitability, liquidity, efficiency)
- **Sentiment Analysis**: FinBERT-powered tone analysis for financial documents
- **GPU Acceleration**: NVIDIA A10G GPU support via Modal for fast processing
- **Multi-currency Support**: Full support for KES (Kenyan Shilling) and other currencies
- **Interactive UI**: Gradio-based interface for easy file uploads and analysis

## 📁 Project Structure

```
fin_forecasting/
├── src/
│   ├── main.py                 # Application entry point
│   ├── frontend/
│   │   └── gradio_app.py       # Gradio UI
│   └── backend/
│       ├── agent_logic.py      # Main analysis logic
│       ├── modal_server.py     # Modal GPU deployment
│       └── mcp/                # Analysis modules
│           ├── parsing.py
│           ├── ratios.py
│           ├── sentiment.py
│           ├── forecasting.py
│           └── extraction.py
├── financials/                 # Financial data (2020-2024)
├── requirements.txt
└── documentation/              # Full guides and references
```

## 🧠 Analysis Modules

- **Balance Sheet Analysis**: Asset composition, leverage ratios, working capital
- **Income Statement Analysis**: Revenue trends, profitability margins, cost structure
- **Cash Flow Analysis**: Operating cash flow, financing activities, liquidity metrics
- **Advanced Ratios**: ROE, ROA, debt-to-equity, current ratio, efficiency metrics
- **Trend Analysis**: Year-over-year comparisons, moving averages, forecasting
- **Sentiment Analysis**: Tone detection in financial documents
- **Extraction**: Automated line item identification and normalization

## 🌐 Deployment

### Local Development
```bash
python src/main.py
```

### Modal GPU Deployment

**Option 1: Gradio Web App (Recommended - Interactive UI)**
```bash
./deploy_modal_gradio.sh
```
Opens an interactive web interface at: `https://hf-hackathon-mcp--samani-web.modal.run`

**Option 2: Backend Only (API - For integrations)**
```bash
./deploy_modal.sh
```
Deploys compute backend only (no web UI)

View deployment guides: `documentation/MODAL_DEPLOYMENT_GUIDE.md` and `documentation/MODAL_GRADIO_LIVE.md`

## 📚 Documentation

All comprehensive guides are in the `documentation/` folder:

| Document | Purpose |
|----------|---------|
| **MODAL_QUICK_START.md** | 5-minute deployment guide |
| **MODAL_DEPLOYMENT_GUIDE.md** | Complete deployment reference |
| **MODAL_INDEX.md** | Navigation for 3 deployment paths |
| **QUICK_START.md** | Getting started guide |
| **TECHNICAL_REFERENCE.md** | Architecture & API reference |
| **IMPLEMENTATION_SUMMARY.md** | Feature implementation details |
| **ENHANCEMENT_GUIDE.md** | Extension & customization |
| **DEPLOYMENT_CHECKLIST.md** | Pre-deployment verification |
| **DELIVERY_SUMMARY.md** | Full development summary |

## 🔧 Configuration

### Requirements
- Python 3.9+
- torch >= 2.6.0
- transformers
- pandas, openpyxl
- gradio >= 4.0
- Modal (for GPU deployment)

### Environment Variables
```bash
HF_TOKEN=<your_huggingface_token>        # For FinBERT
MODAL_TOKEN_ID=<your_modal_token>        # For GPU deployment
OPEN_AI_API_TOKEN=<optional>             # For extended features
```

## 💱 Currency Support

Default currency: **KES (Kenyan Shilling)**

All financial values are in thousands (KES '000)

## 📈 Financial Data

Sample data included for fiscal years 2020-2024:
- Statement of Financial Position (Balance Sheet)
- Statement of Profit or Loss (Income Statement)
- Statement of Cash Flows

Add your own Excel files to the `financials/` folder organized by year.

## 🎯 Use Cases

- Financial statement analysis and interpretation
- Trend identification and forecasting
- Ratio-based company valuation
- Sentiment tracking in financial reports
- Multi-year comparative analysis
- Risk assessment and monitoring

## ⚡ Performance

- **Local**: ~2-5 seconds per analysis
- **GPU (Modal A10G)**: <1 second per analysis with FinBERT

## 📝 License

See `Fin_analysis/LICENSE` for details

## 🤝 Support

For deployment issues, refer to `documentation/MODAL_DEPLOYMENT_GUIDE.md`

For feature details, see `documentation/TECHNICAL_REFERENCE.md`

---

**Status**: Production-ready with GPU acceleration ✅

