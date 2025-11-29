#!/usr/bin/env python3
"""
Modal GPU Deployment for Financial Analysis App
Simplified compute-focused version (no web serving)
"""

import modal
import sys
import os
import base64
import io
from typing import List, Tuple
from pydantic import BaseModel
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define Docker image with all dependencies
image = (
    modal.Image.debian_slim()
    .pip_install(
        "torch==2.2.2",
        "transformers",
        "pandas",
        "openpyxl",
        "pypdf",
        "statsmodels",
        "scipy",
        "numpy<2.0.0",
    )
)

# Create Modal app
app = modal.App("samani-financial-analyst")

# Input/Output schemas
class FileData(BaseModel):
    name: str
    content_b64: str

class QueryRequest(BaseModel):
    files: List[FileData]
    query: str

# GPU-powered analysis class
@app.cls(
    image=image,
    gpu="A10G",  # NVIDIA A10G GPU (24GB VRAM)
    timeout=600,  # 10 minutes
    memory=30000,  # 30GB memory
)
class FinancialAnalyzer:
    """Financial analysis engine running on A10G GPU"""
    
    def __enter__(self):
        """Setup when container starts"""
        print("🟢 Loading FinBERT model on A10G GPU...")
        import torch
        from transformers import pipeline
        
        # Load sentiment model on GPU
        device = 0 if torch.cuda.is_available() else -1
        self.nlp = pipeline(
            "sentiment-analysis",
            model="yiyanghkust/finbert-tone",
            device=device
        )
        print("✅ FinBERT loaded on GPU")
        sys.path.insert(0, "/root")
        return self

    @modal.method()
    def analyze(self, files: List[FileData], query: str) -> Tuple[str, str]:
        """
        Process financial files and return analysis
        
        Args:
            files: List of financial documents (base64 encoded)
            query: Analysis query from user
        
        Returns:
            (analysis_result, status_message)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"[{timestamp}] 📊 Received analysis request: {len(files)} files, query='{query[:50]}'")
        
        try:
            # Import analysis modules
            from src.backend.mcp.parsing import parse_file
            from src.backend.agent_logic import process_request
            import src.backend.mcp.sentiment as sentiment_module
            
            # Reconstruct files from base64
            file_objects = []
            for f in files:
                decoded = base64.b64decode(f.content_b64)
                file_obj = io.BytesIO(decoded)
                file_obj.name = f.name
                file_objects.append(file_obj)
                logging.debug(f"   ✓ Loaded file: {f.name}")
            
            # Use GPU-loaded sentiment model
            sentiment_module.nlp = self.nlp
            
            # Run analysis
            logging.info(f"[{timestamp}] ⚙️  Processing analysis...")
            result, logs = process_request(file_objects, query)
            
            logging.info(f"[{timestamp}] ✅ Analysis complete - returning results")
            return result, logs
            
        except Exception as e:
            error_msg = f"Error during analysis: {str(e)}"
            logging.error(f"[{timestamp}] ❌ {error_msg}")
            return "", error_msg

# CLI entry point for testing
@app.local_entrypoint()
def main():
    """Test the deployment locally"""
    print("✅ Modal app deployed successfully!")
    print("\nTo use from Python:")
    print("  analyzer = FinancialAnalyzer()")
    print("  result, logs = analyzer.analyze.remote(files, query)")
