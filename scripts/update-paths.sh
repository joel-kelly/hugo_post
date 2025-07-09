#!/bin/bash

# Update all file paths in scripts after reorganization
echo "Updating file paths in all scripts..."

SCRIPTS_DIR="/home/jelly/Documents/hugo_post/scripts"
CONFIG_DIR="/home/jelly/Documents/hugo_post/config"

# Update configure-domain.sh
sed -i 's|cloudflare-tunnel.yaml|../config/cloudflare-tunnel.yaml|g' "$SCRIPTS_DIR/configure-domain.sh"

# Update fix-tunnel-complete.sh
sed -i 's|/home/jelly/Documents/hugo_post/cloudflare-tunnel.yaml|/home/jelly/Documents/hugo_post/config/cloudflare-tunnel.yaml|g' "$SCRIPTS_DIR/fix-tunnel-complete.sh"

# Update setup-monitoring.sh
sed -i 's|logrotate.conf|../config/logrotate.conf|g' "$SCRIPTS_DIR/setup-monitoring.sh"

# Update backup.sh
sed -i 's|--exclude=venv|--exclude=venv --exclude=scripts --exclude=config --exclude=docs|g' "$SCRIPTS_DIR/backup.sh"

# Update deploy.sh
sed -i 's|\./backup.sh|scripts/backup.sh|g' "$SCRIPTS_DIR/deploy.sh"

# Update fix-tunnel.sh
sed -i 's|/home/jelly/Documents/hugo_post/cloudflare-tunnel.yaml|/home/jelly/Documents/hugo_post/config/cloudflare-tunnel.yaml|g' "$SCRIPTS_DIR/fix-tunnel.sh"

# Update setup-complete.sh
sed -i 's|\./install-service.sh|scripts/install-service.sh|g' "$SCRIPTS_DIR/setup-complete.sh"
sed -i 's|\./setup-cloudflare.sh|scripts/setup-cloudflare.sh|g' "$SCRIPTS_DIR/setup-complete.sh"
sed -i 's|\./configure-domain.sh|scripts/configure-domain.sh|g' "$SCRIPTS_DIR/setup-complete.sh"
sed -i 's|\./setup-monitoring.sh|scripts/setup-monitoring.sh|g' "$SCRIPTS_DIR/setup-complete.sh"
sed -i 's|\./backup.sh|scripts/backup.sh|g' "$SCRIPTS_DIR/setup-complete.sh"
sed -i 's|\./deploy.sh|scripts/deploy.sh|g' "$SCRIPTS_DIR/setup-complete.sh"
sed -i 's|\./monitor.sh|scripts/monitor.sh|g' "$SCRIPTS_DIR/setup-complete.sh"

echo "✅ All file paths updated!"