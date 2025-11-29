import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings

# Suppress statsmodels warnings for clean output
warnings.filterwarnings("ignore")

def generate_forecast(series, steps=4):
    """
    MCP Tool: Time-Series Forecasting
    Takes a pandas Series of historical data and forecasts future periods.
    """
    if series is None or len(series) < 3:
        return None, "Not enough data points to generate a forecast (minimum 3 required)."

    try:
        # Ensure data is float
        series = series.astype(float)
        
        # Reset index for clean processing
        series = series.reset_index(drop=True)

        # Statistical Model: Holt-Winters Exponential Smoothing
        # 'trend=add' handles linear growth
        # 'damped_trend=True' prevents unrealistic infinite growth
        model = ExponentialSmoothing(series, trend='add', damped_trend=True, seasonal=None).fit()
        forecast = model.forecast(steps)
        
        return forecast, "Forecast generated successfully using Holt-Winters Exponential Smoothing."

    except Exception as e:
        return None, f"Forecasting model failed: {str(e)}"