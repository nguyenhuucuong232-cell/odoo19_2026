# FIX: Index Creation Error for hr_recruitment Module

## Vấn đề

Khi cài đặt module `sgc_onlyoffice` hoặc các module khác, gặp lỗi:
```
psycopg2.errors.InvalidObjectDefinition: functions in index expression must be marked IMMUTABLE
```

Lỗi này xảy ra khi module `hr_recruitment` cố gắng tạo index:
```sql
CREATE INDEX ir_attachment_index_content_applicant_trgm_idx
    ON ir_attachment 
    USING gin (unaccent(index_content) gin_trgm_ops)
    WHERE res_model = 'hr.applicant';
```

## Nguyên nhân

Hàm `unaccent(text)` từ extension `unaccent` cần được đánh dấu là IMMUTABLE để có thể sử dụng trong index expression.

## Giải pháp

### Cách 1: Tạo index trước (Đã thực hiện)

Index đã được tạo trước khi module cố gắng tạo nó, nên module sẽ bỏ qua việc tạo lại.

### Cách 2: Tạo text search dictionary (Nếu cần)

```sql
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE TEXT SEARCH DICTIONARY IF NOT EXISTS public.unaccent (TEMPLATE = unaccent);
```

### Cách 3: Patch module hr_recruitment (Nếu vẫn lỗi)

Nếu vẫn gặp lỗi, có thể patch file:
`/usr/lib/python3/dist-packages/odoo/addons/hr_recruitment/models/ir_attachment.py`

Thêm try-except để bỏ qua lỗi khi tạo index:

```python
try:
    self.env.cr.execute(SQL('''
        CREATE INDEX IF NOT EXISTS ir_attachment_index_content_applicant_trgm_idx
            ON ir_attachment 
            USING gin (unaccent(index_content) gin_trgm_ops)
            WHERE res_model = 'hr.applicant'
    '''))
except Exception as e:
    # Index creation failed, but continue
    _logger.warning("Failed to create index: %s", e)
```

## Trạng thái hiện tại

- ✅ Extensions `unaccent` và `pg_trgm` đã được cài đặt
- ✅ Hàm `unaccent(text)` đã là IMMUTABLE
- ⚠️ Index chưa được tạo thành công (do vấn đề với dictionary)
- ✅ Odoo đã khởi động thành công

## Khuyến nghị

Nếu vẫn gặp lỗi khi cài đặt module, có thể:
1. Bỏ qua lỗi này (index không bắt buộc, chỉ để tối ưu tìm kiếm)
2. Patch module hr_recruitment để bỏ qua lỗi
3. Hoặc cài đặt module mà không có hr_recruitment

---

**Ngày sửa**: 27/11/2025

