#!/usr/bin/env python3
# Script to create additional sample data for Odoo 19
# Run with: docker-compose exec odoo19 odoo shell -d odoo19 -c /etc/odoo/odoo.conf < additional_sample_data.py

import random
from datetime import datetime, timedelta

# Check if running in Odoo shell
try:
    env
    IN_ODOO_SHELL = True
except NameError:
    IN_ODOO_SHELL = False

if IN_ODOO_SHELL:
    print("=== TẠO DỮ LIỆU MẪU BỔ SUNG ===")
    
    # Get existing data counts
    existing_partners = env['res.partner'].search_count([])
    existing_products = env['product.product'].search_count([])
    existing_users = env['res.users'].search_count([])
    
    print(f"Dữ liệu hiện tại: {existing_partners} khách hàng, {existing_products} sản phẩm, {existing_users} người dùng")
    
    # Create additional customers
    print("\n--- TẠO THÊM KHÁCH HÀNG ---")
    customers_data = [
        {'name': 'Công ty TNHH ABC Technology', 'email': 'contact@abc-tech.vn', 'phone': '028-1234-5678', 'street': '123 Đường ABC, Quận 1', 'city': 'TP.HCM'},
        {'name': 'Trường Đại học Bách khoa', 'email': 'admin@hcmut.edu.vn', 'phone': '028-3864-7136', 'street': '268 Lý Thường Kiệt', 'city': 'TP.HCM'},
        {'name': 'Bệnh viện Đại học Y Dược', 'email': 'info@yd.edu.vn', 'phone': '028-3855-4269', 'street': '215 Hồng Bàng', 'city': 'TP.HCM'},
        {'name': 'Công ty CP Phần mềm XYZ', 'email': 'sales@xyz-software.com', 'phone': '024-1234-5678', 'street': '45 Đường XYZ', 'city': 'Hà Nội'},
        {'name': 'Trung tâm Nghiên cứu CNTT', 'email': 'research@cntt-center.vn', 'phone': '024-9876-5432', 'street': '89 Đường CNTT', 'city': 'Hà Nội'},
    ]
    
    for customer in customers_data:
        partner = env['res.partner'].create({
            'name': customer['name'],
            'email': customer['email'],
            'phone': customer['phone'],
            'street': customer['street'],
            'city': customer['city'],
            'country_id': env['res.country'].search([('code', '=', 'VN')], limit=1).id,
            'customer_rank': 1,
        })
        print(f"✓ Tạo khách hàng: {partner.name}")
    
    # Create additional products
    print("\n--- TẠO THÊM SẢN PHẨM/DỊCH VỤ ---")
    products_data = [
        {'name': 'Dịch vụ Tư vấn CNTT', 'type': 'service', 'list_price': 5000000, 'standard_price': 3000000},
        {'name': 'Phát triển Ứng dụng Mobile', 'type': 'service', 'list_price': 15000000, 'standard_price': 10000000},
        {'name': 'Thiết kế Website', 'type': 'service', 'list_price': 8000000, 'standard_price': 5000000},
        {'name': 'Đào tạo Lập trình Python', 'type': 'service', 'list_price': 3000000, 'standard_price': 2000000},
        {'name': 'Bảo trì Hệ thống', 'type': 'service', 'list_price': 2000000, 'standard_price': 1500000},
        {'name': 'Máy chủ Cloud VPS', 'type': 'service', 'list_price': 1000000, 'standard_price': 800000},
        {'name': 'License Phần mềm', 'type': 'consu', 'list_price': 5000000, 'standard_price': 4000000},
        {'name': 'Thiết bị Mạng', 'type': 'consu', 'list_price': 2000000, 'standard_price': 1500000},
    ]
    
    for product in products_data:
        prod = env['product.product'].create({
            'name': product['name'],
            'type': product['type'],
            'list_price': product['list_price'],
            'standard_price': product['standard_price'],
            'uom_id': env['uom.uom'].search([('name', '=', 'Units')], limit=1).id,
            'uom_po_id': env['uom.uom'].search([('name', '=', 'Units')], limit=1).id,
        })
        print(f"✓ Tạo sản phẩm: {prod.name} - {prod.list_price:,.0f} VND")
    
    # Create additional employees
    print("\n--- TẠO THÊM NHÂN VIÊN ---")
    employees_data = [
        {'name': 'Nguyễn Văn A', 'work_email': 'nguyenvana@company.com', 'department': 'IT'},
        {'name': 'Trần Thị B', 'work_email': 'tranthib@company.com', 'department': 'Sale'},
        {'name': 'Lê Văn C', 'work_email': 'levanc@company.com', 'department': 'HR'},
        {'name': 'Phạm Thị D', 'work_email': 'phamthid@company.com', 'department': 'Finance'},
        {'name': 'Hoàng Văn E', 'work_email': 'hoangvane@company.com', 'department': 'Project'},
    ]
    
    for emp in employees_data:
        # Create user first
        user = env['res.users'].create({
            'name': emp['name'],
            'login': emp['work_email'],
            'email': emp['work_email'],
            'password': '123456',  # Simple password for demo
        })
        
        # Create employee
        employee = env['hr.employee'].create({
            'name': emp['name'],
            'user_id': user.id,
            'work_email': emp['work_email'],
            'department_id': env['hr.department'].search([('name', 'ilike', emp['department'])], limit=1).id or env['hr.department'].search([], limit=1).id,
        })
        print(f"✓ Tạo nhân viên: {employee.name} ({emp['department']})")
    
    # Create sample purchase orders
    print("\n--- TẠO ĐƠN MUA HÀNG MẪU ---")
    vendors = env['res.partner'].search([('supplier_rank', '>', 0)], limit=3)
    products = env['product.product'].search([('type', '!=', 'service')], limit=5)
    
    if vendors and products:
        for i in range(3):
            vendor = random.choice(vendors)
            po_lines = []
            
            # Create 2-4 line items per PO
            for j in range(random.randint(2, 4)):
                product = random.choice(products)
                po_lines.append((0, 0, {
                    'product_id': product.id,
                    'product_qty': random.randint(1, 10),
                    'price_unit': product.standard_price,
                }))
            
            po = env['purchase.order'].create({
                'partner_id': vendor.id,
                'order_line': po_lines,
                'date_order': datetime.now() - timedelta(days=random.randint(1, 30)),
            })
            print(f"✓ Tạo đơn mua hàng: {po.name} - Nhà cung cấp: {vendor.name}")
    
    # Commit all changes
    env.cr.commit()
    
    # Final summary
    new_partners = env['res.partner'].search_count([]) - existing_partners
    new_products = env['product.product'].search_count([]) - existing_products
    new_users = env['res.users'].search_count([]) - existing_users
    
    print("
=== TÓM TẮT DỮ LIỆU MỚI TẠO ===")
    print(f"✓ Khách hàng mới: {new_partners}")
    print(f"✓ Sản phẩm mới: {new_products}")
    print(f"✓ Người dùng mới: {new_users}")
    print(f"✓ Đơn mua hàng mẫu: 3")
    print("\n✅ Hoàn thành tạo dữ liệu mẫu bổ sung!")
    
else:
    print("Script này chỉ chạy được trong Odoo shell!")
