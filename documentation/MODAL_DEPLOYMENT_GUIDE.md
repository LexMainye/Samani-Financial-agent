# 🚀 Modal GPU Deployment Guide

**Host Your Financial Analysis App on Modal with NVIDIA A10 GPUs**

---

## 📋 Quick Start

Deploy your app to Modal cloud in 3 steps:

```bash
# 1. Install Modal CLI
pip install modal

# 2. Authenticate with Modal
modal token new

# 3. Deploy the app
modal deploy src/backend/modal_server.py
```

✅ Your app will be live at a Modal-provided URL!

---

## 🎯 What is Modal?

Modal is a serverless platform that:
- ✅ Runs Python code on GPU-powered cloud infrastructure
- ✅ Auto-scales based on demand
- ✅ Charges only for compute used (pay-per-invocation)
- ✅ No DevOps needed
- ✅ Includes NVIDIA A10, A100, and H100 GPUs

**Your app**: Sentiment analysis + Financial Ratio calculations = Perfect for GPU acceleration

---

## 🔧 Setup Steps

### Step 1: Install Modal
```bash
pip install modal
```

### Step 2: Create Modal Account & Authenticate
```bash
# Create account at https://modal.com
# Then authenticate locally:
modal token new

# Follow the prompts to log in via browser
# This creates ~/.modal/config_staging.json
```

### Step 3: Review Deployment Config
The app is pre-configured with:
- **GPU**: NVIDIA A10G (performant for ML inference)
- **Memory**: 30GB VRAM (sufficient for FinBERT)
- **Timeout**: 10 minutes per request
- **Model**: yiyanghkust/finbert-tone (pre-loaded in image)

Located in: `src/backend/modal_server.py`

### Step 4: Deploy
```bash
modal deploy src/backend/modal_server.py
```

Expected output:
```
✓ Created app 'samani-financial-analyst'
✓ Building image...
✓ Starting GPU container...
✅ Deployed at: https://your-username--samani-financial-analyst.modal.run
```

---

## 💡 How It Works

### Architecture

```
┌─────────────────────────────────────────┐
│    Your Laptop (Gradio UI)              │
│    ./run.sh or python3 src/main.py      │
└──────────────┬──────────────────────────┘
               │ Upload files + Query
               ▼
┌──────────────────────────────────────────────────┐
│    Modal Cloud (NVIDIA A10G GPU)                 │
├──────────────────────────────────────────────────┤
│  Container:                                      │
│  • Python + PyTorch + Transformers               │
│  • FinBERT model (pre-loaded)                    │
│  • Your src/ code                                │
│  • Parse & Analyze files                         │
└──────────────┬───────────────────────────────────┘
               │ Return analysis results
               ▼
┌────────────────────────────────────┐
│    Display in Gradio UI            │
│    (Ratio, Sentiment, Forecast)    │
└────────────────────────────────────┘
```

### What Happens When You Deploy

1. **Image Building** (once per deploy)
   - Modal creates a Docker image with all dependencies
   - Pre-downloads FinBERT model to avoid cold starts
   - Result: ~200MB Docker image

2. **API Endpoint** (always running)
   - `/analyze_financials` endpoint is live
   - Listens for POST requests
   - Auto-scales to handle multiple concurrent requests

3. **GPU Container** (warm start)
   - NVIDIA A10G GPU reserved
   - FinBERT model stays in GPU memory
   - Ready for instant inference

4. **Billing**
   - Only charged when container is active
   - ~$0.40/hour for A10G GPU
   - Containers auto-suspend after idle timeout

---

## 📱 Using the Deployed App

### Local Gradio Interface (Calls Modal Backend)

You can modify `src/frontend/gradio_app.py` to call the Modal API:

