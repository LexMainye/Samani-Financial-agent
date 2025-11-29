#!/usr/bin/env python3
"""
Modal Gradio Deployment - Simple Web App
Hosts the Gradio UI directly on Modal with A10G GPU backend
"""

import modal

# Define Docker image with all dependencies
image = (
    modal.Image.debian_slim()
    .pip_install(
        "gradio>=4.36.1",
        "torch>=2.6.0",
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
app = modal.App("samani-financial-analyst-web")

# Mount local source code
src_mount = modal.Mount.from_local_dir(
    local_path="/Users/alexmainye/Documents/Projects/fin_forecasting/src",
    remote_path="/root/src"
)


@app.function(image=image, gpu="A10G", memory=30000, timeout=600, mounts=[src_mount])
@modal.asgi_app()
def gradio_app():
    """Gradio app served via ASGI"""
    import sys
    import os
    
    # Add the project root to the path
    sys.path.insert(0, "/root/src")
    sys.path.insert(0, "/root")
    
    # Import after setting path
    import gradio as gr
    from backend.agent_logic import process_request
    from transformers import pipeline
    import torch
    
    print("🟢 Loading FinBERT model on A10G GPU...")
    device = 0 if torch.cuda.is_available() else -1
    nlp = pipeline(
        "sentiment-analysis",
        model="yiyanghkust/finbert-tone",
        device=device
    )
    print("✅ FinBERT loaded on GPU")
    
    def analyze(files, query):
        """Analyze function"""
        if not files:
            return "❌ Please upload financial statement files", ""
        if not query.strip():
            return "❌ Please enter an analysis query", ""
        
        try:
            result, logs = process_request(files, query)
            return result, logs
        except Exception as e:
            return "", f"❌ Error: {str(e)}"
    
    # Build Gradio interface
    with gr.Blocks(title="Samani Financial Analyst", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🛋 Samani Ltd Financial Analyst
            **Advanced Multi-Year Analysis & Forecasting**
            
            Upload financial statements and get instant insights powered by A10G GPU acceleration.
            
            💱 **Currency: KES** | All values displayed in KES
            """
        )
        
        with gr.Row():
            with gr.Column(scale=4):
                file_input = gr.File(
                    label="1. Upload Financial Statements (Multiple Years)",
                    file_count="multiple", 
                    file_types=[".xlsx", ".csv", ".pdf"]
                )
            with gr.Column(scale=6):
                gr.Markdown(
                    """
                    **How to use:**
                    1. Select financial statements from your device
                    2. Upload statements for **multiple years** (2020-2024, etc.)
                    3. Ask a question or request analysis type
                    4. Get instant GPU-powered insights
                    
                    📊 **All figures should be in KES**
                    """
                )
        
        with gr.Row():
            with gr.Column(scale=1):
                query_input = gr.Textbox(
                    label="2. What would you like to know?", 
                    placeholder="e.g., 'Advanced ratio analysis' or 'Cash flow trends'",
                    lines=3
                )
                submit_btn = gr.Button("🚀 Run Analysis", variant="primary", size="lg")
            
            with gr.Column(scale=1):
                output_text = gr.Markdown(label="Analysis Results")
                
                with gr.Accordion("📋 Debug Logs", open=False):
                    log_output = gr.Textbox(
                        label="System Logs", 
                        lines=10, 
                        interactive=False
                    )
        
        # Event handler
        submit_btn.click(
            fn=analyze,
            inputs=[file_input, query_input],
            outputs=[output_text, log_output]
        )
        
        # Example queries
        gr.Examples(
            examples=[
                ["Advanced financial ratio analysis"],
                ["Cash flow analysis and trends"],
                ["Balance sheet composition"],
                ["Income statement analysis"],
                ["Trend analysis and forecasting"],
                ["Sentiment analysis"],
            ],
            inputs=query_input
        )
        
        # Analysis guide
        with gr.Accordion("📖 Available Analyses", open=False):
            gr.Markdown("""
            ### 📊 **Advanced Ratios**
            - Profitability, liquidity, efficiency, solvency ratios
            - DuPont analysis for ROE decomposition
            - Trend analysis of all metrics
            
            ### 💰 **Cash Flow Analysis**
            - Operating, investing, financing flows
            - Free cash flow and cash conversion
            - Cash position trends
            
            ### 📋 **Balance Sheet Analysis**
            - Asset/liability composition
            - Leverage and working capital
            - Financial health assessment
            
            ### 📈 **Income Statement Analysis**
            - Revenue and expense trends
            - Profitability margins
            - Profitability waterfall
            
            ### 📐 **Trend & Forecasting**
            - Year-over-year growth rates
            - Statistical anomaly detection
            - 3-year forward projections
            
            ### 🤖 **Sentiment Analysis**
            - FinBERT sentiment on reports
            - Management tone assessment
            """)
    
    return demo
