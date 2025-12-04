#!/bin/bash

# Script backup Odoo 19 với timestamp
# Tạo thư mục backup với format: bakup_odoo19_DD_MM_YYYY_HH_MM

BACKUP_DIR="/home/sgc/file luu trữ/bakup_odoo19_$(date +%d_%m_%Y_%H_%M)"
ODOO_DIR="/home/sgc/odoo19"

echo "Tạo thư mục backup: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

echo "Backup database..."
cd "$ODOO_DIR"
docker-compose exec db pg_dump -U odoo -d odoo > "$BACKUP_DIR/odoo19_backup_$(date +%Y%m%d_%H%M%S).sql"

echo "Backup filestore..."
cp -r ../odoo-backups/filestore "$BACKUP_DIR/"

echo "Backup addons tùy chỉnh..."
cp -r "$ODOO_DIR/addons" "$BACKUP_DIR/"

echo "Backup cấu hình..."
cp "$ODOO_DIR/docker-compose.yml" "$BACKUP_DIR/"
cp -r "$ODOO_DIR/etc" "$BACKUP_DIR/"

echo "Backup hoàn thành: $BACKUP_DIR"
echo "Kích thước backup:"
du -sh "$BACKUP_DIR"

echo ""
echo "Để restore, sử dụng script restore.sh trong thư mục backup hoặc thủ công:"
echo "1. Restore database: docker-compose exec -T db psql -U odoo -d odoo < backup.sql"
echo "2. Restore filestore: cp -r filestore ../odoo-backups/"
echo "3. Restore addons: cp -r addons ../odoo19/"