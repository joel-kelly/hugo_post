# Hugo Link Poster

A mobile-friendly web tool for quickly creating link posts on your Hugo blog.

## Quick Start (Debug Mode)

Test the tool locally without any GitHub setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Run in debug mode
python debug_run.py
```

Open http://localhost:5000 in your browser. In debug mode:
- No login required
- No GitHub token needed
- Posts are displayed but not savedpy

## Features

- 📱 Mobile-friendly interface
- 🔍 Auto-fetches page metadata (title, images)
- 🖼️ Image selection and automatic optimization
- 📝 Support for excerpts and commentary
- 🚀 Direct GitHub commits (in production mode)
- 🔒 Simple token-based authentication

## Production Setup

1. **Create GitHub Personal Access Token**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate token with `repo` permissions

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. **Run in Production Mode**
   ```bash
   # Set DEBUG_MODE=false in .env
   python app.py
   ```

## Environment Variables

- `DEBUG_MODE`: Set to `true` for local testing without GitHub
- `LINK_POSTER_TOKEN`: Your secret access token
- `GITHUB_TOKEN`: GitHub personal access token (not needed in debug mode)
- `GITHUB_REPO`: Your repo in format `username/repo-name`
- `FLASK_SECRET_KEY`: Random secret for sessions

## How It Works

1. Paste a URL
2. Click "Fetch Metadata" to auto-populate fields
3. Select an image (optional)
4. Add your commentary
5. Click "Create Post"

In production mode, this creates a markdown file in `content/links/` and uploads any selected images to `static/images/`.