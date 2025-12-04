#!/bin/bash
# Script to restore database from backup before the restore operation

BACKUP_FILE="/home/sgc/odoo19/backups/odoo19_db_full_backup_before_restore_20251127_013442.dump"
DB_NAME="odoo19"
DB_USER="odoo"
DB_CONTAINER="odoo19-db-1"

echo "============================================================"
echo "Restore Database from Backup (Before Restore)"
echo "============================================================"
echo "Backup file: $BACKUP_FILE"
echo "Database: $DB_NAME"
echo ""

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    echo ""
    echo "Available backups:"
    ls -lh /home/sgc/odoo19/backups/*.dump /home/sgc/odoo19/backups/*.sql 2>/dev/null | head -5
    exit 1
fi

# Check file size
FILE_SIZE=$(stat -f%z "$BACKUP_FILE" 2>/dev/null || stat -c%s "$BACKUP_FILE" 2>/dev/null)
if [ "$FILE_SIZE" -lt 1000 ]; then
    echo "Warning: Backup file seems too small ($FILE_SIZE bytes). It might be corrupted."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if database container is running
if ! docker ps | grep -q "$DB_CONTAINER"; then
    echo "Error: Database container not running: $DB_CONTAINER"
    exit 1
fi

echo "Step 1: Stopping Odoo server..."
docker stop odoo19_odoo19_1 2>/dev/null || echo "  Odoo container not found or already stopped"

echo ""
echo "Step 2: Dropping existing database connections..."
docker exec $DB_CONTAINER psql -U $DB_USER -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$DB_NAME' AND pid <> pg_backend_pid();" 2>/dev/null || true

echo ""
echo "Step 3: Dropping and recreating database..."
docker exec $DB_CONTAINER psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS ${DB_NAME};" 2>/dev/null
docker exec $DB_CONTAINER psql -U $DB_USER -d postgres -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Error: Failed to recreate database"
    exit 1
fi

echo ""
echo "Step 4: Restoring database from backup..."
echo "  This may take a few minutes..."

# Check if it's a custom format dump or SQL
if [[ "$BACKUP_FILE" == *.dump ]]; then
    # Custom format dump
    docker exec -i $DB_CONTAINER pg_restore -U $DB_USER -d $DB_NAME --verbose < "$BACKUP_FILE" 2>&1 | tail -20
    RESTORE_EXIT=$?
else
    # SQL format
    docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME < "$BACKUP_FILE" 2>&1 | tail -20
    RESTORE_EXIT=$?
fi

if [ $RESTORE_EXIT -eq 0 ]; then
    echo ""
    echo "✓ Database restored successfully!"
else
    echo ""
    echo "✗ Error: Database restore failed (exit code: $RESTORE_EXIT)"
    echo "  The backup file might be corrupted or incomplete."
    exit 1
fi

echo ""
echo "Step 5: Starting Odoo server..."
docker start odoo19_odoo19_1 2>/dev/null || echo "  Odoo container not found"

echo ""
echo "============================================================"
echo "Restore completed!"
echo "============================================================"
echo ""
echo "Please wait for Odoo to start (30-60 seconds)"
echo "Then clear your browser cache (Ctrl+F5) and check the website"

