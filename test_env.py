from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

print("Environment variables from .env:")
print(f"DEBUG_MODE = {os.environ.get('DEBUG_MODE')}")
print(f"GITHUB_TOKEN = {os.environ.get('GITHUB_TOKEN', 'NOT SET')[:20]}...")  # Show first 20 chars
print(f"GITHUB_REPO = {os.environ.get('GITHUB_REPO', 'NOT SET')}")
print(f"LINK_POSTER_TOKEN exists = {'Yes' if os.environ.get('LINK_POSTER_TOKEN') else 'No'}")
print(f"\nDEBUG_MODE evaluates to: {os.environ.get('DEBUG_MODE', 'false').lower() == 'true'}")