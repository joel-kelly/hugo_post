#!/bin/bash

# Backup script for Hugo Post service
BACKUP_DIR="/home/jelly/backups/hugo_post"
DATE=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="hugo_post_backup_$DATE.tar.gz"

echo "Creating backup of Hugo Post service..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude=venv --exclude=scripts --exclude=config --exclude=docs \
    --exclude=__pycache__ \
    --exclude=*.pyc \
    --exclude=.git \
    -C /home/jelly/Documents \
    hugo_post

if [ $? -eq 0 ]; then
    echo "✅ Backup created successfully: $BACKUP_DIR/$BACKUP_FILE"
    
    # Keep only last 7 backups
    cd $BACKUP_DIR
    ls -t hugo_post_backup_*.tar.gz | tail -n +8 | xargs rm -f
    
    echo "Backup size: $(du -h $BACKUP_DIR/$BACKUP_FILE | cut -f1)"
else
    echo "❌ Backup failed"
    exit 1
fi