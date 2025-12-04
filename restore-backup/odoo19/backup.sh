#!/bin/bash
# Automated Backup Script for Odoo Production

BACKUP_DIR="/home/sgc/odoo-backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/odoo19_backup_$TIMESTAMP.tar.gz"
DB_BACKUP="$BACKUP_DIR/odoo19_db_$TIMESTAMP.sql"

echo "🔄 Starting automated backup: $TIMESTAMP"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
echo "📦 Backing up database..."
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U odoo odoo19 > "$DB_BACKUP"

# Backup filestore and configuration
echo "📦 Backing up files and configuration..."
tar -czf "$BACKUP_FILE" \
    --exclude='*.log' \
    --exclude='__pycache__' \
    --exclude='.git' \
    -C "/home/sgc/odoo19" .

# Compress database backup
gzip "$DB_BACKUP"

# Cleanup old backups (keep last 7 days)
echo "🧹 Cleaning up old backups..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete

echo "✅ Backup completed: $BACKUP_FILE"
echo "📊 Backup size: $(du -sh "$BACKUP_FILE" | cut -f1)"
