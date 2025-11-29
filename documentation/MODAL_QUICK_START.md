# 🚀 Modal Deployment - Quick Reference

## TL;DR - Deploy in 3 Commands

```bash
# 1. Install & Authenticate
pip install modal
modal token new

# 2. Deploy
./deploy_modal.sh

# 3. Your app is live! 🎉
```

---

## What You Get

✅ **NVIDIA A10G GPU** (24GB VRAM)  
✅ **FinBERT Model** (pre-loaded)  
✅ **Auto-Scaling** (handles spikes)  
✅ **HTTPS Endpoint** (secure API)  
✅ **Pay-Per-Use** (~$0.40/hr when running)  

---

## Key Commands

```bash
# Deploy app
./deploy_modal.sh
modal deploy src/backend/modal_server.py

# View logs
modal logs samani-financial-analyst

# Monitor app
modal get-app samani-financial-analyst
modal dashboard

# Stop app
modal delete app samani-financial-analyst

# Serve locally with GPU
modal serve src/backend/modal_server.py
```

---

## API Endpoint Usage

```python
import requests
import base64

MODAL_URL = "https://your-username--samani-financial-analyst.modal.run"

# Prepare files
files_data = []
for file_path in ["statement1.xlsx", "statement2.xlsx"]:
    with open(file_path, "rb") as f:
        files_data.append({
            "name": file_path,
            "content_b64": base64.b64encode(f.read()).decode()
        })

# Send request
response = requests.post(
    f"{MODAL_URL}/analyze_financials",
    json={
        "files": files_data,
        "query": "Advanced ratio analysis"
    }
)

result = response.json()
print(result["response"])
```

---

## GPU Options

| GPU | VRAM | Cost/hr | Best For |
|-----|------|---------|----------|
| **A10G** | 24GB | $0.40 | ✅ FinBERT (Default) |
| A100 | 40GB | $1.10 | Larger models |
| H100 | 80GB | $1.98 | LLMs |

**Change GPU** in `src/backend/modal_server.py` line 35:
```python
@app.cls(image=image, gpu="A10G", ...)  # ← Change this
```

---

## Troubleshooting

**App won't deploy?**
```bash
# Check logs
modal logs samani-financial-analyst

# Rebuild
modal deploy --force src/backend/modal_server.py
```

**API returns errors?**
```bash
# Check container is running
modal get-app samani-financial-analyst

# View real-time logs
modal logs -f samani-financial-analyst
```

**Want to test locally first?**
```bash
# Serve with GPU locally
modal serve src/backend/modal_server.py

# Then test at: http://localhost:8000
```

---

## Cost Estimate

| Daily Analyses | Monthly Cost |
|---|---|
| 10 | ~$2.40 |
| 50 | ~$12 |
| 100 | ~$24 |
| 500 | ~$120 |

*Only charged when container is active*

---

## Links

📖 [Full Deployment Guide](./MODAL_DEPLOYMENT_GUIDE.md)  
🌐 [Modal Docs](https://modal.com/docs)  
💰 [Pricing](https://modal.com/pricing)  
🆘 [Community](https://modal.com/community)  

---

## Next: Integrate with Gradio

Modify `src/frontend/gradio_app.py`:

```python
import os
MODAL_URL = os.getenv("MODAL_URL", "http://localhost:7860")

def process_request_modal(files, query):
    """Send to Modal backend instead of local"""
    import requests
    import base64
    
    files_data = [{
        "name": f.name,
        "content_b64": base64.b64encode(open(f.name, 'rb').read()).decode()
    } for f in files]
    
    response = requests.post(
        f"{MODAL_URL}/analyze_financials",
        json={"files": files_data, "query": query}
    )
    return response.json()["response"], ""
```

---

**Ready?** Run: `./deploy_modal.sh` 🚀
