#!/usr/bin/env python3
"""
Simple test to trigger Modal app activity
"""
import subprocess
import sys
from datetime import datetime

def test_modal_app():
    """Test Modal app by triggering a method call"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 🚀 Testing Modal app...")
    print("   App: samani-financial-analyst")
    print("   Region: A10G GPU\n")
    
    # Use modal run to test the app
    cmd = """
import sys
sys.path.insert(0, 'src')

from src.backend.modal_server import app, FinancialAnalyzer
from pydantic import BaseModel

# Spawn the analyzer
analyzer = FinancialAnalyzer()
analyzer.__enter__()

# Test with empty files
result, logs = analyzer.analyze([], "test_query")
print("✅ Analyzer responded successfully!")
print(f"   Result length: {len(result)} chars")
print(f"   Logs: {logs[:100]}...")
"""
    
    try:
        result = subprocess.run(
            ["python", "-c", cmd],
            capture_output=True,
            text=True,
            cwd="/Users/alexmainye/Documents/Projects/fin_forecasting"
        )
        
        if result.returncode == 0:
            print("✅ TEST PASSED!")
            print("\n" + result.stdout)
            return True
        else:
            print("❌ TEST FAILED")
            print("\nError output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_modal_app()
    sys.exit(0 if success else 1)
