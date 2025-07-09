#!/bin/bash

# Configure domain and SSL for Hugo Post Tool
echo "Configuring domain and SSL for post.jelly.science..."

# Function to get tunnel ID from cloudflared
get_tunnel_id() {
    cloudflared tunnel list | grep -v "ID" | head -1 | awk '{print $1}'
}

# Check if cloudflared is configured
if ! command -v cloudflared &> /dev/null; then
    echo "Error: cloudflared not found. Please run ./setup-cloudflare.sh first"
    exit 1
fi

# Get tunnel ID
TUNNEL_ID=$(get_tunnel_id)

if [ -z "$TUNNEL_ID" ]; then
    echo "No tunnel found. Please run ./setup-cloudflare.sh first"
    exit 1
fi

echo "Using tunnel ID: $TUNNEL_ID"

# Update tunnel configuration
sed -i "s/YOUR_TUNNEL_ID/$TUNNEL_ID/g" ../config/cloudflare-tunnel.yaml

# Copy configuration to cloudflared directory
sudo mkdir -p /etc/cloudflared
sudo cp ../config/cloudflare-tunnel.yaml /etc/cloudflared/config.yml

# Set proper permissions
sudo chown -R root:root /etc/cloudflared
sudo chmod 600 /etc/cloudflared/config.yml

echo "Domain configuration complete!"
echo "SSL is automatically handled by Cloudflare"
echo ""
echo "Configuration summary:"
echo "- Domain: post.jelly.science"
echo "- Local service: http://127.0.0.1:5001"
echo "- SSL: Automatic via Cloudflare"
echo "- Tunnel ID: $TUNNEL_ID"