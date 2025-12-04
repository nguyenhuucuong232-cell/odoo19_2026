# 🚀 HƯỚNG DẪN KHÔI PHỤC HỆ THỐNG ODOO 19

## 📋 Các Backup Có Sẵn

Dưới đây là các backup đã được tạo theo kế hoạch:

### Full System Backups (Toàn bộ hệ thống):
- `pre_production_20251123_164534.tar.gz` (16:45:34)
- `pre_production_20251123_165901.tar.gz` (16:59:01)
- `pre_production_20251123_172148.tar.gz` (17:21:48)

### Database Backups (Chỉ cơ sở dữ liệu):
- `odoo19_pre_production_20251123_164534.sql`
- `odoo19_pre_production_20251123_165901.sql`
- `odoo19_pre_production_20251123_172148.sql`

## 🔄 Cách Khôi Phục

### 1. Liệt kê backup có sẵn:
```bash
cd /home/sgc/odoo19
./restore.sh --list
```

### 2. Khôi phục từ backup cụ thể:
```bash
# Thay thế timestamp bằng thời gian backup bạn muốn
./restore.sh 20251123_164534
```

### 3. Ví dụ thực tế:
```bash
# Khôi phục từ backup đầu tiên
./restore.sh 20251123_164534

# Khôi phục từ backup gần nhất
./restore.sh 20251123_172148
```

## ⚠️ Lưu Ý Quan Trọng

1. **Script sẽ tự động tạo backup khẩn cấp** trước khi khôi phục
2. **Cần xác nhận** trước khi thực hiện khôi phục
3. **Dịch vụ sẽ bị dừng** trong quá trình khôi phục
4. **Thời gian khôi phục** khoảng 5-10 phút

## 📝 Quy Trình Khôi Phục

1. **Dừng dịch vụ hiện tại**
2. **Tạo backup khẩn cấp**
3. **Khôi phục cơ sở dữ liệu**
4. **Khôi phục file và cấu hình**
5. **Khởi động lại dịch vụ**
6. **Kiểm tra tính toàn vẹn**

## 🎯 Kiểm tra sau khi khôi phục

Sau khi khôi phục thành công:

1. Truy cập: `http://localhost:10019`
2. Kiểm tra dữ liệu quan trọng
3. Test các workflow chính
4. Xác nhận cấu hình

## 🆘 Trường hợp khẩn cấp

Nếu khôi phục gặp vấn đề:
- Kiểm tra file backup khẩn cấp: `/home/sgc/odoo-backups/emergency_before_restore_*.tar.gz`
- Chạy lại script với backup khác
- Liên hệ admin nếu cần hỗ trợ

---
*Tạo bởi: Odoo 19 Setup Assistant*
*Ngày: 23/11/2025*