import pandas as pd
import pypdf
import os
import re

def normalize_row_name(row_name):
    """
    Maps various financial terms to a standard set using fuzzy keyword matching.
    Supports multiple accounting standards: IAS, GAAP, and local standards.
    Example: 'Total Net Sales' -> 'Revenue'
    """
    row_name = str(row_name).strip().lower()
    
    # Comprehensive mapping covering Income Statement, Balance Sheet, and Cash Flow items
    mapping = {
        # ============ REVENUE/SALES ============
        'Revenue': [
            'revenue', 'sales', 'turnover', 'gross income', 'receipts',
            'operating revenue', 'total sales', 'net sales', 'sales revenue',
            'total revenue', 'annual revenue'
        ],
        
        # ============ COST OF GOODS SOLD ============
        'COGS': [
            'cost of goods sold', 'cost of sales', 'cogs', 'cost of goods',
            'cost of revenue', 'purchase of materials', 'cost of inventory'
        ],
        
        # ============ GROSS PROFIT ============
        'Gross Profit': [
            'gross profit', 'gross income', 'gross margin', 'contribution margin'
        ],
        
        # ============ OPERATING EXPENSES ============
        'Operating Expenses': [
            'operating expenses', 'operating expense', 'opex',
            'selling general and administrative', 'sg&a', 'sga',
            'admin expenses', 'selling and distribution', 'distribution costs',
            'administrative and selling', 'general and administrative',
            'operating costs'
        ],
        
        'Depreciation': [
            'depreciation', 'depreciation and amortization',
            'amortization', 'depreciation & amortization', 'd&a',
            'depr & amort'
        ],
        
        # ============ OPERATING PROFIT ============
        'Operating Profit': [
            'operating profit', 'operating income', 'ebit',
            'earnings before interest and tax', 'operating earnings',
            'profit from operations', 'operating result'
        ],
        
        # ============ INTEREST & FINANCE ============
        'Interest Expense': [
            'interest expense', 'interest cost', 'finance cost',
            'finance costs', 'interest paid', 'borrowing costs'
        ],
        
        'Interest Income': [
            'interest income', 'interest received', 'finance income'
        ],
        
        # ============ TAXES ============
        'Tax Expense': [
            'income tax expense', 'tax expense', 'provision for tax',
            'income tax', 'tax provision', 'corporate tax'
        ],
        
        # ============ NET INCOME ============
        'Net Income': [
            'net income', 'net profit', 'profit for the year',
            'profit for the period', 'profit after tax', 'pat',
            'net earnings', 'net profit for the year', 'profit attributable',
            'earnings', 'comprehensive income', 'total comprehensive income',
            'bottom line profit'
        ],
        
        # ============ BALANCE SHEET - ASSETS ============
        'Current Assets': [
            'total current assets', 'current assets', 'short-term assets',
            'total short term assets'
        ],
        
        'Cash': [
            'cash', 'cash and equivalents', 'cash and cash equivalents',
            'bank balances', 'cash balance', 'cash in hand',
            'cash and bank'
        ],
        
        'Receivables': [
            'accounts receivable', 'trade receivable', 'receivables',
            'customer receivables', 'trade receivables', 'account receivable'
        ],
        
        'Inventory': [
            'inventory', 'inventories', 'stock', 'stocks',
            'finished goods', 'raw materials', 'work in progress',
            'goods on hand'
        ],
        
        'Non-Current Assets': [
            'total non-current assets', 'non-current assets', 'fixed assets',
            'long-term assets', 'total fixed assets', 'total long-term assets'
        ],
        
        'PPE': [
            'property plant and equipment', 'ppe', 'property, plant & equipment',
            'fixed assets', 'tangible fixed assets', 'pp&e'
        ],
        
        'Intangible Assets': [
            'intangible assets', 'goodwill', 'intangible asset',
            'patents', 'trademarks', 'licenses'
        ],
        
        'Total Assets': [
            'total assets', 'total asset', 'assets', 'total assets',
            'total assets and liabilities', 'total of assets'
        ],
        
        # ============ BALANCE SHEET - LIABILITIES ============
        'Current Liabilities': [
            'total current liabilities', 'current liabilities',
            'short-term liabilities', 'total short term liabilities',
            'current obligations'
        ],
        
        'Payables': [
            'accounts payable', 'trade payable', 'payables',
            'supplier payables', 'trade payables', 'account payable'
        ],
        
        'Short-term Debt': [
            'short-term debt', 'short term borrowings', 'current debt',
            'current portion of long-term debt', 'short-term loan',
            'current borrowings'
        ],
        
        'Non-Current Liabilities': [
            'total non-current liabilities', 'non-current liabilities',
            'long-term liabilities', 'total long-term liabilities',
            'total non current liabilities'
        ],
        
        'Long-term Debt': [
            'long-term debt', 'long term debt', 'long-term borrowings',
            'long term borrowings', 'non-current debt', 'long-term loan',
            'long term loan'
        ],
        
        'Total Liabilities': [
            'total liabilities', 'total liability', 'liabilities',
            'total debt', 'total obligation'
        ],
        
        # ============ BALANCE SHEET - EQUITY ============
        'Total Equity': [
            'total equity', 'total shareholders equity', 'shareholders equity',
            'shareholders\' equity', 'total equity and reserves',
            'shareholder equity', 'equity', 'capital and reserves',
            'total capital and reserves'
        ],
        
        # ============ CASH FLOW ============
        'Operating Cash Flow': [
            'cash flow from operations', 'operating cash flow', 'cfo',
            'cash from operating', 'cash generated from operations',
            'net cash from operations', 'operating activities'
        ],
        
        'Investing Cash Flow': [
            'cash flow from investing', 'investing cash flow', 'cfi',
            'cash from investing', 'investing activities',
            'cash used in investing'
        ],
        
        'Financing Cash Flow': [
            'cash flow from financing', 'financing cash flow', 'cff',
            'cash from financing', 'financing activities'
        ],
        
        'Net Cash Flow': [
            'net change in cash', 'net cash flow', 'net cash change',
            'change in cash balance', 'net increase/(decrease) in cash'
        ],
        
        # ============ EBITDA ============
        'EBITDA': [
            'ebitda', 'earnings before interest tax depreciation amortization',
            'ebit da', 'operating cash earnings'
        ],
    }

    for standard_term, keywords in mapping.items():
        if any(k in row_name for k in keywords):
            return standard_term
            
    return row_name  # Return original if no match found

