#!/usr/bin/env python3
"""
Production runner for Hugo Link Poster
"""
import os
import sys
from dotenv import load_dotenv
from app import app

# Load environment variables
load_dotenv()

# Production configuration
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'
HOST = os.environ.get('HOST', '127.0.0.1')
PORT = int(os.environ.get('PORT', '5001'))

# Security checks
if not DEBUG_MODE:
    required_vars = ['FLASK_SECRET_KEY', 'LINK_POSTER_TOKEN', 'GITHUB_TOKEN', 'GITHUB_REPO']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
    
    if os.environ.get('LINK_POSTER_TOKEN') == 'change-this-token-in-production':
        print("❌ Please update LINK_POSTER_TOKEN in your .env file")
        sys.exit(1)

print(f"🚀 Starting Hugo Link Poster in {'DEBUG' if DEBUG_MODE else 'PRODUCTION'} mode")
print(f"📡 Listening on {HOST}:{PORT}")

if __name__ == '__main__':
    app.run(
        debug=DEBUG_MODE,
        host=HOST,
        port=PORT,
        use_reloader=False  # Disable reloader in production
    )