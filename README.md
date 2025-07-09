# Hugo Link Poster

A 100% vibe-coded tool for quickly creating shortform posts on my Hugo blog.

## Quick Start (Debug Mode)

Test the tool locally without any GitHub setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Run in debug mode
python debug_run.py
```

Open http://localhost:5001 in your browser. In debug mode:
- No login required
- No GitHub token needed
- Posts are displayed but not saved

## Production Deployment

For production deployment with Cloudflare tunnels and systemd service:

```bash
# Complete setup
scripts/setup-complete.sh
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## Features

- 📱 Mobile-friendly interface
- 🔍 Auto-fetches page metadata (title, images)
- 🖼️ Image selection and automatic optimization
- 📝 Support for excerpts and commentary
- 🚀 Direct GitHub commits (in production mode)
- 🔒 Simple token-based authentication
- 🌐 Cloudflare tunnel integration
- 📊 Health monitoring and logging
- 🔄 Automatic service management

## Directory Structure

```
hugo_post/
├── app.py                     # Main Flask application
├── production.py              # Production runner
├── debug_run.py               # Debug mode runner
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── config/                   # Configuration files
├── scripts/                  # Deployment and management scripts
├── docs/                     # Documentation
└── venv/                     # Virtual environment (created on setup)
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

## Production Features

- **Systemd Service**: Automatic startup and restart
- **Cloudflare Tunnel**: Secure domain access with SSL
- **Health Monitoring**: Automated health checks every 5 minutes
- **Log Rotation**: Automatic log management
- **Backup System**: Regular configuration backups
- **Zero-downtime Deployment**: Seamless updates

## Quick Commands

```bash
# Monitor service status
scripts/monitor.sh

# Deploy updates
scripts/deploy.sh

# Create backup
scripts/backup.sh

# View logs
sudo journalctl -u hugo-post -f
```

## URLs

- **Production**: https://post.jelly.science
- **Local Debug**: http://localhost:5001
