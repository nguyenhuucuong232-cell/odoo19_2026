#!/bin/bash
# Script kiểm tra và init database mới trong Odoo

DB_NAME=$1

if [ -z "$DB_NAME" ]; then
    echo "Usage: $0 <database_name>"
    echo ""
    echo "Danh sách database hiện có:"
    docker exec odoo19-db-1 psql -U odoo -d postgres -c "SELECT datname FROM pg_database WHERE datistemplate = false AND datname NOT IN ('postgres') ORDER BY datname;" 2>&1 | grep -v "datname\|----\|row"
    exit 1
fi

echo "=== Kiểm tra database: $DB_NAME ==="

# Kiểm tra database có tồn tại không
EXISTS=$(docker exec odoo19-db-1 psql -U odoo -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME';" 2>&1)

if [ -z "$EXISTS" ] || [ "$EXISTS" != "1" ]; then
    echo "✗ Database '$DB_NAME' không tồn tại!"
    echo "Tạo database mới..."
    docker exec odoo19-db-1 psql -U odoo -d postgres -c "CREATE DATABASE $DB_NAME OWNER odoo;" 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ Database '$DB_NAME' đã được tạo"
    else
        echo "✗ Lỗi khi tạo database"
        exit 1
    fi
else
    echo "✓ Database '$DB_NAME' đã tồn tại"
fi

# Kiểm tra database đã được init chưa
HAS_TABLES=$(docker exec odoo19-db-1 psql -U odoo -d $DB_NAME -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'ir_module_module';" 2>&1)

if [ "$HAS_TABLES" = "0" ] || [ -z "$HAS_TABLES" ]; then
    echo "✗ Database '$DB_NAME' chưa được init"
    echo "Đang init database với module base..."
    docker exec odoo19_odoo19_1 odoo -d $DB_NAME -i base --stop-after-init 2>&1 | tail -10
    if [ $? -eq 0 ]; then
        echo "✓ Database '$DB_NAME' đã được init thành công"
    else
        echo "✗ Lỗi khi init database"
        exit 1
    fi
else
    echo "✓ Database '$DB_NAME' đã được init (có $HAS_TABLES bảng)"
fi

echo ""
echo "=== Hoàn tất ==="
echo "Database '$DB_NAME' đã sẵn sàng sử dụng!"
echo "Vui lòng refresh trang web Odoo để thấy database mới."

