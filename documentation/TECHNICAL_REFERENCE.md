# 🔧 Technical Reference - Module Documentation

## Module Overview

```
src/backend/mcp/
├── parsing.py                    ├─ File parsing and normalization
├── advanced_ratios.py            ├─ Professional ratio calculations
├── cashflow_analysis.py          ├─ Cash flow statement analysis
├── balance_sheet_analysis.py     ├─ Balance sheet structure analysis
├── income_statement_analysis.py  ├─ P&L and profitability analysis
├── trend_analysis.py             ├─ Trend detection and forecasting
├── extraction.py                 ├─ Financial data extraction
├── forecasting.py                ├─ Time-series forecasting
├── ratios.py                     ├─ Basic ratio calculations
└── sentiment.py                  └─ FinBERT sentiment analysis
```

---

## Advanced Ratios Module (`advanced_ratios.py`)

### Class: `AdvancedRatioAnalyzer`

```python
class AdvancedRatioAnalyzer:
    def __init__(self, df: pd.DataFrame)
    def calculate_all_ratios(self) -> Tuple[pd.DataFrame, str]
    def _generate_report(self, ratio_df: pd.DataFrame) -> str
    def _analyze_trend(self, series: pd.Series) -> str
```

### Ratios Calculated

| Category | Ratios | Formula |
|----------|--------|---------|
| **Profitability** | Gross Margin | (Gross Profit / Revenue) × 100 |
| | Operating Margin | (Operating Profit / Revenue) × 100 |
| | Net Margin | (Net Income / Revenue) × 100 |
| **Returns** | ROA | (Net Income / Total Assets) × 100 |
| | ROE | (Net Income / Total Equity) × 100 |
| | DuPont ROE | Net Margin × Asset Turnover × Equity Multiplier |
| **Liquidity** | Current Ratio | Current Assets / Current Liabilities |
| | Quick Ratio | (Current Assets - Inventory) / Current Liabilities |
| | Cash Ratio | Cash / Current Liabilities |
| **Efficiency** | Asset Turnover | Revenue / Total Assets |
| | Receivables Turnover | Revenue / Receivables |
| | DSO | 365 / Receivables Turnover |
| | Inventory Turnover | COGS / Inventory |
| | DIO | 365 / Inventory Turnover |
| **Solvency** | Debt-to-Equity | Total Liabilities / Total Equity |
| | Debt-to-Assets | Total Debt / Total Assets |
| | Equity Multiplier | Total Assets / Total Equity |
| | Interest Coverage | Operating Profit / Interest Expense |

### Usage
```python
from src.backend.mcp.advanced_ratios import analyze_financial_ratios

report, status_msg = analyze_financial_ratios(data_df)
```

---

## Cash Flow Analysis Module (`cashflow_analysis.py`)

### Class: `CashFlowAnalyzer`

```python
class CashFlowAnalyzer:
    def __init__(self, df: pd.DataFrame)
    def analyze_cash_flows(self) -> Tuple[str, str]
    def analyze_cash_conversion(self) -> str
```

### Key Metrics

| Metric | Description | Interpretation |
|--------|-------------|-----------------|
| **OCF Margin** | Operating CF / Revenue | % of revenue converted to operating cash |
| **OCF/NI Ratio** | Operating CF / Net Income | > 1.0 = good earnings quality |
| **CapEx/OCF** | Investing CF / Operating CF | < 1.0 = sustainable capex |
| **Free Cash Flow** | Operating CF + Investing CF | Cash available after reinvestment |
| **Cash Conversion** | Operating CF / Net Income | How well earnings convert to cash |

### Analysis Components
1. Operating Cash Flow Analysis
2. Investing Cash Flow Analysis
3. Financing Cash Flow Analysis
4. Free Cash Flow Calculation
5. Cash Balance Trends
6. Cash Conversion Quality

### Usage
```python
from src.backend.mcp.cashflow_analysis import analyze_cash_flow

report, status_msg = analyze_cash_flow(data_df)
```

---

## Balance Sheet Analysis Module (`balance_sheet_analysis.py`)

### Class: `BalanceSheetAnalyzer`

```python
class BalanceSheetAnalyzer:
    def __init__(self, df: pd.DataFrame)
    def analyze_balance_sheet(self) -> Tuple[str, str]
```

### Analysis Sections

1. **Balance Sheet Structure**
   - Current vs. Non-current assets
   - Current vs. Non-current liabilities
   - Equity composition

2. **Asset Quality**
   - Liquidity percentage
   - Working capital trends
   - Capital intensity (PPE %)
   - Intangible assets assessment

3. **Financial Leverage**
   - Debt-to-Equity ratio trends
   - Leverage classification (conservative/moderate/high)

4. **Debt Structure**
   - Short-term vs. long-term debt mix
   - Debt maturity profile

5. **Equity Analysis**
   - Equity ratio (equity/assets)
   - Equity growth trends
   - Equity strength assessment

### Key Insights
- Working capital adequacy
- Financial risk assessment
- Capital structure sustainability
- Growth vs. stability balance

