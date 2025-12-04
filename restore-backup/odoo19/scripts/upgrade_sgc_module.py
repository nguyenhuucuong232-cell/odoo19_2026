#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upgrade module sgc_management_core
"""
import xmlrpc.client
import time

url = 'http://localhost:10019'
db = 'odoo19'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print(f"✓ Kết nối Odoo thành công (User ID: {uid})\n")

# Tìm module sgc_management_core
module_ids = models.execute_kw(db, uid, password,
    'ir.module.module', 'search',
    [[('name', '=', 'sgc_management_core')]], {'limit': 1})

if not module_ids:
    print("❌ Không tìm thấy module sgc_management_core")
    print("→ Cần cài đặt module trước!")
    exit(1)

module = models.execute_kw(db, uid, password,
    'ir.module.module', 'read',
    [module_ids], {'fields': ['name', 'state']})[0]

print(f"📦 Module: {module['name']}")
print(f"📊 Trạng thái: {module['state']}")

if module['state'] == 'installed':
    print("\n→ Upgrade module...")
    try:
        models.execute_kw(db, uid, password,
            'ir.module.module', 'button_immediate_upgrade', [module_ids])
        print("✅ Đã kích hoạt upgrade!")
        print("⏳ Đợi Odoo xử lý... (30 giây)")
        time.sleep(30)
        print("✓ Hoàn thành!")
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        
elif module['state'] == 'uninstalled':
    print("\n→ Cài đặt module...")
    try:
        models.execute_kw(db, uid, password,
            'ir.module.module', 'button_immediate_install', [module_ids])
        print("✅ Đã kích hoạt cài đặt!")
        print("⏳ Đợi Odoo xử lý... (60 giây)")
        time.sleep(60)
        print("✓ Hoàn thành!")
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
else:
    print(f"⚠️ Module đang ở trạng thái: {module['state']}")
    print("→ Vui lòng kiểm tra trong Apps")

print(f"""
{"="*70}
📝 HƯỚNG DẪN KIỂM TRA BÁO GIÁ:
{"="*70}

1. Mở trình duyệt: http://localhost:10019
2. Đăng nhập: admin / admin
3. Vào: Sales → Orders
4. Mở báo giá: S00002
5. Click nút "Print" → chọn "Báo giá SGC"
6. PDF sẽ hiển thị với header/footer đẹp!

Nếu không thấy "Báo giá SGC" trong menu Print:
→ Vào Apps → tìm "SGC Management Core" → click Upgrade
""")

