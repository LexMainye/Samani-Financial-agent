# 📊 Analysis Types Visual Guide

## Quick Reference - What to Ask For

```
┌─────────────────────────────────────────────────────────────────┐
│                    FINANCIAL ANALYSIS QUERIES                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   PROFITABILITY │  │    SOLVENCY     │  │   LIQUIDITY     │
│                 │  │                 │  │                 │
│ "Profit Margins"│  │"Leverage Analysis"│ │"Working Capital"│
│ "Margins Trend" │  │"Debt-to-Equity" │  │"Current Ratio"  │
│ "ROA/ROE"       │  │"Interest Cover" │  │"Quick Ratio"    │
│ "DuPont Analysis"  │  │"Debt Structure" │  │"Cash Position"  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
     ↓                      ↓                      ↓
  Advanced Ratios    Balance Sheet Analysis   Advanced Ratios
  Income Statement   Cash Flow Analysis       Balance Sheet

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   EFFICIENCY    │  │ CASH GENERATION │  │   TRENDS        │
│                 │  │                 │  │                 │
│ "Asset Turnover"│  │"Operating Cash" │  │"Revenue Growth" │
│ "Days Inventory"│  │"Free Cash Flow" │  │"Margin Trends"  │
│ "DSO"           │  │"Cash Conversion"│  │"Anomalies"      │
│ "DIO"           │  │"Cash Balance"   │  │"Volatility"     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
     ↓                      ↓                      ↓
  Advanced Ratios    Cash Flow Analysis    Trend Analysis
  Income Statement   Advanced Ratios       Income Statement
```

---

## By Financial Statement Type

### 📈 Income Statement Analysis
```
"Give me income statement analysis"
"Analyze profitability and margins"
"Revenue trends and growth"
"Expense structure analysis"

Returns:
├─ Revenue trends (absolute & YoY growth)
├─ Expense breakdown (% of revenue)
├─ Profitability margins (3 types)
├─ Profitability waterfall
└─ Cost insights
```

### 📋 Balance Sheet Analysis
```
"Analyze balance sheet"
"Asset and liability structure"
"Leverage analysis"
"Working capital"

Returns:
├─ Asset composition
├─ Liability breakdown
├─ Equity assessment
├─ Working capital trends
└─ Leverage metrics
```

### 💰 Cash Flow Analysis
```
"Cash flow analysis"
"Free cash flow trends"
"Cash generation"
"Operating cash flow"

Returns:
├─ Operating CF analysis
├─ Investing CF analysis
├─ Financing CF analysis
├─ Free cash flow
└─ Cash conversion
```

### 📊 Ratio Analysis
```
"Advanced ratio analysis"
"DuPont ROE"
"Efficiency ratios"
"Solvency metrics"

Returns:
├─ Profitability ratios (4)
├─ Return ratios (3)
├─ Liquidity ratios (3)
├─ Efficiency ratios (5+)
└─ Solvency ratios (4)
```

### 📐 Trend Analysis
```
"Trend analysis"
"Anomaly detection"
"Volatility analysis"
"Future forecast"

Returns:
├─ YoY growth rates
├─ Anomalies detected
├─ Volatility metrics
└─ Trend forecast
```

---

## By Investment Decision Type

### For Equity Investor
```
QUERY SEQUENCE:
1. "Comprehensive financial health check"
2. "Profitability and margin trends"
3. "Leverage and solvency analysis"
4. "Cash flow and free cash flow"
5. "Trends and anomalies"

FOCUS ON:
├─ ROE and ROA (returns)
├─ Debt-to-Equity (leverage)
├─ Free Cash Flow (cash generation)
├─ Profit margins (profitability)
└─ Growth trends (momentum)
```

### For Debt/Credit Analyst
```
QUERY SEQUENCE:
1. "Leverage and debt analysis"
2. "Interest coverage ratio"
3. "Operating cash flow analysis"
4. "Working capital trends"
5. "Liquidity ratios"

FOCUS ON:
├─ Debt ratios (leverage)
├─ Interest coverage (safety)
├─ Operating CF (repayment ability)
├─ Current ratio (short-term)
└─ Equity structure (safety margin)
```

