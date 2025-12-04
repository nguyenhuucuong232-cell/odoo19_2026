#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo các mẫu báo giá (Quotation Templates) cho SGC
"""
import xmlrpc.client

url = 'http://localhost:10019'
db = 'odoo19'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print(f"✓ Kết nối Odoo thành công (User ID: {uid})\n")

# ========================================
# LẤY SẢN PHẨM
# ========================================
print("="*70)
print("📦 Chuẩn bị dữ liệu sản phẩm")
print("="*70 + "\n")

# Lấy các sản phẩm dịch vụ môi trường
products_dict = {}
search_patterns = {
    'Vi khí hậu': 'vi khí hậu',
    'Ánh sáng': 'ánh sáng',
    'Tiếng ồn': 'tiếng ồn',
    'Bụi': 'bụi',
    'CO': 'CO',
    'CO2': 'CO2',
    'NO2': 'NO2',
    'SO2': 'SO2',
    'HC mạch thẳng': 'HC',
    'Xylene': 'xylene',
}

for key, pattern in search_patterns.items():
    prods = models.execute_kw(db, uid, password,
        'product.product', 'search_read',
        [[('name', 'ilike', pattern), ('type', '=', 'service')]], 
        {'fields': ['id', 'name', 'list_price'], 'limit': 1})
    if prods:
        products_dict[key] = prods[0]
        print(f"  ✓ {key}: {prods[0]['name']}")

print(f"\n✓ Đã chuẩn bị {len(products_dict)} loại sản phẩm\n")

# ========================================
# TẠO CÁC MẪU BÁO GIÁ
# ========================================
print("="*70)
print("📋 TẠO CÁC MẪU BÁO GIÁ (QUOTATION TEMPLATES)")
print("="*70 + "\n")

quotation_templates = [
    {
        'name': 'BÁO QUAN TRẮC MÔI TRƯỜNG LAO ĐỘNG NĂM',
        'note': 'Mẫu chuẩn cho quan trắc môi trường lao động định kỳ theo QCVN 09:2015/BYT',
        'products': [
            {'key': 'Vi khí hậu', 'qty': 48, 'price': 25000},
            {'key': 'Ánh sáng', 'qty': 48, 'price': 10000},
            {'key': 'Tiếng ồn', 'qty': 48, 'price': 50000},
            {'key': 'Bụi', 'qty': 48, 'price': 50000},
            {'key': 'CO', 'qty': 20, 'price': 60000},
            {'key': 'CO2', 'qty': 26, 'price': 60000},
            {'key': 'NO2', 'qty': 20, 'price': 60000},
            {'key': 'SO2', 'qty': 21, 'price': 60000},
        ],
    },
    {
        'name': 'BG QTMTLD + QTMT',
        'note': 'Gói kết hợp Quan trắc Môi trường Lao động + Môi trường',
        'products': [
            {'key': 'Tiếng ồn', 'qty': 12, 'price': 50000},
            {'key': 'Bụi', 'qty': 12, 'price': 50000},
            {'key': 'Vi khí hậu', 'qty': 12, 'price': 25000},
        ],
    },
    {
        'name': 'BG Lập hồ sơ Đánh giá tác động môi trường',
        'note': 'Dịch vụ lập hồ sơ ĐTM cho các dự án đầu tư theo Nghị định 08/2022/NĐ-CP',
        'products': [
            {'key': 'Vi khí hậu', 'qty': 4, 'price': 100000},
        ],
    },
    {
        'name': 'BG QUAN TRẮC MÔI TRƯỜNG NĂM 2025 (KK, NT, KT, ĐT)',
        'note': 'Gói toàn diện: Không khí, Nước thải, Khí thải, Đất',
        'products': [
            {'key': 'CO', 'qty': 12, 'price': 60000},
            {'key': 'SO2', 'qty': 12, 'price': 60000},
            {'key': 'NO2', 'qty': 12, 'price': 60000},
            {'key': 'Bụi', 'qty': 12, 'price': 50000},
        ],
    },
    {
        'name': 'BG QUAN TRẮC MÔI TRƯỜNG NĂM 2025',
        'note': 'Gói cơ bản quan trắc định kỳ năm 2025',
        'products': [
            {'key': 'Bụi', 'qty': 12, 'price': 50000},
            {'key': 'CO', 'qty': 4, 'price': 60000},
        ],
    },
    {
        'name': 'BG - ĐÁNH GIÁ MÔI TRƯỜNG',
        'note': 'Dịch vụ đánh giá hiện trạng môi trường',
        'products': [
            {'key': 'Bụi', 'qty': 6, 'price': 50000},
        ],
    },
    {
        'name': 'HUẤN LUYỆN ATLD KI ĐẦU ĐINH',
        'note': 'Đào tạo an toàn lao động và kiểm định thiết bị',
        'products': [
            {'key': 'Vi khí hậu', 'qty': 1, 'price': 5000000},
        ],
    },
    {
        'name': 'BG QUAN TRẮC MÔI TRƯỜNG NĂM 2025 (KT, NT)',
        'note': 'Gói quan trắc Khí thải + Nước thải',
        'products': [
            {'key': 'CO', 'qty': 12, 'price': 60000},
            {'key': 'Bụi', 'qty': 12, 'price': 50000},
        ],
    },
    {
        'name': 'Giám Sát Hiệu Ứng Nhà Kính 2025-PA2',
        'note': 'Quan trắc khí nhà kính (CO2, CH4, N2O)',
        'products': [
            {'key': 'CO2', 'qty': 4, 'price': 100000},
        ],
    },
    {
        'name': 'BG Phân loại lao động',
        'note': 'Dịch vụ đánh giá phân loại lao động theo Luật An toàn lao động',
        'products': [
            {'key': 'Tiếng ồn', 'qty': 10, 'price': 50000},
            {'key': 'Bụi', 'qty': 10, 'price': 50000},
        ],
    },
    {
        'name': 'GIẤY PHÉP MÔI TRƯỜNG',
        'note': 'Dịch vụ tư vấn xin giấy phép môi trường',
        'products': [
            {'key': 'Vi khí hậu', 'qty': 1, 'price': 20000000},
        ],
    },
    {
        'name': 'HÀNG HÓA',
        'note': 'Cung cấp hóa chất và thiết bị phân tích',
        'products': [
            {'key': 'Bụi', 'qty': 10, 'price': 100000},
        ],
    },
    {
        'name': 'Lập báo cáo Kiểm kê khí thải nhà kính',
        'note': 'Dịch vụ kiểm kê GHG theo ISO 14064',
        'products': [
            {'key': 'CO2', 'qty': 1, 'price': 50000000},
        ],
    },
    {
        'name': 'Lập kế hoạch giảm thải KNK-theo NĐ 06',
        'note': 'Tư vấn lập kế hoạch giảm phát thải khí nhà kính',
        'products': [
            {'key': 'CO2', 'qty': 1, 'price': 30000000},
        ],
    },
    {
        'name': 'KẾ HOẠCH GIẢM THẢI KNK',
        'note': 'Kế hoạch giảm phát thải khí nhà kính cho doanh nghiệp',
        'products': [
            {'key': 'CO2', 'qty': 1, 'price': 25000000},
        ],
    },
    {
        'name': 'TƯ VẤN ISO',
        'note': 'Tư vấn và chứng nhận ISO 14001, 45001',
        'products': [
            {'key': 'Vi khí hậu', 'qty': 1, 'price': 40000000},
        ],
    },
]

created = 0
errors = 0

for idx, template in enumerate(quotation_templates, 1):
    try:
        # Kiểm tra tồn tại
        existing = models.execute_kw(db, uid, password,
            'sale.order', 'search',
            [[('name', '=', template['name']), ('state', '=', 'draft')]], 
            {'limit': 1})
        
        if existing:
            print(f"  {idx:2d}. ⊘ {template['name'][:50]:<50} [Đã tồn tại]")
            continue
        
        # Tạo quotation template (draft sale order)
        so_data = {
            'partner_id': 1,  # Default partner
            'state': 'draft',
            'note': template['note'],
        }
        
        so_id = models.execute_kw(db, uid, password,
            'sale.order', 'create', [so_data])
        
        # Thêm sản phẩm
        order_lines = []
        
        # Section header
        order_lines.append((0, 0, {
            'display_type': 'line_section',
            'name': template['name'],
        }))
        
        # Products
        for prod_info in template['products']:
            if prod_info['key'] in products_dict:
                product = products_dict[prod_info['key']]
                order_lines.append((0, 0, {
                    'product_id': product['id'],
                    'product_uom_qty': prod_info['qty'],
                    'price_unit': prod_info.get('price', product['list_price']),
                }))
        
        # Update
        models.execute_kw(db, uid, password,
            'sale.order', 'write',
            [[so_id], {'order_line': order_lines}])
        
        # Rename
        models.execute_kw(db, uid, password,
            'sale.order', 'write',
            [[so_id], {'name': template['name']}])
        
        created += 1
        print(f"  {idx:2d}. ✅ {template['name'][:50]:<50} [Đã tạo]")
        
    except Exception as e:
        errors += 1
        print(f"  {idx:2d}. ❌ {template['name'][:50]:<50} [Lỗi: {str(e)[:30]}]")

print(f"\n{'='*70}")
print(f"✅ HOÀN THÀNH!")
print(f"  • Đã tạo mới: {created}")
print(f"  • Lỗi: {errors}")
print(f"{'='*70}")

print("""
📋 Các mẫu báo giá đã tạo:
  1. BÁO QUAN TRẮC MÔI TRƯỜNG LAO ĐỘNG NĂM
  2. BG QTMTLD + QTMT
  3. BG Lập hồ sơ Đánh giá tác động môi trường
  4. BG QUAN TRẮC MÔI TRƯỜNG NĂM 2025 (KK, NT, KT, ĐT)
  5. BG QUAN TRẮC MÔI TRƯỜNG NĂM 2025
  6. BG - ĐÁNH GIÁ MÔI TRƯỜNG
  7. HUẤN LUYỆN ATLD KI ĐẦU ĐINH
  8. BG QUAN TRẮC MÔI TRƯỜNG NĂM 2025 (KT, NT)
  9. Giám Sát Hiệu Ứng Nhà Kính 2025-PA2
 10. BG Phân loại lao động
 11. GIẤY PHÉP MÔI TRƯỜNG
 12. HÀNG HÓA
 13. Lập báo cáo Kiểm kê khí thải nhà kính
 14. Lập kế hoạch giảm thải KNK-theo NĐ 06
 15. KẾ HOẠCH GIẢM THẢI KNK
 16. TƯ VẤN ISO

📍 Xem trong Odoo:
  → Sales → Orders
  → Lọc theo trạng thái "Quotation"
  → Sử dụng làm template khi tạo báo giá mới
""")

