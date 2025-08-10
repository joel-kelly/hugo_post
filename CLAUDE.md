# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hugo Link Poster is a Flask web application for creating shortform link posts on a Hugo blog. It features URL metadata extraction, image processing, and direct GitHub integration for content publishing.

## Architecture

- **app.py**: Main Flask application with embedded HTML template (single-file architecture)
- **production.py**: Production WSGI runner with environment validation
- **debug_run.py**: Local development runner that disables GitHub integration
- **Two-mode operation**: Debug mode (local testing) vs Production mode (full GitHub integration)
- **Service deployment**: Runs as systemd service with Cloudflare tunnel for secure access

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run in debug mode (no GitHub integration)
python debug_run.py

# Test environment variables
python test_env.py

# Test image processing specifically
python test_image_processing.py
```

### Testing
```bash
# Run image processing tests
python test_image_processing.py

# Quick image download test
python test_image_processing.py --quick
```

### Deployment
```bash
# Deploy to production
scripts/deploy.sh

# Monitor service status
scripts/monitor.sh

# Check service health
scripts/health-check.sh

# View service logs
sudo journalctl -u hugo-post -f
```

## Key Features

### Dual Metadata Extraction
- **Basic scraping**: BeautifulSoup-based extraction for Open Graph/meta tags
- **Advanced scraping**: Playwright-based extraction for dynamic content and lazy-loaded images
- Users can trigger "Load More Images" for sites with JavaScript-heavy image loading

### Image Processing Pipeline
- Downloads and validates images from URLs
- Automatically resizes images wider than 1200px
- Converts RGBA to RGB with white background
- Optimizes JPEG quality (85%) and PNG compression
- Comprehensive error handling with detailed logging

### Authentication & Security
- Token-based authentication in production mode
- Session persistence (180 days)
- Debug mode bypasses all authentication
- Environment variable validation on startup

## Environment Variables

Required for production:
- `FLASK_SECRET_KEY`: Session encryption key
- `LINK_POSTER_TOKEN`: Access token for authentication  
- `GITHUB_TOKEN`: GitHub personal access token with repo permissions
- `GITHUB_REPO`: Target repository in format `username/repo-name`

Optional:
- `DEBUG_MODE`: Set to `true` for local development (default: false)
- `HOST`: Bind address (default: 127.0.0.1)
- `PORT`: Port number (default: 5001)

## Content Generation

### Output Structure
- Creates markdown files in `content/links/` directory
- Uploads images to `static/images/` directory
- Generates Hugo-compatible front matter with Open Graph metadata
- Supports optional excerpts and user commentary

### Front Matter Format
```yaml
---
title: "Article Title"
date: 2025-01-01T12:00:00-0700
externalLink: "https://example.com/article"
sourceUrl: "example.com"
featuredImage: "/images/article_title.jpg"
excerpt: "Optional excerpt text"
---
```

## Service Management

The application runs as a systemd service in production:
- **Service name**: `hugo-post`
- **Cloudflare tunnel**: `cloudflared` service for secure domain access
- **Logs**: Available via `journalctl -u hugo-post`
- **Health checks**: Automated monitoring every 5 minutes
- **Auto-restart**: Systemd handles service failures

## Error Handling

- Comprehensive logging with request IDs for tracking
- Graceful fallbacks for network timeouts
- Image processing validates format and size constraints
- GitHub API errors are caught and returned to user
- Session timeout handling

## Development Notes

- The application uses embedded HTML templates (single-file design)
- Dark/light theme toggle with localStorage persistence
- Mobile-responsive design
- All GitHub operations are skipped in debug mode
- Image processing includes detailed timing and size logging for debugging