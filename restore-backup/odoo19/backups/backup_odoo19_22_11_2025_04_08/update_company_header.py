#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Odoo để cập nhật Header report và thông tin đại diện cho công ty
Chạy trong Odoo shell: odoo-bin shell -d odoo19 -c odoo.conf < update_company_header.py
Hoặc: python3 odoo-bin shell -d odoo19 < update_company_header.py
"""

# Nội dung Header report theo hình ảnh thứ 2
header_report_html = """<div style="font-family: serif; color: #4A148C;">
<div style="font-size: 18pt; font-weight: bold; margin-bottom: 10px; color: #4A148C;">
CÔNG TY CỔ PHẦN DỊCH VỤ CÔNG NGHỆ SÀI GÒN
</div>
<div style="font-size: 11pt; line-height: 1.6;">
<div style="margin-bottom: 5px;">
<span style="text-decoration: underline;">Trụ sở:</span> Tầng 14, HM Town, 412 Nguyễn Thị Minh Khai, Phường Bàn Cờ, HCM, VN
</div>
<div style="margin-bottom: 5px;">
<span style="text-decoration: underline;">VPGD/PTN:</span> 65/17 Nguyễn Thị Xinh, P. Thới An, HCM, VN
</div>
<div style="margin-bottom: 5px;">
<span style="text-decoration: underline;">VP Hà Nội:</span> 08-DG2, 125 Phố Đại Linh, P. Đại Mỗ, TP. HN, VN
</div>
<div style="margin-bottom: 5px;">
<span style="text-decoration: underline;">Email:</span> info@hsevn.com.vn <span style="text-decoration: underline;">Web:</span> https://hsevn.com.vn <span style="text-decoration: underline;">Hotline:</span> 1900 1713
</div>
</div>
"""

# Tìm công ty
company_name = "CÔNG TY CỔ PHẦN DỊCH VỤ CÔNG NGHỆ SÀI GÒN"
company = env['res.company'].search([('name', '=', company_name)], limit=1)

if not company:
    print(f"Không tìm thấy công ty: {company_name}")
    print("Danh sách các công ty hiện có:")
    for c in env['res.company'].search([]):
        print(f"  - {c.name}")
else:
    # Cập nhật thông tin
    company.write({
        'report_header_text': header_report_html,
        'representative_name': 'Nguyễn Hữu Dương',
    })
    
    print(f"✓ Đã cập nhật Header report cho công ty: {company.name}")
    print(f"✓ Đã cập nhật Đại diện: Nguyễn Hữu Dương")
    print(f"\nNội dung Header report đã được cập nhật theo hình ảnh thứ 2")

