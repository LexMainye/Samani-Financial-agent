#!/bin/bash

# Deploy Samani Financial Analyst Gradio App to Modal
# This deploys the interactive web interface (not just the backend)

set -e

echo "🚀 Deploying Samani Financial Analyst (Gradio Web) to Modal..."
echo ""

# Check if Modal is installed
if ! command -v modal &> /dev/null; then
    echo "❌ Modal CLI not found. Install with: pip install modal"
    exit 1
fi

# Check if authenticated
echo "🔐 Checking Modal authentication..."
if ! modal token set &> /dev/null; then
    echo "⚠️  Setting up Modal token..."
    modal token new
fi

echo "✅ Authentication verified"
echo ""

# Verify Python environment
echo "📦 Checking Python environment..."
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  No venv found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -q modal gradio torch transformers pandas openpyxl
    echo "✅ Virtual environment created and dependencies installed"
fi

echo ""
echo "🐳 Building and deploying Docker image..."
echo "   GPU: NVIDIA A10G (24GB VRAM)"
echo "   Memory: 30GB"
echo "   Concurrency: 5 users"
echo ""

# Deploy the Gradio web app
modal deploy src/backend/modal_gradio_server.py

echo ""
echo "✅ Deployment successful!"
echo ""
echo "🌐 Your app is now live at:"
echo "   https://hf-hackathon-mcp--samani-web.modal.run"
echo ""
echo "📊 Dashboard:"
echo "   https://modal.com/apps/hf-hackathon-mcp/main/deployed/samani-financial-analyst-web"
echo ""
echo "💡 View logs:"
echo "   modal app logs samani-financial-analyst-web --follow"
echo ""
echo "🎉 Open the URL in your browser to access the app!"
