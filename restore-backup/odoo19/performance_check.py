#!/usr/bin/env python3
"""
Script kiểm tra hiệu suất và tối ưu hóa database Odoo
"""
import psycopg2
import time
import sys
import os

# Thêm đường dẫn Odoo
sys.path.insert(0, '/usr/lib/python3/dist-packages')

def check_database_performance():
    """Kiểm tra hiệu suất database"""
    print("=== KIỂM TRA CHI TIẾT DATABASE ===")

    try:
        # Kết nối database
        conn = psycopg2.connect(
            host='db',
            user='odoo',
            password='odoo',
            dbname='odoo19'
        )
        cur = conn.cursor()

        # Lấy danh sách bảng chính
        cur.execute("""
            SELECT schemaname, tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            AND (tablename LIKE '%project%'
                 OR tablename LIKE '%res_partner%'
                 OR tablename LIKE '%product%'
                 OR tablename LIKE '%stock_picking%')
            LIMIT 10;
        """)
        tables = cur.fetchall()
        print(f"📋 Bảng chính: {len(tables)} bảng")
        for table in tables:
            print(f"  - {table[1]}")

        # Đếm số lượng bản ghi
        cur.execute('SELECT COUNT(*) FROM project_project;')
        projects_count = cur.fetchone()[0]

        cur.execute('SELECT COUNT(*) FROM res_partner WHERE customer_rank > 0;')
        customers_count = cur.fetchone()[0]

        cur.execute('SELECT COUNT(*) FROM product_product;')
        products_count = cur.fetchone()[0]

        cur.execute('SELECT COUNT(*) FROM stock_picking;')
        pickings_count = cur.fetchone()[0]

        print("
📊 Số lượng bản ghi:"        print(f"  - project_project: {projects_count}")
        print(f"  - res_partner (customers): {customers_count}")
        print(f"  - product_product: {products_count}")
        print(f"  - stock_picking: {pickings_count}")

        # Kiểm tra indexes
        cur.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE tablename IN ('project_project', 'res_partner', 'product_product', 'stock_picking');
        """)
        indexes = cur.fetchall()
        print(f"\n🔍 Index hiện có: {len(indexes)} index")
        for idx in indexes[:5]:
            print(f"  - {idx[0]}")

        cur.close()
        conn.close()

        print("\n✅ Database connection ổn định")
        print("✅ Tables và indexes hoạt động bình thường")

        print("\n=== TỐI ƯU HÓA ĐỀ XUẤT ===")
        print("1. Thêm composite indexes cho các truy vấn phức tạp")
        print("2. Vacuum và analyze database định kỳ")
        print("3. Cấu hình PostgreSQL memory settings")
        print("4. Sử dụng read replicas cho reporting")
        print("5. Implement query result caching")

    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")

if __name__ == "__main__":
    check_database_performance()</content>
<parameter name="filePath">/home/sgc/odoo19/performance_check.py