#!/bin/bash

# Install Hugo Post Service
echo "Installing Hugo Post systemd service..."

# Copy service file to systemd directory
sudo cp ../config/hugo-post.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable the service
sudo systemctl enable hugo-post

echo "Service installed successfully!"
echo "To start the service: sudo systemctl start hugo-post"
echo "To check status: sudo systemctl status hugo-post"
echo "To view logs: sudo journalctl -u hugo-post -f"