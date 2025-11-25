#!/usr/bin/env python3
"""
Quick debug runner for testing the Hugo Link Poster without GitHub integration
"""
import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

# Set debug mode
os.environ['DEBUG_MODE'] = 'true'
os.environ['FLASK_SECRET_KEY'] = 'debug-secret-key'

# Import and run the app
from app import app

print("\n🚀 Starting Hugo Link Poster in DEBUG MODE")
print("📝 Posts will be shown but not pushed to GitHub")
print("🔗 Open http://localhost:5001 in your browser")
print("🛑 Press Ctrl+C to stop\n")

app.run(debug=True, host='0.0.0.0', port=5001)