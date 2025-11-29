from src.backend.mcp.parsing import parse_file
from src.backend.mcp.extraction import extract_financial_data
from src.backend.mcp.forecasting import generate_forecast
from src.backend.mcp.ratios import calculate_ratios
from src.backend.mcp.sentiment import analyze_sentiment
from src.backend.mcp.advanced_ratios import analyze_financial_ratios
from src.backend.mcp.cashflow_analysis import analyze_cash_flow
from src.backend.mcp.balance_sheet_analysis import analyze_balance_sheet
from src.backend.mcp.income_statement_analysis import analyze_income_statement
from src.backend.mcp.trend_analysis import analyze_trends_and_anomalies
from src.backend.cloud_config.config import ModalConfig

def process_request(file_objs, query):
    logs = []
    
    # 1. Parsing (Returns Data AND Text)
    logs.append("--- Step 1: Ingesting Files ---")
    data, text_content, msg = parse_file(file_objs)
    logs.append(msg)
    
    if data is None and not text_content:
        return "Error: Could not parse files.", "\n".join(logs)

    # 2. Intent Analysis - Enhanced with new analysis types
    intent = "extract"
    query_lower = query.lower()
    
    if any(x in query_lower for x in ["sentiment", "tone", "feeling", "opinion", "qualitative", "summary", "tone of management"]):
        intent = "sentiment"
    elif any(x in query_lower for x in ["advanced ratio", "dupont", "efficiency", "solvency", "coverage", "liquidity ratio", "profitability ratio"]):
        intent = "advanced_ratios"
    elif any(x in query_lower for x in ["cash flow", "cfo", "fcf", "free cash", "operating cash", "cash from operations"]):
        intent = "cashflow"
    elif any(x in query_lower for x in ["balance sheet", "assets", "liabilities", "equity", "leverage", "debt-to-equity"]):
        intent = "balance_sheet"
    elif any(x in query_lower for x in ["income statement", "revenue", "expenses", "profitability", "margin", "ebit", "ebitda"]):
        intent = "income_statement"
    elif any(x in query_lower for x in ["trend", "anomaly", "volatility", "consistency", "forecast next", "projection"]):
        intent = "trends"
    elif any(x in query_lower for x in ["ratio", "margin", "profitability", "liquidity"]):
        intent = "ratios"
    elif any(x in query_lower for x in ["forecast", "predict", "future"]):
        intent = "forecast"
    
    # 3. Execution
    result_text = ""
    
    # --- PATH A: FINBERT SENTIMENT ---
    if intent == "sentiment":
        if not text_content:
            return "⚠️ Sentiment Analysis requires text. Please upload a PDF (Annual Report) or .txt file containing management commentary.", "\n".join(logs)
        
        logs.append("--- Step 3: Running FinBERT Sentiment Model ---")
        sentiment_report, s_msg = analyze_sentiment(text_content)
        logs.append(s_msg)
        result_text = sentiment_report

    # --- PATH B: ADVANCED RATIOS ---
    elif intent == "advanced_ratios":
        if data is None: 
            return "No numeric data found for advanced ratio analysis.", "\n".join(logs)
        logs.append("--- Step 3: Calculating Advanced Financial Ratios ---")
        result_text, msg = analyze_financial_ratios(data)
        logs.append(msg)

    # --- PATH C: CASH FLOW ANALYSIS ---
    elif intent == "cashflow":
        if data is None: 
            return "No numeric data found for cash flow analysis.", "\n".join(logs)
        logs.append("--- Step 3: Analyzing Cash Flows ---")
        result_text, msg = analyze_cash_flow(data)
        logs.append(msg)

    # --- PATH D: BALANCE SHEET ANALYSIS ---
    elif intent == "balance_sheet":
        if data is None: 
            return "No numeric data found for balance sheet analysis.", "\n".join(logs)
        logs.append("--- Step 3: Analyzing Balance Sheet ---")
        result_text, msg = analyze_balance_sheet(data)
        logs.append(msg)

    # --- PATH E: INCOME STATEMENT ANALYSIS ---
    elif intent == "income_statement":
        if data is None: 
            return "No numeric data found for income statement analysis.", "\n".join(logs)
        logs.append("--- Step 3: Analyzing Income Statement ---")
        result_text, msg = analyze_income_statement(data)
        logs.append(msg)

    # --- PATH F: TREND & ANOMALY ANALYSIS ---
    elif intent == "trends":
        if data is None: 
            return "No numeric data found for trend analysis.", "\n".join(logs)
        logs.append("--- Step 3: Performing Trend & Anomaly Detection ---")
        result_text, msg = analyze_trends_and_anomalies(data)
        logs.append(msg)

    # --- PATH G: BASIC RATIOS ---
    elif intent == "ratios":
        if data is None: 
            return "No numeric data found for ratios.", "\n".join(logs)
        logs.append("--- Step 3: Calculating Basic Financial Ratios ---")
        result_text, _ = calculate_ratios(data)

    # --- PATH H: FORECASTING ---
    elif intent == "forecast":
        if data is None: 
            return "No numeric data found for forecasting.", "\n".join(logs)
        term_map = {"revenue": "Revenue", "sales": "Revenue", "profit": "Net Income", "earnings": "Net Income"}
        target_keyword = "Revenue"  # default
        for k, v in term_map.items(): 
            if k in query_lower: 
                target_keyword = v
            
        logs.append(f"--- Step 3: Forecasting {target_keyword} ---")
        series, _ = extract_financial_data(data, target_keyword)
        
        if series is not None:
            pred, f_msg = generate_forecast(series, steps=3)
            logs.append(f_msg)
            if pred is not None:
                result_text = f"### 🔮 Forecast: {target_keyword}\nNext 3 Years: {[round(x,0) for x in pred.values]}"
        else:
             result_text = f"Could not find data for '{target_keyword}'."

    # --- PATH I: EXTRACTION (DEFAULT) ---
    else:
        if data is None: 
            return "No numeric data found.", "\n".join(logs)
        # Default fallback
        result_text = """### 📊 Available Analyses
        
Try asking for:
• **Advanced Ratios**: DuPont analysis, efficiency, solvency ratios
• **Cash Flow Analysis**: Operating, investing, financing flows
• **Balance Sheet Analysis**: Asset composition, leverage, equity strength
• **Income Statement Analysis**: Revenue trends, margin analysis, expense structure
• **Trend Analysis**: Anomaly detection, volatility, forecasts
• **Sentiment Analysis**: Upload a PDF annual report for tone analysis
• **Forecast**: Predict future revenue or earnings
"""

    return result_text, "\n".join(logs)