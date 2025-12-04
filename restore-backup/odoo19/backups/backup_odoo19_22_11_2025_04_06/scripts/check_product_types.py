#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm tra và cập nhật type sản phẩm
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

# Kiểm tra 1 sản phẩm mẫu
product = models.execute_kw(db, uid, password,
    'product.template', 'search_read',
    [[('name', '=', 'Acetone')]], 
    {'fields': ['name', 'type', 'categ_id', 'default_code', 'list_price'], 'limit': 1})

if product:
    p = product[0]
    print("📦 Sản phẩm mẫu: Acetone")
    print(f"  • Type: {p['type']}")
    print(f"  • Danh mục: {p['categ_id'][1] if p['categ_id'] else 'N/A'}")
    print(f"  • Mã: {p['default_code']}")
    print(f"  • Giá: {p['list_price']}")
    print()

# Kiểm tra các type có sẵn
print("🔍 Checking product types in Odoo 19...")
print("Các type hợp lệ trong Odoo:")
print("  • 'consu' = Consumable (Tiêu dùng) - Không quản lý tồn kho")
print("  • 'service' = Service (Dịch vụ)")
print("  • 'product' = Storable Product (Hàng tồn kho) - CÓ quản lý tồn kho")
print()

# Thống kê type hiện tại
print("📊 Thống kê type sản phẩm hiện tại:")
all_products = models.execute_kw(db, uid, password,
    'product.template', 'search_read',
    [[]], {'fields': ['type']})

type_count = {}
for p in all_products:
    t = p['type']
    type_count[t] = type_count.get(t, 0) + 1

for t, count in type_count.items():
    print(f"  • {t}: {count} sản phẩm")

