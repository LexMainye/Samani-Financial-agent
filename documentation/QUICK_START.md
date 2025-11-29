# 🎯 Quick Start Guide - Enhanced Financial Analysis

## Installation & Setup

### Step 1: Install Dependencies
```bash
cd /Users/alexmainye/Documents/Projects/fin_forecasting
pip install -r requirements.txt
```

### Step 2: Prepare Your Data
Place financial statements in the `financials/` folder with this structure:
```
financials/
├── 2022/
│   ├── Income_Statement_2022.xlsx
│   ├── Balance_Sheet_2022.xlsx
│   └── Cash_Flow_2022.xlsx
├── 2023/
├── 2024/
```

**Data Format** (for Excel/CSV files):
- Column A: Line items (e.g., Revenue, Total Assets, Net Income)
- Column B onwards: Values for each year or metric

Example:
```
Line Item                    | Value
Revenue                      | 1,000,000
Cost of Goods Sold          | 600,000
Gross Profit                | 400,000
Operating Expenses          | 150,000
Operating Profit            | 250,000
Interest Expense            | 25,000
Net Income                  | 200,000
```

### Step 3: Launch the App
```bash
python src/main.py
```

The app will start at `http://localhost:7860`

---

## 📊 Analysis Types & Commands

### 1. Advanced Financial Ratios
```
Query: "Give me comprehensive ratio analysis"
Returns:
├─ Profitability Ratios (margins, ROA, ROE)
├─ Liquidity Ratios (current, quick, cash)
├─ Efficiency Ratios (turnover, DSO, DIO)
└─ Solvency Ratios (leverage, coverage)
```

**Best for**: Understanding overall financial health and performance

---

### 2. Cash Flow Analysis
```
Query: "Analyze cash flows"
Returns:
├─ Operating Cash Flow trends
├─ Investing Cash Flow patterns
├─ Financing Cash Flow activity
├─ Free Cash Flow calculations
└─ Cash Conversion metrics
```

**Best for**: Assessing liquidity and cash generation capability

---

### 3. Balance Sheet Analysis
```
Query: "Balance sheet composition and leverage"
Returns:
├─ Asset structure (current/non-current)
├─ Liability breakdown (short/long-term)
├─ Equity strength & trends
├─ Working capital analysis
└─ Leverage assessment
```

**Best for**: Understanding capital structure and financial position

---

### 4. Income Statement Analysis
```
Query: "Income statement and profitability analysis"
Returns:
├─ Revenue trends & CAGR
├─ Expense structure (% of revenue)
├─ Margin trends (gross, operating, net)
├─ Profitability waterfall
└─ Cost analysis
```

**Best for**: Evaluating profitability trends and cost management

---

### 5. Trend & Anomaly Analysis
```
Query: "Detect trends and anomalies"
Returns:
├─ Year-over-year growth rates
├─ Anomaly detection (statistical)
├─ Volatility assessment
├─ Consistency metrics
└─ Simple forecasts
```

**Best for**: Identifying unusual patterns and future trends

---

### 6. Combined Analysis
```
Query: "Comprehensive financial health check"
Agent automatically runs:
1. Advanced Ratios
2. Cash Flow Analysis
3. Balance Sheet Health
4. Profitability Trends
```

---

## 💡 Common Use Cases

### Scenario 1: Investment Decision
```
1. Upload: 3-5 years of financial statements
2. Query: "Comprehensive financial health check"
3. Review: Profitability, cash flow, and leverage
4. Follow-up: "Trend and anomaly detection"
```

### Scenario 2: Operational Management
```
1. Upload: Last 3 years of statements
2. Query: "Expense analysis and margin trends"
3. Review: Cost structure and profitability
4. Follow-up: "Cash conversion analysis"
```

### Scenario 3: Risk Assessment
```
1. Upload: 4-5 years of historical data
2. Query: "Leverage and solvency analysis"
3. Review: Debt ratios and coverage
4. Follow-up: "Liquidity and working capital"
```

### Scenario 4: Planning & Forecasting
```
1. Upload: 3-5 years of statements
2. Query: "Trend analysis and anomaly detection"
3. Review: Historical patterns
4. Query: "Forecast revenue for next 3 years"
```

---

## 📈 Expected Output Format

Each analysis returns:
```
### 📊 [Analysis Type]

**Key Metric 1**
• Value 1: X.XX
• Value 2: Y.YY
• Trend: ↗️ Improving / ↘️ Declining

**Key Metric 2**
• Ratio: Z.ZZ
• Assessment: ✅ Healthy / ⚠️ Warning / ❌ Critical

**Summary**
• Key observation 1
• Key observation 2
• Recommendation
```

