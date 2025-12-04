#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cài module Sale Quotation Builder để có chức năng Quotation Templates
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

# Các module cần thiết cho Quotation Templates
modules_to_install = [
    'sale_management',  # Quản lý bán hàng
    'sale_quotation_builder',  # Trình tạo báo giá (nếu có)
]

print("="*70)
print("📦 CÀI ĐẶT MODULE QUOTATION TEMPLATES")
print("="*70 + "\n")

for module_name in modules_to_install:
    try:
        # Tìm module
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[('name', '=', module_name)]], {'limit': 1})
        
        if module_ids:
            module = models.execute_kw(db, uid, password,
                'ir.module.module', 'read',
                [module_ids], {'fields': ['name', 'state', 'summary']})[0]
            
            if module['state'] == 'installed':
                print(f"  ✅ {module_name:<30} [Đã cài đặt]")
            else:
                print(f"  → Đang cài {module_name}...")
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'button_immediate_install', [module_ids])
                print(f"  ✅ {module_name:<30} [Đã kích hoạt cài đặt]")
        else:
            print(f"  ⚠️  {module_name:<30} [Không tìm thấy trong hệ thống]")
    except Exception as e:
        print(f"  ❌ {module_name}: {str(e)[:60]}")

print(f"\n{'='*70}")
print("✅ HOÀN THÀNH!")
print("="*70)
print("""
📍 SAU KHI CÀI XONG, VÀO PHẦN NÀY ĐỂ CHỈNH SỬA:

CÁCH 1 - QUA MENU BÁN HÀNG:
  1. Bán hàng → Cấu hình → Mẫu báo giá
  2. Click "Tạo mới" hoặc "Sửa" mẫu có sẵn
  3. Chỉnh sửa các trường và sản phẩm
  4. Lưu lại

CÁCH 2 - TẠO TỪ BÁO GIÁ CÓ SẴN:
  1. Bán hàng → Đơn hàng → Chọn báo giá
  2. Click ⚙️ Action → Lưu làm mẫu
  3. Mẫu sẽ được lưu để dùng lại

CÁCH 3 - QUA SETTINGS:
  1. Cài đặt → Bán hàng
  2. Tìm mục "Báo giá & Đơn hàng"
  3. Bật tùy chọn "Quotation Templates"
  4. Vào Cấu hình → Mẫu báo giá
""")

