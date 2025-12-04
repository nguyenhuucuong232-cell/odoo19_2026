#!/usr/bin/env python3
"""
Script để kiểm tra xem Odoo có nhận diện database odoo19_web không
"""
import sys
import os

# Set environment variables
os.environ['HOST'] = 'db'
os.environ['USER'] = 'odoo'
os.environ['PASSWORD'] = 'odoo19@2025'

# Add Odoo to path
sys.path.insert(0, '/usr/lib/python3/dist-packages')

try:
    # Import và parse config
    from odoo.tools import config
    config.parse_config(['-c', '/etc/odoo/odoo.conf'])
    
    print("=== CẤU HÌNH ODOO ===")
    print(f"list_db: {config.get('list_db', 'Not set (default: True)')}")
    print(f"dbfilter: {config.get('dbfilter', 'Not set')}")
    print()
    
    # Test database connection và lấy danh sách
    import psycopg2
    conn = psycopg2.connect(
        host='db',
        user='odoo',
        password='odoo19@2025',
        database='postgres'
    )
    cur = conn.cursor()
    
    # Lấy danh sách database
    cur.execute("""
        SELECT datname 
        FROM pg_database 
        WHERE datistemplate = false 
        AND datname NOT IN ('postgres', 'template0', 'template1')
        ORDER BY datname;
    """)
    
    all_dbs = [row[0] for row in cur.fetchall()]
    print("=== DATABASES TRONG POSTGRESQL ===")
    for db in all_dbs:
        # Kiểm tra từng database
        try:
            db_conn = psycopg2.connect(
                host='db',
                user='odoo',
                password='odoo19@2025',
                database=db
            )
            db_cur = db_conn.cursor()
            
            # Kiểm tra có bảng không
            db_cur.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            table_count = db_cur.fetchone()[0]
            
            # Kiểm tra có module base installed không
            db_cur.execute("""
                SELECT COUNT(*) 
                FROM ir_module_module 
                WHERE name = 'base' AND state = 'installed';
            """)
            base_installed = db_cur.fetchone()[0] > 0
            
            # Kiểm tra có company không
            db_cur.execute("SELECT COUNT(*) FROM res_company;")
            company_count = db_cur.fetchone()[0]
            
            status = "✓" if (table_count > 0 and base_installed) else "✗"
            print(f"{status} {db}: {table_count} tables, base installed: {base_installed}, companies: {company_count}")
            
            db_conn.close()
        except Exception as e:
            print(f"✗ {db}: Error - {str(e)[:50]}")
    
    conn.close()
    
    print()
    print("=== KẾT LUẬN ===")
    if 'odoo19_web' in all_dbs:
        print("✓ Database odoo19_web tồn tại trong PostgreSQL")
        print("Nếu không hiển thị trong Database Manager, có thể do:")
        print("  1. Browser cache - cần hard refresh (Cmd+Shift+R)")
        print("  2. Odoo chưa reload danh sách - đã restart Odoo")
        print("  3. Có thể cần truy cập trực tiếp qua URL")
    else:
        print("✗ Database odoo19_web không tồn tại!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

