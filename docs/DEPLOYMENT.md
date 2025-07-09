# Hugo Post Service Deployment Guide

## Quick Start

Run the complete setup script:

```bash
scripts/setup-complete.sh
```

## Manual Setup Steps

### 1. Environment Configuration

```bash
# Copy and edit environment file
cp .env.example .env
# Edit .env with your actual values
```

Required environment variables:
- `FLASK_SECRET_KEY`: Random secret key for Flask sessions
- `LINK_POSTER_TOKEN`: Access token for the service
- `GITHUB_TOKEN`: GitHub personal access token with repo permissions
- `GITHUB_REPO`: Your repository in format `username/repo-name`

### 2. Install System Service

```bash
scripts/install-service.sh
```

### 3. Setup Cloudflare Tunnel

```bash
# Setup and authenticate tunnel
scripts/setup-cloudflare.sh

# Configure domain routing
scripts/configure-domain.sh
```

### 4. Setup Monitoring

```bash
scripts/setup-monitoring.sh
```

### 5. Deploy Service

```bash
scripts/deploy.sh
```

## Service Management

### Start/Stop Services

```bash
# Start both services
sudo systemctl start cloudflared
sudo systemctl start hugo-post

# Stop both services
sudo systemctl stop hugo-post
sudo systemctl stop cloudflared

# Check status
sudo systemctl status hugo-post
sudo systemctl status cloudflared
```

### Monitoring

```bash
# Quick status check
scripts/monitor.sh

# View live logs
sudo journalctl -u hugo-post -f
sudo journalctl -u cloudflared -f

# Health check
scripts/health-check.sh
```

### Backup and Maintenance

```bash
# Create backup
scripts/backup.sh

# Redeploy after changes
scripts/deploy.sh
```

## File Structure

```
hugo_post/
├── app.py                 # Main Flask application
├── production.py          # Production runner
├── requirements.txt       # Python dependencies
├── venv/                  # Virtual environment
├── .env                   # Environment variables
├── .env.example          # Environment template
├── config/               # Configuration files
│   ├── hugo-post.service     # Systemd service file
│   ├── cloudflare-tunnel.yaml # Tunnel configuration
│   └── logrotate.conf        # Log rotation config
├── scripts/              # Shell scripts
│   ├── setup-complete.sh     # Complete setup script
│   ├── install-service.sh    # Install systemd service
│   ├── setup-cloudflare.sh   # Setup Cloudflare tunnel
│   ├── configure-domain.sh   # Configure domain routing
│   ├── setup-monitoring.sh   # Setup monitoring
│   ├── deploy.sh             # Deploy service
│   ├── backup.sh             # Create backup
│   ├── monitor.sh            # Check service status
│   ├── health-check.sh       # Health check script
│   ├── update-service.sh     # Update running service
│   └── update-paths.sh       # Update file paths
└── docs/                 # Documentation
    └── DEPLOYMENT.md         # This file
```

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status hugo-post

# Check logs
sudo journalctl -u hugo-post -n 50

# Check environment
source venv/bin/activate
python production.py
```

### Tunnel Issues

```bash
# Check tunnel status
cloudflared tunnel list
cloudflared tunnel info

# Check tunnel logs
sudo journalctl -u cloudflared -n 50

# Test tunnel connectivity
curl -v https://post.jelly.science
```

### Port Issues

```bash
# Check if port 5001 is in use
netstat -tlnp | grep :5001
lsof -i :5001

# Test local connectivity
curl -v http://127.0.0.1:5001
```

## Security Notes

- The service runs as the `jelly` user with restricted permissions
- Cloudflare handles SSL termination automatically
- Environment variables contain sensitive tokens - keep `.env` secure
- Regular backups are created in `/home/jelly/backups/hugo_post/`
- Logs are rotated daily to prevent disk space issues

## URLs

- **Production**: https://post.jelly.science
- **Local**: http://127.0.0.1:5001
- **Debug**: http://127.0.0.1:5001 (with DEBUG_MODE=true)