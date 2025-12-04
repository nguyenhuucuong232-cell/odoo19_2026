# Setup Môi Trường Phát Triển Odoo 19 (Enterprise)

## 1. Chạy bằng Docker (Xem kết quả nhanh)
Tôi đã cập nhật Docker để nó tự động nhận diện thư mục Enterprise và cài đặt danh sách module bạn yêu cầu.
```bash
docker compose up -d
```
- **Truy cập Local:** `http://localhost:10019`
- **Truy cập qua Tailscale:** `http://100.122.93.102:10019`
- Tài khoản mặc định: `admin` / `admin`.

### Danh Sách Module Đã Kích Hoạt:
`CRM`, `Kho`, `Kế toán`, `Mua hàng`, `Dự án`, `Sản xuất`, `Timesheet`, `Chi phí`, `Studio`, `Tài liệu`, `Ngày nghỉ`, `Tuyển dụng`, `Nhân viên`, `AI`, `ESG`, `Kiến thức`, `Bảo trì`, `Ký số`, `Helpdesk`, `Học Online`, `Kế hoạch`, `Sự kiện`, `Liên hệ`, `PLM`, `Cho thuê`, `Lịch`, `Field Service`, `Đánh giá`, `Đội xe`, `Phê duyệt`, `Lịch hẹn`, `Sửa chữa`, `Chấm công`, `Mã vạch`, `Việc cần làm`, `VoIP`, `Bữa ăn`.

## 2. Chạy bằng VS Code (Để lập trình/Debug)
Nếu bạn muốn sửa code và debug chi tiết:
1. Mở tab **Run & Debug**.
2. Chọn **"Odoo 19 Enterprise Local"**.
3. Nhấn Play (F5).
4. **Truy cập Local:** `http://localhost:8069`
5. **Truy cập qua Tailscale:** `http://100.122.93.102:8069`

*Lưu ý: Nếu không truy cập được qua Tailscale, hãy kiểm tra Firewall trên máy này (Ubuntu):*
```bash
sudo ufw allow 8069/tcp
sudo ufw allow 10019/tcp
```

## Cấu Trúc Thư Mục
- `odoo-enterprise/src/`: Source code Odoo Enterprise.
- `addons/`: Chứa các module custom của bạn.
- `etc/odoo.conf`: File cấu hình.

## Git Sync
- `git pull`: Cập nhật code custom từ remote.
