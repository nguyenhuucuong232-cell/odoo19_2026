#!/bin/bash
# Script tạo Backup toàn bộ hệ thống (Database + Custom Code)
# Usage: ./tools/backup_time_machine.sh [Ghi chú tùy chọn]

# 1. Cấu hình
TIMESTAMP=$(date +%d_%m_%Y_%H_%M)
BACKUP_ROOT="./backups"
BACKUP_NAME="backup_odoo19_${TIMESTAMP}"
TARGET_DIR="${BACKUP_ROOT}/${BACKUP_NAME}"

DB_CONTAINER="odoo19_db_1"
DB_USER="odoo"
DB_NAME="odoo19"

echo "========================================================"
echo "🚀 ĐANG KHỞI ĐỘNG 'CỖ MÁY THỜI GIAN'..."
echo "🕒 Thời điểm: $TIMESTAMP"
echo "📂 Thư mục đích: $TARGET_DIR"
echo "========================================================"

# 2. Tạo thư mục backup
mkdir -p "$TARGET_DIR"

# 3. Backup Database (PostgreSQL Dump)
echo "📦 1/3. Đang sao lưu Database ($DB_NAME)..."
docker exec -t $DB_CONTAINER pg_dump -U $DB_USER -d $DB_NAME -F c -b -v -f /tmp/dump.backup
docker cp $DB_CONTAINER:/tmp/dump.backup "$TARGET_DIR/database.dump"
docker exec $DB_CONTAINER rm /tmp/dump.backup

if [ -f "$TARGET_DIR/database.dump" ]; then
    echo "   ✅ Database backup thành công."
else
    echo "   ❌ LỖI: Không thể backup Database."
    exit 1
fi

# 4. Backup Custom Addons (Code)
echo "📂 2/3. Đang sao lưu Source Code (addons)..."
cp -r ./addons "$TARGET_DIR/addons"
echo "   ✅ Source code backup thành công."

# 5. Backup Filestore (File đính kèm - Optional nhưng quan trọng)
# Lưu ý: Đường dẫn filestore mặc định trong container Odoo
echo "🗂️ 3/3. Đang sao lưu Filestore..."
ODOO_CONTAINER="odoo19_odoo19_1"
# Tạo thư mục filestore trong backup
mkdir -p "$TARGET_DIR/filestore"
# Copy từ container ra (đường dẫn này chuẩn cho Odoo Docker mặc định)
docker cp $ODOO_CONTAINER:/var/lib/odoo/.local/share/Odoo/filestore/$DB_NAME "$TARGET_DIR/filestore/" 2>/dev/null

echo "========================================================"
echo "✅ HOÀN TẤT! ĐIỂM LƯU ĐÃ ĐƯỢC TẠO."
echo "👉 Bạn có thể tìm thấy tại: $TARGET_DIR"
echo "========================================================"

