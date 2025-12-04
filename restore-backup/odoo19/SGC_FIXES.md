# SGC Modules - Các lỗi đã sửa

## Lỗi 1: "Service rpc is not available" trong sgc_activity_dashboard

### Nguyên nhân
- Trong Odoo 19, service `rpc` không còn tồn tại
- Code đang sử dụng `useService("rpc")` không hợp lệ

### Giải pháp
**File**: `sgc_activity_dashboard/static/src/js/activity_dashboard.js`
- Xóa dòng: `this.rpc = useService("rpc");`
- Chỉ sử dụng `this.orm = useService('orm');` thay thế

### Thay đổi
```javascript
// TRƯỚC
setup() {
    this.rpc = useService("rpc");  // ❌ Lỗi
    this.orm = useService('orm');
    ...
}

// SAU
setup() {
    // ✅ Đã xóa dòng rpc
    this.orm = useService('orm');
    ...
}
```

## Lỗi 2: Method get_activity không hoạt động đúng

### Nguyên nhân
- Method `get_activity` được gọi với tham số không đúng
- JavaScript gọi với `[0, parseInt(id)]` nhưng method chỉ nhận 1 tham số

### Giải pháp
**File 1**: `sgc_activity_dashboard/models/mail_activity.py`
```python
# TRƯỚC
def get_activity(self, activity_id):
    activity = self.env['mail.activity'].browse(activity_id)
    ...

# SAU
def get_activity(self, activity_id):
    activity = self.browse(activity_id)  # ✅ Sử dụng self thay vì env
    if not activity.exists():
        return {'model': False, 'res_id': False}
    ...
```

**File 2**: `sgc_activity_dashboard/static/src/js/activity_dashboard.js`
```javascript
// TRƯỚC
const result = await this.orm.call('mail.activity', 'get_activity', [0, parseInt(id)], {});

// SAU
const result = await this.orm.call('mail.activity', 'get_activity', [parseInt(id)]);
if (result && result.model && result.res_id) {
    // Xử lý kết quả
}
```

## Các module đã được cấu hình hiển thị trên Apps Menu

Tất cả các module sau đã có `application: True` và sẽ hiển thị trên Apps menu:

1. ✅ sgc_activity_dashboard
2. ✅ sgc_activity_reminder  
3. ✅ sgc_hr_reward_warning
4. ✅ sgc_crm_sale
5. ✅ sgc_account_payment
6. ✅ sgc_approval_management
7. ✅ sgc_document_management
8. ✅ sgc_onlyoffice
9. ✅ sgc_kpi

## Cách kiểm tra sau khi sửa

1. **Restart Odoo container**:
   ```bash
   docker restart odoo19_odoo_1
   ```

2. **Upgrade module**:
   ```bash
   docker exec odoo19_odoo_1 /mnt/extra-addons/odoo-src/odoo-bin -c /mnt/extra-addons/etc/odoo.conf -u sgc_activity_dashboard --stop-after-init
   ```

3. **Kiểm tra trong Odoo**:
   - Vào **Apps** menu
   - Tìm "SGC Activity Dashboard"
   - Mở Dashboard và kiểm tra không còn lỗi

## Lưu ý

- Sau khi sửa code JavaScript/CSS, cần **restart Odoo** để assets được reload
- Sau khi sửa Python models, cần **upgrade module** để áp dụng thay đổi
- Kiểm tra browser console (F12) để xem lỗi JavaScript nếu có

