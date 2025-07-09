#!/bin/bash

echo "Updating systemd service with new directory structure..."

# Stop the service first
sudo systemctl stop hugo-post

# Copy the updated service file
sudo cp /home/jelly/Documents/hugo_post/config/hugo-post.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Update cloudflared config
sudo cp /home/jelly/Documents/hugo_post/config/cloudflare-tunnel.yaml /etc/cloudflared/config.yml
sudo chown -R root:root /etc/cloudflared
sudo chmod 600 /etc/cloudflared/config.yml

# Restart services
sudo systemctl restart cloudflared
sudo systemctl restart hugo-post

echo "✅ Services updated and restarted!"