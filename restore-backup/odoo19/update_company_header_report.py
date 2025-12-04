#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để cập nhật Header report cho công ty
"""

import xmlrpc.client
import sys

# Thông tin kết nối Odoo
url = 'http://localhost:10019'
db = 'odoo19'
username = 'admin'
password = 'admin'

# Kết nối đến Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("Không thể kết nối đến Odoo!")
    sys.exit(1)

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Tìm công ty
company_name = "CÔNG TY CỔ PHẦN DỊCH VỤ CÔNG NGHỆ SÀI GÒN"
company_ids = models.execute_kw(db, uid, password,
    'res.company', 'search',
    [[('name', '=', company_name)]])

if not company_ids:
    print(f"Không tìm thấy công ty: {company_name}")
    sys.exit(1)

company_id = company_ids[0]

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

# Cập nhật thông tin công ty
update_data = {
    'report_header_text': header_report_html,
    'representative_name': 'Nguyễn Hữu Dương',
}

models.execute_kw(db, uid, password,
    'res.company', 'write',
    [[company_id], update_data])

print(f"Đã cập nhật Header report cho công ty: {company_name}")
print(f"Đã cập nhật Đại diện: Nguyễn Hữu Dương")

