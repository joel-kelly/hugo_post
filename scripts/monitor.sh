#!/bin/bash

# Hugo Post Service Monitoring Script
echo "Hugo Post Service Status Monitor"
echo "================================"

# Check if service is running
if systemctl is-active --quiet hugo-post; then
    echo "✅ Hugo Post Service: RUNNING"
else
    echo "❌ Hugo Post Service: STOPPED"
fi

# Check if cloudflared is running
if systemctl is-active --quiet cloudflared; then
    echo "✅ Cloudflare Tunnel: RUNNING"
else
    echo "❌ Cloudflare Tunnel: STOPPED"
fi

# Check if port 5001 is listening
if command -v netstat &> /dev/null; then
    if netstat -tlnp | grep -q ":5001 "; then
        echo "✅ Port 5001: LISTENING"
    else
        echo "❌ Port 5001: NOT LISTENING"
    fi
elif command -v ss &> /dev/null; then
    if ss -tlnp | grep -q ":5001 "; then
        echo "✅ Port 5001: LISTENING"
    else
        echo "❌ Port 5001: NOT LISTENING"
    fi
else
    echo "⚠️  Port check: Unable to verify (netstat/ss not available)"
fi

# Check disk usage
DISK_USAGE=$(df -h /home/jelly/Documents/hugo_post | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    echo "✅ Disk Usage: ${DISK_USAGE}%"
else
    echo "⚠️  Disk Usage: ${DISK_USAGE}% (HIGH)"
fi

# Check recent logs for errors
echo ""
echo "Recent Logs:"
echo "============"
sudo journalctl -u hugo-post --no-pager -n 5 --since "1 hour ago"

# Check tunnel connectivity
echo ""
echo "Tunnel Status:"
echo "============="
cloudflared tunnel info 2>/dev/null || echo "Unable to fetch tunnel info"

# Health check
echo ""
echo "Health Check:"
echo "============"
if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001 | grep -q "200"; then
    echo "✅ Local service responding"
else
    echo "❌ Local service not responding"
fi