```python
import requests

MODAL_API_URL = "https://your-username--samani-financial-analyst.modal.run"

def process_request_remote(files, query):
    """Send request to Modal backend"""
    payload = {
        "files": [
            {"name": f.name, "content_b64": base64.b64encode(open(f.name, 'rb').read()).decode()}
            for f in files
        ],
        "query": query
    }
    response = requests.post(f"{MODAL_API_URL}/analyze_financials", json=payload)
    return response.json()["response"], response.json()["logs"]
```

### Or: Full Cloud Deployment

Deploy a cloud-hosted Gradio UI on Modal:

```bash
modal serve src/backend/modal_server.py
```

This serves both:
- Gradio UI (web interface)
- API endpoints (for external calls)

---

## 🖥️ Choosing the Right GPU

| GPU | VRAM | Cost/hr | Best For |
|-----|------|---------|----------|
| **A10G** | 24GB | $0.40 | ✅ FinBERT, Transformer models |
| A100 | 40GB | $1.10 | Large models, batch processing |
| H100 | 80GB | $1.98 | LLMs, multi-model inference |
| CPU | - | $0.05 | Ratio calculation only |

**Your app choice: A10G** - Perfect balance of performance & cost

---

## 🔐 Security & Best Practices

### 1. Protect API Key
```bash
# Store Modal token securely
export MODAL_TOKEN_ID="your-token-id"
export MODAL_TOKEN_SECRET="your-token-secret"
```

### 2. Add Authentication to API
```python
@app.function()
@modal.web_endpoint(method="POST")
def analyze_financials(item: QueryRequest):
    # Add API key check
    api_key = item.get("api_key")
    if api_key != os.getenv("APP_API_KEY"):
        return {"error": "Unauthorized"}
    
    # ... rest of logic
```

### 3. Enable HTTPS
Modal endpoints are auto-HTTPS by default ✅

### 4. Monitor Usage
```bash
# View app logs
modal logs samani-financial-analyst

# Check container status
modal get-app samani-financial-analyst
```

---

## 🐛 Troubleshooting

### Container fails to start
```bash
# Check logs
modal logs samani-financial-analyst

# Common issues:
# - Torch compatibility: Ensure torch>=2.6.0
# - VRAM exceeded: Model too large for GPU
# - Dependencies missing: Check requirements.txt
```

### Slow performance
```bash
# Modal runs containers in ~2 second cold start
# Subsequent requests use warm container (~100ms)

# To keep container warm:
# Set longer timeout or ping endpoint periodically
```

### Model download fails
```bash
# Pre-download model in image build:
modal_server.py already handles this

# If still failing, manually pre-download:
python -c "from transformers import AutoModel; AutoModel.from_pretrained('yiyanghkust/finbert-tone')"
```

---

## 📊 Monitoring & Optimization

### Monitor Costs
```bash
# View usage dashboard
modal dashboard  # Opens at https://modal.com/account/usage

# Estimated cost for your app:
# - FinBERT inference: ~50ms per request
# - A10G: $0.40/hour = $0.00011 per request
# - 1000 analyses/day = ~$0.11/day
```

### Optimize Performance
```python
# 1. Batch requests
@modal.method()
def process_batch(self, requests: List[QueryRequest]):
    # Process multiple files together
    results = []
    for req in requests:
        results.append(self.process(req.files, req.query))
    return results

# 2. Cache model at container level
# (Already done in modal_server.py via @app.cls)

# 3. Use lighter model for sentiment if needed
# Replace 'yiyanghkust/finbert-tone' with distilbert variant
```

---

## 🚀 Advanced: Custom GPU Deployment

### Use H100 for Faster Inference
```python
@app.cls(image=image, gpu="H100", mounts=[local_src], timeout=600)
class FinancialAgent:
    # Same code, different GPU
```

### Use Multiple GPUs
```python
@app.cls(image=image, gpu=modal.gpu.A100(count=2), mounts=[local_src])
class FinancialAgent:
    # Use 2x A100 GPUs for parallel processing
```

