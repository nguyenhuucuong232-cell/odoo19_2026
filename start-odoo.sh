#!/bin/bash

echo "=========================================="
echo "  Khởi động Odoo 19 Enterprise"
echo "=========================================="
echo ""

# Kiểm tra Docker
echo "[1/5] Kiểm tra Docker daemon..."
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker daemon chưa chạy. Vui lòng khởi động Docker Desktop trước!"
    exit 1
fi
echo "✓ Docker daemon đã sẵn sàng"
echo ""

# Kiểm tra enterprise addons
echo "[2/5] Kiểm tra Enterprise addons..."
ADDON_COUNT=$(ls enterprise-addons/ 2>/dev/null | wc -l | xargs)
if [ "$ADDON_COUNT" -lt 100 ]; then
    echo "⚠ Cảnh báo: Chỉ tìm thấy $ADDON_COUNT addons. Có thể chưa copy đầy đủ."
else
    echo "✓ Tìm thấy $ADDON_COUNT Enterprise addons"
fi
echo ""

# Khởi động containers
echo "[3/5] Đang khởi động containers..."
docker compose up -d
echo ""

# Chờ containers khởi động
echo "[4/5] Đang chờ containers khởi động (15 giây)..."
sleep 15
echo ""

# Kiểm tra trạng thái
echo "[5/5] Kiểm tra trạng thái containers:"
docker compose ps
echo ""

# Hiển thị logs
echo "=========================================="
echo "  Logs Odoo (30 dòng cuối):"
echo "=========================================="
docker compose logs --tail=30 odoo
echo ""

# Kiểm tra addons path
echo "=========================================="
echo "  Kiểm tra Enterprise addons trong container:"
echo "=========================================="
docker exec odoo-19-enterprise ls -la /mnt/enterprise-addons/ 2>/dev/null | head -10 || echo "⚠ Chưa mount được thư mục enterprise-addons"
echo ""

echo "=========================================="
echo "  Hoàn tất!"
echo "=========================================="
echo "Truy cập Odoo tại: http://localhost:10019"
echo ""
echo "Để xem logs real-time, chạy:"
echo "  docker compose logs -f odoo"
echo ""

