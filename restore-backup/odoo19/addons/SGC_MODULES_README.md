# Tổng hợp các Module SGC cho Odoo 19

## Danh sách Module đã tạo

### 1. **sgc_activity_dashboard** - Giám sát hoạt động
- Dashboard quản lý và theo dõi hoạt động (Activities)
- Lọc theo người dùng, phòng ban, khoảng thời gian
- Quản lý Activity Tags
- **Menu:** "Các hoạt động" (hiển thị trên dashboard)

### 2. **sgc_activity_reminder** - Nhắc nhở hoạt động
- Nhắc nhở hoạt động qua Email và Popup
- Tự động nhắc nhở theo lịch trình
- Cấu hình thời gian nhắc nhở linh hoạt

### 3. **sgc_hr_reward_warning** - Thông báo nhân sự
- Quản lý thông báo, khen thưởng và kỷ luật nhân sự
- Thông báo theo nhân viên, phòng ban hoặc vị trí công việc
- Quy trình phê duyệt thông báo
- **Menu:** "Thông báo" (hiển thị trên dashboard)

### 4. **sgc_crm_sale** - Tự động chuyển giai đoạn CRM
- Tự động chuyển giai đoạn CRM sau thời gian định trước
- Thông báo nhắc nhở trước khi hết hạn giai đoạn

### 5. **sgc_account_payment** - Quản lý thanh toán
- Quản lý giao dịch thanh toán thu/chi
- Phân loại danh mục thanh toán
- Theo dõi chi tiết từng dòng thanh toán
- **Menu:** "Thanh toán" (hiển thị trên dashboard)

### 6. **sgc_approval_management** - Quản lý phê duyệt
- Phê duyệt đơn bán hàng
- Phê duyệt theo cấp độ
- Quy trình phê duyệt linh hoạt
- **Menu:** "Phê duyệt" (hiển thị trên dashboard)

### 7. **sgc_document_management** - Quản lý văn bản
- Quản lý công văn đi/đến
- Workflow xử lý văn bản
- Theo dõi lịch sử xử lý
- **Menu:** "Quản lý văn bản" (hiển thị trên dashboard)

### 8. **sgc_onlyoffice** - Tích hợp OnlyOffice
- Chỉnh sửa tài liệu Office trực tuyến (docx, xlsx, pptx)
- Xem trước tài liệu
- Cộng tác chỉnh sửa thời gian thực

### 9. **sgc_kpi** - Quản lý KPI
- Định nghĩa tiêu chí KPI
- Báo cáo KPI theo tháng
- Theo dõi hiệu suất nhân viên
- **Menu:** "KPI" (hiển thị trên dashboard)

### 10. **sgc_management_core** - Module core
- Quản lý Hợp đồng đã ký
- Tùy chỉnh Báo giá, Hợp đồng, Dự án
- **Menu:** "Hợp đồng ký kết" (hiển thị trên dashboard)

## Cài đặt

1. **Restart Odoo container:**
   ```bash
   docker restart <odoo_container_name>
   ```

2. **Update Apps List:**
   - Vào Odoo: Apps > Update Apps List

3. **Cài đặt các module:**
   - Cài đặt theo thứ tự phụ thuộc:
     - sgc_activity_dashboard
     - sgc_activity_reminder
     - sgc_hr_reward_warning
     - sgc_crm_sale
     - sgc_account_payment
     - sgc_approval_management
     - sgc_document_management
     - sgc_onlyoffice (cần cấu hình OnlyOffice Server URL)
     - sgc_kpi
     - sgc_management_core

## Cấu hình OnlyOffice

1. Vào **Settings > General Settings > OnlyOffice Integration**
2. Nhập **OnlyOffice Server URL** (ví dụ: `https://documentserver.example.com`)
3. (Tùy chọn) Nhập **JWT Secret** nếu OnlyOffice server yêu cầu

## Lưu ý

- Tất cả module đã được đổi prefix thành `sgc_`
- Không bao gồm module Zalo (theo yêu cầu)
- Tích hợp OnlyOffice đã được thêm vào
- Tất cả module tương thích với Odoo 19

## Sửa lỗi

### Lỗi "Service rpc is not available"
- Đã sửa trong `sgc_activity_dashboard` - xóa service rpc không còn tồn tại trong Odoo 19

### Module không hiển thị trên dashboard
- Kiểm tra file `sgc_main_menus.xml` đã được load trong `__manifest__.py`
- Đảm bảo action ID đúng trong menu

