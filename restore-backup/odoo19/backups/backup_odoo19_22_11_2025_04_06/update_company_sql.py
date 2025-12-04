#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script SQL để cập nhật Header report và thông tin đại diện cho công ty
Chạy: python3 update_company_sql.py
"""

import psycopg2
from psycopg2 import sql

# Thông tin kết nối database
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'odoo19',
    'user': 'odoo',
    'password': 'odoo19@2025'
}

# Nội dung Header report
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
    
    try:
        # Kết nối database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Tìm công ty
        company_name = "CÔNG TY CỔ PHẦN DỊCH VỤ CÔNG NGHỆ SÀI GÒN"
        cur.execute("SELECT id FROM res_company WHERE name = %s", (company_name,))
        company = cur.fetchone()
        
        if not company:
            print(f"❌ Không tìm thấy công ty: {company_name}")
            cur.execute("SELECT id, name FROM res_company")
            companies = cur.fetchall()
            print("\n📋 Danh sách các công ty hiện có:")
            for c in companies:
                print(f"   • {c[1]} (ID: {c[0]})")
            return
        
        company_id = company[0]
        print(f"✓ Tìm thấy công ty: {company_name} (ID: {company_id})")
        
        # Kiểm tra xem trường report_header_text có tồn tại không
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='res_company' AND column_name='report_header_text'
        """)
        field_exists = cur.fetchone()
        
        if not field_exists:
            print("⚠️  Trường 'report_header_text' chưa tồn tại trong database.")
            print("   Vui lòng upgrade module 'sgc_management_core' trước.")
            print("   Hoặc chạy lệnh sau trong Odoo shell:")
            print("   - Vào Apps → sgc_management_core → Upgrade")
            return
        
        # Cập nhật dữ liệu
        cur.execute("""
            UPDATE res_company 
            SET report_header_text = %s,
                representative_name = %s
            WHERE id = %s
        """, (header_report_html, 'Nguyễn Hữu Dương', company_id))
        
        conn.commit()
        
        print(f"\n✅ ĐÃ CẬP NHẬT THÀNH CÔNG!")
        print(f"   • Công ty: {company_name}")
        print(f"   • Header report: Đã cập nhật theo hình ảnh thứ 2")
        print(f"   • Đại diện: Nguyễn Hữu Dương")
        print("\n" + "="*80)
        
        cur.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ LỖI DATABASE: {e}")
    except Exception as e:
        print(f"❌ LỖI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

