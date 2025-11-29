#!/usr/bin/env python3
"""
Test script to verify Modal app is active and working
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from modal import App
import modal

def test_modal_app():
    """Test the Modal financial analyzer app"""
    try:
        print("🔍 Looking up Modal app...")
        app = modal.App.lookup("samani-financial-analyst")
        
        print("✅ App found!")
        print(f"   App: samani-financial-analyst")
        
        # Get the analyzer class directly
        analyzer_cls = modal.PartialFunction.lookup("samani-financial-analyst", "FinancialAnalyzer.analyze")
        print("✅ Analyze method found!")
        
        # Test with minimal data
        print("\n📊 Testing analysis method...")
        
        # This will trigger the app to spin up if idle
        print("   Sending test request to wake up the app...")
        
        result = analyzer_cls.analyze.remote([], "test")
        print(f"✅ Test request successful!")
        print(f"\n📈 Result preview:")
        print(f"   {result[:200] if isinstance(result, str) else result}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Ensure you're authenticated: modal token set")
        print("   2. Check app status: modal app list")
        print("   3. Redeploy if needed: modal deploy src/backend/modal_server.py")
        return False

if __name__ == "__main__":
    success = test_modal_app()
    sys.exit(0 if success else 1)