---

## 🔍 Line Item Normalization

The system automatically recognizes:

**Revenue Terms**:
- Revenue, Sales, Turnover, Total Revenue, Total Sales, Net Sales

**Profit Terms**:
- Net Income, Net Profit, Profit for the Year, Profit After Tax, PAT, Earnings

**Asset Terms**:
- Total Assets, Current Assets, Non-current Assets, Fixed Assets, PPE

**And 50+ more variations across all three statement types!**

---

## ⚙️ Tips for Best Results

1. **Data Consistency**
   - Use consistent line item names across files
   - Include full fiscal years (not partial quarters)
   - Ensure numbers are in the same currency

2. **File Format**
   - Excel (.xlsx) recommended for best parsing
   - CSV works but requires proper headers
   - PDFs supported for sentiment analysis only

3. **Time Series**
   - 3+ years: Better trend analysis
   - 4+ years: Anomaly detection becomes more accurate
   - 5+ years: Excellent for forecasting and pattern identification

4. **Complete Statements**
   - Include all three: Income, Balance Sheet, Cash Flow
   - More detail = better analysis (COGS, OpEx, depreciation, etc.)
   - Breakdown items when possible

---

## 🛠️ Troubleshooting

### Files Not Parsing
```
✓ Check: Column A has line item names
✓ Check: Data columns have numeric values
✓ Check: Year is in filename (e.g., "2023_IS.xlsx") or first 10 rows
✓ Try: Save as .xlsx (not .xls or .csv initially)
```

### Missing Line Items in Results
```
✓ The system normalized unrecognized items
✓ Check the logs - they show what was parsed
✓ Verify spelling matches the 50+ supported terms
✓ Contact: Provide original line item name for mapping
```

### Incomplete Analysis
```
✓ Some metrics need specific data:
  - Cash Flow ratios need cash flow statements
  - Working capital needs current assets/liabilities
  - Days calculations need receivables/inventory
✓ Upload complete statements for full analysis
```

### Forecasting Unrealistic
```
✓ Need at least 3 data points
✓ Works best with 4-5 consistent years
✓ Handles trends but not step changes well
✓ Use for trends, not absolute predictions
```

---

## 📚 Financial Concepts

### Key Ratios to Monitor

**Profitability** (Higher is better)
- Net Profit Margin: Shows % of revenue that's profit
- ROE: Return on shareholder equity
- ROA: Return on all assets

**Liquidity** (Higher is better)
- Current Ratio > 1.0: Can cover short-term obligations
- Quick Ratio > 0.8: Quick asset liquidity
- Cash Ratio > 0.2: Immediate cash availability

**Solvency** (Lower is better)
- Debt-to-Equity < 1.0: Equity exceeds debt
- Interest Coverage > 2.5x: Can cover interest payments

**Efficiency** (Context-dependent)
- Asset Turnover: Revenue generated per $ of assets
- Receivables Turnover: How quickly receivables are collected
- Inventory Turnover: Inventory movement speed

---

## 🚀 Advanced Features

### DuPont Analysis
```
Query: "DuPont ROE analysis"
Shows: ROE = Net Margin × Asset Turnover × Equity Multiplier
Reveals: How profitability, efficiency, and leverage drive returns
```

### Cash Conversion Quality
```
Query: "Cash conversion analysis"
Shows: OCF / Net Income ratio
Interpretation:
  > 1.2: High quality earnings (cash > profit)
  0.8-1.2: Normal conversion
  < 0.8: Earnings quality concern (profit > cash)
```

### Anomaly Detection
```
Query: "Detect anomalies"
Uses: Z-score statistical method
Identifies: Values > 2 std devs from mean
Helps with: Finding unusual years or data entry errors
```

---

## 📞 Getting Help

1. **Check Debug Logs**
   - Open "Debug Logs & Consolidation" accordion
   - See what files were parsed
   - Identify any warnings

2. **Verify Data Quality**
   - Spot check a few values in the output
   - Confirm calculations make sense
   - Compare with known benchmarks

3. **Try Examples**
   - Use the pre-built example queries
   - Modify them for your specific needs

4. **Test with Sample Data**
   - Start with clean, formatted data
   - Add complexity gradually
   - Document what works

---

## 🎓 Next Steps

1. **Prepare** your financial data in the recommended format
2. **Upload** 3-5 years of statements
3. **Start** with "Comprehensive financial health check"
4. **Explore** specific analyses as needed
5. **Track** metrics over time for your company

---

Happy analyzing! 📊✨
