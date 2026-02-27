#!/usr/bin/env python3
"""
Simple script to run the Stock Prediction API
Run this with: python run_api.py
"""

import subprocess
import sys

def main():
    print("🚀 Starting Stock Prediction API...")
    print("=" * 50)
    
    try:
        # Run uvicorn using Python module syntax
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ API stopped successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure you've installed dependencies:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