### Usage
```python
from src.backend.mcp.balance_sheet_analysis import analyze_balance_sheet

report, status_msg = analyze_balance_sheet(data_df)
```

---

## Income Statement Analysis Module (`income_statement_analysis.py`)

### Class: `IncomeStatementAnalyzer`

```python
class IncomeStatementAnalyzer:
    def __init__(self, df: pd.DataFrame)
    def analyze_income_statement(self) -> Tuple[str, str]
```

### Analysis Components

1. **Revenue Analysis**
   - Absolute values
   - YoY growth rates
   - CAGR calculation
   
2. **Expense Structure**
   - Each expense as % of revenue
   - Year-over-year trends
   
3. **Profitability Margins**
   - Gross margin trends
   - Operating margin trends
   - Net margin trends
   - Margin direction (improving/declining)
   
4. **Profitability Waterfall**
   - Revenue starting point
   - Sequential expense deductions
   - Final net income
   - Visual flow of profits

### CAGR Formula
```
CAGR = (Ending Value / Beginning Value) ^ (1 / Number of Years) - 1
```

### Usage
```python
from src.backend.mcp.income_statement_analysis import analyze_income_statement

report, status_msg = analyze_income_statement(data_df)
```

---

## Trend Analysis Module (`trend_analysis.py`)

### Class: `TrendAnalyzer`

```python
class TrendAnalyzer:
    def __init__(self, df: pd.DataFrame)
    def detect_anomalies(self, series: pd.Series, name: str, 
                        threshold_zscore: float = 2.0) -> List[Tuple[str, str]]
    def analyze_all_trends(self) -> Tuple[str, str]
    def analyze_consistency(self) -> str
    def forecast_next_periods(self) -> str
```

### Anomaly Detection Method

Uses Z-score statistical method:
```
Z-score = (Value - Mean) / Standard Deviation

Anomaly if |Z-score| > threshold (default: 2.0)
= 95% confidence level
```

### Consistency Metrics

```
Coefficient of Variation (CV) = (Std Dev / Mean) × 100

Categories:
< 10%       → Very Stable 🟢
10-20%      → Stable 🟡
20-35%      → Moderate Volatility 🟠
> 35%       → High Volatility 🔴
```

### Trend Forecasting

Uses linear regression:
```
y = slope × x + intercept

R² indicates model quality
```

### Analysis Sections
1. Overall Trend Analysis (YoY growth, CAGR, momentum)
2. Anomaly Detection (statistical outliers)
3. Consistency & Volatility (CV calculation)
4. Trend Forecasting (linear regression)

### Usage
```python
from src.backend.mcp.trend_analysis import analyze_trends_and_anomalies

report, status_msg = analyze_trends_and_anomalies(data_df)
```

---

## Parsing Module Enhancement (`parsing.py`)

### Function: `normalize_row_name(row_name: str) -> str`

Comprehensive line item normalization covering:
- 8 revenue variations
- 8 COGS variations
- 10+ operating expense variations
- 10+ asset classifications
- 15+ liability classifications
- 50+ total variations

### Line Item Categories

**Income Statement (20+ items)**
- Revenue, COGS, Gross Profit
- Operating Expenses, Depreciation
- Operating Profit, Interest, Taxes
- Net Income, EBITDA

**Balance Sheet (25+ items)**
- Current/Non-Current Assets
- Cash, Receivables, Inventory
- PPE, Intangibles
- Current/Non-Current Liabilities
- Short/Long-term Debt
- Total Equity

**Cash Flow (5+ items)**
- Operating/Investing/Financing CF
- Net Cash Flow

### Normalization Algorithm
```python
def normalize_row_name(row_name):
    # 1. Convert to lowercase and strip whitespace
    # 2. Search through comprehensive keyword mapping
    # 3. Return standardized name or original if no match
```

---

## Agent Logic (`agent_logic.py`)

### Intent Detection Keywords

| Intent | Keywords | Module |
|--------|----------|--------|
| sentiment | sentiment, tone, opinion, qualitative | sentiment.py |
| advanced_ratios | advanced ratio, dupont, efficiency, solvency | advanced_ratios.py |
| cashflow | cash flow, cfo, fcf, free cash | cashflow_analysis.py |
| balance_sheet | balance sheet, assets, leverage | balance_sheet_analysis.py |
| income_statement | income statement, revenue, profitability | income_statement_analysis.py |
| trends | trend, anomaly, volatility, forecast | trend_analysis.py |
| ratios | ratio, margin, liquidity | ratios.py |
| forecast | forecast, predict, future | forecasting.py |

### Processing Flow
```
1. Parse Files → Extract Data
2. Analyze Intent → Select Module
3. Run Analysis → Generate Report
4. Format Output → Return to UI
```

---

## Data Structure

### Input DataFrame Format
```
   Line Item      | 2022    | 2023    | 2024
---|-------------|---------|---------|---------
 0 | Revenue     | 1000000 | 1200000 | 1500000
 1 | COGS        | 600000  | 720000  | 900000
 2 | Gross Prof  | 400000  | 480000  | 600000
 ...
```

