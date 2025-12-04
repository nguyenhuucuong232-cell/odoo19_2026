#!/bin/bash
# Script to restore full database from backup SQL file

BACKUP_FILE="/home/sgc/odoo19/backups/odoo19_db_20251124_082003.sql"
DB_NAME="odoo19"
DB_USER="odoo"
DB_CONTAINER="odoo19-db-1"

echo "============================================================"
echo "Full Database Restore Script"
echo "============================================================"
echo "Backup file: $BACKUP_FILE"
echo "Database: $DB_NAME"
echo ""

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
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

# Restore database
docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME < "$BACKUP_FILE" 2>&1 | tail -20

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "✓ Database restored successfully!"
else
    echo ""
    echo "✗ Error: Database restore failed"
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

