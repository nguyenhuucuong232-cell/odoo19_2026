#!/usr/bin/env python3
import sys
sys.path.insert(0, '/usr/lib/python3/dist-packages')

try:
    from passlib.context import CryptContext
    ctx = CryptContext(schemes=['pbkdf2_sha512'])
    password_hash = ctx.hash('admin')
    
    import psycopg2
    conn = psycopg2.connect(
        host='db',
        port=5432,
        user='odoo',
        password='odoo',
        database='sgco1'
    )
    cur = conn.cursor()
    
    # Update password for user id=2 (nhd.hsevn@gmail.com)
    cur.execute("UPDATE res_users SET password = %s WHERE id = 2;", (password_hash,))
    conn.commit()
    
    # Get user info
    cur.execute("SELECT login FROM res_users WHERE id = 2;")
    user_login = cur.fetchone()[0]
    
    print(f"✓ Đã đổi password cho user '{user_login}' thành 'admin'")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

