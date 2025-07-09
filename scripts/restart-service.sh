#!/bin/bash

echo "Restarting Hugo Post service..."

# Stop the service
sudo systemctl stop hugo-post

# Wait a moment
sleep 2

# Start the service
sudo systemctl start hugo-post

# Wait for startup
sleep 3

# Check status
sudo systemctl status hugo-post --no-pager -l

echo "✅ Service restarted!"