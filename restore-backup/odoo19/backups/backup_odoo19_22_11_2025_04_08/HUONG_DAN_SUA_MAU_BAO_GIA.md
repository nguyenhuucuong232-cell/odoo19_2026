# 📝 HƯỚNG DẪN SỬA MẪU BÁO GIÁ VÀ CẤU HÌNH ODOO 19

## 🎯 MỤC TIÊU
- Tùy chỉnh mẫu báo giá PDF (header, footer, bảng chi tiết)
- Thêm/sửa các trường trong form báo giá
- Cấu hình menu và quy trình làm việc

---

## 📄 PHẦN 1: SỬA MẪU IN PDF (REPORT)

### 📍 File cần sửa:
```
/home/sgc/odoo19/addons/sgc_management_core/report/report_sale_order_sgc.xml
```

### 🎨 Các phần có thể tùy chỉnh:

#### 1️⃣ **HEADER (Đầu trang)** - Dòng 66-94
```xml
<!-- Sửa thông tin công ty -->
<div class="company-info">
    <strong>Trụ sở:</strong> [ĐỊA CHỈ MỚI]<br/>
    <strong>VP Hà Nội:</strong> [ĐỊA CHỈ HÀ NỘI]<br/>
    <strong>Email:</strong> [EMAIL MỚI]<br/>
    <strong>Hotline:</strong> [SỐ ĐIỆN THOẠI]
</div>

<!-- Sửa logo/tên công ty -->
<div class="logo-box">
    <div style="font-size: 32pt;">SGC</div>
    <div>HSE Consulting</div>
</div>
```

#### 2️⃣ **TIÊU ĐỀ** - Dòng 96-103
```xml
<h2 class="title-main">BẢNG BÁO GIÁ</h2>
<h3 class="title-sub">
    QUAN TRẮC MÔI TRƯỜNG LAO ĐỘNG NĂM 2025
</h3>
```

#### 3️⃣ **BẢNG CHI TIẾT** - Dòng 144-164
```xml
<!-- Sửa header bảng -->
<th>STT</th>
<th>Chỉ tiêu</th>
<th>Đơn vị tính</th>
<th>Số lượng</th>
<th>Đơn giá</th>
<th>Thành tiền (VNĐ)</th>
```

#### 4️⃣ **MÀU SẮC** - Dòng 42-64
```css
.main-table th {
    background-color: #FFFF00;  /* Màu vàng header */
}
.grand-total-row {
    background-color: #FFFF99;  /* Màu vàng nhạt */
}
```

#### 5️⃣ **FOOTER (Cuối trang)** - Dòng 237-254
```xml
<strong>QL Dự Án:</strong> <span t-field="doc.user_id.name"/>
<strong>ĐT:</strong> <span t-field="doc.user_id.phone"/>
<strong>Mail:</strong> <span t-field="doc.user_id.email"/>
```

#### 6️⃣ **GHI CHÚ & ĐIỀU KIỆN** - Dòng 217-235
```xml
<li>Thời gian dự kiến lấy mẫu: trong vòng 10 ngày...</li>
<li>Lần thanh toán đợt 1 (70%)...</li>
```

### 🔄 **Sau khi sửa file XML:**
```bash
cd /home/sgc/odoo19
python3 scripts/upgrade_sgc_module.py
```

---

## ⚙️ PHẦN 2: THÊM TRƯỜNG VÀO FORM BÁO GIÁ (WEB UI)

### 📍 File cần sửa:
```
/home/sgc/odoo19/addons/sgc_management_core/views/sale_order_views.xml
```

### 📝 Ví dụ thêm trường:

```xml
<record id="view_order_form_inherit_sgc" model="ir.ui.view">
    <field name="name">sale.order.form.inherit.sgc</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        
        <!-- Thêm trường sau "Khách hàng" -->
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="x_project_type" string="Loại dự án"/>
            <field name="x_sampling_location" string="Địa điểm lấy mẫu"/>
        </xpath>
        
        <!-- Thêm tab mới -->
        <xpath expr="//notebook" position="inside">
            <page string="Thông tin kỹ thuật">
                <group>
                    <field name="x_technician" string="Kỹ thuật viên"/>
                    <field name="x_sampling_date" string="Ngày lấy mẫu"/>
                    <field name="x_result_date" string="Ngày trả kết quả"/>
                </group>
            </page>
        </xpath>
        
    </field>
</record>
```

