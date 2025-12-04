#!/usr/bin/env python3
import sys
import os

# Add Odoo to path
sys.path.insert(0, '/usr/lib/python3/dist-packages')

import odoo
from odoo import api, SUPERUSER_ID

# Configure Odoo
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf'])

db_name = 'sgco1'

try:
    # Initialize Odoo
    odoo.service.db.exp_db()
    
    # Get registry
    registry = odoo.registry(db_name)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Find user
        user = env['res.users'].sudo().search([('login', '=', 'nhd.hsevn@gmail.com')], limit=1)
        
        if not user:
            user = env['res.users'].sudo().search([('login', '=', 'admin')], limit=1)
        
        if user:
            # Reset password using Odoo's method
            user.sudo().write({'password': 'admin'})
            cr.commit()
            print(f"✓ Password đã được reset thành công!")
            print(f"  Tài khoản: {user.login}")
            print(f"  Mật khẩu: admin")
            print(f"  ID: {user.id}")
        else:
            print("✖ Không tìm thấy user")
            # List all users
            all_users = env['res.users'].sudo().search([])
            print("\nDanh sách users trong database:")
            for u in all_users:
                print(f"  - ID: {u.id}, Login: {u.login}, Active: {u.active}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

