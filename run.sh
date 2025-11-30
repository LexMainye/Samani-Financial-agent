#!/bin/bash

# Use the conda Python interpreter
PYTHON="/Users/alexmainye/.julia/conda/3/x86_64/bin/python"
PIP="/Users/alexmainye/.julia/conda/3/x86_64/bin/pip"

# 3. Install dependencies (ensures openpyxl, torch, etc. are ready)
echo "Installing dependencies..."
$PIP install -r requirements.txt

# 4. Generate the Samani Limited Financial Data
echo "Generating Financial Statements & Commentary..."
if [ -f "generate_samani_financials.py" ]; then
    $PYTHON generate_samani_financials.py
else
    echo "⚠️  Warning: generate_samani_financials.py not found."
fi

if [ -f "generate_samani_text.py" ]; then
    $PYTHON generate_samani_text.py
else
    echo "⚠️  Warning: generate_samani_text.py not found."
fi

# 5. Run the application
echo "Starting Financial Analyst Agent..."
# We run from the root, pointing to the main file in src
$PYTHON src/main.py