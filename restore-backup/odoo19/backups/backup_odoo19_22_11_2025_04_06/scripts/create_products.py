#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo 100 sản phẩm quan trắc môi trường cho SGC
Chạy: docker compose exec odoo19 python3 /mnt/extra-addons/scripts/create_products.py
"""

import xmlrpc.client

# Cấu hình kết nối
url = 'http://localhost:10019'
db = 'odoo19'
username = 'admin'
password = 'admin'

# Kết nối
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

print(f"Connected to Odoo as user ID: {uid}")

# ========================================
# BƯỚC 1: TẠO DANH MỤC SẢN PHẨM
# ========================================
print("\n=== BƯỚC 1: Tạo Danh mục Sản phẩm ===")

categories = [
    {
        'name': 'Dịch vụ Môi trường',
        'parent_id': False,
        'property_cost_method': 'standard',
    },
    {
        'name': 'Quan trắc Môi trường',
        'parent': 'Dịch vụ Môi trường',
        'property_cost_method': 'standard',
    },
    {
        'name': 'Quan trắc Môi trường Lao động',
        'parent': 'Dịch vụ Môi trường',
        'property_cost_method': 'standard',
    },
    {
        'name': 'Giấy phép Môi trường',
        'parent': 'Dịch vụ Môi trường',
        'property_cost_method': 'standard',
    },
]

category_ids = {}
for cat in categories:
    parent_name = cat.pop('parent', None)
    parent_id = category_ids.get(parent_name, False)
    
    # Kiểm tra tồn tại
    existing = models.execute_kw(db, uid, password,
        'product.category', 'search',
        [[('name', '=', cat['name'])]])
    
    if existing:
        cat_id = existing[0]
        print(f"  ✓ Danh mục '{cat['name']}' đã tồn tại (ID: {cat_id})")
    else:
        if parent_id:
            cat['parent_id'] = parent_id
        cat_id = models.execute_kw(db, uid, password,
            'product.category', 'create', [cat])
        print(f"  ✓ Tạo danh mục '{cat['name']}' (ID: {cat_id})")
    
    category_ids[cat['name']] = cat_id

# ========================================
# BƯỚC 2: TẠO THUỘC TÍNH & GIÁ TRỊ (cho biến thể)
# ========================================
print("\n=== BƯỚC 2: Tạo Thuộc tính cho Biến thể ===")

attributes_data = {
    'Số lần lấy mẫu': ['1 lần', '2 lần', '3 lần', '4 lần', '6 lần', '12 lần'],
    'Loại mẫu': ['Không khí', 'Nước thải', 'Nước mặt', 'Đất', 'Tiếng ồn'],
    'Phạm vi': ['Cơ bản', 'Mở rộng', 'Toàn diện'],
}

attribute_ids = {}
for attr_name, values in attributes_data.items():
    # Kiểm tra attribute
    existing_attr = models.execute_kw(db, uid, password,
        'product.attribute', 'search',
        [[('name', '=', attr_name)]])
    
    if existing_attr:
        attr_id = existing_attr[0]
        print(f"  ✓ Thuộc tính '{attr_name}' đã tồn tại (ID: {attr_id})")
    else:
        attr_id = models.execute_kw(db, uid, password,
            'product.attribute', 'create',
            [{'name': attr_name, 'create_variant': 'always'}])
        print(f"  ✓ Tạo thuộc tính '{attr_name}' (ID: {attr_id})")
    
    attribute_ids[attr_name] = attr_id
    
    # Tạo các giá trị
    for value_name in values:
        existing_val = models.execute_kw(db, uid, password,
            'product.attribute.value', 'search',
            [[('attribute_id', '=', attr_id), ('name', '=', value_name)]])
        
        if not existing_val:
            models.execute_kw(db, uid, password,
                'product.attribute.value', 'create',
                [{'attribute_id': attr_id, 'name': value_name}])
            print(f"    + Giá trị '{value_name}'")

# ========================================
# BƯỚC 3: TẠO 100 SẢN PHẨM
# ========================================
print("\n=== BƯỚC 3: Tạo 100 Sản phẩm ===")

# Dữ liệu sản phẩm Quan trắc Môi trường
products_qtmt = [
    {
        'name': 'Quan trắc Không khí',
        'description': 'Dịch vụ quan trắc chất lượng không khí xung quanh',
        'base_price': 5000000,
        'parameters': ['Bụi TSP', 'CO', 'SO2', 'NO2', 'Pb trong bụi'],
    },
    {
        'name': 'Quan trắc Nước thải',
        'description': 'Quan trắc chất lượng nước thải công nghiệp và sinh hoạt',
        'base_price': 4500000,
        'parameters': ['pH', 'BOD5', 'COD', 'TSS', 'Coliform', 'Dầu mỡ'],
    },
    {
        'name': 'Quan trắc Nước mặt',
        'description': 'Quan trắc chất lượng nước sông, hồ, ao',
        'base_price': 4000000,
        'parameters': ['pH', 'DO', 'BOD5', 'COD', 'Amoni', 'Phosphat'],
    },
    {
        'name': 'Quan trắc Nước dưới đất',
        'description': 'Quan trắc chất lượng nước ngầm',
        'base_price': 3500000,
        'parameters': ['pH', 'TDS', 'Độ cứng', 'Clorua', 'Nitrat', 'Asen'],
    },
    {
        'name': 'Quan trắc Đất',
        'description': 'Phân tích chất lượng đất nông nghiệp và công nghiệp',
        'base_price': 6000000,
        'parameters': ['pH', 'As', 'Pb', 'Cd', 'Cu', 'Zn', 'Hg'],
    },
    {
        'name': 'Đo Tiếng ồn',
        'description': 'Đo độ ồn môi trường xung quanh',
        'base_price': 2000000,
        'parameters': ['Leq', 'Lmax', 'Lmin'],
    },
    {
        'name': 'Đo Độ rung',
        'description': 'Đo độ rung môi trường',
        'base_price': 2500000,
        'parameters': ['Vận tốc rung', 'Gia tốc rung', 'Tần số'],
    },
    {
        'name': 'Quan trắc Khí thải',
        'description': 'Quan trắc khí thải từ ống khói, lò đốt',
        'base_price': 7000000,
        'parameters': ['Bụi', 'SO2', 'NOx', 'CO', 'HCl', 'Dioxin'],
    },
    {
        'name': 'Phân tích Kim loại nặng',
        'description': 'Phân tích kim loại nặng trong nước/đất/không khí',
        'base_price': 5500000,
        'parameters': ['As', 'Pb', 'Cd', 'Hg', 'Cr', 'Ni'],
    },
    {
        'name': 'Phân tích Vi sinh',
        'description': 'Phân tích vi sinh vật trong nước và thực phẩm',
        'base_price': 3000000,
        'parameters': ['Tổng số vi khuẩn', 'Coliform', 'E.coli', 'Salmonella'],
    },
]

# Dữ liệu sản phẩm Môi trường Lao động
products_mtld = [
    {
        'name': 'MTLĐ - Đo Bụi',
        'description': 'Đo nồng độ bụi tại nơi làm việc',
        'base_price': 1500000,
        'parameters': ['Bụi hít vào', 'Bụi hô hấp', 'Bụi tổng số'],
    },
    {
        'name': 'MTLĐ - Đo Khí độc',
        'description': 'Đo nồng độ khí độc tại nơi làm việc',
        'base_price': 2000000,
        'parameters': ['CO', 'H2S', 'NH3', 'Cl2', 'HCl'],
    },
    {
        'name': 'MTLĐ - Vi khí hậu',
        'description': 'Đo vi khí hậu môi trường lao động',
        'base_price': 1800000,
        'parameters': ['Nhiệt độ', 'Độ ẩm', 'Tốc độ gió', 'Nhiệt bức xạ'],
    },
    {
        'name': 'MTLĐ - Ánh sáng',
        'description': 'Đo độ rọi tại nơi làm việc',
        'base_price': 1200000,
        'parameters': ['Cường độ ánh sáng', 'Độ chói', 'Độ tương phản'],
    },
    {
        'name': 'MTLĐ - Tiếng ồn',
        'description': 'Đo độ ồn tại nơi làm việc',
        'base_price': 1500000,
        'parameters': ['Leq 8h', 'Lmax', 'Phổ tần số'],
    },
    {
        'name': 'MTLĐ - Độ rung',
        'description': 'Đo độ rung tác động lên người lao động',
        'base_price': 1800000,
        'parameters': ['Rung toàn thân', 'Rung cục bộ', 'Gia tốc rung'],
    },
    {
        'name': 'MTLĐ - Hơi dung môi',
        'description': 'Đo nồng độ hơi dung môi hữu cơ',
        'base_price': 2500000,
        'parameters': ['Benzen', 'Toluen', 'Xylen', 'Axeton', 'MEK'],
    },
    {
        'name': 'MTLĐ - Kim loại nặng',
        'description': 'Phân tích kim loại nặng trong không khí làm việc',
        'base_price': 3000000,
        'parameters': ['Pb', 'Cd', 'Hg', 'Cr', 'Mn'],
    },
    {
        'name': 'MTLĐ - Bức xạ nhiệt',
        'description': 'Đo bức xạ nhiệt tại nơi làm việc',
        'base_price': 2000000,
        'parameters': ['Cường độ bức xạ', 'Nhiệt độ bức xạ', 'WBGT'],
    },
    {
        'name': 'MTLĐ - Trường điện từ',
        'description': 'Đo cường độ trường điện từ',
        'base_price': 2200000,
        'parameters': ['Cường độ điện trường', 'Cường độ từ trường', 'Mật độ công suất'],
    },
]

# Mở rộng danh sách sản phẩm lên 100
all_products = []

# Thêm các sản phẩm QTMT với các biến thể
for i, prod in enumerate(products_qtmt):
    for freq in ['Định kỳ', 'Đột xuất', 'Liên tục']:
        all_products.append({
            'name': f"{prod['name']} - {freq}",
            'category': 'Quan trắc Môi trường',
            'description': f"{prod['description']} - Phương thức {freq.lower()}",
            'list_price': prod['base_price'],
            'standard_price': prod['base_price'] * 0.6,
            'type': 'service',
            'parameters': prod['parameters'],
            'uom_id': 1,  # Unit
            'uom_po_id': 1,
        })

# Thêm các sản phẩm MTLĐ
for i, prod in enumerate(products_mtld):
    for scale in ['Cơ bản', 'Tiêu chuẩn', 'Mở rộng']:
        all_products.append({
            'name': f"{prod['name']} - {scale}",
            'category': 'Quan trắc Môi trường Lao động',
            'description': f"{prod['description']} - Gói {scale}",
            'list_price': prod['base_price'],
            'standard_price': prod['base_price'] * 0.6,
            'type': 'service',
            'parameters': prod['parameters'],
            'uom_id': 1,
        })

# Thêm các dịch vụ khác để đủ 100
additional_services = [
    {
        'name': 'Lập Báo cáo Đánh giá Tác động Môi trường (ĐTM)',
        'category': 'Giấy phép Môi trường',
        'description': 'Lập hồ sơ ĐTM cho các dự án đầu tư',
        'list_price': 50000000,
        'standard_price': 30000000,
    },
    {
        'name': 'Lập Bản Cam kết Bảo vệ Môi trường',
        'category': 'Giấy phép Môi trường',
        'description': 'Lập hồ sơ cam kết bảo vệ môi trường',
        'list_price': 15000000,
        'standard_price': 9000000,
    },
    {
        'name': 'Lập Kế hoạch Bảo vệ Môi trường',
        'category': 'Giấy phép Môi trường',
        'description': 'Lập kế hoạch bảo vệ môi trường cho doanh nghiệp',
        'list_price': 20000000,
        'standard_price': 12000000,
    },
    {
        'name': 'Xin Giấy phép Xả thải',
        'category': 'Giấy phép Môi trường',
        'description': 'Hồ sơ đề nghị cấp giấy phép xả nước thải',
        'list_price': 25000000,
        'standard_price': 15000000,
    },
    {
        'name': 'Đào tạo Quản lý Môi trường',
        'category': 'Dịch vụ Môi trường',
        'description': 'Đào tạo nội bộ về quản lý môi trường',
        'list_price': 10000000,
        'standard_price': 6000000,
    },
]

for svc in additional_services:
    for package in ['Gói 1', 'Gói 2', 'Gói 3', 'Gói 4']:
        all_products.append({
            'name': f"{svc['name']} - {package}",
            'category': svc['category'],
            'description': svc['description'],
            'list_price': svc['list_price'],
            'standard_price': svc['standard_price'],
            'type': 'service',
            'parameters': [],
            'uom_id': 1,
            'uom_po_id': 1,
        })

# Cắt chính xác 100 sản phẩm
all_products = all_products[:100]

print(f"Tổng số sản phẩm sẽ tạo: {len(all_products)}")

# Tạo từng sản phẩm
created_count = 0
for idx, prod in enumerate(all_products, 1):
    try:
        # Kiểm tra tồn tại
        existing = models.execute_kw(db, uid, password,
            'product.template', 'search',
            [[('name', '=', prod['name'])]], {'limit': 1})
        
        if existing:
            print(f"  {idx:3d}. ⊘ '{prod['name']}' đã tồn tại")
            continue
        
        # Chuẩn bị dữ liệu
        cat_id = category_ids.get(prod['category'])
        params_text = '\n'.join([f"  • {p}" for p in prod.get('parameters', [])])
        
        product_data = {
            'name': prod['name'],
            'categ_id': cat_id,
            'type': prod['type'],
            'list_price': prod['list_price'],
            'standard_price': prod['standard_price'],
            'uom_id': prod['uom_id'],
            'sale_ok': True,
            'purchase_ok': True,
            'description_sale': prod['description'] + '\n\nCác thông số:\n' + params_text if params_text else prod['description'],
        }
        
        # Tạo sản phẩm
        product_id = models.execute_kw(db, uid, password,
            'product.template', 'create', [product_data])
        
        created_count += 1
        print(f"  {idx:3d}. ✓ Tạo '{prod['name']}' (ID: {product_id}) - {prod['list_price']:,} VND")
        
    except Exception as e:
        print(f"  {idx:3d}. ✗ Lỗi '{prod['name']}': {str(e)}")

print(f"\n{'='*60}")
print(f"Hoàn thành! Đã tạo {created_count}/{len(all_products)} sản phẩm mới.")
print(f"{'='*60}")

