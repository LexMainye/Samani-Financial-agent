#!/bin/bash

# 1. Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Install dependencies (ensures openpyxl, torch, etc. are ready)
echo "Installing dependencies..."
pip install -r requirements.txt

# 4. Generate the Samani Limited Financial Data
echo "Generating Financial Statements & Commentary..."
if [ -f "generate_samani_financials.py" ]; then
    python generate_samani_financials.py
else
    echo "⚠️  Warning: generate_samani_financials.py not found."
fi

if [ -f "generate_samani_text.py" ]; then
    python generate_samani_text.py
else
    echo "⚠️  Warning: generate_samani_text.py not found."
fi

# 5. Run the application
echo "Starting Financial Analyst Agent..."
# We run from the root, pointing to the main file in src
python src/main.py