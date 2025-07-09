#!/bin/bash

# Setup Cloudflare Tunnel for Hugo Post Tool
echo "Setting up Cloudflare Tunnel for post.jelly.science..."

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "Installing cloudflared..."
    
    # Download and install cloudflared
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared-linux-amd64.deb
    rm cloudflared-linux-amd64.deb
    
    echo "cloudflared installed successfully"
else
    echo "cloudflared is already installed"
fi

# Authenticate with Cloudflare (this will open a browser)
echo "Please authenticate with Cloudflare..."
echo "This will open a browser window. Please login to your Cloudflare account."
read -p "Press Enter to continue..."

cloudflared tunnel login

# Create a tunnel
echo "Creating tunnel..."
TUNNEL_NAME="hugo-post-$(date +%s)"
cloudflared tunnel create $TUNNEL_NAME

# Get tunnel ID
TUNNEL_ID=$(cloudflared tunnel list | grep $TUNNEL_NAME | awk '{print $1}')

if [ -z "$TUNNEL_ID" ]; then
    echo "Failed to create tunnel. Please check your Cloudflare authentication."
    exit 1
fi

echo "Tunnel created with ID: $TUNNEL_ID"

# Update the tunnel configuration file
sed -i "s/YOUR_TUNNEL_ID/$TUNNEL_ID/g" ../config/cloudflare-tunnel.yaml

# Create DNS record
echo "Creating DNS record for post.jelly.science..."
cloudflared tunnel route dns $TUNNEL_ID post.jelly.science

# Install tunnel as a service
echo "Installing tunnel service..."
sudo cloudflared service install

echo "Cloudflare tunnel setup complete!"
echo "Tunnel ID: $TUNNEL_ID"
echo "Domain: post.jelly.science"
echo ""
echo "Next steps:"
echo "1. Configure your .env file with production settings"
echo "2. Install the Hugo Post service: ./install-service.sh"
echo "3. Start the tunnel: sudo systemctl start cloudflared"
echo "4. Start the Hugo Post service: sudo systemctl start hugo-post"