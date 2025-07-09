#!/bin/bash

# Deployment script for Hugo Post service
echo "Deploying Hugo Post service..."

# Function to check if service is running
check_service() {
    if systemctl is-active --quiet hugo-post; then
        echo "✅ $1: Service is running"
        return 0
    else
        echo "❌ $1: Service is not running"
        return 1
    fi
}

# Function to check if tunnel is running
check_tunnel() {
    if systemctl is-active --quiet cloudflared; then
        echo "✅ $1: Tunnel is running"
        return 0
    else
        echo "❌ $1: Tunnel is not running"
        return 1
    fi
}

# Pre-deployment checks
echo "Pre-deployment checks..."
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first"
    exit 1
fi

# Create backup before deployment
scripts/backup.sh

# Stop services
echo "Stopping services..."
sudo systemctl stop hugo-post 2>/dev/null || true
sudo systemctl stop cloudflared 2>/dev/null || true

# Update dependencies
echo "Updating dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Start services
echo "Starting services..."
sudo systemctl start cloudflared
sleep 3
sudo systemctl start hugo-post
sleep 3

# Post-deployment checks
echo "Post-deployment checks..."
check_tunnel "Post-deployment"
check_service "Post-deployment"

# Health check
echo "Running health check..."
if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001 | grep -q "200"; then
    echo "✅ Service is responding"
else
    echo "❌ Service is not responding"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo "Service is available at: https://post.jelly.science"