### Custom Image with More Dependencies
```python
image = (
    modal.Image.debian_slim()
    .pip_install("torch", "transformers", "pandas", ...)
    .apt_install("libsm6", "libxext6")  # Additional system libs
    .run_commands(
        "git clone https://github.com/custom-repo.git"
    )
)
```

---

## 📝 Deployment Checklist

- [ ] Modal account created at https://modal.com
- [ ] Modal CLI installed: `pip install modal`
- [ ] Authenticated: `modal token new`
- [ ] Reviewed `src/backend/modal_server.py`
- [ ] Verified GPU choice: A10G (default)
- [ ] Checked `requirements.txt` for all dependencies
- [ ] Deployed: `modal deploy src/backend/modal_server.py`
- [ ] Tested endpoint with sample request
- [ ] Set up monitoring/alerts
- [ ] Documented API endpoint URL
- [ ] Added API key authentication (recommended)

---

## 🎓 Example: End-to-End Deployment

### Step 1: Setup
```bash
cd /Users/alexmainye/Documents/Projects/fin_forecasting
source venv/bin/activate
pip install modal
modal token new
```

### Step 2: Deploy
```bash
modal deploy src/backend/modal_server.py
```

Output:
```
✓ Created app 'samani-financial-analyst'
✓ Mounted /root/src from local directory
✓ Building image...
  • Installing pip packages...
  • Pre-downloading FinBERT model...
✓ Created GPU container (A10G)
✅ App live at: https://alexmainye--samani-financial-analyst.modal.run

To call the API:
  curl -X POST https://alexmainye--samani-financial-analyst.modal.run/analyze_financials \
    -H "Content-Type: application/json" \
    -d '{"files": [...], "query": "Advanced ratio analysis"}'
```

### Step 3: Test
```bash
# Upload files and query
curl -X POST https://alexmainye--samani-financial-analyst.modal.run/analyze_financials \
  -H "Content-Type: application/json" \
  -d '{
    "files": [{"name": "statement.xlsx", "content_b64": "..."}],
    "query": "Cash flow analysis"
  }'
```

### Step 4: Use from Gradio
```python
# In gradio_app.py
MODAL_URL = "https://alexmainye--samani-financial-analyst.modal.run"

def submit_with_modal(files, query):
    response = requests.post(f"{MODAL_URL}/analyze_financials", json={
        "files": files,
        "query": query
    })
    return response.json()["response"]
```

---

## 💰 Cost Breakdown

| Usage | GPU Hours | Cost |
|-------|-----------|------|
| 10 analyses/day | 0.17 hrs/month | ~$2.40/month |
| 100 analyses/day | 1.7 hrs/month | ~$24/month |
| 1000 analyses/day | 17 hrs/month | ~$240/month |

**Includes**: API endpoint, GPU compute, auto-scaling

---

## 🔗 Resources

- **Modal Documentation**: https://modal.com/docs
- **GPU Options**: https://modal.com/docs/reference/model#modal.gpu
- **Pricing**: https://modal.com/pricing
- **Community**: https://modal.com/community

---

## ❓ FAQ

**Q: Can I use different GPU?**  
A: Yes! Change `gpu="A10G"` to `gpu="A100"` or `gpu="H100"` in modal_server.py

**Q: How long does deployment take?**  
A: 2-5 minutes for first deploy (image build). Subsequent deploys: 30 seconds.

**Q: Is my data secure?**  
A: Yes. Files are processed server-side only. No logs stored. HTTPS encrypted.

**Q: Can I use GPU without Modal?**  
A: Yes! Use any GPU cloud provider (AWS SageMaker, Google Colab, Lambda Labs, etc.)

**Q: How do I stop the app?**  
A: `modal delete app samani-financial-analyst` or let it auto-suspend on idle.

---

**Ready to go cloud?** 🚀

```bash
modal deploy src/backend/modal_server.py
```

Your app will be live in seconds with auto-scaling GPU support!
