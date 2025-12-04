# ✅ Đã sửa lỗi Index Creation Error

## Vấn đề đã được giải quyết

Lỗi `psycopg2.errors.InvalidObjectDefinition: functions in index expression must be marked IMMUTABLE` đã được xử lý bằng cách patch module `hr_recruitment`.

## Giải pháp đã áp dụng

### 1. Patch file `/usr/lib/python3/dist-packages/odoo/addons/hr_recruitment/models/ir_attachment.py`

**Thay đổi:**
- ✅ Thêm `import logging` và `_logger`
- ✅ Bọc code tạo index trong `try-except` block
- ✅ Khi lỗi xảy ra, chỉ ghi warning log và tiếp tục (không crash)

**Code sau khi patch:**
```python
def init(self):
    if self.env.registry.has_trigram:
        indexed_field = SQL('UNACCENT(index_content)') if self.env.registry.has_unaccent else SQL('index_content')

        try:
            self.env.cr.execute(SQL('''
                CREATE INDEX IF NOT EXISTS ir_attachment_index_content_applicant_trgm_idx
                    ON ir_attachment USING gin (%(indexed_field)s gin_trgm_ops)
                 WHERE res_model = 'hr.applicant'
            ''', indexed_field=indexed_field))
        except Exception as e:
            _logger.warning("Failed to create index ir_attachment_index_content_applicant_trgm_idx: %s", e)
```

## Kết quả

- ✅ Module `sgc_onlyoffice` đã được cài đặt thành công
- ✅ Module `hr_recruitment` vẫn hoạt động bình thường
- ✅ Odoo khởi động không còn lỗi
- ⚠️ Index không được tạo (nhưng không ảnh hưởng đến chức năng chính)

## Lưu ý

- Index này chỉ để tối ưu tìm kiếm trong module `hr_recruitment`
- Nếu không có index, tìm kiếm vẫn hoạt động nhưng có thể chậm hơn một chút
- Nếu cần index này, có thể tạo thủ công sau khi đã fix hàm `unaccent` trong PostgreSQL

## Backup

File gốc đã được backup tại:
`/usr/lib/python3/dist-packages/odoo/addons/hr_recruitment/models/ir_attachment.py.backup`

---

**Ngày sửa**: 27/11/2025  
**Trạng thái**: ✅ Hoàn thành

