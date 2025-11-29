"""
Balance Sheet Analysis Module
Analyzes assets, liabilities, and equity structure
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional

class BalanceSheetAnalyzer:
    """Analyzes balance sheet composition and health"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with consolidated financial data
        Args:
            df: DataFrame with balance sheet data
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
    
    def analyze_balance_sheet(self) -> Tuple[str, str]:
        """Comprehensive balance sheet analysis"""
        
        report = "### 📊 Balance Sheet Analysis\n\n"
        
        # Extract balance sheet items
        current_assets = self._get_series(['Total Current Assets', 'Current Assets'])
        non_current_assets = self._get_series(['Non-Current Assets', 'Total Non-Current Assets', 'Fixed Assets'])
        total_assets = self._get_series(['Total Assets', 'TOTAL ASSETS'])
        
        current_liabilities = self._get_series(['Total Current Liabilities', 'Current Liabilities'])
        non_current_liabilities = self._get_series(['Non-Current Liabilities', 'Long-term Liabilities'])
        total_liabilities = self._get_series(['Total Liabilities'])
        
        total_equity = self._get_series(['Total Equity', 'Shareholders Equity', 'Total Shareholders Equity'])
        
        # Asset breakdown
        cash = self._get_series(['Cash', 'Cash and Cash Equivalents'])
        receivables = self._get_series(['Accounts Receivable', 'Trade Receivables'])
        inventory = self._get_series(['Inventory', 'Inventories'])
        ppe = self._get_series(['Property Plant and Equipment', 'Fixed Assets', 'PPE'])
        intangibles = self._get_series(['Intangible Assets', 'Goodwill'])
        
        # Liability breakdown
        short_term_debt = self._get_series(['Short-term Borrowings', 'Current Portion of Long-term Debt'])
        long_term_debt = self._get_series(['Long-term Debt', 'Long-term Borrowings'])
        
        # ============ BALANCE SHEET STRUCTURE ============
        if total_assets is not None and total_liabilities is not None and total_equity is not None:
            report += "**Balance Sheet Composition (% of Total Assets)**\n"
            
            for year in total_assets.index:
                if pd.notna(total_assets[year]):
                    report += f"\n{year}:\n"
                    
                    # Asset composition
                    if current_assets is not None and pd.notna(current_assets[year]):
                        pct_ca = (current_assets[year] / total_assets[year]) * 100
                        report += f"• Current Assets: {pct_ca:.1f}%\n"
                    
                    if non_current_assets is not None and pd.notna(non_current_assets[year]):
                        pct_nca = (non_current_assets[year] / total_assets[year]) * 100
                        report += f"• Non-Current Assets: {pct_nca:.1f}%\n"
                    
                    # Liability & Equity composition
                    if total_liabilities is not None and pd.notna(total_liabilities[year]):
                        pct_liab = (total_liabilities[year] / total_assets[year]) * 100
                        report += f"• Total Liabilities: {pct_liab:.1f}%\n"
                    
                    if total_equity is not None and pd.notna(total_equity[year]):
                        pct_eq = (total_equity[year] / total_assets[year]) * 100
                        report += f"• Total Equity: {pct_eq:.1f}%\n"
            
            report += "\n"
        
        # ============ ASSET QUALITY ANALYSIS ============
        if total_assets is not None:
            report += "**Asset Quality & Composition**\n"
            
            # Liquid assets ratio
            if current_assets is not None:
                liquid_ratio = (current_assets / total_assets) * 100
                report += f"• Liquidity: {liquid_ratio.mean():.1f}% in current assets\n"
            
            # Working capital
            if current_assets is not None and current_liabilities is not None:
                working_capital = current_assets - current_liabilities
                report += f"• Working Capital Trend:\n"
                for year, wc in working_capital.items():
                    if pd.notna(wc):
                        status = "✅ Positive" if wc > 0 else "❌ Negative"
                        report += f"  {year}: KES {wc:,.0f} {status}\n"
            
            # Fixed assets ratio
            if ppe is not None:
                ppe_ratio = (ppe / total_assets) * 100
                report += f"• Capital Intensity: {ppe_ratio.mean():.1f}% in PPE\n"
            
            # Intangible assets
            if intangibles is not None:
                intang_ratio = (intangibles / total_assets) * 100
                if intang_ratio.mean() > 10:
                    report += f"⚠️ • High Intangible Assets: {intang_ratio.mean():.1f}%\n"
            
            report += "\n"
        
        # ============ FINANCIAL LEVERAGE ============
        if total_liabilities is not None and total_equity is not None:
            report += "**Financial Leverage Analysis**\n"
            
            debt_to_equity = total_liabilities / total_equity
            report += f"• Debt-to-Equity Ratio:\n"
            for year, de in debt_to_equity.items():
                if pd.notna(de):
                    report += f"  {year}: {de:.2f}x\n"
            
            # Evaluate leverage
            avg_de = debt_to_equity.mean()
            if avg_de < 0.5:
                report += "  ✅ Conservative leverage (low risk)\n"
            elif avg_de < 1.0:
                report += "  ✅ Moderate leverage (balanced)\n"
            elif avg_de < 2.0:
                report += "  ⚠️ Higher leverage (higher risk)\n"
            else:
                report += "  ❌ High leverage (significant risk)\n"
            
            report += "\n"
        
        # ============ DEBT STRUCTURE ============
        if short_term_debt is not None or long_term_debt is not None:
            report += "**Debt Structure**\n"
            
            total_debt = pd.Series(0.0, index=self.df.columns[1:])
            
            if short_term_debt is not None:
                total_debt += short_term_debt.fillna(0)
                report += f"• Average Short-term Debt: KES {short_term_debt.mean():,.0f}\n"
            
            if long_term_debt is not None:
                total_debt += long_term_debt.fillna(0)
                report += f"• Average Long-term Debt: KES {long_term_debt.mean():,.0f}\n"
            
            if short_term_debt is not None and long_term_debt is not None:
                total_debt_val = short_term_debt + long_term_debt
                st_pct = (short_term_debt / total_debt_val) * 100
                report += f"• Short-term Debt %: {st_pct.mean():.1f}%\n"
            
            report += "\n"
        
        # ============ EQUITY ANALYSIS ============
        if total_equity is not None and total_assets is not None:
            report += "**Equity Strength**\n"
            
            equity_ratio = (total_equity / total_assets) * 100
            report += f"• Equity Ratio (Equity/Assets):\n"
            for year, eq_ratio in equity_ratio.items():
                if pd.notna(eq_ratio):
                    status = "✅ Strong" if eq_ratio > 50 else "⚠️ Moderate"
                    report += f"  {year}: {eq_ratio:.1f}% {status}\n"
            
            # Equity trend
            if len(total_equity) > 1:
                first_equity = total_equity.iloc[0]
                last_equity = total_equity.iloc[-1]
                if first_equity > 0:
                    equity_growth = ((last_equity - first_equity) / first_equity) * 100
                    direction = "↗️" if equity_growth > 0 else "↘️"
                    report += f"• Equity Growth: {equity_growth:+.1f}% {direction}\n"
            
            report += "\n"
        
        return report, "✅ Balance sheet analysis complete."


def analyze_balance_sheet(data: pd.DataFrame) -> Tuple[str, str]:
    """
    Main MCP Tool: Balance Sheet Analysis
    
    Args:
        data: Consolidated financial DataFrame
    
    Returns:
        tuple: (report_text, status_message)
    """
    if data is None or data.empty:
        return "", "No data available for balance sheet analysis."
    
    try:
        analyzer = BalanceSheetAnalyzer(data)
        report, msg = analyzer.analyze_balance_sheet()
        
        return report, msg
    
    except Exception as e:
        return "", f"❌ Error in balance sheet analysis: {str(e)}"