### For Operations Manager
```
QUERY SEQUENCE:
1. "Income statement analysis"
2. "Expense structure"
3. "Cash flow from operations"
4. "Efficiency ratios"
5. "Trends in costs"

FOCUS ON:
├─ Gross margin (pricing power)
├─ OpEx ratio (cost control)
├─ Operating CF (cash generation)
├─ Asset turnover (efficiency)
└─ Margin trends (management)
```

### For Investment Committee
```
QUERY SEQUENCE:
1. "Comprehensive financial health check"
2. "Advanced ratio analysis"
3. "Trend and anomaly detection"
4. "Cash flow sustainability"
5. "Forecast next 3 years"

FOCUS ON:
├─ All key ratios (20+)
├─ Historical trends
├─ Anomalies/risks
├─ Cash generation
└─ Forward estimates
```

---

## Ratios Organized by Category

### 📊 PROFITABILITY RATIOS (Higher is Better)
```
Metric                    | Calculation              | Benchmark
--------------------------|--------------------------|----------
Gross Profit Margin       | GP / Revenue × 100       | Varies by industry
Operating Profit Margin   | EBIT / Revenue × 100     | 5-20%
EBITDA Margin            | EBITDA / Revenue × 100   | 10-25%
Net Profit Margin        | NI / Revenue × 100       | 3-10%

👍 Good Signs:
  • Margins > 10-15%
  • Stable or improving over time
  • Above industry average
```

### 💰 RETURN RATIOS (Higher is Better)
```
Metric                    | Calculation              | Benchmark
--------------------------|--------------------------|----------
Return on Assets (ROA)    | NI / Total Assets × 100  | > 5%
Return on Equity (ROE)    | NI / Equity × 100        | > 15%
DuPont ROE               | NM × AT × EM              | > 15%

👍 Good Signs:
  • ROE > 15%
  • ROA > 5%
  • Consistent returns
```

### 💧 LIQUIDITY RATIOS (1.0-2.0 is Good)
```
Metric                    | Calculation              | Benchmark
--------------------------|--------------------------|----------
Current Ratio             | CA / CL                  | 1.0-2.0
Quick Ratio              | (CA - Inv) / CL          | 0.8-1.0
Cash Ratio               | Cash / CL                | > 0.2

👍 Good Signs:
  • Current Ratio 1.5-2.0
  • Quick Ratio > 1.0
  • Cash Ratio > 0.2
  • Stable working capital
```

### ⚙️ EFFICIENCY RATIOS (Higher is Usually Better)
```
Metric                    | Calculation              | Benchmark
--------------------------|--------------------------|----------
Asset Turnover            | Revenue / Assets         | > 1.0
Receivables Turnover      | Revenue / AR             | 6-12x
Days Sales Outstanding    | 365 / RTO                | 30-60 days
Inventory Turnover        | COGS / Inventory         | 6-12x
Days Inventory Outstanding| 365 / ITO                | 30-90 days

👍 Good Signs:
  • Asset Turnover > 1.0
  • DSO < 60 days (fast collection)
  • DIO < 90 days (fast turnover)
  • Improving efficiency trends
```

### 🛡️ SOLVENCY RATIOS (Context-Dependent)
```
Metric                    | Calculation              | Benchmark
--------------------------|--------------------------|----------
Debt-to-Equity            | Total Debt / Equity      | < 1.0
Debt-to-Assets            | Total Debt / Assets      | < 0.5
Equity Multiplier         | Assets / Equity          | < 2.5
Interest Coverage         | EBIT / Interest          | > 2.5x

👍 Good Signs:
  • Debt-to-Equity < 1.0 (more equity)
  • Interest Coverage > 2.5x (safe)
  • Stable leverage
  • Improving debt reduction
```

---

## Assessment Color Coding

### PROFITABILITY
```
🟢 Healthy          | Margin > 10%, ROE > 15%, improving trend
🟡 Moderate         | Margin 5-10%, ROE 10-15%, stable
🟠 Caution          | Margin 2-5%, ROE 5-10%, declining trend
🔴 Warning          | Margin < 2%, ROE < 5%, deteriorating
```

### LIQUIDITY
```
🟢 Strong           | Current Ratio 1.5-2.5, Quick > 1.0
🟡 Adequate         | Current Ratio 1.0-1.5, Quick 0.8-1.0
🟠 Caution          | Current Ratio 0.8-1.0, Quick < 0.8
🔴 Warning          | Current Ratio < 0.8 (liquidity stress)
```