### Định nghĩa trường trong Model:
```
/home/sgc/odoo19/addons/sgc_management_core/models/sale_order.py
```

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    x_project_type = fields.Selection([
        ('qtmt', 'Quan trắc MT'),
        ('mtld', 'MT Lao động'),
        ('gpmt', 'Giấy phép MT'),
    ], string='Loại dự án')
    
    x_sampling_location = fields.Char(string='Địa điểm lấy mẫu')
    x_technician = fields.Many2one('hr.employee', string='Kỹ thuật viên')
    x_sampling_date = fields.Date(string='Ngày lấy mẫu')
    x_result_date = fields.Date(string='Ngày trả kết quả')
```

---

## 🎨 PHẦN 3: CÁC MẪU CÓ SẴN

### ✅ Đã tạo 16 mẫu báo giá:

1. **BÁO QUAN TRẮC MÔI TRƯỜNG LAO ĐỘNG NĂM** - 8 chỉ tiêu chuẩn
2. **BG QTMTLD + QTMT** - Gói kết hợp
3. **BG Lập hồ sơ ĐTM** - Đánh giá tác động
4. **BG QUAN TRẮC 2025 (KK, NT, KT, ĐT)** - Gói toàn diện
5. **BG QUAN TRẮC 2025** - Gói cơ bản
6. **BG ĐÁNH GIÁ MÔI TRƯỜNG** - Đánh giá hiện trạng
7. **HUẤN LUYỆN ATLD** - Đào tạo
8. **BG QUAN TRẮC 2025 (KT, NT)** - Khí + Nước
9. **Giám Sát Khí Nhà Kính PA2** - GHG monitoring
10. **BG Phân loại lao động** - Classification
11. **GIẤY PHÉP MÔI TRƯỜNG** - Licensing
12. **HÀNG HÓA** - Cung cấp thiết bị
13. **Kiểm kê khí thải nhà kính** - GHG inventory
14. **Kế hoạch giảm thải KNK** - Emission reduction
15. **KẾ HOẠCH GIẢM THẢI KNK** - Alternative
16. **TƯ VẤN ISO** - ISO 14001/45001

### 📍 Cách sử dụng mẫu:
1. Vào **Sales → Orders**
2. Tìm mẫu (filter: Quotation)
3. **Duplicate** mẫu
4. Thay đổi khách hàng và số lượng
5. Gửi cho khách

---

## 🔧 PHẦN 4: CẤU HÌNH MENU (Giống Odoo cũ)

### Menu "Cấu hình" cần có:

Odoo 19 đã có sẵn trong **Sales → Configuration:**
- ✅ Cài đặt (Settings)
- ✅ Bộ phận sales (Sales Teams)
- ✅ Đơn bán hàng (Quotation Templates) - dùng duplicated SO
- ✅ Header/Footer - dùng file XML custom
- ✅ Phương thức giao hàng (Delivery Methods)
- ✅ Thẻ (Tags)
- ✅ Sản phẩm (Products)
- ✅ Danh mục (Product Categories)
- ✅ Đơn vị tính (Units of Measure)
- ✅ Khoản thanh toán online (Payment Providers)
- ✅ Hoạt động (Activities)

---

## 📊 PHẦN 5: TỔNG KẾT HIỆN TẠI

### ✅ Đã có:
- ✅ 18 phòng ban
- ✅ 40 nhân viên
- ✅ 259 sản phẩm (hóa chất, thiết bị, dịch vụ)
- ✅ 30 khách hàng
- ✅ 16 mẫu báo giá
- ✅ 17 báo giá/đơn hàng thực tế
- ✅ 5 dự án
- ✅ Thuế GTGT Việt Nam (0%, 5%, 8%, 10%)
- ✅ Kế toán Việt Nam (l10n_vn)
- ✅ Module sgc_management_core

### 📋 Tiếp theo nên làm:
1. ✅ Đã xong: **Mẫu báo giá** 
2. ⏳ Cần làm: **Mẫu hợp đồng**
3. ⏳ Cần làm: **Mẫu biên bản lấy mẫu**
4. ⏳ Cần làm: **Mẫu biên bản nghiệm thu**
5. ⏳ Cần làm: **Quy trình tự động hóa**

---

## 📞 HỖ TRỢ

Nếu cần sửa:
- **Màu sắc**: Sửa CSS trong file XML
- **Thông tin công ty**: Sửa dòng 72-76 trong XML
- **Cấu trúc bảng**: Sửa dòng 144-215
- **Thêm trường mới**: Tạo file trong models/ và views/

Sau mỗi thay đổi: 
```bash
python3 scripts/upgrade_sgc_module.py
```

