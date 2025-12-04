#!/bin/bash

echo "=========================================="
echo "  Khởi động lại Odoo"
echo "=========================================="

# Kiểm tra Docker
if ! docker info > /dev/null 2>&1; then
    echo "✖ Docker chưa chạy. Vui lòng khởi động Docker Desktop."
    exit 1
fi

echo "[1/4] Đang dừng containers..."
cd /Users/nguyenhuucuong/Downloads/dockerodoo19
docker compose down

echo "[2/4] Đang khởi động containers..."
docker compose up -d

echo "[3/4] Đang chờ Odoo khởi động (20 giây)..."
sleep 20

echo "[4/4] Kiểm tra trạng thái:"
docker compose ps

echo ""
echo "Kiểm tra logs:"
docker compose logs odoo --tail 20

echo ""
echo "=========================================="
echo "  Kiểm tra kết nối:"
echo "=========================================="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:10019/web/login)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ Odoo đang chạy bình thường!"
    echo ""
    echo "Truy cập: http://localhost:10019/web/login"
    echo "Tài khoản: nhd.hsevn@gmail.com"
    echo "Mật khẩu: admin"
else
    echo "✖ Odoo chưa sẵn sàng (HTTP $HTTP_CODE)"
    echo "Vui lòng đợi thêm vài giây..."
fi

echo "=========================================="

