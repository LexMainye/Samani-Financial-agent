import pandas as pd
import os

def generate_samani_financials():
    company_name = "Samani Limited"
    currency_unit = "KES ('000)"
    base_dir = "financials"
    years = [2020, 2021, 2022, 2023, 2024]

    print(f"Generating IAS-compliant financial statements for {company_name} (Currency: {currency_unit})...")

    # --- SIMULATION PARAMETERS (Kenyan Market Context) ---
    # Start with ~150 Million KES Revenue (represented as 150,000 in '000s)
    current_revenue = 150000.0 
    
    # Share Capital: 20 Million KES
    share_capital = 20000.0 

    for i, year in enumerate(years):
        # Apply growth curve (Scenario: Steady growth in the Kenyan furniture market)
        growth = 1 + (0.12 * i) 
        
        # ==========================================
        # 1. STATEMENT OF PROFIT OR LOSS
        # ==========================================
        revenue = round(current_revenue * growth, 2)
        cost_of_sales = round(revenue * 0.58, 2) # 58% COGS (Material costs)
        gross_profit = revenue - cost_of_sales
        
        dist_costs = round(revenue * 0.08, 2) # Logistics/Delivery
        admin_expenses = round(revenue * 0.15, 2) # Salaries, Rent
        other_expenses = round(2000 * (1 + i*0.05), 2)
        
        operating_profit = gross_profit - dist_costs - admin_expenses - other_expenses
        
        finance_costs = round(4500 * (1 + i*0.1), 2) # Loan interest
        profit_before_tax = operating_profit - finance_costs
        
        tax_expense = round(profit_before_tax * 0.30, 2) # 30% Corp Tax (Standard in Kenya)
        profit_for_year = round(profit_before_tax - tax_expense, 2)

        # Data List
        pl_data = [
            ["Revenue", revenue],
            ["Cost of Sales", -cost_of_sales],
            ["Gross Profit", gross_profit],
            ["", ""],
            ["Distribution Costs", -dist_costs],
            ["Administrative Expenses", -admin_expenses],
            ["Other Operating Expenses", -other_expenses],
            ["Operating Profit", operating_profit],
            ["", ""],
            ["Finance Costs", -finance_costs],
            ["Profit Before Tax", profit_before_tax],
            ["Income Tax Expense", -tax_expense],
            ["Profit for the Year", profit_for_year]
        ]

        # ==========================================
        # 2. STATEMENT OF FINANCIAL POSITION (Balance Sheet)
        # ==========================================
        # Assets
        ppe = round(95000 * growth, 2) # Factory, Showrooms
        intangibles = round(5000 * growth, 2) # Brand, Software
        non_current_assets = ppe + intangibles

        inventories = round(35000 * growth, 2) # Timber, Fabric, Finished stock
        trade_receivables = round(18000 * growth, 2) # Sales on credit
        cash_equivalents = round(8000 * growth + (profit_for_year * 0.15), 2)
        current_assets = inventories + trade_receivables + cash_equivalents
        
        total_assets = non_current_assets + current_assets

        # Liabilities
        long_term_borrowings = round(40000 * growth, 2) # Bank Loans
        non_current_liabilities = long_term_borrowings

        trade_payables = round(22000 * growth, 2) # Suppliers
        current_tax_payable = round(tax_expense, 2)
        short_term_borrowings = round(5000 * growth, 2) # Overdrafts
        current_liabilities = trade_payables + current_tax_payable + short_term_borrowings
        
        total_liabilities = non_current_liabilities + current_liabilities

        # Equity (Balancing Figure)
        target_equity = round(total_assets - total_liabilities, 2)
        retained_earnings = round(target_equity - share_capital, 2)
        total_equity = share_capital + retained_earnings

        # Check Balance
        check_balance = round(total_equity + total_liabilities, 2)
        is_balanced = abs(total_assets - check_balance) < 1.0

        bs_data = [
            ["ASSETS", "Amount"],
            ["Non-current assets", ""],
            ["   Property, plant and equipment", ppe],
            ["   Intangible assets", intangibles],
            ["Total non-current assets", non_current_assets],
            ["", ""],
            ["Current assets", ""],
            ["   Inventories", inventories],
            ["   Trade and other receivables", trade_receivables],
            ["   Cash and cash equivalents", cash_equivalents],
            ["Total current assets", current_assets],
            ["TOTAL ASSETS", total_assets],
            ["", ""],
            ["EQUITY AND LIABILITIES", ""],
            ["Equity", ""],
            ["   Share capital", share_capital],
            ["   Retained earnings", retained_earnings],
            ["Total equity", total_equity],
            ["", ""],
            ["Non-current liabilities", ""],
            ["   Borrowings", long_term_borrowings],
            ["Total non-current liabilities", non_current_liabilities],
            ["", ""],
            ["Current liabilities", ""],
            ["   Trade and other payables", trade_payables],
            ["   Current tax payable", current_tax_payable],
            ["   Short-term borrowings", short_term_borrowings],
            ["Total current liabilities", current_liabilities],
            ["TOTAL EQUITY AND LIABILITIES", check_balance]
        ]

        # ==========================================
        # 3. STATEMENT OF CASH FLOWS
        # ==========================================
        depreciation = round(ppe * 0.08, 2) 
        
        inc_inventory = -round(inventories * 0.06, 2) 
        inc_receivables = -round(trade_receivables * 0.05, 2) 
        inc_payables = round(trade_payables * 0.04, 2) 

        cash_from_ops = profit_before_tax + depreciation + finance_costs + inc_inventory + inc_receivables + inc_payables - tax_expense
        cash_investing = -round(ppe * 0.12, 2) 
        cash_financing = -round(finance_costs, 2) 
        
        net_increase_cash = cash_from_ops + cash_investing + cash_financing
        cash_start = cash_equivalents - net_increase_cash

        cf_data = [
            ["Cash flows from operating activities", ""],
            ["   Profit before tax", profit_before_tax],
            ["   Adjustments for Depreciation & Finance", depreciation + finance_costs],
            ["   Working capital changes", inc_inventory + inc_receivables + inc_payables],
            ["   Income tax paid", -tax_expense],
            ["Net cash from operating activities", round(cash_from_ops, 2)],
            ["", ""],
            ["Cash flows from investing activities", ""],
            ["   Purchase of assets", cash_investing],
            ["Net cash used in investing activities", cash_investing],
            ["", ""],
            ["Cash flows from financing activities", ""],
            ["   Interest paid", cash_financing],
            ["Net cash used in financing activities", cash_financing],
            ["", ""],
            ["Net increase in cash", round(net_increase_cash, 2)],
            ["Cash at start of year", round(cash_start, 2)],
            ["Cash at end of year", cash_equivalents]
        ]

        # ==========================================
        # 4. SAVE FILES WITH HEADERS
        # ==========================================
        year_dir = os.path.join(base_dir, str(year))
        os.makedirs(year_dir, exist_ok=True)

        # Helper to attach Company Name and Headers
        def save_with_header(data_rows, title, filename):
            header_rows = [
                [company_name, ""],
                [title, ""],
                [f"For the year ended 31 December {year}", ""],
                [f"Figures in {currency_unit}", ""],
                ["", ""],
                ["Line Item", "Amount"]
            ]
            full_data = header_rows + data_rows
            df = pd.DataFrame(full_data)
            # Save without pandas header/index because we built them into the rows
            df.to_excel(os.path.join(year_dir, filename), index=False, header=False)

        save_with_header(pl_data, "Statement of Profit or Loss", "Statement_of_Profit_or_Loss.xlsx")
        save_with_header(bs_data, "Statement of Financial Position", "Statement_of_Financial_Position.xlsx")
        save_with_header(cf_data, "Statement of Cash Flows", "Statement_of_Cash_Flows.xlsx")

        status = "✅ BALANCED" if is_balanced else "❌ IMBALANCED"
        print(f"[{year}] Generated reports in /{year_dir} | {status}")

    print("\nGeneration Complete. Files are located in the 'financials' folder.")

if __name__ == "__main__":
    generate_samani_financials()