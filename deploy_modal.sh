#!/bin/bash

# 🚀 Modal Deployment Script for Financial Analysis App
# Usage: ./deploy_modal.sh

set -e

echo "=================================================="
echo "🚀 Samani Financial Analyst - Modal Deployment"
echo "=================================================="
echo ""

# Check if Modal is installed
if ! command -v modal &> /dev/null; then
    echo "📦 Installing Modal CLI..."
    pip install modal
fi

# Check if authenticated
if [ ! -f ~/.modal/config_staging.json ]; then
    echo ""
    echo "🔐 Modal authentication required"
    echo "   Running: modal token new"
    echo ""
    modal token new
fi

echo ""
echo "📝 Deployment Configuration:"
echo "   App Name: samani-financial-analyst"
echo "   GPU: NVIDIA A10G (24GB VRAM)"
echo "   Model: FinBERT (yiyanghkust/finbert-tone)"
echo "   Timeout: 10 minutes"
echo ""

# Verify key files exist
if [ ! -f "src/backend/modal_server.py" ]; then
    echo "❌ Error: src/backend/modal_server.py not found"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    exit 1
fi

echo "🔍 Verifying dependencies..."
grep -q "torch" requirements.txt && echo "   ✅ torch"
grep -q "transformers" requirements.txt && echo "   ✅ transformers"
grep -q "pandas" requirements.txt && echo "   ✅ pandas"

echo ""
echo "🚀 Deploying to Modal..."
echo "   This may take 2-5 minutes on first deploy"
echo ""

# Deploy
modal deploy src/backend/modal_server.py

echo ""
echo "=================================================="
echo "✅ Deployment Complete!"
echo "=================================================="
echo ""
echo "📊 Your app is now live on Modal!"
echo ""
echo "Next steps:"
echo "1. View logs: modal logs samani-financial-analyst"
echo "2. View app: modal get-app samani-financial-analyst"
echo "3. Monitor usage: modal dashboard"
echo ""
echo "To use in your Gradio app:"
echo "   Set MODAL_API_URL in gradio_app.py"
echo ""
echo "To stop the app:"
echo "   modal delete app samani-financial-analyst"
echo ""
