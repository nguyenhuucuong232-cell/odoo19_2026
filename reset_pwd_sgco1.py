#!/usr/bin/env python3
import sys
import os

# Add Odoo to path
sys.path.insert(0, '/usr/lib/python3/dist-packages')

try:
    from odoo.tools import config, crypt
    import psycopg2
    
    # Database configuration
    db_host = 'db'
    db_port = 5432
    db_user = 'odoo'
    db_password = 'odoo'
    db_name = 'sgco1'
    new_password = 'admin'
    
    # Generate password hash
    password_hash = crypt.encrypt(new_password)
    
    # Connect to database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cur = conn.cursor()
    
    # Find active user (nhd.hsevn@gmail.com or admin)
    cur.execute("SELECT id, login FROM res_users WHERE active = true AND (login = 'nhd.hsevn@gmail.com' OR login = 'admin') ORDER BY id LIMIT 1;")
    user_result = cur.fetchone()
    
    if user_result:
        user_id, user_login = user_result
        cur.execute("UPDATE res_users SET password = %s WHERE id = %s;", (password_hash, user_id))
        conn.commit()
        print(f"✓ Password đã được reset thành công!")
        print(f"  Tài khoản: {user_login}")
        print(f"  Mật khẩu: {new_password}")
    else:
        print("✖ Không tìm thấy user active trong database")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
