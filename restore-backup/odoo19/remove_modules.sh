#!/bin/bash
# Script xóa hoàn toàn các module khỏi database Odoo
# Sử dụng: bash remove_modules.sh <db_user> <db_name>

DB_USER="$1"
DB_NAME="$2"

if [ -z "$DB_USER" ] || [ -z "$DB_NAME" ]; then
  echo "Cách dùng: bash remove_modules.sh <db_user> <db_name>"
  exit 1
fi

MODULES="'activity_management','document_manager','documentmanagement'"

psql -U "$DB_USER" -d "$DB_NAME" -c "DELETE FROM ir_module_module WHERE name IN ($MODULES);"
psql -U "$DB_USER" -d "$DB_NAME" -c "DELETE FROM ir_model_data WHERE module IN ($MODULES);"
psql -U "$DB_USER" -d "$DB_NAME" -c "DELETE FROM ir_attachment WHERE res_model IN ($MODULES);"

# Có thể bổ sung thêm các bảng khác nếu cần xóa sâu hơn

echo "Đã xóa các module khỏi database!"
