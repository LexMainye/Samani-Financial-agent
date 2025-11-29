import pandas as pd
import re

def extract_financial_data(data, keyword):
    """
    MCP Tool: Information Extraction
    Scans the data (DataFrame or String) for a specific financial line item.
    
    Returns:
        tuple: (pandas.Series numeric data, Status Message [str])
    """
    clean_keyword = keyword.lower().strip()
    
    # 1. Handle DataFrame Input (CSV/XLSX)
    if isinstance(data, pd.DataFrame):
        # Clean column names for search
        data.columns = data.columns.astype(str)
        
        # Strategy A: Look for keyword in the first column (common in financial statements)
        # Strategy B: Scan all string columns
        
        for col in data.select_dtypes(include=['object', 'string']).columns:
            # Find rows where the column contains the keyword
            matches = data[data[col].astype(str).str.lower().str.contains(clean_keyword, na=False)]
            
            if not matches.empty:
                # We extract the numeric values from the first matching row
                row_values = matches.iloc[0]
                
                # Convert row to numeric, dropping the label column(s)
                numeric_series = pd.to_numeric(row_values, errors='coerce').dropna()
                
                # If we found enough data points (e.g., > 1), return it
                if len(numeric_series) > 1:
                    return numeric_series, f"Found '{keyword}' in structured data row."
        
        return None, f"Could not find a numeric series for '{keyword}' in the spreadsheet."

    # 2. Handle String Input (PDF)
    elif isinstance(data, str):
        # Strategy: Regex for "Revenue: 100, 200, 300" or tabular text patterns
        lines = data.split('\n')
        for line in lines:
            if clean_keyword in line.lower():
                # Extract numbers from this line
                # Regex looks for numbers, possibly with decimals, ignoring commas
                numbers = re.findall(r"[-+]?\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?", line)
                
                # Clean commas and convert to floats
                clean_numbers = []
                for n in numbers:
                    try:
                        clean_numbers.append(float(n.replace(',', '')))
                    except ValueError:
                        continue
                        
                if len(clean_numbers) > 1:
                    series = pd.Series(clean_numbers)
                    return series, f"Found '{keyword}' in text line: {line.strip()[:50]}..."
        
        return None, f"Could not find data for '{keyword}' in the document text."

    return None, "Invalid data format."