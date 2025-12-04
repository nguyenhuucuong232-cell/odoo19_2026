#!/bin/bash
# Script xóa sạch dữ liệu để làm lại từ đầu (Factory Reset)
# CẢNH BÁO: DỮ LIỆU SẼ MẤT HẾT!

echo "========================================================"
echo "⚠️  CẢNH BÁO: BẠN ĐANG YÊU CẦU XÓA SẠCH HỆ THỐNG!"
echo "⚠️  Toàn bộ Database và Dữ liệu sẽ bị xóa vĩnh viễn."
echo "========================================================"
read -p "Bạn có chắc chắn muốn tiếp tục không? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ Đã hủy thao tác."
    exit 1
fi

echo "1. Đang dừng các Container..."
docker-compose down

echo "2. Đang xóa các Volume dữ liệu (Database & Filestore)..."
docker-compose down -v

echo "3. Dọn dẹp file tạm..."
rm -rf ./postgresql/* 2>/dev/null

echo "4. Khởi động lại hệ thống sạch..."
docker-compose up -d

echo "⏳ Đang chờ Database khởi tạo (15s)..."
sleep 15

echo "========================================================"
echo "✅ HỆ THỐNG ĐÃ ĐƯỢC RESET VỀ TRẠNG THÁI BAN ĐẦU (TRẮNG TINH)."
echo "👉 Hãy truy cập http://localhost:10019 để thiết lập Database mới."
echo "========================================================"

