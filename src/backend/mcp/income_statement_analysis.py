"""
Income Statement Analysis Module
Analyzes profitability, expenses, and revenue drivers
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional

class IncomeStatementAnalyzer:
    """Analyzes income statement and profitability trends"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with consolidated financial data
        Args:
            df: DataFrame with income statement data
        """
        self.df = df
    
    def _get_series(self, keywords: list) -> Optional[pd.Series]:
        """Safely retrieve financial line item by keywords"""
        for key in keywords:
            match = self.df[self.df['Line Item'].astype(str).str.lower().str.contains(key.lower(), na=False)]
            if not match.empty:
                numeric_data = match.iloc[0, 1:].apply(pd.to_numeric, errors='coerce')
                if numeric_data.notna().sum() > 0:
                    return numeric_data
        return None
    
    def analyze_income_statement(self) -> Tuple[str, str]:
        """Comprehensive income statement analysis"""
        
        report = "### 📈 Income Statement Analysis\n\n"
        
        # Extract P&L items
        revenue = self._get_series(['Revenue', 'Total Revenue', 'Sales', 'Total Sales'])
        cogs = self._get_series(['Cost of Goods Sold', 'COGS', 'Cost of Sales'])
        gross_profit = self._get_series(['Gross Profit'])
        operating_expenses = self._get_series(['Operating Expenses', 'Selling General Admin', 'SG&A'])
        operating_profit = self._get_series(['Operating Profit', 'EBIT', 'Operating Income'])
        interest_expense = self._get_series(['Interest Expense', 'Finance Costs'])
        tax_expense = self._get_series(['Income Tax Expense', 'Tax Expense'])
        net_income = self._get_series(['Net Income', 'Profit for the Year', 'Net Profit', 'PAT'])
        depreciation = self._get_series(['Depreciation', 'Depreciation and Amortization'])
        
        # ============ REVENUE ANALYSIS ============
        if revenue is not None:
            report += "**Revenue Trend Analysis**\n"
            
            report += "• Absolute Revenue:\n"
            for year, val in revenue.items():
                if pd.notna(val):
                    report += f"  {year}: KES {val:,.0f}\n"
            
            # YoY Growth
            if len(revenue) > 1:
                report += f"\n• Year-over-Year Growth:\n"
                prev_val = None
                for year, val in revenue.items():
                    if pd.notna(val) and prev_val is not None:
                        growth = ((val - prev_val) / prev_val) * 100
                        direction = "↗️" if growth > 0 else "↘️"
                        report += f"  {year}: {growth:+.1f}% {direction}\n"
                    if pd.notna(val):
                        prev_val = val
            
            # CAGR Calculation
            if len(revenue) > 1:
                first_val = revenue.dropna().iloc[0]
                last_val = revenue.dropna().iloc[-1]
                years = len(revenue.dropna()) - 1
                if years > 0:
                    cagr = ((last_val / first_val) ** (1 / years) - 1) * 100
                    report += f"\n• CAGR (Multi-year): {cagr:+.1f}%\n"
            
            report += "\n"
        
        # ============ EXPENSE ANALYSIS ============
        if revenue is not None:
            report += "**Expense Structure (% of Revenue)**\n"
            
            for year in revenue.index:
                if pd.notna(revenue[year]):
                    report += f"\n{year}:\n"
                    
                    if cogs is not None and pd.notna(cogs[year]):
                        cogs_pct = (cogs[year] / revenue[year]) * 100
                        report += f"• COGS: {cogs_pct:.1f}%\n"
                    
                    if operating_expenses is not None and pd.notna(operating_expenses[year]):
                        opex_pct = (operating_expenses[year] / revenue[year]) * 100
                        report += f"• Operating Expenses: {opex_pct:.1f}%\n"
                    
                    if depreciation is not None and pd.notna(depreciation[year]):
                        depr_pct = (depreciation[year] / revenue[year]) * 100
                        report += f"• Depreciation: {depr_pct:.1f}%\n"
                    
                    if interest_expense is not None and pd.notna(interest_expense[year]):
                        int_pct = (interest_expense[year] / revenue[year]) * 100
                        report += f"• Interest Expense: {int_pct:.1f}%\n"
                    
                    if tax_expense is not None and pd.notna(tax_expense[year]):
                        tax_pct = (tax_expense[year] / revenue[year]) * 100
                        report += f"• Tax Expense: {tax_pct:.1f}%\n"
            
            report += "\n"
        
        # ============ PROFITABILITY MARGINS ============
        if revenue is not None:
            report += "**Profitability Margins Trend**\n"
            
            margins = {}
            
            if gross_profit is not None:
                margins['Gross Margin'] = (gross_profit / revenue) * 100
            if operating_profit is not None:
                margins['Operating Margin'] = (operating_profit / revenue) * 100
            if net_income is not None:
                margins['Net Profit Margin'] = (net_income / revenue) * 100
            
            for margin_name, margin_series in margins.items():
                report += f"\n**{margin_name}:**\n"
                for year, val in margin_series.items():
                    if pd.notna(val):
                        report += f"  {year}: {val:.1f}%\n"
                
                # Trend
                if len(margin_series.dropna()) > 1:
                    first_m = margin_series.dropna().iloc[0]
                    last_m = margin_series.dropna().iloc[-1]
                    change = last_m - first_m
                    direction = "↗️ Improving" if change > 0 else "↘️ Declining"
                    report += f"  Trend: {change:+.1f}pp {direction}\n"
            
            report += "\n"
        
        # ============ PROFITABILITY WATERFALL ============
        if revenue is not None and cogs is not None and net_income is not None:
            report += "**Profitability Waterfall (Latest Year)**\n"
            
            latest_year = revenue.index[-1]
            if pd.notna(revenue[latest_year]) and pd.notna(net_income[latest_year]):
                report += f"\nStarting (Revenue): KES {revenue[latest_year]:,.0f}\n"
                
                if cogs is not None and pd.notna(cogs[latest_year]):
                    gross = revenue[latest_year] - cogs[latest_year]
                    report += f"Less: COGS (KES {cogs[latest_year]:,.0f}) → Gross Profit: KES {gross:,.0f}\n"
                
                if operating_expenses is not None and pd.notna(operating_expenses[latest_year]):
                    report += f"Less: OpEx (KES {operating_expenses[latest_year]:,.0f})\n"
                
                if depreciation is not None and pd.notna(depreciation[latest_year]):
                    report += f"Less: Depreciation (KES {depreciation[latest_year]:,.0f})\n"
                
                if interest_expense is not None and pd.notna(interest_expense[latest_year]):
                    report += f"Less: Interest (KES {interest_expense[latest_year]:,.0f})\n"
                
                if tax_expense is not None and pd.notna(tax_expense[latest_year]):
                    report += f"Less: Taxes (KES {tax_expense[latest_year]:,.0f})\n"
                
                report += f"\nFinal (Net Income): KES {net_income[latest_year]:,.0f}\n"
            
            report += "\n"
        
        # ============ KEY OBSERVATIONS ============
        report += "**Key Observations**\n"
        
        if revenue is not None and len(revenue.dropna()) > 1:
            latest_rev = revenue.dropna().iloc[-1]
            earliest_rev = revenue.dropna().iloc[0]
            total_growth = ((latest_rev - earliest_rev) / earliest_rev) * 100
            report += f"• Total Revenue Growth: {total_growth:+.1f}%\n"
        
        if cogs is not None and revenue is not None:
            cogs_ratio = (cogs / revenue) * 100
            avg_cogs_ratio = cogs_ratio.mean()
            report += f"• Average COGS/Revenue: {avg_cogs_ratio:.1f}%\n"
            if avg_cogs_ratio < 40:
                report += "  ✅ Healthy COGS structure\n"
            elif avg_cogs_ratio > 60:
                report += "  ⚠️ High COGS - examine cost structure\n"
        
        return report, "✅ Income statement analysis complete."


def analyze_income_statement(data: pd.DataFrame) -> Tuple[str, str]:
    """
    Main MCP Tool: Income Statement Analysis
    
    Args:
        data: Consolidated financial DataFrame
    
    Returns:
        tuple: (report_text, status_message)
    """
    if data is None or data.empty:
        return "", "No data available for income statement analysis."
    
    try:
        analyzer = IncomeStatementAnalyzer(data)
        report, msg = analyzer.analyze_income_statement()
        
        return report, msg
    
    except Exception as e:
        return "", f"❌ Error in income statement analysis: {str(e)}"
