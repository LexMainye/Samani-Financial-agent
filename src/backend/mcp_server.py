from mcp.server.fastmcp import FastMCP
import pandas as pd
import json
import sys
import os
from typing import Optional

# Add the project root to the python path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import existing backend modules
from src.backend.mcp.parsing import parse_file
from src.backend.mcp.sentiment import analyze_sentiment
from src.backend.mcp.ratios import calculate_ratios
from src.backend.mcp.advanced_ratios import analyze_financial_ratios
from src.backend.mcp.cashflow_analysis import analyze_cash_flow
from src.backend.mcp.balance_sheet_analysis import analyze_balance_sheet
from src.backend.mcp.income_statement_analysis import analyze_income_statement
from src.backend.mcp.trend_analysis import analyze_trends_and_anomalies
from src.backend.mcp.extraction import extract_financial_data
from src.backend.mcp.forecasting import generate_forecast

# Initialize MCP Server
mcp = FastMCP("Samani Financial Agent")

class MockFile:
    """Helper class to mimic the file object expected by the parser"""
    def __init__(self, path):
        self.name = path

@mcp.tool()
def parse_financial_file(file_path: str) -> str:
    """
    Parses a local financial file (PDF, CSV, XLSX, TXT) and returns the extracted data as a JSON string.
    The output JSON contains:
    - 'financial_data': Structured data suitable for other analysis tools (CSV/Excel only).
    - 'text_content': Extracted text (PDF/TXT only) for sentiment analysis.
    - 'logs': Parsing status logs.
    """
    if not os.path.exists(file_path):
        return json.dumps({"error": f"File not found: {file_path}"})
    
    # Mock the file object expected by parse_file logic
    mock_file = MockFile(file_path)
    
    try:
        # Call the existing parser
        data_df, text_content, logs = parse_file([mock_file])
        
        result = {
            "status": "success",
            "logs": logs,
            "text_content": text_content,
            # Convert DataFrame to JSON records for portability
            "financial_data": data_df.to_json(orient='records') if data_df is not None else None
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def analyze_financial_text_sentiment(text: str) -> str:
    """
    Analyzes the sentiment/tone of financial text (e.g., management commentary from an Annual Report).
    Returns a formatted markdown report.
    """
    if not text:
        return "Error: No text provided."
        
    report, msg = analyze_sentiment(text)
    return f"{report}\n\n(Status: {msg})"

@mcp.tool()
def calculate_standard_ratios(financial_data_json: str) -> str:
    """
    Calculates basic financial ratios (Liquidity, Profitability, ROA/ROE) from structured financial data.
    Requires the 'financial_data' JSON string obtained from `parse_financial_file`.
    """
    try:
        if not financial_data_json: return "Error: No data provided."
        df = pd.read_json(financial_data_json)
        report, msg = calculate_ratios(df)
        return report
    except ValueError:
        return "Error: Invalid JSON data format."
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def analyze_advanced_ratios(financial_data_json: str) -> str:
    """
    Performs advanced ratio analysis (DuPont, Efficiency, Solvency).
    Requires the 'financial_data' JSON string.
    """
    try:
        if not financial_data_json: return "Error: No data provided."
        df = pd.read_json(financial_data_json)
        report, msg = analyze_financial_ratios(df)
        return report
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def analyze_cash_flows(financial_data_json: str) -> str:
    """
    Analyzes cash flow statements (Operating, Investing, Financing).
    Requires the 'financial_data' JSON string.
    """
    try:
        if not financial_data_json: return "Error: No data provided."
        df = pd.read_json(financial_data_json)
        report, msg = analyze_cash_flow(df)
        return report
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def analyze_balance_sheet(financial_data_json: str) -> str:
    """
    Analyzes balance sheet composition, leverage, and liquidity.
    Requires the 'financial_data' JSON string.
    """
    try:
        if not financial_data_json: return "Error: No data provided."
        df = pd.read_json(financial_data_json)
        report, msg = analyze_balance_sheet(df)
        return report
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def analyze_income_statement(financial_data_json: str) -> str:
    """
    Analyzes income statement trends, margins, and profitability.
    Requires the 'financial_data' JSON string.
    """
    try:
        if not financial_data_json: return "Error: No data provided."
        df = pd.read_json(financial_data_json)
        report, msg = analyze_income_statement(df)
        return report
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def detect_trends_and_anomalies(financial_data_json: str) -> str:
    """
    Detects trends, anomalies, and volatility in financial metrics.
    Requires the 'financial_data' JSON string.
    """
    try:
        if not financial_data_json: return "Error: No data provided."
        df = pd.read_json(financial_data_json)
        report, msg = analyze_trends_and_anomalies(df)
        return report
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def forecast_metric(financial_data_json: str, metric_name: str, years: int = 3) -> str:
    """
    Forecasts a specific financial metric (e.g., 'Revenue', 'Net Income') for N years.
    Requires the 'financial_data' JSON string.
    """
    try:
        if not financial_data_json: return "Error: No data provided."
        df = pd.read_json(financial_data_json)
        
        # Extract the specific series
        series, msg = extract_financial_data(df, metric_name)
        
        if series is not None:
            forecast, f_msg = generate_forecast(series, steps=years)
            if forecast is not None:
                formatted_forecast = [round(x, 2) for x in forecast.values]
                return f"### 🔮 Forecast for {metric_name}\nNext {years} Years: {formatted_forecast}\n\nAnalysis: {f_msg}"
            return f_msg
        else:
            return f"Could not find data for '{metric_name}' to forecast."
            
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Run the MCP server
    print("Starting Samani Financial Agent MCP Server...", file=sys.stderr)
    mcp.run()