#!/bin/bash
# Script để cài đặt Odoo Enterprise addons

echo "🔄 Đang giải nén và cài đặt Odoo Enterprise addons..."

# Giải nén vào thư mục tạm
TEMP_DIR="/tmp/odoo-enterprise-temp"
SOURCE_FILE="/home/sgc/file luu trữ/odoo_19.0+e.20251109.tar.gz"
TARGET_DIR="/home/sgc/odoo19/odoo-enterprise/src/odoo/addons"

# Xóa thư mục tạm cũ nếu có
rm -rf "$TEMP_DIR"

# Giải nén
echo "📦 Đang giải nén file..."
tar -xzf "$SOURCE_FILE" -C /tmp

# Thay đổi quyền sở hữu thư mục đích
echo "🔐 Đang thay đổi quyền sở hữu..."
sudo chown -R sgc:sgc "$TARGET_DIR"

# Sao chép các addons
echo "📋 Đang sao chép các addons enterprise..."
cp -r "$TEMP_DIR/odoo-19.0+e.20251109/odoo/addons/"* "$TARGET_DIR/"

# Đếm số addons đã cài đặt
ADDON_COUNT=$(ls -d "$TARGET_DIR"/*/ 2>/dev/null | wc -l)

echo "✅ Hoàn thành!"
echo "📊 Tổng số addons đã cài đặt: $ADDON_COUNT"
echo ""
echo "💡 Lưu ý: Nếu bạn gặp lỗi permission, hãy chạy:"
echo "   sudo chown -R sgc:sgc $TARGET_DIR"

