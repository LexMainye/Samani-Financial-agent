#!/usr/bin/env python3
"""
Keep-alive script to prevent Modal app from going idle
Runs periodic test calls to keep the app active
"""
import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "src"))

from modal import App

def keep_alive(interval_minutes=10):
    """Keep Modal app active with periodic test calls"""
    print(f"🚀 Starting keep-alive service (interval: {interval_minutes}m)")
    print("   Press Ctrl+C to stop\n")
    
    try:
        app = App.lookup("hf-hackathon-mcp", "samani-financial-analyst")
        analyzer_cls = app.cls.lookup("FinancialAnalyzer")
        
        call_count = 0
        while True:
            call_count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            try:
                print(f"[{timestamp}] Call #{call_count}: Sending keep-alive ping...")
                result = analyzer_cls.analyze.remote([], "keepalive_test")
                print(f"[{timestamp}] ✅ App responding - Status: Active\n")
            except Exception as e:
                print(f"[{timestamp}] ⚠️  Error: {e}\n")
            
            # Wait for next interval
            time.sleep(interval_minutes * 60)
            
    except KeyboardInterrupt:
        print(f"\n\n👋 Keep-alive stopped after {call_count} calls")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("\n💡 Make sure the Modal app is deployed:")
        print("   modal deploy src/backend/modal_server.py")
        sys.exit(1)

if __name__ == "__main__":
    # Default 10 minutes, can pass custom interval as argument
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    keep_alive(interval)
