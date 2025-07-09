#!/bin/bash

echo "🔧 Fixing Cloudflare tunnel configuration..."

# Get the existing tunnel ID
TUNNEL_ID="63326415-4bc3-4e21-b34b-adb241b87ac6"

# Check if credentials file exists
CREDS_FILE="/home/jelly/.cloudflared/${TUNNEL_ID}.json"

if [ ! -f "$CREDS_FILE" ]; then
    echo "❌ Credentials file missing for tunnel $TUNNEL_ID"
    echo "This tunnel might be configured on another system."
    echo ""
    echo "Options:"
    echo "1. Create a new tunnel (recommended)"
    echo "2. Transfer credentials from another system"
    echo ""
    read -p "Do you want to create a new tunnel? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating new tunnel..."
        
        # Create new tunnel
        NEW_TUNNEL_NAME="hugo-post-$(date +%s)"
        cloudflared tunnel create $NEW_TUNNEL_NAME
        
        # Get new tunnel ID
        NEW_TUNNEL_ID=$(cloudflared tunnel list | grep $NEW_TUNNEL_NAME | awk '{print $1}')
        
        if [ -z "$NEW_TUNNEL_ID" ]; then
            echo "❌ Failed to create new tunnel"
            exit 1
        fi
        
        echo "✅ New tunnel created: $NEW_TUNNEL_ID"
        
        # Update configuration
        sed -i "s/tunnel: .*/tunnel: $NEW_TUNNEL_ID/" /home/jelly/Documents/hugo_post/config/cloudflare-tunnel.yaml
        sed -i "s/credentials-file: .*/credentials-file: \/home\/jelly\/.cloudflared\/$NEW_TUNNEL_ID.json/" /home/jelly/Documents/hugo_post/config/cloudflare-tunnel.yaml
        
        # Create DNS record
        echo "Creating DNS record..."
        cloudflared tunnel route dns $NEW_TUNNEL_ID post.jelly.science
        
        # Update tunnel ID for rest of script
        TUNNEL_ID=$NEW_TUNNEL_ID
        
    else
        echo "❌ Cannot proceed without credentials file"
        exit 1
    fi
fi

# Copy configuration
sudo mkdir -p /etc/cloudflared
sudo cp /home/jelly/Documents/hugo_post/config/cloudflare-tunnel.yaml /etc/cloudflared/config.yml
sudo chown -R root:root /etc/cloudflared
sudo chmod 600 /etc/cloudflared/config.yml

# Install and start service
if ! systemctl list-unit-files | grep -q cloudflared; then
    echo "Installing cloudflared service..."
    sudo cloudflared service install
fi

echo "Starting cloudflared service..."
sudo systemctl enable cloudflared
sudo systemctl restart cloudflared

# Wait and check status
sleep 3
echo "Checking tunnel status..."
sudo systemctl status cloudflared --no-pager

echo ""
echo "✅ Tunnel configuration complete!"
echo "🌐 Your service should be available at: https://post.jelly.science"