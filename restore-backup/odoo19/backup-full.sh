#!/bin/bash

# Odoo Full Backup Script
# Backup database, filestore, and addons

set -e

# Configuration
ODOO_CONTAINER="odoo19"
DB_HOST="db"
DB_USER="odoo"
DB_PASSWORD="odoo19@2025"
DB_NAME="odoo19"
BACKUP_DIR="/home/sgc/odoo-backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="odoo19_full_${TIMESTAMP}"

echo "Starting Odoo full backup: ${BACKUP_NAME}"

# Create backup directory
mkdir -p "${BACKUP_DIR}/${BACKUP_NAME}"

# Backup database
echo "Backing up database..."
docker exec -e PGPASSWORD="${DB_PASSWORD}" "${ODOO_CONTAINER}_${ODOO_CONTAINER}_1" pg_dump -h "${DB_HOST}" -U "${DB_USER}" "${DB_NAME}" > "${BACKUP_DIR}/${BACKUP_NAME}/database.sql"

# Backup filestore
echo "Backing up filestore..."
docker exec "${ODOO_CONTAINER}_${ODOO_CONTAINER}_1" tar czf - /var/lib/odoo/filestore | tar xzf - -C "${BACKUP_DIR}/${BACKUP_NAME}"

# Backup addons (custom modules)
echo "Backing up custom addons..."
tar czf "${BACKUP_DIR}/${BACKUP_NAME}/addons.tar.gz" -C /home/sgc/odoo19 addons

# Create restore script
cat > "${BACKUP_DIR}/${BACKUP_NAME}/restore.sh" << EOF
#!/bin/bash
# Restore script for ${BACKUP_NAME}

set -e

echo "Restoring Odoo from backup: ${BACKUP_NAME}"

# Stop Odoo
docker-compose stop odoo19

# Restore database
echo "Restoring database..."
docker exec -i -e PGPASSWORD="${DB_PASSWORD}" db psql -h db -U ${DB_USER} -d postgres -c "DROP DATABASE IF EXISTS ${DB_NAME};"
docker exec -i -e PGPASSWORD="${DB_PASSWORD}" db psql -h db -U ${DB_USER} -d postgres -c "CREATE DATABASE ${DB_NAME};"
docker exec -i -e PGPASSWORD="${DB_PASSWORD}" db psql -h db -U ${DB_USER} -d ${DB_NAME} < database.sql

# Restore filestore
echo "Restoring filestore..."
docker exec odoo19 mkdir -p /var/lib/odoo/filestore
docker cp filestore odoo19:/var/lib/odoo/

# Restore addons
echo "Restoring addons..."
tar xzf addons.tar.gz -C /home/sgc/odoo19

# Start Odoo
docker-compose start odoo19

echo "Restore completed!"
EOF

chmod +x "${BACKUP_DIR}/${BACKUP_NAME}/restore.sh"

echo "Backup completed successfully!"
echo "Backup location: ${BACKUP_DIR}/${BACKUP_NAME}"
echo "To restore, run: cd ${BACKUP_DIR}/${BACKUP_NAME} && ./restore.sh"