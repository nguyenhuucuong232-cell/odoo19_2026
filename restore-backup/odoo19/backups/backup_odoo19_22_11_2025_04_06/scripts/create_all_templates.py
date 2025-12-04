#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo tất cả các mẫu: Email, Báo giá, Hợp đồng
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
# PHẦN 1: TẠO MẪU EMAIL
# ========================================
print("="*70)
print("📧 PHẦN 1: TẠO MẪU EMAIL")
print("="*70 + "\n")

email_templates = [
    {
        'name': 'Email gửi báo giá',
        'model': 'sale.order',
        'subject': 'Báo giá dịch vụ môi trường - {{object.name}}',
        'body_html': '''
<div style="font-family: Arial, sans-serif; padding: 20px;">
    <p>Kính gửi: <strong>{{object.partner_id.name}}</strong>,</p>
    
    <p>Công ty chúng tôi xin gửi đến Quý khách hàng báo giá dịch vụ quan trắc môi trường 
    như sau:</p>
    
    <ul>
        <li>Số báo giá: <strong>{{object.name}}</strong></li>
        <li>Ngày: {{object.date_order}}</li>
        <li>Tổng giá trị: <strong>{{object.amount_total}} VND</strong></li>
    </ul>
    
    <p>Vui lòng xem file đính kèm để biết chi tiết.</p>
    
    <p>Mọi thắc mắc xin liên hệ:</p>
    <ul>
        <li>Người phụ trách: {{object.user_id.name}}</li>
        <li>Email: {{object.user_id.email}}</li>
        <li>Hotline: 19001713</li>
    </ul>
    
    <p>Trân trọng!</p>
    <p><strong>CÔNG TY CỔ PHẦN DỊCH VỤ CÔNG NGHỆ SÀI GÒN</strong><br/>
    HSE Consulting</p>
</div>
        ''',
        'report_template': 'sgc_management_core.action_report_saleorder_sgc',
    },
    {
        'name': 'Email nhắc nhở khách hàng',
        'model': 'sale.order',
        'subject': 'Nhắc nhở: Báo giá {{object.name}} sắp hết hạn',
        'body_html': '''
<p>Kính gửi <strong>{{object.partner_id.name}}</strong>,</p>

<p>Báo giá <strong>{{object.name}}</strong> của chúng tôi sẽ hết hạn vào ngày 
<strong>{{object.validity_date}}</strong>.</p>

<p>Nếu Quý khách có nhu cầu, vui lòng liên hệ lại trong thời gian sớm nhất.</p>

<p>Trân trọng,<br/>
{{object.user_id.name}}<br/>
{{object.user_id.email}}</p>
        ''',
    },
    {
        'name': 'Email cảm ơn sau khi ký hợp đồng',
        'model': 'sale.order',
        'subject': 'Cảm ơn Quý khách - Hợp đồng {{object.name}}',
        'body_html': '''
<p>Kính gửi <strong>{{object.partner_id.name}}</strong>,</p>

<p>Chúng tôi xin chân thành cảm ơn Quý khách đã tin tưởng và ký hợp đồng 
<strong>{{object.name}}</strong> với công ty chúng tôi.</p>

<p>Chúng tôi cam kết sẽ thực hiện dịch vụ với chất lượng cao nhất.</p>

<p>Thông tin dự án:</p>
<ul>
    <li>Số hợp đồng: {{object.name}}</li>
    <li>Người phụ trách: {{object.user_id.name}}</li>
    <li>ĐT: {{object.user_id.phone}}</li>
</ul>

<p>Trân trọng!</p>
        ''',
    },
]

created_emails = 0

for template in email_templates:
    try:
        # Kiểm tra tồn tại
        existing = models.execute_kw(db, uid, password,
            'mail.template', 'search',
            [[('name', '=', template['name'])]], {'limit': 1})
        
        if existing:
            print(f"  ⊘ {template['name']:<45} [Đã tồn tại]")
            continue
        
        # Lấy model ID
        model_id = models.execute_kw(db, uid, password,
            'ir.model', 'search',
            [[('model', '=', template['model'])]], {'limit': 1})
        
        if not model_id:
            print(f"  ❌ {template['name']:<45} [Không tìm thấy model]")
            continue
        
        # Tạo email template
        email_data = {
            'name': template['name'],
            'model_id': model_id[0],
            'subject': template['subject'],
            'body_html': template['body_html'],
            'auto_delete': False,
        }
        
        # Thêm report nếu có
        if template.get('report_template'):
            try:
                report_id = models.execute_kw(db, uid, password,
                    'ir.actions.report', 'search',
                    [[('report_name', '=', template['report_template'])]], {'limit': 1})
                if report_id:
                    email_data['report_template'] = report_id[0]
            except:
                pass
        
        models.execute_kw(db, uid, password,
            'mail.template', 'create', [email_data])
        
        created_emails += 1
        print(f"  ✅ {template['name']:<45} [Đã tạo]")
        
    except Exception as e:
        print(f"  ❌ {template['name']:<45} [Lỗi: {str(e)[:30]}]")

# ========================================
# TÓM TẮT
# ========================================
print(f"\n{'='*70}")
print(f"✅ HOÀN THÀNH!")
print(f"  • Đã tạo {created_emails} mẫu email")
print("="*70)

print("""
📍 VÀO ĐÂU ĐỂ XEM/SỬA CÁC MẪU?

┌──────────────────────────────────────────────────────────────────┐
│ 📧 MẪU EMAIL                                                     │
├──────────────────────────────────────────────────────────────────┤
│ Settings → Technical → Email → Mẫu email (Email Templates)       │
│                                                                  │
│ URL: http://localhost:10019/web#action=mail.action_email_       │
│      template_tree_all&model=mail.template                       │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ 📋 MẪU BÁO GIÁ                                                   │
├──────────────────────────────────────────────────────────────────┤
│ Bán hàng → Đơn hàng → Lọc "Quotation" (Báo giá)                  │
│                                                                  │
│ Hoặc: Bán hàng → Cấu hình → Đơn bán hàng                         │
│                                                                  │
│ URL: http://localhost:10019/web#action=sale.action_quotations   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ 📄 MẪU IN PDF (Báo giá, Hợp đồng, Biên bản...)                   │
├──────────────────────────────────────────────────────────────────┤
│ Settings → Technical → Báo cáo (Reports)                         │
│                                                                  │
│ Tìm: "Báo giá SGC", "Hợp đồng SGC"...                            │
│                                                                  │
│ URL: http://localhost:10019/web#action=base.action_report       │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ 📝 MẪU HỢP ĐỒNG (nếu có module)                                  │
├──────────────────────────────────────────────────────────────────┤
│ Tạm thời dùng Sale Order                                         │
│ Hoặc cài module: contract, sale_contract                         │
└──────────────────────────────────────────────────────────────────┘
""")

