#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo 10 báo giá + 10 hợp đồng mẫu với các tình huống thực tế
"""
import xmlrpc.client
import random
from datetime import datetime, timedelta

url = 'http://localhost:10019'
db = 'odoo19'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print(f"✓ Kết nối Odoo thành công (User ID: {uid})\n")

# ========================================
# LẤY DỮ LIỆU CẦN THIẾT
# ========================================
print("="*70)
print("📦 CHUẨN BỊ DỮ LIỆU")
print("="*70)

# Lấy danh sách khách hàng
customers = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[('customer_rank', '>', 0), ('is_company', '=', True)]], 
    {'fields': ['id', 'name'], 'limit': 15})

print(f"✓ Tìm thấy {len(customers)} khách hàng")

# Lấy sản phẩm dịch vụ (loại trừ Event Registration)
products = models.execute_kw(db, uid, password,
    'product.product', 'search_read',
    [[('sale_ok', '=', True), ('name', 'not ilike', 'Event Registration')]], 
    {'fields': ['id', 'name', 'list_price'], 'limit': 50})

print(f"✓ Tìm thấy {len(products)} sản phẩm")

# Lấy user hiện tại
users = models.execute_kw(db, uid, password,
    'res.users', 'search_read',
    [[]], {'fields': ['id', 'name'], 'limit': 5})

print(f"✓ Tìm thấy {len(users)} users\n")

# ========================================
# PHẦN 1: TẠO 10 BÁO GIÁ MẪU
# ========================================
print("="*70)
print("📋 PHẦN 1: TẠO 10 BÁO GIÁ VỚI CÁC TÌNH HUỐNG")
print("="*70 + "\n")

quotation_scenarios = [
    {
        'name': 'Báo giá QTMT - Chờ gửi khách',
        'state': 'draft',
        'note': 'Báo giá đang soạn thảo, chưa gửi cho khách hàng',
        'validity_days': 30,
        'product_count': 5,
    },
    {
        'name': 'Báo giá MTLĐ - Đã gửi, chờ phản hồi',
        'state': 'sent',
        'note': 'Đã gửi email cho khách hàng ngày 15/11, đang chờ phản hồi',
        'validity_days': 30,
        'product_count': 8,
    },
    {
        'name': 'Báo giá GPMT - Khách chấp nhận',
        'state': 'sale',
        'note': 'Khách hàng đồng ý, đã chuyển thành đơn hàng và ký hợp đồng',
        'validity_days': 30,
        'product_count': 12,
    },
    {
        'name': 'Báo giá Phân tích - Khách từ chối (giá cao)',
        'state': 'cancel',
        'note': 'Khách hàng cho rằng giá cao hơn đối thủ 15%, đã từ chối',
        'validity_days': 30,
        'product_count': 6,
    },
    {
        'name': 'Báo giá QTMT - Đang đàm phán giảm giá',
        'state': 'sent',
        'note': 'Khách yêu cầu giảm 10%, đang chờ phê duyệt từ Ban lãnh đạo',
        'validity_days': 15,
        'product_count': 10,
    },
    {
        'name': 'Báo giá Lấy mẫu - Khách yêu cầu bổ sung',
        'state': 'draft',
        'note': 'Khách yêu cầu thêm 5 chỉ tiêu, đang cập nhật báo giá',
        'validity_days': 20,
        'product_count': 7,
    },
    {
        'name': 'Báo giá MTLĐ - Hết hạn, chưa ký',
        'state': 'sent',
        'note': 'Báo giá đã hết hạn 5 ngày, khách chưa quyết định, cần làm mới',
        'validity_days': -5,
        'product_count': 9,
    },
    {
        'name': 'Báo giá ĐTM - Chấp nhận, chờ ký HĐ',
        'state': 'sale',
        'note': 'Khách đồng ý, hẹn ký hợp đồng tuần sau',
        'validity_days': 25,
        'product_count': 3,
    },
    {
        'name': 'Báo giá Khí thải - Khách chọn đối thủ',
        'state': 'cancel',
        'note': 'Khách hàng đã chọn đơn vị khác do thời gian nhanh hơn',
        'validity_days': 30,
        'product_count': 8,
    },
    {
        'name': 'Báo giá Combo - Đang chờ duyệt nội bộ',
        'state': 'draft',
        'note': 'Báo giá lớn >500tr, cần Giám đốc phê duyệt trước khi gửi',
        'validity_days': 30,
        'product_count': 15,
    },
]

created_quotes = []

for idx, scenario in enumerate(quotation_scenarios, 1):
    try:
        # Chọn khách hàng ngẫu nhiên
        customer = random.choice(customers)
        user = random.choice(users)
        
        # Tạo ngày
        base_date = datetime.now()
        date_order = (base_date - timedelta(days=random.randint(1, 15))).strftime('%Y-%m-%d')
        validity_date = (base_date + timedelta(days=scenario['validity_days'])).strftime('%Y-%m-%d')
        
        # Tạo báo giá
        quote_data = {
            'partner_id': customer['id'],
            'user_id': user['id'],
            'date_order': date_order,
            'validity_date': validity_date,
            'note': scenario['note'],
        }
        
        quote_id = models.execute_kw(db, uid, password,
            'sale.order', 'create', [quote_data])
        
        # Thêm sản phẩm
        order_lines = []
        
        # Section header
        order_lines.append((0, 0, {
            'display_type': 'line_section',
            'name': scenario['name'].upper(),
        }))
        
        # Chọn sản phẩm ngẫu nhiên
        selected_products = random.sample(products, min(scenario['product_count'], len(products)))
        
        for product in selected_products:
            qty = random.choice([1, 2, 4, 12, 24, 48])
            order_lines.append((0, 0, {
                'product_id': product['id'],
                'product_uom_qty': qty,
                'price_unit': product['list_price'] if product['list_price'] > 0 else 100000,
            }))
        
        # Update order lines
        models.execute_kw(db, uid, password,
            'sale.order', 'write',
            [[quote_id], {'order_line': order_lines}])
        
        # Chuyển trạng thái
        if scenario['state'] == 'sent':
            # Gửi báo giá
            models.execute_kw(db, uid, password,
                'sale.order', 'action_quotation_sent', [[quote_id]])
        elif scenario['state'] == 'sale':
            # Xác nhận đơn hàng
            models.execute_kw(db, uid, password,
                'sale.order', 'action_confirm', [[quote_id]])
        elif scenario['state'] == 'cancel':
            # Hủy báo giá
            models.execute_kw(db, uid, password,
                'sale.order', 'action_cancel', [[quote_id]])
        
        # Lấy số báo giá
        quote = models.execute_kw(db, uid, password,
            'sale.order', 'read',
            [[quote_id]], {'fields': ['name', 'state', 'amount_total']})[0]
        
        created_quotes.append(quote)
        
        state_icon = {
            'draft': '📝',
            'sent': '📤',
            'sale': '✅',
            'cancel': '❌',
        }.get(quote['state'], '❓')
        
        print(f"  {idx:2d}. {state_icon} {quote['name']:<12} | {scenario['name'][:40]:<40} | {quote['amount_total']:>12,.0f} đ")
        
    except Exception as e:
        print(f"  {idx:2d}. ❌ Lỗi: {str(e)[:60]}")

# ========================================
# PHẦN 2: TẠO 10 HỢP ĐỒNG MẪU
# ========================================
print("\n" + "="*70)
print("📜 PHẦN 2: TẠO 10 HỢP ĐỒNG VỚI CÁC TÌNH HUỐNG")
print("="*70 + "\n")

contract_scenarios = [
    {
        'name': 'HĐ QTMT - Mới ký, chưa triển khai',
        'state': 'draft',
        'linked_project': False,
        'note': 'Hợp đồng vừa ký xong, chưa tạo dự án, đang chờ khách thanh toán đợt 1',
        'product_count': 8,
    },
    {
        'name': 'HĐ MTLĐ - Đang thực hiện 30%',
        'state': 'confirmed',
        'linked_project': True,
        'note': 'Dự án đang triển khai, đã lấy mẫu 15/48 điểm, tiến độ 30%',
        'product_count': 10,
    },
    {
        'name': 'HĐ Phân tích - Đang thực hiện 70%',
        'state': 'confirmed',
        'linked_project': True,
        'note': 'Đã hoàn thành lấy mẫu, đang phân tích tại lab, tiến độ 70%',
        'product_count': 12,
    },
    {
        'name': 'HĐ GPMT - Hoàn thành, chờ thanh toán',
        'state': 'done',
        'linked_project': True,
        'note': 'Đã bàn giao báo cáo, khách chưa thanh toán đợt 2 (30%)',
        'product_count': 5,
    },
    {
        'name': 'HĐ ĐTM - Chưa liên kết dự án (lỗi hệ thống)',
        'state': 'confirmed',
        'linked_project': False,
        'note': 'HĐ đã ký nhưng dự án không tự động tạo, cần tạo thủ công',
        'product_count': 6,
    },
    {
        'name': 'HĐ Quan trắc - Tạm dừng (khách yêu cầu)',
        'state': 'on_hold',
        'linked_project': True,
        'note': 'Khách hàng yêu cầu tạm dừng 1 tháng do sửa chữa nhà máy',
        'product_count': 9,
    },
    {
        'name': 'HĐ Lấy mẫu - Hủy (khách phá sản)',
        'state': 'cancel',
        'linked_project': False,
        'note': 'Khách hàng ngừng hoạt động, đã hủy hợp đồng và hoàn tiền',
        'product_count': 4,
    },
    {
        'name': 'HĐ MTLĐ - Chậm tiến độ (thiếu thiết bị)',
        'state': 'confirmed',
        'linked_project': True,
        'note': 'Thiết bị đo bụi hỏng, đang chờ sửa chữa, chậm 10 ngày',
        'product_count': 11,
    },
    {
        'name': 'HĐ Năm 2025 - Chưa bắt đầu (chờ Q1/2025)',
        'state': 'confirmed',
        'linked_project': False,
        'note': 'HĐ khung cả năm, bắt đầu thực hiện từ tháng 1/2025',
        'product_count': 20,
    },
    {
        'name': 'HĐ VIP - Hoàn thành xuất sắc',
        'state': 'done',
        'linked_project': True,
        'note': 'Hoàn thành đúng hạn, khách hài lòng, đã thanh toán 100%, có feedback 5 sao',
        'product_count': 14,
    },
]

created_contracts = []

for idx, scenario in enumerate(contract_scenarios, 1):
    try:
        # Chọn khách hàng và user
        customer = random.choice(customers)
        user = random.choice(users)
        
        # Tạo sale order trước (để làm cơ sở cho hợp đồng)
        base_date = datetime.now()
        date_order = (base_date - timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d')
        
        so_data = {
            'partner_id': customer['id'],
            'user_id': user['id'],
            'date_order': date_order,
        }
        
        so_id = models.execute_kw(db, uid, password,
            'sale.order', 'create', [so_data])
        
        # Thêm sản phẩm vào SO
        order_lines = []
        order_lines.append((0, 0, {
            'display_type': 'line_section',
            'name': scenario['name'].upper(),
        }))
        
        selected_products = random.sample(products, min(scenario['product_count'], len(products)))
        total_amount = 0
        
        for product in selected_products:
            qty = random.choice([1, 2, 4, 6, 12, 24, 48])
            price = product['list_price'] if product['list_price'] > 0 else 100000
            order_lines.append((0, 0, {
                'product_id': product['id'],
                'product_uom_qty': qty,
                'price_unit': price,
            }))
            total_amount += qty * price
        
        models.execute_kw(db, uid, password,
            'sale.order', 'write',
            [[so_id], {'order_line': order_lines}])
        
        # Chuyển trạng thái sale order
        if scenario['state'] in ['confirmed', 'done', 'on_hold']:
            models.execute_kw(db, uid, password,
                'sale.order', 'action_confirm', [[so_id]])
        elif scenario['state'] == 'cancel':
            models.execute_kw(db, uid, password,
                'sale.order', 'action_cancel', [[so_id]])
        
        # Tạo hợp đồng (sgc.signed.contract) nếu có module
        # Tạm thời dùng sale.order làm contract
        
        # Nếu cần project
        if scenario['linked_project']:
            try:
                # Tạo project
                project_data = {
                    'name': f"[DỰ ÁN] {scenario['name']}",
                    'partner_id': customer['id'],
                    'user_id': user['id'],
                }
                
                project_id = models.execute_kw(db, uid, password,
                    'project.project', 'create', [project_data])
                
                # Link project với SO
                models.execute_kw(db, uid, password,
                    'sale.order', 'write',
                    [[so_id], {'project_id': project_id}])
                
            except:
                pass
        
        # Lấy thông tin SO
        so = models.execute_kw(db, uid, password,
            'sale.order', 'read',
            [[so_id]], {'fields': ['name', 'state', 'amount_total']})[0]
        
        created_contracts.append(so)
        
        state_icon = {
            'draft': '📝',
            'sent': '📤',
            'sale': '🟢',
            'done': '✅',
            'cancel': '❌',
            'confirmed': '🔵',
            'on_hold': '⏸️',
        }.get(scenario['state'], '❓')
        
        project_status = '🔗 Có dự án' if scenario['linked_project'] else '⚠️ Chưa có'
        
        print(f"  {idx:2d}. {state_icon} {so['name']:<12} | {scenario['name'][:35]:<35} | {project_status:<15} | {so['amount_total']:>12,.0f} đ")
        
    except Exception as e:
        print(f"  {idx:2d}. ❌ Lỗi: {str(e)[:80]}")

# ========================================
# TÓM TẮT
# ========================================
print("\n" + "="*70)
print("✅ HOÀN THÀNH TẠO DỮ LIỆU MẪU!")
print("="*70)

print(f"""
📊 Thống kê Báo giá:
  • Tổng số: {len(created_quotes)}
  • Draft (Nháp): {sum(1 for q in created_quotes if q['state'] == 'draft')}
  • Sent (Đã gửi): {sum(1 for q in created_quotes if q['state'] == 'sent')}
  • Sale (Chấp nhận): {sum(1 for q in created_quotes if q['state'] == 'sale')}
  • Cancel (Từ chối): {sum(1 for q in created_quotes if q['state'] == 'cancel')}

