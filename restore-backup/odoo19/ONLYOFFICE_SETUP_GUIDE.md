# HƯỚNG DẪN CÀI ĐẶT VÀ CẤU HÌNH ONLYOFFICE CHO ODOO 19

## ✅ Module đã được cài đặt

Module `sgc_onlyoffice` đã được cài đặt thành công trên Odoo 19.

---

## 📋 Yêu cầu

### 1. OnlyOffice Document Server

Bạn cần có một OnlyOffice Document Server đang chạy. Có 2 cách:

#### Cách 1: Sử dụng OnlyOffice Cloud (Khuyến nghị cho test)
- Đăng ký tại: https://www.onlyoffice.com/
- Sử dụng URL: `https://documentserver.onlyoffice.com`

#### Cách 2: Cài đặt OnlyOffice Document Server trên Docker (Khuyến nghị cho production)

```bash
docker run -i -t -d -p 80:80 --restart=always \
    -v /app/onlyoffice/DocumentServer/logs:/var/log/onlyoffice \
    -v /app/onlyoffice/DocumentServer/data:/var/www/onlyoffice/Data \
    -v /app/onlyoffice/DocumentServer/lib:/var/lib/onlyoffice \
    -v /app/onlyoffice/DocumentServer/db:/var/lib/postgresql \
    onlyoffice/documentserver
```

Hoặc sử dụng docker-compose:

```yaml
version: '3.8'
services:
  onlyoffice:
    image: onlyoffice/documentserver
    ports:
      - "8080:80"
    volumes:
      - onlyoffice_data:/var/www/onlyoffice/Data
      - onlyoffice_logs:/var/log/onlyoffice
    restart: always

volumes:
  onlyoffice_data:
  onlyoffice_logs:
```

---

## ⚙️ Cấu hình trong Odoo

### Bước 1: Truy cập Cài đặt

1. Đăng nhập vào Odoo với quyền Administrator
2. Vào **Settings** (Cài đặt)
3. Tìm phần **OnlyOffice Integration**

### Bước 2: Cấu hình OnlyOffice Server

1. **OnlyOffice Server URL**: 
   - Nhập URL của OnlyOffice Document Server
   - Ví dụ: `http://localhost:8080` (nếu chạy local)
   - Hoặc: `https://documentserver.example.com` (nếu chạy trên server)

2. **JWT Secret** (Tùy chọn):
   - Nếu OnlyOffice Server có bật JWT, nhập secret key
   - Nếu không có, để trống

### Bước 3: Lưu cấu hình

Click **Save** để lưu cấu hình.

---

## 📝 Sử dụng OnlyOffice

### Mở file với OnlyOffice

1. Vào bất kỳ module nào có attachment (ví dụ: Document Management, Mail, etc.)
2. Mở một attachment (file Word, Excel, PowerPoint)
3. Click nút **"Mở với OnlyOffice"** (sẽ hiển thị nếu file được hỗ trợ)
4. File sẽ mở trong OnlyOffice editor trong tab mới

### Định dạng được hỗ trợ

**Word Documents:**
- doc, docx, docm, dot, dotx, dotm
- odt, fodt, ott, rtf, txt

**Excel Spreadsheets:**
- xls, xlsx, xlsm, xlt, xltx, xltm
- ods, fods, ots, csv

**PowerPoint Presentations:**
- ppt, pptx, pptm, pot, potx, potm
- odp, fodp, otp

---

## 🔧 Kiểm tra cài đặt

### Kiểm tra module đã cài đặt:

```sql
SELECT name, state FROM ir_module_module WHERE name = 'sgc_onlyoffice';
```

Kết quả mong đợi: `state = 'installed'`

### Kiểm tra cấu hình:

1. Vào **Settings** → **OnlyOffice Integration**
2. Xác nhận URL và Secret đã được cấu hình

---

## 🐛 Xử lý lỗi

### Lỗi: "OnlyOffice Server chưa được cấu hình"
- **Giải pháp**: Vào Settings và cấu hình OnlyOffice Server URL

### Lỗi: "Định dạng file không được hỗ trợ"
- **Giải pháp**: Chỉ các file Office (Word, Excel, PowerPoint) mới được hỗ trợ

### Lỗi: Không thể kết nối đến OnlyOffice Server
- **Giải pháp**: 
  - Kiểm tra OnlyOffice Server đang chạy
  - Kiểm tra URL đúng
  - Kiểm tra firewall/network

### Lỗi: JWT authentication failed
- **Giải pháp**: 
  - Kiểm tra JWT Secret đúng
  - Hoặc tắt JWT trong OnlyOffice Server config

---

## 📚 Tài liệu tham khảo

- OnlyOffice Document Server: https://www.onlyoffice.com/document-server.aspx
- OnlyOffice API Documentation: https://api.onlyoffice.com/
- Odoo Integration: Module `sgc_onlyoffice`

---

## ✅ Trạng thái cài đặt

- ✅ Module `sgc_onlyoffice` đã được cài đặt
- ✅ Dependencies (PyJWT, requests) đã được cài đặt
- ⚠️ Cần cấu hình OnlyOffice Server URL trong Settings
- ⚠️ Cần có OnlyOffice Document Server đang chạy

---

**Ngày tạo**: 27/11/2025
**Module version**: 19.0.1.0.0

