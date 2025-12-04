# SGC Modules - Hướng dẫn cài đặt và sử dụng

## Danh sách các module đã tạo

### 1. Module cơ sở
- **sgc_activity_dashboard** - Dashboard quản lý hoạt động
- **sgc_activity_reminder** - Nhắc nhở hoạt động qua Email/Popup
- **sgc_hr_reward_warning** - Khen thưởng/Kỷ luật và Thông báo nhân sự
- **sgc_crm_sale** - Tự động chuyển giai đoạn CRM

### 2. Module tài chính
- **sgc_account_payment** - Quản lý giao dịch thanh toán mở rộng

### 3. Module phê duyệt
- **sgc_approval_management** - Quản lý phê duyệt đơn hàng

### 4. Module tài liệu
- **sgc_document_management** - Quản lý văn bản, công văn đi/đến
- **sgc_onlyoffice** - Tích hợp OnlyOffice để chỉnh sửa tài liệu

### 5. Module KPI
- **sgc_kpi** - Quản lý KPI nhân sự

## Cách cài đặt

### Cách 1: Upgrade từng module
```bash
docker exec odoo19_odoo_1 /mnt/extra-addons/odoo-src/odoo-bin -c /mnt/extra-addons/etc/odoo.conf -u sgc_activity_dashboard --stop-after-init
```

### Cách 2: Upgrade tất cả module SGC
```bash
cd /home/sgc/odoo19
./upgrade_sgc_modules.sh
```

### Cách 3: Upgrade qua Odoo UI
1. Vào **Apps** menu
2. Bỏ filter "Apps"
3. Tìm module cần upgrade (ví dụ: "SGC Activity Dashboard")
4. Click **Upgrade**

## Lưu ý khi upgrade

1. **Backup database** trước khi upgrade
2. Upgrade theo thứ tự phụ thuộc:
   - Các module cơ sở trước (activity, hr)
   - Module tài chính
   - Module phê duyệt
   - Module tài liệu
   - Module KPI

## Cấu hình OnlyOffice

1. Vào **Settings** > **General Settings**
2. Tìm section **OnlyOffice Integration**
3. Nhập:
   - **OnlyOffice Server URL**: URL của OnlyOffice Document Server
   - **JWT Secret**: (Tùy chọn) Secret để xác thực

## Sửa lỗi đã thực hiện

### Lỗi: "Service rpc is not available"
- **Đã sửa**: Xóa `useService("rpc")` trong `sgc_activity_dashboard/static/src/js/activity_dashboard.js`
- **Giải pháp**: Chỉ sử dụng `useService("orm")` thay thế

### Lỗi: Method get_activity
- **Đã sửa**: Cập nhật method `get_activity` trong `sgc_activity_dashboard/models/mail_activity.py`
- **Giải pháp**: Sửa signature và cách gọi từ JavaScript

## Hiển thị trên Apps Menu

Tất cả các module đã được cấu hình với:
- `application: True` trong `__manifest__.py`
- Menu root trong views
- Icon placeholder (có thể thay thế sau)

Sau khi upgrade, các module sẽ tự động hiển thị trên Apps menu.

## Thứ tự cài đặt đề xuất

1. sgc_activity_dashboard
2. sgc_activity_reminder
3. sgc_hr_reward_warning
4. sgc_crm_sale
5. sgc_account_payment
6. sgc_approval_management
7. sgc_document_management
8. sgc_onlyoffice
9. sgc_kpi

## Hỗ trợ

Nếu gặp lỗi, kiểm tra:
1. Logs trong Odoo: Settings > Technical > Logging
2. Console browser (F12) để xem lỗi JavaScript
3. Docker logs: `docker logs odoo19_odoo_1`

