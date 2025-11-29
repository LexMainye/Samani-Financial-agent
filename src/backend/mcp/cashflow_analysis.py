"""
Cash Flow Analysis Module
Analyzes operating, investing, and financing cash flows
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional

class CashFlowAnalyzer:
    """Analyzes cash flow statements and cash position"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with consolidated financial data
        Args:
            df: DataFrame with cash flow or P&L data
        """
        self.df = df
        self.analysis = {}
    
    def _get_series(self, keywords: list) -> Optional[pd.Series]:
        """Safely retrieve financial line item by keywords"""
        for key in keywords:
            match = self.df[self.df['Line Item'].astype(str).str.lower().str.contains(key.lower(), na=False)]
            if not match.empty:
                numeric_data = match.iloc[0, 1:].apply(pd.to_numeric, errors='coerce')
                if numeric_data.notna().sum() > 0:
                    return numeric_data
        return None
    
    def analyze_cash_flows(self) -> Tuple[str, str]:
        """Analyze all cash flow metrics"""
        
        report = "### 💰 Cash Flow Analysis\n\n"
        
        # Extract cash flow items
        operating_cf = self._get_series(['Cash Flow from Operations', 'Operating Cash Flow', 'CFO'])
        investing_cf = self._get_series(['Cash Flow from Investing', 'Investing Cash Flow', 'CFI'])
        financing_cf = self._get_series(['Cash Flow from Financing', 'Financing Cash Flow', 'CFF'])
        net_cf = self._get_series(['Net Change in Cash', 'Net Cash Flow', 'Net Cash'])
        cash_balance = self._get_series(['Cash', 'Cash and Cash Equivalents'])
        
        # Extract P&L for cash conversion metrics
        net_income = self._get_series(['Net Income', 'Profit for the Year', 'Net Profit'])
        revenue = self._get_series(['Revenue', 'Total Revenue', 'Sales'])
        depreciation = self._get_series(['Depreciation', 'Depreciation and Amortization'])
        
        # ============ OPERATING CASH FLOW ANALYSIS ============
        if operating_cf is not None:
            report += "**Operating Cash Flow Analysis**\n"
            
            for year, value in operating_cf.items():
                if pd.notna(value):
                    report += f"• {year}: KES {value:,.0f}\n"
            
            # Calculate OCF margin
            if revenue is not None:
                ocf_margin = (operating_cf / revenue) * 100
                avg_margin = ocf_margin.mean()
                report += f"• Operating CF Margin (Avg): {avg_margin:.1f}%\n"
            
            # OCF vs Net Income (Quality of Earnings)
            if net_income is not None:
                ocf_to_ni = operating_cf / net_income
                report += f"• OCF/Net Income Ratio (Quality): {ocf_to_ni.mean():.2f}x\n"
                if ocf_to_ni.mean() > 1.2:
                    report += "  ✅ High quality earnings (OCF > Net Income)\n"
                elif ocf_to_ni.mean() < 0.8:
                    report += "  ⚠️ Potential earnings quality issue (OCF < Net Income)\n"
            
            report += "\n"
        
        # ============ INVESTING CASH FLOW ANALYSIS ============
        if investing_cf is not None:
            report += "**Investing Cash Flow Analysis**\n"
            
            for year, value in investing_cf.items():
                if pd.notna(value):
                    direction = "↗️ Inflow" if value > 0 else "↘️ Outflow"
                    report += f"• {year}: KES {value:,.0f} {direction}\n"
            
            # CapEx vs OCF (Reinvestment)
            if operating_cf is not None:
                capex_ratio = abs(investing_cf / operating_cf)
                report += f"• CapEx/OCF Ratio: {capex_ratio.mean():.2f}x\n"
                if capex_ratio.mean() > 1:
                    report += "  ⚠️ Heavy capital expenditure (CapEx > OCF)\n"
                else:
                    report += "  ✅ Sustainable capex (CapEx < OCF)\n"
            
            report += "\n"
        
        # ============ FINANCING CASH FLOW ANALYSIS ============
        if financing_cf is not None:
            report += "**Financing Cash Flow Analysis**\n"
            
            for year, value in financing_cf.items():
                if pd.notna(value):
                    direction = "↗️ Raising" if value > 0 else "↘️ Returning"
                    report += f"• {year}: KES {value:,.0f} {direction}\n"
            
            report += "\n"
        
        # ============ FREE CASH FLOW ============
        if operating_cf is not None and investing_cf is not None:
            report += "**Free Cash Flow (OCF - CapEx)**\n"
            fcf = operating_cf + investing_cf  # Investing CF is typically negative
            
            for year, value in fcf.items():
                if pd.notna(value):
                    status = "✅ Positive" if value > 0 else "❌ Negative"
                    report += f"• {year}: KES {value:,.0f} {status}\n"
            
            avg_fcf = fcf.mean()
            if avg_fcf > 0:
                report += f"• Average FCF: KES {avg_fcf:,.0f} (Healthy)\n"
            else:
                report += f"• Average FCF: KES {avg_fcf:,.0f} (Watch)\n"
            
            report += "\n"
        
        # ============ CASH BALANCE TREND ============
        if cash_balance is not None:
            report += "**Cash & Equivalents Position**\n"
            
            for year, value in cash_balance.items():
                if pd.notna(value):
                    report += f"• {year}: KES {value:,.0f}\n"
            
            first_val = cash_balance.iloc[0]
            last_val = cash_balance.iloc[-1]
            if first_val > 0:
                change_pct = ((last_val - first_val) / first_val) * 100
                direction = "↗️" if change_pct > 0 else "↘️"
                report += f"• Change: {change_pct:+.1f}% {direction}\n"
            
            report += "\n"
        
        # ============ KEY METRICS SUMMARY ============
        report += "**Key Metrics Summary**\n"
        if operating_cf is not None:
            report += f"• Avg Operating CF: KES {operating_cf.mean():,.0f}\n"
        if net_cf is not None:
            report += f"• Avg Net CF: KES {net_cf.mean():,.0f}\n"
        
        return report, "✅ Cash flow analysis complete."
    
    def analyze_cash_conversion(self) -> str:
        """Analyze how well the company converts earnings to cash"""
        report = "### 🔄 Cash Conversion Analysis\n\n"
        
        net_income = self._get_series(['Net Income', 'Profit for the Year'])
        operating_cf = self._get_series(['Cash Flow from Operations', 'Operating Cash Flow'])
        revenue = self._get_series(['Revenue', 'Total Revenue', 'Sales'])
        
        if net_income is not None and operating_cf is not None:
            # Cash Conversion Ratio
            ccr = operating_cf / net_income
            ccr_avg = ccr.mean()
            
            report += f"**Cash Conversion Ratio: {ccr_avg:.2f}x**\n"
            
            if ccr_avg > 1.1:
                report += "✅ Excellent - Company converts earnings to cash efficiently\n"
            elif ccr_avg > 0.9:
                report += "✅ Good - Normal conversion ratio\n"
            elif ccr_avg > 0.7:
                report += "⚠️ Fair - Some non-cash items affecting earnings\n"
            else:
                report += "❌ Poor - Significant gap between earnings and cash\n"
            
            report += "\n"
        
        return report


def analyze_cash_flow(data: pd.DataFrame) -> Tuple[str, str]:
    """
    Main MCP Tool: Cash Flow Analysis
    
    Args:
        data: Consolidated financial DataFrame
    
    Returns:
        tuple: (report_text, status_message)
    """
    if data is None or data.empty:
        return "", "No data available for cash flow analysis."
    
    try:
        analyzer = CashFlowAnalyzer(data)
        report, msg = analyzer.analyze_cash_flows()
        report += "\n" + analyzer.analyze_cash_conversion()
        
        return report, msg
    
    except Exception as e:
        return "", f"❌ Error in cash flow analysis: {str(e)}"