### Output Format
Each analysis returns:
```python
Tuple[report_text: str, status_message: str]

report_text: Formatted markdown with:
- Section headers (###)
- Bold metrics (**text**)
- Bullet points (•)
- Trend indicators (↗️ ↘️ →)
- Status indicators (✅ ⚠️ ❌)

status_message: "✅ Analysis complete" or error message
```

---

## Error Handling

### Common Error Scenarios

| Scenario | Handling | Recovery |
|----------|----------|----------|
| No data provided | Return error message | User uploads files |
| Invalid line items | Skip unrecognized items | Continue with available data |
| Insufficient data points | Skip analysis section | Provide partial analysis |
| Division by zero | Skip ratio calculation | Report as N/A |
| Parsing failure | Log error, continue | Process next file |

### Exception Handling
```python
try:
    # Analysis code
except Exception as e:
    return "", f"❌ Error: {str(e)}"
```

---

## Performance Considerations

### Computational Complexity
- **Parsing**: O(n) where n = number of rows
- **Ratio Calculation**: O(m) where m = number of metrics
- **Trend Analysis**: O(n log n) for sorting/statistics
- **Anomaly Detection**: O(n) Z-score calculation

### Memory Usage
- DataFrame storage: O(rows × columns)
- Series objects: O(data points)
- No external API calls (local processing)

### Optimization Tips
1. Pre-compute commonly used series
2. Cache normalization results
3. Use vectorized operations (pandas/numpy)
4. Limit anomaly detection to key metrics

---

## Extension Points

### Adding New Analysis Type
```python
# 1. Create new module: new_analysis.py
# 2. Implement main function:
def analyze_new(data: pd.DataFrame) -> Tuple[str, str]:
    # Analysis logic
    return report, status_message

# 3. Update agent_logic.py:
from src.backend.mcp.new_analysis import analyze_new

# 4. Add intent detection:
if "trigger_word" in query_lower:
    intent = "new_analysis"

# 5. Add execution path:
elif intent == "new_analysis":
    result_text, msg = analyze_new(data)
```

### Adding New Line Item Mapping
```python
# In parsing.py, expand normalize_row_name() mapping:
mapping = {
    'New Standard Term': [
        'variation1', 'variation2', 'variation3'
    ],
    ...
}
```

---

## Testing Recommendations

### Unit Tests
```python
# Test normalization
assert normalize_row_name("Total Revenue") == "Revenue"

# Test ratio calculations
assert advanced_ratios.calculate_current_ratio(assets, liabs) > 0

# Test anomaly detection
anomalies = trend_analyzer.detect_anomalies(series)
```

### Integration Tests
```python
# Test full pipeline
report, msg = process_request(files, query)
assert report != ""
assert "✅" in msg or "❌" in msg
```

### Data Quality Tests
```python
# Verify output reasonableness
assert current_ratio > 0
assert debt_ratio < 1.0 or debt_ratio < 3.0  # context-dependent
assert all(margins between 0 and 100 for margins)
```

---

## Configuration & Customization

### Threshold Adjustments
- Anomaly Z-score threshold: `threshold_zscore = 2.0` (95% confidence)
- Leverage assessment: Modify in `balance_sheet_analysis.py`
- Volatility categories: Modify CV thresholds in `trend_analysis.py`

### Output Formatting
- Emoji indicators: Modify in analysis modules
- Decimal precision: Adjust `.2f` formatting
- Report structure: Modify section headers and order

---

## Logging & Debugging

### Debug Output Locations
1. **File Parsing Logs**: Shows files processed and years detected
2. **Step Logs**: Shows analysis progression
3. **Error Logs**: Shows any parsing or calculation errors
4. **Status Messages**: Final completion status

### Enable Detailed Logging
```python
# Add to any module:
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Detailed message")
```

---

## API Reference

### Main Entry Point
```python
def process_request(file_objs: list, query: str) -> Tuple[str, str]:
    """
    Process financial analysis request
    
    Args:
        file_objs: List of uploaded files
        query: Natural language query
    
    Returns:
        (report_text, debug_logs)
    """
```

### Analysis Functions
All follow the pattern:
```python
def analyze_[type](data: pd.DataFrame) -> Tuple[str, str]:
    """
    Analyze financial data
    
    Args:
        data: Consolidated financial DataFrame
    
    Returns:
        (formatted_report, status_message)
    """
```

---

## Version History

**v2.0 - Enhanced**
- ✅ Advanced ratio analysis
- ✅ Cash flow analysis
- ✅ Balance sheet analysis
- ✅ Income statement analysis
- ✅ Trend & anomaly detection
- ✅ Enhanced parsing (50+ line items)
- ✅ Improved UI with analysis guide

**v1.0 - Original**
- Basic ratio calculations
- Time-series forecasting
- Sentiment analysis

---

This documentation covers all technical aspects of the enhanced financial analysis system. For usage examples, see `QUICK_START.md`. For feature overview, see `ENHANCEMENT_GUIDE.md`.
