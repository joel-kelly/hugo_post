#!/bin/bash

echo "🔧 Fixing DNS routing for post.jelly.science..."

# Get the current tunnel ID from our config
CURRENT_TUNNEL_ID="a34f8738-7e39-4fa8-b3e4-08f8f5d9a235"
OLD_TUNNEL_ID="63326415-4bc3-4e21-b34b-adb241b87ac6"

echo "Current tunnel ID: $CURRENT_TUNNEL_ID"
echo "Old tunnel ID: $OLD_TUNNEL_ID"

# First, try to delete the old DNS record
echo "Attempting to remove old DNS record..."
cloudflared tunnel route dns $OLD_TUNNEL_ID post.jelly.science --overwrite-dns 2>/dev/null || echo "Old record might not exist or already removed"

# Now create the new DNS record with overwrite flag
echo "Creating new DNS record for current tunnel..."
cloudflared tunnel route dns $CURRENT_TUNNEL_ID post.jelly.science --overwrite-dns

if [ $? -eq 0 ]; then
    echo "✅ DNS record updated successfully!"
else
    echo "❌ Failed to update DNS record"
    echo "Let's check what's happening..."
    
    # Check tunnel status
    echo "Checking tunnel status..."
    cloudflared tunnel info $CURRENT_TUNNEL_ID
    
    # Check DNS resolution
    echo "Checking DNS resolution..."
    nslookup post.jelly.science
    
    echo "Manual fix required - see troubleshooting below"
fi

echo ""
echo "Waiting 30 seconds for DNS to propagate..."
sleep 30

echo "Testing connection..."
curl -I https://post.jelly.science 2>&1 | head -5

echo ""
echo "If you still get Error 1033, try:"
echo "1. Wait 5-10 minutes for DNS propagation"
echo "2. Clear your browser cache"
echo "3. Try incognito/private browsing"