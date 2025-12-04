#!/usr/bin/env python3
import sys
import os

# Add Odoo to path
sys.path.insert(0, '/usr/lib/python3/dist-packages')

# Import Odoo
import odoo
from odoo import api, SUPERUSER_ID

# Set up minimal config
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_port'] = 5432
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'
odoo.tools.config['db_name'] = 'sgco1'

db_name = 'sgco1'

try:
    # Initialize Odoo registry
    with odoo.api.Environment.manage():
        registry = odoo.registry(db_name)
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            
            # Find user
            user = env['res.users'].sudo().search([('login', '=', 'nhd.hsevn@gmail.com')], limit=1)
            
            if user:
                # Use Odoo's password setter
                user.sudo().password = 'admin'
                cr.commit()
                print(f"✓ Password reset thành công!")
                print(f"  Tài khoản: {user.login}")
                print(f"  Mật khẩu: admin")
            else:
                print("✖ Không tìm thấy user nhd.hsevn@gmail.com")
                all_users = env['res.users'].sudo().search([])
                print("\nDanh sách users:")
                for u in all_users:
                    print(f"  - {u.login} (ID: {u.id}, Active: {u.active})")
                    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
