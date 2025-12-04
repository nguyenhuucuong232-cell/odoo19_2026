#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cài đặt Kế toán Việt Nam và Quy chuẩn đo lường
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
# BƯỚC 1: CÀI MODULE KẾ TOÁN VIỆT NAM
# ========================================
print("\n" + "="*60)
print("BƯỚC 1: CÀI ĐẶT KẾ TOÁN VIỆT NAM")
print("="*60)

# Cập nhật danh sách module
print("\n  → Cập nhật danh sách module...")
try:
    models.execute_kw(db, uid, password, 'ir.module.module', 'update_list', [])
except:
    # Nếu lỗi, bỏ qua vì có thể module list đã được cập nhật
    pass

# Tìm module kế toán Việt Nam
vn_modules = [
    'l10n_vn',  # Vietnamese Localization
    'account',   # Accounting
    'account_invoicing',  # Invoicing
]

for module_name in vn_modules:
    try:
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[('name', '=', module_name)]], {'limit': 1})
        
        if module_ids:
            module = models.execute_kw(db, uid, password,
                'ir.module.module', 'read',
                [module_ids], {'fields': ['name', 'state']})[0]
            
            if module['state'] == 'installed':
                print(f"  ✓ {module_name}: Đã cài đặt")
            elif module['state'] == 'to install' or module['state'] == 'to upgrade':
                print(f"  ⏳ {module_name}: Đang chờ cài đặt...")
            else:
                print(f"  → Cài đặt {module_name}...")
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'button_immediate_install', [module_ids])
                print(f"  ✓ {module_name}: Đã kích hoạt cài đặt")
        else:
            print(f"  ⚠ {module_name}: Không tìm thấy trong hệ thống")
    except Exception as e:
        print(f"  ✗ Lỗi cài {module_name}: {str(e)[:100]}")

# ========================================
# BƯỚC 2: TẠO QUY CHUẨN ĐO LƯỜNG VIỆT NAM
# ========================================
print("\n" + "="*60)
print("BƯỚC 2: TẠO QUY CHUẨN ĐO LƯỜNG VIỆT NAM")
print("="*60)

# Lấy hoặc tạo UoM Categories
def get_or_create_uom_category(name):
    """Lấy hoặc tạo nhóm đơn vị đo"""
    cat_id = models.execute_kw(db, uid, password,
        'uom.category', 'search',
        [[('name', '=', name)]], {'limit': 1})
    
    if cat_id:
        return cat_id[0]
    
    return models.execute_kw(db, uid, password,
        'uom.category', 'create',
        [{'name': name}])

# Lấy hoặc tạo UoM
def get_or_create_uom(name, category_name, uom_type='reference', ratio=1.0, rounding=0.01):
    """Lấy hoặc tạo đơn vị đo"""
    # Kiểm tra tồn tại
    uom_id = models.execute_kw(db, uid, password,
        'uom.uom', 'search',
        [[('name', '=', name)]], {'limit': 1})
    
    if uom_id:
        print(f"  ✓ {name}: Đã tồn tại")
        return uom_id[0]
    
    # Lấy category
    cat_id = get_or_create_uom_category(category_name)
    
    # Tạo mới
    try:
        new_id = models.execute_kw(db, uid, password,
            'uom.uom', 'create',
            [{
                'name': name,
                'category_id': cat_id,
                'uom_type': uom_type,
                'ratio': ratio,
                'rounding': rounding,
            }])
        print(f"  ✓ {name}: Đã tạo mới")
        return new_id
    except Exception as e:
        print(f"  ✗ Lỗi tạo {name}: {str(e)[:100]}")
        return None

# NHÓM 1: ĐƠN VỊ KHỐI LƯỢNG
print("\n→ Nhóm: Khối lượng")
get_or_create_uom('Kilogram', 'Khối lượng', 'reference', 1.0)
get_or_create_uom('Gram', 'Khối lượng', 'smaller', 1000.0)
get_or_create_uom('Milligram', 'Khối lượng', 'smaller', 1000000.0)
get_or_create_uom('Tấn', 'Khối lượng', 'bigger', 0.001)
get_or_create_uom('Tạ', 'Khối lượng', 'bigger', 0.01)
get_or_create_uom('Yến', 'Khối lượng', 'smaller', 26.666667)  # 1kg = 26.67 yến

# NHÓM 2: ĐƠN VỊ THỂ TÍCH
print("\n→ Nhóm: Thể tích")
get_or_create_uom('Lít', 'Thể tích', 'reference', 1.0)
get_or_create_uom('Mililít', 'Thể tích', 'smaller', 1000.0)
get_or_create_uom('mL', 'Thể tích', 'smaller', 1000.0)
get_or_create_uom('m³', 'Thể tích', 'bigger', 0.001)

# NHÓM 3: ĐƠN VỊ CHIỀU DÀI
print("\n→ Nhóm: Chiều dài")
get_or_create_uom('Mét', 'Chiều dài', 'reference', 1.0)
get_or_create_uom('Centimet', 'Chiều dài', 'smaller', 100.0)
get_or_create_uom('Milimét', 'Chiều dài', 'smaller', 1000.0)
get_or_create_uom('Kilomét', 'Chiều dài', 'bigger', 0.001)

# NHÓM 4: ĐƠN VỊ DIỆN TÍCH
print("\n→ Nhóm: Diện tích")
get_or_create_uom('m²', 'Diện tích', 'reference', 1.0)
get_or_create_uom('cm²', 'Diện tích', 'smaller', 10000.0)
get_or_create_uom('km²', 'Diện tích', 'bigger', 0.000001)
get_or_create_uom('Hecta', 'Diện tích', 'bigger', 0.0001)
get_or_create_uom('Sào', 'Diện tích', 'bigger', 0.28)  # 1 sào = ~360m²

