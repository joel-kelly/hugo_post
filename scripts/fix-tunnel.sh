#!/bin/bash

# Fix Cloudflare tunnel configuration
echo "Fixing Cloudflare tunnel configuration..."

# Create cloudflared config directory
sudo mkdir -p /etc/cloudflared

# Copy tunnel configuration
sudo cp /home/jelly/Documents/hugo_post/config/cloudflare-tunnel.yaml /etc/cloudflared/config.yml

# Set proper permissions
sudo chown -R root:root /etc/cloudflared
sudo chmod 600 /etc/cloudflared/config.yml

# Check if the tunnel service is installed
if ! systemctl list-unit-files | grep -q cloudflared; then
    echo "Installing cloudflared service..."
    sudo cloudflared service install
fi

# Start the tunnel service
echo "Starting cloudflared service..."
sudo systemctl enable cloudflared
sudo systemctl restart cloudflared

# Wait a moment for the service to start
sleep 3

# Check status
echo "Checking tunnel status..."
sudo systemctl status cloudflared --no-pager

echo "✅ Tunnel configuration fixed!"
echo "The tunnel should now be running with the correct configuration."