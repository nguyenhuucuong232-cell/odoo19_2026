#!/bin/bash
# Script to restore filestore from backup

BACKUP_FILESTORE="/home/sgc/odoo19/backups/backup_odoo19_22_11_2025_04_08/source_data/sgco1/filestore"
CURRENT_FILESTORE="/home/sgc/odoo19/data/filestore"
DB_NAME="odoo19"

echo "============================================================"
echo "Filestore Restore Script"
echo "============================================================"
echo "Backup filestore: $BACKUP_FILESTORE"
echo "Current filestore: $CURRENT_FILESTORE"
echo ""

# Check if backup filestore exists
if [ ! -d "$BACKUP_FILESTORE" ]; then
    echo "Error: Backup filestore not found: $BACKUP_FILESTORE"
    exit 1
fi

# Find database folder in backup
BACKUP_DB_FOLDER=""
for folder in "$BACKUP_FILESTORE"/*; do
    if [ -d "$folder" ]; then
        BACKUP_DB_FOLDER="$folder"
        echo "Found database folder in backup: $(basename $BACKUP_DB_FOLDER)"
        break
    fi
done

if [ -z "$BACKUP_DB_FOLDER" ]; then
    echo "Error: Could not find database folder in backup filestore"
    exit 1
fi

# Create current filestore directory if it doesn't exist
mkdir -p "$CURRENT_FILESTORE"

# Backup current filestore
if [ -d "$CURRENT_FILESTORE/$DB_NAME" ]; then
    echo ""
    echo "Step 1: Backing up current filestore..."
    BACKUP_CURRENT="/home/sgc/odoo19/backups/filestore_backup_$(date +%Y%m%d_%H%M%S)"
    cp -r "$CURRENT_FILESTORE/$DB_NAME" "$BACKUP_CURRENT" 2>/dev/null
    echo "  Current filestore backed up to: $BACKUP_CURRENT"
fi

# Stop Odoo to prevent file conflicts
echo ""
echo "Step 2: Stopping Odoo server..."
docker stop odoo19_odoo19_1 2>/dev/null || echo "  Odoo already stopped"

# Remove current filestore
echo ""
echo "Step 3: Removing current filestore..."
rm -rf "$CURRENT_FILESTORE/$DB_NAME"

# Copy filestore from backup
echo ""
echo "Step 4: Copying filestore from backup..."
echo "  This may take a few minutes..."

cp -r "$BACKUP_DB_FOLDER" "$CURRENT_FILESTORE/$DB_NAME"

if [ $? -eq 0 ]; then
    echo "  ✓ Filestore copied successfully"
    
    # Set proper permissions
    chmod -R 755 "$CURRENT_FILESTORE/$DB_NAME"
    echo "  ✓ Permissions set"
else
    echo "  ✗ Error: Failed to copy filestore"
    exit 1
fi

# Start Odoo
echo ""
echo "Step 5: Starting Odoo server..."
docker start odoo19_odoo19_1 2>/dev/null || echo "  Odoo container not found"

echo ""
echo "============================================================"
echo "Filestore restore completed!"
echo "============================================================"
echo ""
echo "Please wait for Odoo to start (30-60 seconds)"
echo "Then clear your browser cache (Ctrl+F5) and check the website"