### SOLVENCY/LEVERAGE
```
🟢 Conservative     | Debt-to-Equity < 0.5, Int. Coverage > 5x
🟡 Moderate         | Debt-to-Equity 0.5-1.0, Int. Coverage 2.5-5x
🟠 Caution          | Debt-to-Equity 1.0-2.0, Int. Coverage 1.5-2.5x
🔴 Warning          | Debt-to-Equity > 2.0, Int. Coverage < 1.5x
```

### TRENDS
```
↗️  Improving       | Growth > 5%, margins expanding, consistent
→   Stable          | Growth 0-5%, margins flat, predictable
↘️  Declining       | Growth < 0%, margins shrinking, concerning
⚠️  Volatile        | Inconsistent changes, anomalies detected
```

---

## Decision Tree - Which Analysis?

```
START: What do you want to know?

├─ "Is the company making money?"
│  └─ → Income Statement Analysis + Profitability Ratios
│
├─ "Can it pay its bills?"
│  └─ → Liquidity Ratios + Balance Sheet Analysis
│
├─ "Can it service its debt?"
│  └─ → Solvency Ratios + Interest Coverage
│
├─ "Is it generating cash?"
│  └─ → Cash Flow Analysis + Free Cash Flow
│
├─ "Is it growing?"
│  └─ → Trend Analysis + Revenue Growth + CAGR
│
├─ "What's the financial structure?"
│  └─ → Balance Sheet Analysis + Leverage Ratios
│
├─ "Is anything unusual happening?"
│  └─ → Trend Analysis + Anomaly Detection
│
├─ "What's the ROE/ROA?"
│  └─ → Return Ratios + DuPont Analysis
│
└─ "Everything - comprehensive view"
   └─ → All analyses (Advanced Ratios + Cash Flow + Balance Sheet + Income + Trends)
```

---

## Sample Output Interpretation

### Example Ratio Output
```
Net Profit Margin
2022: 8.50% → 2023: 9.20% → 2024: 10.15%  ↗️ +1.65pp

Interpretation:
• Company is improving profitability
• Each dollar of revenue generates more profit
• Trend is positive (↗️)
• No red flags
```

### Example Anomaly Output
```
⚠️ 2023: Revenue: +45.5% from mean (Z=2.8)

Interpretation:
• Revenue in 2023 was unusual
• 45.5% higher than average year
• Statistically significant (Z > 2.0)
• Could be: Acquisition, one-time item, or data error
• Action: Investigate why 2023 was different
```

### Example Free Cash Flow Output
```
Free Cash Flow
2022: $250M ✅ → 2023: $220M ✅ → 2024: $180M ⚠️

Average FCF: $150M (Healthy)
• FCF is positive (company generates cash)
• Declining trend (concerning)
• Action: Check if CapEx increased or OCF decreased
```

---

## Quick Memo Template

```
TO: Investment Committee
RE: Financial Analysis of [Company Name]
DATE: [Date]

HEADLINE FINDINGS:
├─ Profitability: [Assessment - use 🟢🟡🟠🔴]
├─ Leverage: [Assessment - use 🟢🟡🟠🔴]
├─ Liquidity: [Assessment - use 🟢🟡🟠🔴]
├─ Cash Generation: [Assessment - use 🟢🟡🟠🔴]
└─ Trends: [Assessment - use ↗️ → ↘️]

KEY METRICS (3-Year):
• Net Margin: ____%
• ROE: ____%
• Debt-to-Equity: ____x
• Free Cash Flow: $____M

RED FLAGS (if any):
├─ [Anomaly 1]
├─ [Anomaly 2]
└─ [Anomaly 3]

RECOMMENDATION:
[Based on overall assessment]
```

---

## 🎯 Best Practices

### DO ✅
- Compare ratios to industry benchmarks
- Look at 3-5 year trends, not single year
- Check for anomalies in the data
- Combine multiple metrics for full picture
- Review absolute values, not just ratios
- Understand WHY metrics changed

### DON'T ❌
- Make decisions on single metric alone
- Ignore trends and context
- Compare across different industries
- Trust forecasts as predictions
- Miss anomalies and outliers
- Ignore cash flow (profits can be fake)

---

This guide provides visual organization of all analysis types and metrics available in your enhanced financial analysis system.
