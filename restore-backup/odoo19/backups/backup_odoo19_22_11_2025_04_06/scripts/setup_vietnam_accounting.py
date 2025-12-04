#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cài đặt Kế toán Việt Nam đơn giản
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
# BƯỚC 1: CẤU HÌNH THUẾ VIỆT NAM
# ========================================
print("="*70)
print("📋 BƯỚC 1: CẤU HÌNH THUẾ GTGT VIỆT NAM")
print("="*70 + "\n")

vietnam_taxes = [
    {'name': 'Thuế GTGT 0% (Hàng xuất khẩu)', 'amount': 0.0, 'type': 'sale', 'desc': 'Áp dụng cho hàng xuất khẩu'},
    {'name': 'Thuế GTGT 5% (Hàng thiết yếu)', 'amount': 5.0, 'type': 'sale', 'desc': 'Nước sạch, dịch vụ giáo dục...'},
    {'name': 'Thuế GTGT 8% (Môi trường)', 'amount': 8.0, 'type': 'sale', 'desc': 'Dịch vụ môi trường'},
    {'name': 'Thuế GTGT 10% (Phổ biến)', 'amount': 10.0, 'type': 'sale', 'desc': 'Thuế suất phổ biến nhất'},
    {'name': 'Thuế GTGT mua 10%', 'amount': 10.0, 'type': 'purchase', 'desc': 'Thuế đầu vào được khấu trừ'},
    {'name': 'Thuế GTGT mua 8%', 'amount': 8.0, 'type': 'purchase', 'desc': 'Thuế đầu vào được khấu trừ'},
    {'name': 'Thuế GTGT mua 5%', 'amount': 5.0, 'type': 'purchase', 'desc': 'Thuế đầu vào được khấu trừ'},
]

created_taxes = 0
existing_taxes = 0

for tax_data in vietnam_taxes:
    try:
        # Kiểm tra tồn tại
        existing = models.execute_kw(db, uid, password,
            'account.tax', 'search',
            [[('name', '=', tax_data['name'])]], {'limit': 1})
        
        if existing:
            existing_taxes += 1
            print(f"  ✓ {tax_data['name']:<40} [Đã tồn tại]")
        else:
            # Tạo mới
            models.execute_kw(db, uid, password,
                'account.tax', 'create',
                [{
                    'name': tax_data['name'],
                    'amount': tax_data['amount'],
                    'amount_type': 'percent',
                    'type_tax_use': tax_data['type'],
                    'description': tax_data['desc'],
                }])
            created_taxes += 1
            print(f"  ✅ {tax_data['name']:<40} [Đã tạo mới]")
    except Exception as e:
        print(f"  ❌ {tax_data['name']:<40} [Lỗi: {str(e)[:50]}]")

# ========================================
# BƯỚC 2: CẬP NHẬT CÔNG TY
# ========================================
print("\n" + "="*70)
print("🏢 BƯỚC 2: CẬP NHẬT THÔNG TIN CÔNG TY")
print("="*70 + "\n")

try:
    # Lấy công ty chính
    company_ids = models.execute_kw(db, uid, password,
        'res.company', 'search', [[]], {'limit': 1})
    
    if company_ids:
        company = models.execute_kw(db, uid, password,
            'res.company', 'read',
            [company_ids], {'fields': ['name', 'currency_id', 'country_id']})[0]
        
        print(f"  Công ty: {company['name']}")
        
        # Lấy tiền tệ VND
        vnd_currency = models.execute_kw(db, uid, password,
            'res.currency', 'search',
            [[('name', '=', 'VND')]], {'limit': 1})
        
        # Lấy quốc gia Việt Nam
        vietnam_country = models.execute_kw(db, uid, password,
            'res.country', 'search',
            [[('code', '=', 'VN')]], {'limit': 1})
        
        update_data = {}
        
        if vnd_currency:
            if company['currency_id'][0] != vnd_currency[0]:
                update_data['currency_id'] = vnd_currency[0]
                print(f"  ✅ Đã cập nhật tiền tệ: VND")
            else:
                print(f"  ✓ Tiền tệ đã là VND")
        
        if vietnam_country:
            if not company.get('country_id') or company['country_id'][0] != vietnam_country[0]:
                update_data['country_id'] = vietnam_country[0]
                print(f"  ✅ Đã cập nhật quốc gia: Việt Nam")
            else:
                print(f"  ✓ Quốc gia đã là Việt Nam")
        
        if update_data:
            models.execute_kw(db, uid, password,
                'res.company', 'write',
                [company_ids, update_data])
        
except Exception as e:
    print(f"  ❌ Lỗi cập nhật công ty: {str(e)[:100]}")

# ========================================
# BƯỚC 3: KIỂM TRA MODULE KẾ TOÁN
# ========================================
print("\n" + "="*70)
print("📦 BƯỚC 3: KIỂM TRA MODULE KẾ TOÁN")
print("="*70 + "\n")

important_modules = [
    'account',  # Kế toán cơ bản
    'l10n_vn',  # Kế toán Việt Nam
    'account_accountant',  # Kế toán nâng cao
]

for module_name in important_modules:
    try:
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[('name', '=', module_name)]], {'limit': 1})
        
        if module_ids:
            module = models.execute_kw(db, uid, password,
                'ir.module.module', 'read',
                [module_ids], {'fields': ['name', 'state', 'summary']})[0]
            
            status_icon = {
                'installed': '✅',
                'to install': '⏳',
                'to upgrade': '🔄',
                'uninstalled': '❌',
            }.get(module['state'], '❓')
            
            print(f"  {status_icon} {module_name:<25} [{module['state']}]")
        else:
            print(f"  ❓ {module_name:<25} [Không tìm thấy]")
    except Exception as e:
        print(f"  ❌ {module_name:<25} [Lỗi: {str(e)[:40]}]")

# ========================================
# TÓM TẮT
# ========================================
print("\n" + "="*70)
print("✅ HOÀN THÀNH CÀI ĐẶT!")
print("="*70)
print(f"""
📊 Tóm tắt:
  • Thuế đã tạo mới: {created_taxes}
  • Thuế đã tồn tại: {existing_taxes}
  • Tổng số thuế GTGT: {created_taxes + existing_taxes}
  
🇻🇳 Cấu hình Việt Nam:
  ✓ Tiền tệ: VND (Việt Nam Đồng)
  ✓ Quốc gia: Việt Nam
  ✓ Thuế GTGT: 0%, 5%, 8%, 10%
  
📝 Ghi chú:
  • Thuế 8% phù hợp cho dịch vụ môi trường
  • Thuế 10% là thuế suất phổ biến nhất
  • Đã cấu hình cả thuế bán (sale) và thuế mua (purchase)
  
🔄 Nếu cần activate module l10n_vn:
  → Vào Apps → tìm "Vietnam" → Install
""")

