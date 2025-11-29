"""
Advanced Financial Ratio Analysis Module
Calculates comprehensive profitability, liquidity, solvency, and efficiency ratios
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional

class AdvancedRatioAnalyzer:
    """Comprehensive financial ratio calculator with trend analysis"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with consolidated financial data
        Args:
            df: DataFrame with 'Line Item' as first column, then years as columns
        """
        self.df = df
        self.ratios = {}
        self.warnings = []
    
    def _get_series(self, keywords: list) -> Optional[pd.Series]:
        """Safely retrieve financial line item by keywords"""
        for key in keywords:
            match = self.df[self.df['Line Item'].astype(str).str.lower().str.contains(key.lower(), na=False)]
            if not match.empty:
                numeric_data = match.iloc[0, 1:].apply(pd.to_numeric, errors='coerce')
                if numeric_data.notna().sum() > 0:  # Has at least one numeric value
                    return numeric_data
        return None
    
    def calculate_all_ratios(self) -> Tuple[pd.DataFrame, str]:
        """Calculate all ratio categories and return report"""
        
        # Extract key line items
        revenue = self._get_series(['Revenue', 'Total Revenue', 'Sales', 'Total Sales'])
        cogs = self._get_series(['Cost of Goods Sold', 'COGS', 'Cost of sales'])
        gross_profit = self._get_series(['Gross Profit'])
        operating_profit = self._get_series(['Operating Profit', 'EBIT', 'Operating Income'])
        ebitda = self._get_series(['EBITDA', 'Earnings Before Tax', 'EBT'])
        net_income = self._get_series(['Net Income', 'Profit for the Year', 'Net Profit', 'PAT', 'Profit After Tax'])
        
        # Balance Sheet Items
        current_assets = self._get_series(['Total Current Assets', 'Current Assets'])
        current_liabilities = self._get_series(['Total Current Liabilities', 'Current Liabilities'])
        inventory = self._get_series(['Inventory', 'Inventories', 'Stock'])
        receivables = self._get_series(['Accounts Receivable', 'Trade Receivables', 'Receivables'])
        cash = self._get_series(['Cash', 'Cash and Cash Equivalents', 'Bank Balances'])
        
        total_assets = self._get_series(['Total Assets', 'TOTAL ASSETS'])
        total_liabilities = self._get_series(['Total Liabilities', 'Total Debt'])
        total_equity = self._get_series(['Total Equity', 'Shareholders Equity', 'Share Capital'])
        
        # Liabilities breakdown
        short_term_debt = self._get_series(['Short-term Debt', 'Current Portion of Long-term Debt'])
        long_term_debt = self._get_series(['Long-term Debt', 'Non-Current Liabilities'])
        
        # Operating expenses
        operating_expenses = self._get_series(['Operating Expenses', 'Selling General and Admin'])
        depreciation = self._get_series(['Depreciation', 'Depreciation and Amortization'])
        interest_expense = self._get_series(['Interest Expense', 'Finance Costs'])
        tax_expense = self._get_series(['Income Tax Expense', 'Tax Expense'])
        
        # ============ PROFITABILITY RATIOS ============
        if revenue is not None:
            if gross_profit is not None:
                self.ratios['Gross Profit Margin (%)'] = (gross_profit / revenue) * 100
            if operating_profit is not None:
                self.ratios['Operating Profit Margin (%)'] = (operating_profit / revenue) * 100
            if ebitda is not None:
                self.ratios['EBITDA Margin (%)'] = (ebitda / revenue) * 100
            if net_income is not None:
                self.ratios['Net Profit Margin (%)'] = (net_income / revenue) * 100
        
        # ============ RETURN RATIOS ============
        if net_income is not None:
            if total_assets is not None:
                self.ratios['Return on Assets (%)'] = (net_income / total_assets) * 100
            if total_equity is not None:
                self.ratios['Return on Equity (%)'] = (net_income / total_equity) * 100
        
        # ============ LIQUIDITY RATIOS ============
        if current_assets is not None and current_liabilities is not None:
            self.ratios['Current Ratio'] = current_assets / current_liabilities
            
            if inventory is not None:
                self.ratios['Quick Ratio'] = (current_assets - inventory) / current_liabilities
            
            if cash is not None:
                self.ratios['Cash Ratio'] = cash / current_liabilities
        
        # ============ EFFICIENCY/ACTIVITY RATIOS ============
        if revenue is not None and total_assets is not None:
            self.ratios['Asset Turnover'] = revenue / total_assets
        
        if revenue is not None and receivables is not None:
            self.ratios['Receivables Turnover'] = revenue / receivables
            self.ratios['Days Sales Outstanding (DSO)'] = 365 / (revenue / receivables)
        
        if cogs is not None and inventory is not None:
            self.ratios['Inventory Turnover'] = cogs / inventory
            self.ratios['Days Inventory Outstanding (DIO)'] = 365 / (cogs / inventory)
        
        # ============ SOLVENCY/LEVERAGE RATIOS ============
        if total_liabilities is not None and total_equity is not None:
            self.ratios['Debt-to-Equity Ratio'] = total_liabilities / total_equity
        
        if total_liabilities is not None and total_assets is not None:
            self.ratios['Debt-to-Assets Ratio'] = total_liabilities / total_assets
        
        if total_equity is not None and total_assets is not None:
            self.ratios['Equity Multiplier'] = total_assets / total_equity
        
        if operating_profit is not None and interest_expense is not None:
            self.ratios['Interest Coverage Ratio'] = operating_profit / interest_expense
        
        # ============ DUPONT ANALYSIS ============
        if net_income is not None and revenue is not None and total_assets is not None and total_equity is not None:
            net_margin = net_income / revenue
            asset_turnover = revenue / total_assets
            equity_multiplier = total_assets / total_equity
            self.ratios['DuPont ROE'] = net_margin * asset_turnover * equity_multiplier
        
        # Convert to DataFrame
        ratio_df = pd.DataFrame(self.ratios).T
        report = self._generate_report(ratio_df)
        
        return ratio_df, report
    
    def _generate_report(self, ratio_df: pd.DataFrame) -> str:
        """Generate formatted analysis report"""
        report = "### 📊 Advanced Financial Ratio Analysis\n\n"
        
        categories = {
            'Profitability Ratios': ['Gross Profit Margin (%)', 'Operating Profit Margin (%)', 
                                     'EBITDA Margin (%)', 'Net Profit Margin (%)'],
            'Return Ratios': ['Return on Assets (%)', 'Return on Equity (%)', 'DuPont ROE'],
            'Liquidity Ratios': ['Current Ratio', 'Quick Ratio', 'Cash Ratio'],
            'Efficiency Ratios': ['Asset Turnover', 'Receivables Turnover', 'Days Sales Outstanding (DSO)',
                                  'Inventory Turnover', 'Days Inventory Outstanding (DIO)'],
            'Solvency Ratios': ['Debt-to-Equity Ratio', 'Debt-to-Assets Ratio', 'Equity Multiplier',
                               'Interest Coverage Ratio']
        }
        
        for category, metrics in categories.items():
            available_metrics = [m for m in metrics if m in ratio_df.index]
            if available_metrics:
                report += f"**{category}**\n"
                for metric in available_metrics:
                    row = ratio_df.loc[metric]
                    values_str = " → ".join([f"{val:.2f}" if pd.notna(val) else "N/A" for val in row.values])
                    
                    # Trend analysis
                    trend = self._analyze_trend(row)
                    
                    report += f"• {metric}: {values_str} {trend}\n"
                report += "\n"
        
        return report
    
    def _analyze_trend(self, series: pd.Series) -> str:
        """Analyze trend direction and magnitude"""
        valid_data = series.dropna()
        if len(valid_data) < 2:
            return ""
        
        first_val = valid_data.iloc[0]
        last_val = valid_data.iloc[-1]
        
        if first_val == 0:
            return ""
        
        pct_change = ((last_val - first_val) / abs(first_val)) * 100
        
        if pct_change > 10:
            return f"↗️ +{pct_change:.1f}%"
        elif pct_change < -10:
            return f"↘️ {pct_change:.1f}%"
        else:
            return f"→ ±{pct_change:.1f}%"


def analyze_financial_ratios(data: pd.DataFrame) -> Tuple[str, str]:
    """
    Main MCP Tool: Advanced Ratio Analysis
    
    Args:
        data: Consolidated financial DataFrame
    
    Returns:
        tuple: (report_text, status_message)
    """
    if data is None or data.empty:
        return "", "No data available for ratio analysis."
    
    try:
        analyzer = AdvancedRatioAnalyzer(data)
        ratio_df, report = analyzer.calculate_all_ratios()
        
        if not analyzer.ratios:
            return "", "Could not identify enough line items to calculate ratios."
        
        return report, "✅ Advanced ratio analysis complete."
    
    except Exception as e:
        return "", f"❌ Error in ratio analysis: {str(e)}"