# NHÓM 5: ĐƠN VỊ PHÂN TÍCH MÔI TRƯỜNG
print("\n→ Nhóm: Phân tích môi trường")
get_or_create_uom('Chỉ tiêu', 'Dịch vụ', 'reference', 1.0)
get_or_create_uom('Mẫu', 'Dịch vụ', 'reference', 1.0)
get_or_create_uom('Lần', 'Dịch vụ', 'reference', 1.0)
get_or_create_uom('Điểm', 'Dịch vụ', 'reference', 1.0)

# NHÓM 6: ĐƠN VỊ THIẾT BỊ
print("\n→ Nhóm: Thiết bị & Vật tư")
get_or_create_uom('Cái', 'Đơn vị', 'reference', 1.0)
get_or_create_uom('Chiếc', 'Đơn vị', 'reference', 1.0)
get_or_create_uom('Bộ', 'Đơn vị', 'reference', 1.0)
get_or_create_uom('Hộp', 'Đơn vị', 'reference', 1.0)
get_or_create_uom('Chai', 'Đơn vị', 'reference', 1.0)
get_or_create_uom('Lọ', 'Đơn vị', 'reference', 1.0)
get_or_create_uom('Bình', 'Đơn vị', 'reference', 1.0)

# NHÓM 7: ĐƠN VỊ THỜI GIAN
print("\n→ Nhóm: Thời gian")
get_or_create_uom('Giờ', 'Thời gian', 'reference', 1.0)
get_or_create_uom('Ngày', 'Thời gian', 'bigger', 0.041667)  # 1 ngày = 24h
get_or_create_uom('Tuần', 'Thời gian', 'bigger', 0.005952)  # 1 tuần = 168h
get_or_create_uom('Tháng', 'Thời gian', 'bigger', 0.001389)  # 1 tháng = 720h

# ========================================
# BƯỚC 3: CẤU HÌNH THUẾ VIỆT NAM
# ========================================
print("\n" + "="*60)
print("BƯỚC 3: CẤU HÌNH THUẾ GTGT VIỆT NAM")
print("="*60)

vietnam_taxes = [
    {'name': 'Thuế GTGT 0%', 'amount': 0.0, 'type': 'sale'},
    {'name': 'Thuế GTGT 5%', 'amount': 5.0, 'type': 'sale'},
    {'name': 'Thuế GTGT 8%', 'amount': 8.0, 'type': 'sale'},
    {'name': 'Thuế GTGT 10%', 'amount': 10.0, 'type': 'sale'},
    {'name': 'Thuế GTGT mua 10%', 'amount': 10.0, 'type': 'purchase'},
    {'name': 'Thuế GTGT mua 8%', 'amount': 8.0, 'type': 'purchase'},
]

for tax_data in vietnam_taxes:
    try:
        # Kiểm tra tồn tại
        existing = models.execute_kw(db, uid, password,
            'account.tax', 'search',
            [[('name', '=', tax_data['name']), ('type_tax_use', '=', tax_data['type'])]], 
            {'limit': 1})
        
        if existing:
            print(f"  ✓ {tax_data['name']}: Đã tồn tại")
        else:
            # Tạo mới
            models.execute_kw(db, uid, password,
                'account.tax', 'create',
                [{
                    'name': tax_data['name'],
                    'amount': tax_data['amount'],
                    'amount_type': 'percent',
                    'type_tax_use': tax_data['type'],
                }])
            print(f"  ✓ {tax_data['name']}: Đã tạo mới")
    except Exception as e:
        print(f"  ✗ Lỗi tạo {tax_data['name']}: {str(e)[:100]}")

# ========================================
# BƯỚC 4: CẬP NHẬT THÔNG TIN CÔNG TY
# ========================================
print("\n" + "="*60)
print("BƯỚC 4: CẬP NHẬT THÔNG TIN CÔNG TY")
print("="*60)

try:
    # Lấy công ty chính
    company_ids = models.execute_kw(db, uid, password,
        'res.company', 'search', [[]], {'limit': 1})
    
    if company_ids:
        # Cập nhật tiền tệ VND
        vnd_currency = models.execute_kw(db, uid, password,
            'res.currency', 'search',
            [[('name', '=', 'VND')]], {'limit': 1})
        
        if vnd_currency:
            models.execute_kw(db, uid, password,
                'res.company', 'write',
                [company_ids, {
                    'currency_id': vnd_currency[0],
                    'country_id': models.execute_kw(db, uid, password,
                        'res.country', 'search',
                        [[('code', '=', 'VN')]], {'limit': 1})[0] if models.execute_kw(db, uid, password,
                        'res.country', 'search',
                        [[('code', '=', 'VN')]], {'limit': 1}) else False,
                }])
            print("  ✓ Đã cập nhật tiền tệ VND cho công ty")
        else:
            print("  ⚠ Không tìm thấy tiền tệ VND")
except Exception as e:
    print(f"  ✗ Lỗi cập nhật công ty: {str(e)[:100]}")

print("\n" + "="*60)
print("✓ HOÀN THÀNH CÀI ĐẶT!")
print("="*60)
print("""
Đã cài đặt:
  ✓ Kế toán Việt Nam (l10n_vn)
  ✓ Thuế GTGT (0%, 5%, 8%, 10%)
  ✓ Đơn vị đo lường Việt Nam (kg, tấn, tạ, lít, m², sào...)
  ✓ Đơn vị phân tích môi trường (Chỉ tiêu, Mẫu, Lần...)
  ✓ Tiền tệ VND

Khởi động lại Odoo để áp dụng đầy đủ các thay đổi:
  docker compose restart odoo19
""")

