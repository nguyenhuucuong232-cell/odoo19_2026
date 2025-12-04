#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cập nhật các sản phẩm đã tồn tại với các trường đầy đủ
"""
import xmlrpc.client

url = 'http://localhost:10019'
db = 'odoo19'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print(f"✓ Kết nối Odoo thành công (User ID: {uid})")

# ========================================
# TÌM HOẶC TẠO THUẾ 8%
# ========================================
print("\n=== Chuẩn bị Thuế ===")
tax_8_id = models.execute_kw(db, uid, password,
    'account.tax', 'search',
    [[('name', 'ilike', '8%'), ('type_tax_use', '=', 'sale')]], {'limit': 1})

if not tax_8_id:
    print("  ! Không tìm thấy thuế 8%, tạo mới...")
    tax_8_id = [models.execute_kw(db, uid, password,
        'account.tax', 'create', [{
            'name': 'Thuế GTGT 8%',
            'amount': 8.0,
            'amount_type': 'percent',
            'type_tax_use': 'sale',
        }])]

print(f"  ✓ Thuế 8% (ID: {tax_8_id[0]})")

# ========================================
# LẤY TẤT CẢ SẢN PHẨM
# ========================================
print("\n=== Lấy danh sách sản phẩm cần cập nhật ===")

# Lấy tất cả sản phẩm không có mã tham chiếu nội bộ hoặc không có thuế
product_ids = models.execute_kw(db, uid, password,
    'product.template', 'search',
    [[
        '|',
        ('default_code', '=', False),
        ('taxes_id', '=', False)
    ]])

print(f"  Tìm thấy {len(product_ids)} sản phẩm cần cập nhật")

if len(product_ids) == 0:
    print("  ✓ Tất cả sản phẩm đã có đầy đủ thông tin!")
    exit(0)

# ========================================
# CẬP NHẬT TỪNG SẢN PHẨM
# ========================================
print("\n=== Cập nhật sản phẩm ===")

updated = 0
errors = 0

# Đọc thông tin danh mục để phân loại
cat_map = {}
categories = models.execute_kw(db, uid, password,
    'product.category', 'search_read',
    [[('name', 'in', ['Hóa chất phân tích', 'Thiết bị & Vật tư', 'Dịch vụ phân tích'])]], 
    {'fields': ['id', 'name']})

for cat in categories:
    cat_map[cat['id']] = cat['name']

for idx, prod_id in enumerate(product_ids, 1):
    try:
        # Đọc thông tin sản phẩm hiện tại
        product = models.execute_kw(db, uid, password,
            'product.template', 'read',
            [[prod_id]], {'fields': ['name', 'categ_id', 'default_code', 'type', 'taxes_id']})[0]
        
        # Xác định prefix cho mã sản phẩm
        cat_id = product['categ_id'][0] if product['categ_id'] else None
        cat_name = cat_map.get(cat_id, '')
        
        if 'Hóa chất' in cat_name:
            prefix = 'HC'
        elif 'Thiết bị' in cat_name or 'Vật tư' in cat_name:
            prefix = 'TB'
        else:
            prefix = 'DV'
        
        # Chuẩn bị dữ liệu cập nhật
        update_vals = {}
        
        # 1. Mã tham chiếu nội bộ (nếu chưa có)
        if not product.get('default_code'):
            update_vals['default_code'] = f"{prefix}{prod_id:04d}"
        
        # 2. Thuế khách hàng (nếu chưa có)
        if not product.get('taxes_id'):
            update_vals['taxes_id'] = [(6, 0, tax_8_id)]
        
        # 3. Chính sách xuất hóa đơn
        update_vals['invoice_policy'] = 'order'  # Số lượng đã đặt
        
        # 4. Mô tả bán hàng (nếu chưa có)
        if 'description_sale' not in product or not product.get('description_sale'):
            update_vals['description_sale'] = f"{product['name']} - Sản phẩm chất lượng cao"
        
        # 5. Ghi chú nội bộ
        if 'description' not in product or not product.get('description'):
            update_vals['description'] = f"Sản phẩm: {product['name']}"
        
        # Cập nhật nếu có thay đổi
        if update_vals:
            models.execute_kw(db, uid, password,
                'product.template', 'write',
                [[prod_id], update_vals])
            
            updated += 1
            if idx % 20 == 0:
                print(f"  {idx}/{len(product_ids)}: ✓ Đã cập nhật {updated} sản phẩm...")
        
    except Exception as e:
        errors += 1
        if errors <= 3:
            print(f"  ✗ Lỗi sản phẩm ID {prod_id}: {str(e)[:100]}")

print(f"\n{'='*60}")
print(f"✓ Hoàn thành!")
print(f"  - Đã cập nhật: {updated}")
print(f"  - Lỗi: {errors}")
print(f"{'='*60}")

