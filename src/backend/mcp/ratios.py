import pandas as pd

def calculate_ratios(df):
    """
    Calculates key financial ratios from the consolidated DataFrame.
    Returns a formatted string report.
    """
    if df is None or df.empty:
        return None, "No data available for ratio analysis."

    # 1. Standardize Data Access
    # We create a helper to find values safely by keyword
    def get_series(keywords):
        for key in keywords:
            # Case-insensitive search in the 'Line Item' column
            match = df[df['Line Item'].astype(str).str.lower().str.contains(key.lower(), na=False)]
            if not match.empty:
                # Return the numeric columns (Years)
                return match.iloc[0, 1:].astype(float)
        return None

    # 2. Define Ratio Components (Mapping to Samani/IAS Standards)
    # P&L Items
    revenue = get_series(['Revenue', 'Total Revenue', 'Sales'])
    net_income = get_series(['Profit for the Year', 'Net Income', 'Profit After Tax'])
    gross_profit = get_series(['Gross Profit'])
    op_profit = get_series(['Operating Profit', 'EBIT'])
    
    # Balance Sheet Items
    curr_assets = get_series(['Total current assets', 'Current Assets'])
    curr_liabs = get_series(['Total current liabilities', 'Current Liabilities'])
    total_assets = get_series(['TOTAL ASSETS', 'Total Assets'])
    total_equity = get_series(['Total equity', 'Shareholder Equity'])
    inventory = get_series(['Inventories', 'Inventory'])

    ratios = {}
    
    # 3. Calculate Ratios (Year by Year)
    try:
        # --- Liquidity Ratios ---
        if curr_assets is not None and curr_liabs is not None:
            ratios['Current Ratio'] = curr_assets / curr_liabs
            
            if inventory is not None:
                ratios['Quick Ratio'] = (curr_assets - inventory) / curr_liabs

        # --- Profitability Ratios ---
        if revenue is not None:
            if gross_profit is not None:
                ratios['Gross Margin (%)'] = (gross_profit / revenue) * 100
            if net_income is not None:
                ratios['Net Profit Margin (%)'] = (net_income / revenue) * 100
            if op_profit is not None:
                ratios['Operating Margin (%)'] = (op_profit / revenue) * 100

        # --- Return Ratios (Cross-Statement) ---
        if net_income is not None:
            if total_assets is not None:
                ratios['Return on Assets (ROA) %'] = (net_income / total_assets) * 100
            if total_equity is not None:
                ratios['Return on Equity (ROE) %'] = (net_income / total_equity) * 100

    except Exception as e:
        return None, f"Error calculating ratios: {str(e)}"

    if not ratios:
        return None, "Could not identify enough matching line items (Assets, Revenue, Equity) to calculate standard ratios."

    # 4. Format Output
    # Convert dict of Series into a DataFrame for display
    ratio_df = pd.DataFrame(ratios).T # Transpose so Years are columns
    
    # Formatting to string
    report = "### 📊 Financial Ratio Analysis\n\n"
    
    for ratio_name, row in ratio_df.iterrows():
        report += f"**{ratio_name}**\n"
        values_str = " → ".join([f"{val:.2f}" for val in row.values])
        
        # Add basic insight
        trend = "Stable"
        if len(row) > 1:
            if row.iloc[-1] > row.iloc[0] * 1.05: trend = "Improving ↗️"
            elif row.iloc[-1] < row.iloc[0] * 0.95: trend = "Declining ↘️"
        
        report += f"{values_str}  *({trend})*\n\n"

    return report, "Ratios calculated successfully."