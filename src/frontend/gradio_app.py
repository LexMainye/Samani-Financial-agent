import gradio as gr
import sys
import os

# Ensure backend modules are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.backend.agent_logic import process_request

# Global currency setting
DEFAULT_CURRENCY = "KES"
CURRENCY_SYMBOL = "KES"

def create_app():
    # REMOVED: theme definitions to ensure compatibility with your current Gradio version
    
    with gr.Blocks() as demo:
        gr.Markdown(
            f"""
            # 🛋 Samani Ltd Financial Analyst
            **Advanced Multi-Year Analysis & Forecasting**
            
            Upload financial statements and get instant insights with advanced ratio analysis, 
            cash flow analysis, balance sheet assessment, income statement breakdown, and trend detection.
            
            💱 **Currency: {CURRENCY_SYMBOL}** | All values displayed in {CURRENCY_SYMBOL}
            """
        )
        
        with gr.Row():
            with gr.Column(scale=4):
                # file_count="multiple" is supported in most versions, but if this fails, change to "single"
                file_input = gr.File(
                    label="1. Upload Financial Statements (Select multiple years)",
                    file_count="multiple", 
                    file_types=[".xlsx", ".csv", ".pdf"]
                )
            with gr.Column(scale=6):
                 gr.Markdown(
                    f"""
                    **How to use:**
                    1. Navigate to the `financials` folder on the [LexMainye/Samani-Financial-agent](https://github.com/LexMainye/Samani-Financial-agent) GitHub repository.
                    2. Select the Statements for **multiple years** (e.g., 2020, 2021, 2022).
                    3. Drag and drop them all here.
                    4. The agent will merge and analyze them comprehensively.
                    
                    📊 **All figures should be in {CURRENCY_SYMBOL}**
                    """
                )

        with gr.Row():
            with gr.Column(scale=1):
                query_input = gr.Textbox(
                    label="2. What would you like to know?", 
                    placeholder="e.g., 'Advanced ratio analysis' or 'Cash flow trends'",
                    lines=3
                )
                submit_btn = gr.Button("Run Analysis", variant="primary")
            
            with gr.Column(scale=1):
                output_text = gr.Markdown(label="Agent Response")
                
                with gr.Accordion("Debug Logs & Consolidation", open=False):
                    log_output = gr.Textbox(label="System Logs", lines=10, interactive=False)

        # Event Handler
        submit_btn.click(
            fn=process_request,
            inputs=[file_input, query_input],
            outputs=[output_text, log_output]
        )
        
        # Examples - Enhanced with new analysis types
        gr.Examples(
            examples=[
                ["Advanced financial ratio analysis including DuPont"],
                ["Cash flow analysis and free cash flow trends"],
                ["Balance sheet composition and leverage analysis"],
                ["Income statement analysis with margin trends"],
                ["Trend analysis and anomaly detection"],
                ["Forecast Revenue for next 3 years"],
                ["Sentiment analysis from annual report"],
                ["Extract Net Income history and profitability"],
            ],
            inputs=query_input
        )
        
        # Add analysis guide
        with gr.Accordion("📖 Analysis Guide", open=False):
            gr.Markdown("""
            ## Available Analyses

            ### 📊 **Advanced Ratios**
            - Profitability ratios (margins, ROA, ROE, DuPont)
            - Liquidity ratios (current, quick, cash ratios)
            - Efficiency ratios (asset turnover, receivables turnover)
            - Solvency ratios (debt-to-equity, interest coverage)
            - Trend analysis of all ratios
            
            Try: "Calculate advanced ratios" or "DuPont analysis"

            ### 💰 **Cash Flow Analysis**
            - Operating, investing, and financing cash flows
            - Free cash flow calculations
            - Cash conversion analysis
            - Cash position trends
            
            Try: "Analyze cash flows" or "Free cash flow trends"

            ### 📋 **Balance Sheet Analysis**
            - Asset composition and quality
            - Liability structure and debt ratios
            - Equity strength and growth
            - Working capital trends
            - Financial leverage assessment
            
            Try: "Balance sheet analysis" or "Leverage analysis"

            ### 📈 **Income Statement Analysis**
            - Revenue trends and CAGR
            - Expense structure as % of revenue
            - Profitability margin trends
            - Profitability waterfall analysis
            
            Try: "Analyze profitability" or "Revenue trends"

            ### 📐 **Trend & Anomaly Analysis**
            - Year-over-year growth rates
            - Volatility and consistency metrics
            - Statistical anomaly detection
            - Simple trend forecasting
            
            Try: "Detect trends and anomalies" or "Volatility analysis"

            ### 🔮 **Forecasting**
            - Time-series forecasting using Holt-Winters
            - Revenue and earnings projections
            - 3-year forward estimates
            
            Try: "Forecast next 3 years" or "Project earnings"

            ### 🤖 **Sentiment Analysis**
            - FinBERT sentiment analysis on annual reports
            - Management tone assessment
            - Financial sentiment scoring
            
            Try: Upload PDF and ask: "Sentiment analysis"
            """)

    return demo