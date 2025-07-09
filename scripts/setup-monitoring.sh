#!/bin/bash

# Setup monitoring and logging for Hugo Post service
echo "Setting up monitoring and logging..."

# Create log directory
sudo mkdir -p /var/log/hugo-post
sudo chown jelly:jelly /var/log/hugo-post

# Install ../config/logrotate.configuration
sudo cp ../config/logrotate.conf /etc/logrotate.d/hugo-post

# Make monitor script executable
chmod +x monitor.sh

# Create a simple health check script
cat > health-check.sh << 'EOF'
#!/bin/bash
# Simple health check for Hugo Post service

LOG_FILE="/var/log/hugo-post/health.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Check if service is running
if ! systemctl is-active --quiet hugo-post; then
    echo "[$DATE] ERROR: Hugo Post service is not running" >> $LOG_FILE
    # Try to restart the service
    sudo systemctl restart hugo-post
    sleep 5
    if systemctl is-active --quiet hugo-post; then
        echo "[$DATE] INFO: Hugo Post service restarted successfully" >> $LOG_FILE
    else
        echo "[$DATE] CRITICAL: Failed to restart Hugo Post service" >> $LOG_FILE
    fi
fi

# Check if tunnel is running
if ! systemctl is-active --quiet cloudflared; then
    echo "[$DATE] ERROR: Cloudflare tunnel is not running" >> $LOG_FILE
    # Try to restart the tunnel
    sudo systemctl restart cloudflared
    sleep 5
    if systemctl is-active --quiet cloudflared; then
        echo "[$DATE] INFO: Cloudflare tunnel restarted successfully" >> $LOG_FILE
    else
        echo "[$DATE] CRITICAL: Failed to restart Cloudflare tunnel" >> $LOG_FILE
    fi
fi

# Test local connectivity
if ! curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001 | grep -q "200"; then
    echo "[$DATE] WARNING: Local service not responding on port 5001" >> $LOG_FILE
fi
EOF

chmod +x health-check.sh

# Create cron job for health checks (every 5 minutes)
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/jelly/Documents/hugo_post/health-check.sh") | crontab -

echo "Monitoring setup complete!"
echo ""
echo "Available commands:"
echo "- ./monitor.sh           - Check service status"
echo "- ./health-check.sh      - Run health checks"
echo "- sudo journalctl -u hugo-post -f  - View live logs"
echo "- sudo systemctl status hugo-post   - Service status"
echo ""
echo "Health checks will run automatically every 5 minutes"
echo "Logs are rotated daily in /var/log/hugo-post/"