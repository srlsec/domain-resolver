#!/bin/bash

# Define the URL and local file path
GITHUB_URL="https://raw.githubusercontent.com/proabiral/Fresh-Resolvers/refs/heads/master/resolvers.txt"
LOCAL_FILE="$HOME/sec-tools/wordlists/domain-resolver/resolvers.txt"
BACKUP_FILE="$HOME/sec-tools/wordlists/domain-resolver/resolvers_backup_$(date +%Y%m%d_%H%M%S).txt"

# Function to download the file
download_resolver() {
    echo "Downloading fresh resolvers from GitHub..."
    if curl -sSL "$GITHUB_URL" -o "$LOCAL_FILE"; then
        echo "Successfully downloaded fresh resolvers to $LOCAL_FILE"
        return 0
    else
        echo "Failed to download resolvers"
        return 1
    fi
}

# Check if local file exists
if [ -f "$LOCAL_FILE" ]; then
    echo "Existing resolver file found. Creating backup..."
    cp "$LOCAL_FILE" "$BACKUP_FILE"
    echo "Backup created as $BACKUP_FILE"
    
    # Download new version
    if download_resolver; then
        echo "Comparing old and new files..."
        if diff "$BACKUP_FILE" "$LOCAL_FILE" > /dev/null; then
            echo "No changes in resolvers. Keeping original file."
            mv "$BACKUP_FILE" "$LOCAL_FILE"
        else
            echo "Resolvers have been updated. Backup kept as $BACKUP_FILE"
        fi
    else
        echo "Restoring original file from backup..."
        mv "$BACKUP_FILE" "$LOCAL_FILE"
    fi
else
    echo "No existing resolver file found. Downloading fresh copy..."
    download_resolver
fi