📊 Thống kê Hợp đồng/Đơn hàng:
  • Tổng số: {len(created_contracts)}
  • Mới tạo: {sum(1 for c in created_contracts if c['state'] == 'draft')}
  • Đã xác nhận: {sum(1 for c in created_contracts if c['state'] == 'sale')}
  • Đã hủy: {sum(1 for c in created_contracts if c['state'] == 'cancel')}

🎯 Các tình huống đã tạo:
  ✓ Báo giá chờ gửi
  ✓ Báo giá đã gửi, chờ phản hồi
  ✓ Báo giá khách chấp nhận
  ✓ Báo giá khách từ chối (nhiều lý do)
  ✓ Báo giá hết hạn
  ✓ Hợp đồng chưa liên kết dự án
  ✓ Hợp đồng đang thực hiện (có dự án)
  ✓ Hợp đồng hoàn thành
  ✓ Hợp đồng tạm dừng
  ✓ Hợp đồng hủy

📍 Xem trong Odoo:
  → Sales → Orders (xem tất cả)
  → Sales → Quotations (chỉ báo giá)
  → Project → Projects (xem các dự án đã tạo)

💡 Mục đích:
  • Training nhân viên mới
  • Demo cho khách hàng
  • Test báo cáo thống kê
  • Phân tích quy trình làm việc
""")

