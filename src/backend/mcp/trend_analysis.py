"""
Trend Analysis & Anomaly Detection Module
Identifies trends, anomalies, and unusual patterns in financial data
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, List, Optional
from scipy import stats

class TrendAnalyzer:
    """Analyzes trends and detects anomalies in financial data"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with consolidated financial data
        Args:
            df: DataFrame with financial data across multiple years
        """
        self.df = df
        self.anomalies = []
    
    def _get_series(self, keywords: list) -> Optional[pd.Series]:
        """Safely retrieve financial line item by keywords"""
        for key in keywords:
            match = self.df[self.df['Line Item'].astype(str).str.lower().str.contains(key.lower(), na=False)]
            if not match.empty:
                numeric_data = match.iloc[0, 1:].apply(pd.to_numeric, errors='coerce')
                if numeric_data.notna().sum() > 0:
                    return numeric_data
        return None
    
    def detect_anomalies(self, series: pd.Series, name: str, threshold_zscore: float = 2.0) -> List[Tuple[str, str]]:
        """
        Detect statistical anomalies using Z-score method
        
        Args:
            series: Data series
            name: Name of the metric
            threshold_zscore: Z-score threshold (2.0 = 95% confidence)
        
        Returns:
            List of (year, description) anomaly tuples
        """
        anomalies_found = []
        
        valid_series = series.dropna()
        if len(valid_series) < 2:
            return anomalies_found
        
        # Calculate Z-scores
        mean = valid_series.mean()
        std = valid_series.std()
        
        if std == 0:  # Constant value
            return anomalies_found
        
        z_scores = np.abs((valid_series - mean) / std)
        
        for year, z_score in z_scores.items():
            if z_score > threshold_zscore:
                value = valid_series[year]
                pct_from_mean = ((value - mean) / abs(mean)) * 100 if mean != 0 else 0
                anomalies_found.append((year, f"{name}: {pct_from_mean:+.1f}% from mean (Z={z_score:.2f})"))
        
        return anomalies_found
    
    def analyze_all_trends(self) -> Tuple[str, str]:
        """Analyze trends across all major financial metrics"""
        
        report = "### 📊 Trend Analysis & Anomaly Detection\n\n"
        
        # Key metrics to analyze
        key_metrics = [
            (['Revenue', 'Total Revenue', 'Sales'], 'Revenue'),
            (['Profit for the Year', 'Net Income', 'Net Profit'], 'Net Income'),
            (['Total Assets', 'TOTAL ASSETS'], 'Total Assets'),
            (['Total Equity', 'Shareholders Equity'], 'Total Equity'),
            (['Operating Profit', 'EBIT'], 'Operating Profit'),
            (['Current Assets', 'Total Current Assets'], 'Current Assets'),
        ]
        
        # ============ TREND ANALYSIS ============
        report += "**Overall Trend Analysis**\n\n"
        
        for keywords, metric_name in key_metrics:
            series = self._get_series(keywords)
            if series is not None and len(series.dropna()) > 1:
                report += f"**{metric_name}:**\n"
                
                # Calculate growth rates
                valid_series = series.dropna()
                values = valid_series.values
                years = valid_series.index.tolist()
                
                # Year-over-year growth
                yoy_growth = []
                for i in range(1, len(values)):
                    growth = ((values[i] - values[i-1]) / abs(values[i-1])) * 100 if values[i-1] != 0 else 0
                    yoy_growth.append(growth)
                    year = years[i]
                    direction = "↗️" if growth > 0 else "↘️"
                    report += f"• {year}: {growth:+.1f}% {direction}\n"
                
                # Trend direction
                if len(yoy_growth) > 0:
                    avg_growth = np.mean(yoy_growth)
                    latest_growth = yoy_growth[-1] if len(yoy_growth) > 0 else 0
                    
                    trend_text = ""
                    if avg_growth > 5:
                        trend_text = "Strong upward ↗️"
                    elif avg_growth > 0:
                        trend_text = "Moderate upward ↗️"
                    elif avg_growth > -5:
                        trend_text = "Stable with slight decline ↘️"
                    else:
                        trend_text = "Strong downward ↘️"
                    
                    report += f"• Average Growth: {avg_growth:+.1f}% ({trend_text})\n"
                    
                    # Recent trend vs average
                    if latest_growth > avg_growth + 5:
                        report += f"  📈 Accelerating (latest > avg by {latest_growth - avg_growth:+.1f}pp)\n"
                    elif latest_growth < avg_growth - 5:
                        report += f"  📉 Decelerating (latest < avg by {latest_growth - avg_growth:+.1f}pp)\n"
                
                report += "\n"
        
        # ============ ANOMALY DETECTION ============
        report += "**Anomalies Detected**\n\n"
        
        all_anomalies = []
        for keywords, metric_name in key_metrics:
            series = self._get_series(keywords)
            if series is not None:
                anomalies = self.detect_anomalies(series, metric_name, threshold_zscore=2.0)
                all_anomalies.extend(anomalies)
        
        if all_anomalies:
            for year, description in sorted(all_anomalies):
                report += f"⚠️ {year}: {description}\n"
        else:
            report += "✅ No significant anomalies detected\n"
        
        report += "\n"
        
        return report, "✅ Trend analysis complete."
    
    def analyze_consistency(self) -> str:
        """Analyze consistency and volatility of metrics"""
        
        report = "### 📐 Consistency & Volatility Analysis\n\n"
        
        metrics_to_check = [
            (['Revenue', 'Total Revenue'], 'Revenue'),
            (['Net Income', 'Profit for the Year'], 'Net Income'),
            (['Total Assets', 'TOTAL ASSETS'], 'Total Assets'),
        ]
        
        report += "**Volatility Metrics (CV = Coefficient of Variation)**\n\n"
        
        for keywords, name in metrics_to_check:
            series = self._get_series(keywords)
            if series is not None and len(series.dropna()) > 1:
                valid_series = series.dropna()
                
                # Coefficient of Variation
                cv = (valid_series.std() / abs(valid_series.mean())) * 100
                
                # Categorize volatility
                if cv < 10:
                    volatility = "Very Stable 🟢"
                elif cv < 20:
                    volatility = "Stable 🟡"
                elif cv < 35:
                    volatility = "Moderate Volatility 🟠"
                else:
                    volatility = "High Volatility 🔴"
                
                report += f"**{name}:**\n"
                report += f"• Coefficient of Variation: {cv:.1f}% ({volatility})\n"
                report += f"• Mean: KES {valid_series.mean():,.0f}\n"
                report += f"• Std Dev: KES {valid_series.std():,.0f}\n"
                report += f"• Range: KES {valid_series.min():,.0f} to KES {valid_series.max():,.0f}\n\n"
        
        return report
    
    def forecast_next_periods(self) -> str:
        """Simple linear regression forecast for next periods"""
        
        report = "### 🔮 Simple Trend Forecast\n\n"
        
        revenue = self._get_series(['Revenue', 'Total Revenue', 'Sales'])
        
        if revenue is not None and len(revenue.dropna()) > 2:
            valid_data = revenue.dropna()
            
            # Prepare data for linear regression
            x = np.arange(len(valid_data))
            y = valid_data.values
            
            # Linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Forecast next 3 periods
            forecast_x = np.arange(len(valid_data), len(valid_data) + 3)
            forecast_y = slope * forecast_x + intercept
            
            report += f"**Revenue Forecast (Linear Extrapolation)**\n"
            report += f"• Model R²: {r_value**2:.3f}\n"
            report += f"• Annual Trend: KES {slope:,.0f}\n\n"
            
            last_year = valid_data.index[-1]
            forecast_years = [str(int(last_year) + i) for i in range(1, 4)]
            
            report += "Projected Revenue:\n"
            for i, (year, value) in enumerate(zip(forecast_years, forecast_y)):
                report += f"• {year}: KES {value:,.0f}\n"
        
        return report


def analyze_trends_and_anomalies(data: pd.DataFrame) -> Tuple[str, str]:
    """
    Main MCP Tool: Trend and Anomaly Analysis
    
    Args:
        data: Consolidated financial DataFrame
    
    Returns:
        tuple: (report_text, status_message)
    """
    if data is None or data.empty:
        return "", "No data available for trend analysis."
    
    try:
        analyzer = TrendAnalyzer(data)
        report, msg = analyzer.analyze_all_trends()
        report += analyzer.analyze_consistency()
        report += analyzer.forecast_next_periods()
        
        return report, msg
    
    except Exception as e:
        return "", f"❌ Error in trend analysis: {str(e)}"
