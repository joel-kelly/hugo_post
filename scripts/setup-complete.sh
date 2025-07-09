#!/bin/bash

# Complete setup script for Hugo Post service
echo "🚀 Hugo Post Service - Complete Setup"
echo "====================================="

# Make all scripts executable
chmod +x *.sh

echo "Setting up Hugo Post service for post.jelly.science..."

# Step 1: Environment setup
echo "1. Setting up environment..."
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file from example..."
    cp .env.example .env
    echo "❗ Please edit .env file with your actual values before proceeding"
    read -p "Press Enter after editing .env file..."
fi

# Step 2: Install system service
echo "2. Installing system service..."
scripts/install-service.sh

# Step 3: Setup Cloudflare tunnel
echo "3. Setting up Cloudflare tunnel..."
read -p "Do you want to setup Cloudflare tunnel now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    scripts/setup-cloudflare.sh
    scripts/configure-domain.sh
fi

# Step 4: Setup monitoring
echo "4. Setting up monitoring..."
scripts/setup-monitoring.sh

# Step 5: Create initial backup
echo "5. Creating initial backup..."
scripts/backup.sh

# Step 6: Test deployment
echo "6. Testing deployment..."
read -p "Do you want to start the services now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    scripts/deploy.sh
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Quick reference:"
echo "- Start services: scripts/deploy.sh"
echo "- Monitor status: scripts/monitor.sh"
echo "- Create backup: scripts/backup.sh"
echo "- View logs: sudo journalctl -u hugo-post -f"
echo "- Service URL: https://post.jelly.science"
echo ""
echo "File locations:"
echo "- Service config: /etc/systemd/system/hugo-post.service"
echo "- Tunnel config: /etc/cloudflared/config.yml"
echo "- Backups: /home/jelly/backups/hugo_post/"
echo "- Logs: /var/log/hugo-post/"