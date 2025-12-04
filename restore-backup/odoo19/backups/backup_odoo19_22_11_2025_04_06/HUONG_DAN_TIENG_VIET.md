# 📚 HƯỚNG DẪN ODOO 19 - TIẾNG VIỆT

## 🎯 PHẦN 1: VÀO CHỈNH SỬA MẪU BÁO GIÁ

### **Cách 1: Qua Menu Bán hàng**

```
Bước 1: Nhấn "Bán hàng" (góc trên bên trái)
        ↓
Bước 2: Chọn "Cấu hình"
        ↓
Bước 3: Click "Đơn bán hàng" hoặc "Báo giá"
        ↓
Bước 4: Tìm mẫu (filter: trạng thái = "Báo giá")
        ↓
Bước 5: Click vào tên mẫu để mở
        ↓
Bước 6: Click "Sửa" (nút Edit) để chỉnh sửa
```

### **Cách 2: Tạo mẫu mới từ báo giá hiện có**

```
Bước 1: Bán hàng → Đơn hàng
        ↓
Bước 2: Mở 1 báo giá bất kỳ
        ↓
Bước 3: Click nút ⚙️ "Hành động" (Action)
        ↓
Bước 4: Chọn "Nhân bản" (Duplicate)
        ↓
Bước 5: Đổi tên thành "MẪU - [Tên mẫu của bạn]"
        ↓
Bước 6: Chỉnh sửa sản phẩm, số lượng, giá
        ↓
Bước 7: Lưu lại (Ctrl+S)
```

---

## 📝 PHẦN 2: CHỈNH SỬA NỘI DUNG MẪU

### **Trong form Mẫu báo giá, bạn có các TAB:**

#### **TAB 1: Chi tiết** 
- 📌 Mẫu báo giá số: BG-QTLD-001/2025
- 📌 Hiệu lực báo giá: 30 ngày
- 📌 Công ty: Chọn công ty
- 📌 Số nhật ký hóa đơn: (Journal)

#### **TAB 2: Sản phẩm tùy chọn** (QUAN TRỌNG NHẤT!)
Đây là nơi bạn thêm/sửa/xóa sản phẩm:

```
┌──────────────────────────────────────────────────────────────┐
│ STT │ Dịch vụ   │ Sản phẩm         │ Frequency │ Số lượng │
├──────────────────────────────────────────────────────────────┤
│  1  │ QTMTLD    │ Vi khí hậu       │   4,00    │   1,00   │
│  2  │ QTMTLD    │ Ánh sáng         │   4,00    │   1,00   │
│  3  │ QTMTLD    │ Tiếng ồn         │   4,00    │   1,00   │
└──────────────────────────────────────────────────────────────┘

CÁCH THÊM SẢN PHẨM:
  1. Click "Thêm dòng" (Add a line)
  2. Chọn sản phẩm từ dropdown
  3. Nhập số lượng
  4. Nhập đơn giá (hoặc để tự động)
  5. Chọn thuế
```

#### **TAB 3: Điều khoản & điều kiện**
Viết các điều khoản, ghi chú cho báo giá

#### **TAB 4: Trình tạo báo giá PDF**
Cấu hình header/footer của PDF (nếu module có)

#### **TAB 5: Chi phí**
Thêm các khoản phí bổ sung (vận chuyển, lắp đặt...)

---

## 🎨 PHẦN 3: SỬA MẪU IN PDF (HEADER/FOOTER/MÀU SẮC)

### **CÁCH 1: Qua Web UI (DỄ)**

```
Bước 1: Bật Developer Mode
        Settings → Developer Tools → Activate
        ↓
Bước 2: Vào phần Reports
        Settings → Technical → Báo cáo → Báo cáo (Reports)
        ↓
Bước 3: Tìm "Báo giá SGC"
        Gõ vào ô tìm kiếm: "Báo giá SGC"
        ↓
Bước 4: Click vào tên để mở
        ↓
Bước 5: Click "Edit View" hoặc nút </>
        Sẽ hiện cửa sổ code editor
        ↓
Bước 6: Sửa code XML
        - Dòng 72-77: Địa chỉ công ty
        - Dòng 96-102: Tiêu đề
        - Dòng 145-151: Tên cột bảng
        ↓
Bước 7: Click "Lưu" (Save)
        ↓
Bước 8: Test
        Mở 1 báo giá → Print → Báo giá SGC
```

### **CÁCH 2: Sửa file XML trực tiếp**

```bash
# Backup file trước khi sửa
cp addons/sgc_management_core/report/report_sale_order_sgc.xml \
   addons/sgc_management_core/report/report_sale_order_sgc.xml.backup

# Mở file để sửa
nano addons/sgc_management_core/report/report_sale_order_sgc.xml

# Sau khi sửa xong, upgrade module
python3 scripts/upgrade_sgc_module.py
```

---

## 📍 PHẦN 4: CÁC TRƯỜNG TRONG FORM BÁO GIÁ

Để thêm trường mới vào form báo giá (như trong hình):

### **Các trường mặc định đã có:**
- ✅ Mẫu báo giá số
- ✅ Hiệu lực báo giá
- ✅ Thư xác nhận
- ✅ Tần suất (Frequency) - có thể cần thêm
- ✅ Mẫu dự án
- ✅ Công ty
- ✅ Số nhật ký hoá đơn
- ✅ Cập nhật lần cuối bởi
- ✅ Chữ ký online
- ✅ Thanh toán online
- ✅ Mẫu hợp đồng

### **Nếu không thấy các trường này:**

**KÍCH HOẠT TRONG SETTINGS:**
```
1. Cài đặt → Bán hàng
2. Tìm các tùy chọn:
   □ Báo giá trực tuyến (Online Quotations)
   □ Chữ ký điện tử (Digital Signature)
   □ Thanh toán trực tuyến (Online Payment)
3. Tích vào checkbox để bật
4. Lưu
```

---

## 🔍 PHẦN 5: TÌM NHANH TRONG ODOO

### **Dùng thanh tìm kiếm:**
```
Nhấn Ctrl+K (hoặc click biểu tượng 🔍)
Gõ từ khóa bằng tiếng Việt:
  - "Mẫu báo giá"
  - "Cấu hình bán hàng"
  - "Báo cáo"
  - "Sản phẩm"
```

### **Menu đầy đủ bằng tiếng Việt:**
```
📌 Bán hàng
   ├─ Đơn hàng (Orders)
   ├─ Báo giá (Quotations) 
   ├─ Khách hàng (Customers)
   ├─ Sản phẩm (Products)
   ├─ Báo cáo (Reporting)
   └─ Cấu hình (Configuration)
       ├─ Cài đặt (Settings)
       ├─ Bộ phận sales (Sales Teams)
       ├─ Đơn bán hàng (Sales Orders) ← MẪU Ở ĐÂY
       ├─ Phương thức giao hàng (Delivery)
       ├─ Thẻ (Tags)
       └─ Sản phẩm (Products)
```

---

## ✅ **TÓM TẮT NHANH:**

### **Để sửa NỘI DUNG mẫu báo giá (sản phẩm, giá):**
```
Bán hàng → Cấu hình → Đơn bán hàng 
→ Chọn mẫu → Sửa → Tab "Sản phẩm tùy chọn"
```

### **Để sửa HÌNH THỨC in PDF (header, footer, màu):**
```
Settings → Technical → Reports → "Báo giá SGC" 
→ Edit Template
```

---

Bạn muốn tôi **chụp màn hình** hoặc **quay video** hướng dẫn từng bước không? Hoặc tôi có thể **remote vào màn hình** để chỉ cho bạn xem trực tiếp?
