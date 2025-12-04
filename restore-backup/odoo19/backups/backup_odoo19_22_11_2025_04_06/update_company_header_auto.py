#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động cập nhật Header report và thông tin đại diện cho công ty
Chạy: python3 update_company_header_auto.py
"""

import os
import sys

# Thêm đường dẫn Odoo vào sys.path
odoo_path = os.path.join(os.path.dirname(__file__), 'odoo-src')
if os.path.exists(odoo_path):
    sys.path.insert(0, odoo_path)

try:
    import odoo
    from odoo import api, SUPERUSER_ID
except ImportError:
    print("❌ Không tìm thấy Odoo. Vui lòng đảm bảo Odoo đã được cài đặt.")
    sys.exit(1)

DB_NAME = 'odoo19'

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

def main():
    print("="*80)
    print("🔄 BẮT ĐẦU CẬP NHẬT HEADER REPORT VÀ THÔNG TIN ĐẠI DIỆN")
    print("="*80)

    # 1. Connect DB
    try:
        # Setup config from Env
        db_host = os.environ.get('HOST', 'localhost')
        db_port = os.environ.get('PORT', '5432')
        db_user = os.environ.get('USER', 'odoo')
        db_password = os.environ.get('PASSWORD', 'odoo19@2025')
        
        odoo.tools.config.parse_config([
            '--db_host', db_host,
            '--db_port', db_port,
            '--db_user', db_user,
            '--db_password', db_password,
        ])
        odoo.tools.config['db_name'] = DB_NAME
        registry = odoo.modules.registry.Registry.new(DB_NAME)
    except Exception as e:
        print(f"❌ LỖI: Không thể kết nối DB. {e}")
        print("💡 Đang thử kết nối với cấu hình mặc định...")
        try:
            registry = odoo.modules.registry.Registry.new(DB_NAME)
        except Exception as e2:
            print(f"❌ CRITICAL ERROR: {e2}")
            return

    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Tìm công ty
        company_name = "CÔNG TY CỔ PHẦN DỊCH VỤ CÔNG NGHỆ SÀI GÒN"
        company = env['res.company'].search([('name', '=', company_name)], limit=1)
        
        if not company:
            print(f"❌ Không tìm thấy công ty: {company_name}")
            print("\n📋 Danh sách các công ty hiện có:")
            companies = env['res.company'].search([])
            for c in companies:
                print(f"   • {c.name}")
            return
        
        # Cập nhật thông tin
        try:
            company.write({
                'report_header_text': header_report_html,
                'representative_name': 'Nguyễn Hữu Dương',
            })
            cr.commit()
            
            print(f"\n✅ ĐÃ CẬP NHẬT THÀNH CÔNG!")
            print(f"   • Công ty: {company.name}")
            print(f"   • Header report: Đã cập nhật theo hình ảnh thứ 2")
            print(f"   • Đại diện: Nguyễn Hữu Dương")
            print("\n" + "="*80)
            
        except Exception as e:
            cr.rollback()
            print(f"❌ LỖI khi cập nhật: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()