def parse_file(file_objs):
    """
    Robust Parser: Handles PDF text extraction and Fuzzy Excel Parsing.
    """
    if file_objs is None:
        return None, None, "No files provided."
    
    if not isinstance(file_objs, list):
        file_objs = [file_objs]

    consolidated_data = {} 
    consolidated_text = ""
    logs = []
    
    for file_obj in file_objs:
        file_path = file_obj.name
        filename = os.path.basename(file_path)
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        try:
            # --- ROBUST EXCEL PARSER ---
            if ext in ['.xlsx', '.xls', '.csv']:
                if ext == '.csv':
                    df_raw = pd.read_csv(file_path, header=None)
                else:
                    df_raw = pd.read_excel(file_path, header=None)
                
                # 1. Detect Year (Look in filename or first few rows)
                detected_year = None
                year_match = re.search(r'20\d{2}', filename)
                if year_match:
                    detected_year = year_match.group(0)
                
                # Scan first 10 rows for a year if not in filename
                if not detected_year:
                    for i in range(min(10, len(df_raw))):
                        row_vals = df_raw.iloc[i].astype(str).values
                        for val in row_vals:
                            ym = re.search(r'20\d{2}', val)
                            if ym:
                                detected_year = ym.group(0)
                                break
                        if detected_year: break
                
                if not detected_year:
                    logs.append(f"⚠️ Warning: Could not detect year for {filename}. Data might be misaligned.")
                    detected_year = "Unknown_Year"

                # 2. Detect Header Row (Look for 'metric', 'item', 'particulars' or just where data starts)
                header_row_idx = -1
                for idx, row in df_raw.iterrows():
                    row_str = row.astype(str).str.lower().values
                    if any(x in row_str for x in ["line item", "particulars", "description", "assets", "revenue"]):
                        header_row_idx = idx
                        break
                
                # If no header found, assume row 0
                start_row = header_row_idx if header_row_idx != -1 else 0
                
                # 3. Extract Data (Col 0 = Name, Col 1...N = Values)
                # We iterate through the dataframe starting from the detected header
                df_clean = df_raw.iloc[start_row+1:]
                
                for _, row in df_clean.iterrows():
                    # Sanity check: Row must have at least 2 columns
                    if len(row) < 2: continue
                    
                    raw_name = str(row.iloc[0]).strip()
                    if raw_name in ["nan", "None", "", "Line Item"]: continue
                    
                    # Try to find the first numeric value in the row
                    val = None
                    for col_idx in range(1, len(row)):
                        try:
                            candidate = str(row.iloc[col_idx]).replace(',', '').replace(' ', '')
                            if candidate.lower() == 'nan': continue
                            val = float(candidate)
                            break # Found the number
                        except (ValueError, AttributeError):
                            continue
                    
                    # Skip rows with no numeric values (headers like "Non-current assets")
                    if val is None:
                        continue
                    
                    # Normalize the name
                    clean_name = normalize_row_name(raw_name)
                    
                    if clean_name not in consolidated_data:
                        consolidated_data[clean_name] = {}
                    
                    # Store using the Standardized Name
                    consolidated_data[clean_name][detected_year] = val
                    # Also store original name for specific queries
                    if raw_name != clean_name:
                        if raw_name not in consolidated_data:
                            consolidated_data[raw_name] = {}
                        consolidated_data[raw_name][detected_year] = val
                
                logs.append(f"✅ Parsed Data from {filename} (Year: {detected_year})")

            # --- PDF / TEXT ---
            elif ext == '.pdf':
                reader = pypdf.PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                consolidated_text += f"\n--- {filename} ---\n{text}"
                logs.append(f"📖 Extracted text from {filename}")

            elif ext == '.txt':
                with open(file_path, 'r') as f:
                    text = f.read()
                consolidated_text += f"\n--- {filename} ---\n{text}"
                logs.append(f"📖 Extracted text from {filename}")

        except Exception as e:
            logs.append(f"❌ Error parsing {filename}: {str(e)}")

    # Final Formatting
    df_final = None
    if consolidated_data:
        df_final = pd.DataFrame.from_dict(consolidated_data, orient='index')
        df_final = df_final.reindex(sorted(df_final.columns), axis=1)
        df_final.reset_index(inplace=True)
        df_final.rename(columns={'index': 'Line Item'}, inplace=True)

    return df_final, consolidated_text, "\n".join(logs)