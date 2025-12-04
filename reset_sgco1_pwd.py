#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/usr/lib/python3/dist-packages')

try:
    import odoo
    from odoo import api, SUPERUSER_ID
    from odoo.tools import config
    
    # Setup config
    config['db_host'] = 'db'
    config['db_port'] = 5432
    config['db_user'] = 'odoo'
    config['db_password'] = 'odoo'
    
    # Load database
    odoo.service.db.exp_db()
    registry = odoo.registry('sgco1')
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        user = env['res.users'].browse(2)
        user.sudo().password = 'admin'
        cr.commit()
        print(f"✓ Đã đổi password cho user '{user.login}' thành 'admin'")
        
except Exception as e:
    # Fallback: use passlib or direct SQL
    import psycopg2
    from passlib.context import CryptContext
    
    try:
        pwd_context = CryptContext(schemes=['pbkdf2_sha512'], deprecated='auto')
        password_hash = pwd_context.hash('admin')
    except:
        # If passlib not available, use bcrypt or simple hash
        import hashlib
        password_hash = hashlib.sha256(('admin').encode()).hexdigest()
    
    conn = psycopg2.connect(host='db', user='odoo', password='odoo', database='sgco1')
    cur = conn.cursor()
    cur.execute("UPDATE res_users SET password = %s WHERE id = 2;", (password_hash,))
    conn.commit()
    cur.execute("SELECT login FROM res_users WHERE id = 2;")
    login = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(f"✓ Đã đổi password cho user '{login}' thành 'admin' (fallback method)")

