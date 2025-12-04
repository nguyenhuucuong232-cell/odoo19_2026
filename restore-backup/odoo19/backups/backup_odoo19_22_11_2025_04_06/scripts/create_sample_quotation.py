#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo báo giá mẫu cho SGC
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

# Lấy khách hàng đầu tiên (SAWACO - Cấp nước)
customer = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[('name', 'ilike', 'CẤP NƯỚC')]], 
    {'fields': ['id', 'name'], 'limit': 1})

if not customer:
    print("❌ Không tìm thấy khách hàng. Lấy khách hàng bất kỳ...")
    customer = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[('customer_rank', '>', 0)]], 
        {'fields': ['id', 'name'], 'limit': 1})

customer_id = customer[0]['id']
print(f"✓ Khách hàng: {customer[0]['name']}")

# Lấy một số sản phẩm quan trắc môi trường lao động
products_mtld = []
search_terms = ['Vi khí hậu', 'Ánh sáng', 'Tiếng ồn', 'Bụi', 'CO', 'CO2', 'NO2', 'SO2']

for term in search_terms:
    product = models.execute_kw(db, uid, password,
        'product.product', 'search_read',
        [[('name', 'ilike', term)]], 
        {'fields': ['id', 'name', 'list_price'], 'limit': 1})
    if product:
        products_mtld.append(product[0])

print(f"✓ Tìm thấy {len(products_mtld)} sản phẩm")

# Tạo báo giá
quotation_data = {
    'partner_id': customer_id,
    'date_order': '2025-11-21',
    'validity_date': '2025-12-21',
}

quotation_id = models.execute_kw(db, uid, password,
    'sale.order', 'create', [quotation_data])

print(f"✓ Đã tạo báo giá ID: {quotation_id}")

# Thêm các dòng sản phẩm
order_lines = []

# Section header
order_lines.append((0, 0, {
    'display_type': 'line_section',
    'name': 'I. CÁC CHỈ TIÊU QUAN TRẮC MÔI TRƯỜNG LAO ĐỘNG',
}))

# Thêm sản phẩm
for idx, product in enumerate(products_mtld, 1):
    order_lines.append((0, 0, {
        'product_id': product['id'],
        'product_uom_qty': 48 if idx <= 4 else 20,  # 48 chỉ tiêu cho các dòng đầu
        'price_unit': product['list_price'] if product['list_price'] > 0 else 50000,
    }))

# Note
order_lines.append((0, 0, {
    'display_type': 'line_note',
    'name': 'Ghi chú: Muốn chắn nhận trong mười một nghiệp bất toàn động',
}))

# Update báo giá với order lines
models.execute_kw(db, uid, password,
    'sale.order', 'write',
    [[quotation_id], {'order_line': order_lines}])

print(f"✓ Đã thêm {len(products_mtld)} sản phẩm vào báo giá")

# Lấy thông tin báo giá
quotation = models.execute_kw(db, uid, password,
    'sale.order', 'read',
    [[quotation_id]], {'fields': ['name', 'amount_total']})[0]

print(f"""
{"="*70}
✅ HOÀN THÀNH TẠO BÁO GIÁ MẪU!
{"="*70}

📄 Thông tin báo giá:
  • Số báo giá: {quotation['name']}
  • Khách hàng: {customer[0]['name']}
  • Tổng tiền: {quotation['amount_total']:,.0f} VND
  • Số sản phẩm: {len(products_mtld)}

📍 Xem báo giá:
  → Vào Sales → Orders → mở báo giá {quotation['name']}
  → Click "Print" → chọn "Báo giá SGC"
  
🎨 Template đã bao gồm:
  ✓ Header: Logo SGC + thông tin công ty
  ✓ Bảng chi tiết với màu sắc chuyên nghiệp
  ✓ Footer: Thông tin người làm báo giá
  ✓ Ghi chú và điều kiện thanh toán
""")

