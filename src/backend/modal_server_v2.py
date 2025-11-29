import modal
import sys
import os
import base64
import io
from typing import List
from pydantic import BaseModel

# 1. Define the Container Image
image = (
    modal.Image.debian_slim()
    .pip_install(
        "torch", 
        "transformers", 
        "pandas", 
        "openpyxl", 
        "pypdf", 
        "statsmodels", 
        "scipy", 
        "numpy",
        "fastapi"
    )
    # Pre-download FinBERT model
    .run_commands(
        "python -c 'from transformers import BertTokenizer, BertForSequenceClassification; "
        "BertTokenizer.from_pretrained(\"yiyanghkust/finbert-tone\"); "
        "BertForSequenceClassification.from_pretrained(\"yiyanghkust/finbert-tone\")'"
    )
)

app = modal.App("samani-financial-analyst")

# 2. Input Schema
class FileData(BaseModel):
    name: str
    content_b64: str

class QueryRequest(BaseModel):
    files: List[FileData]
    query: str

# 3. GPU-powered Analysis Class
@app.cls(image=image, gpu="A10G", timeout=600)
class FinancialAgent:
    def __enter__(self):
        """Initialize FinBERT on GPU"""
        print("🟢 Loading FinBERT on NVIDIA A10G...")
        import torch
        from transformers import BertTokenizer, BertForSequenceClassification, pipeline
        
        device = 0 if torch.cuda.is_available() else -1
        self.tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
        self.model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')
        self.nlp = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer, device=device)
        print("✅ FinBERT Loaded on GPU")
        sys.path.append("/root")
        return self

    @modal.method()
    def process(self, files: List[FileData], query: str):
        """Process financial files and run analysis"""
        # Import backend modules
        from src.backend.mcp.parsing import parse_file
        from src.backend.agent_logic import process_request
        
        # Reconstruct files from base64
        reconstructed_files = []
        for f in files:
            decoded = base64.b64decode(f.content_b64)
            file_obj = io.BytesIO(decoded)
            file_obj.name = f.name
            reconstructed_files.append(file_obj)
        
        # Inject GPU-loaded model
        import src.backend.mcp.sentiment as sentiment_module
        sentiment_module.nlp = self.nlp 
        
        # Run analysis
        return process_request(reconstructed_files, query)

# 4. Direct Python API (can be called from anywhere)
@app.local_entrypoint()
def main(query: str = "Advanced ratio analysis"):
    """Local test endpoint"""
    print(f"Query: {query}")
    print("Running on local GPU support")

# 5. FastAPI web endpoint (if needed for HTTP)
try:
    from modal import fastapi_app
    
    web_app = fastapi_app()
    
    @web_app.post("/analyze_financials")
    async def analyze_endpoint(item: QueryRequest):
        """HTTP endpoint for analysis"""
        agent = FinancialAgent()
        result, logs = await agent.process.remote(item.files, item.query)
        return {"response": result, "logs": logs}
except ImportError:
    # Fallback if fastapi not available
    print("FastAPI not available - using CLI only")
