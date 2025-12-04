#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '/mnt/enterprise-addons')
sys.path.insert(0, '/mnt/extra-addons')

import odoo
from odoo import api, SUPERUSER_ID

# Cấu hình Odoo
odoo.tools.config.parse_config(['--config=/etc/odoo/odoo.conf'])
db_name = odoo.tools.config['db_name']

# Khởi tạo registry
registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Tìm user admin
    admin_user = env['res.users'].search([('login', '=', 'admin')])
    if admin_user:
        print(f'✓ Tìm thấy user admin: {admin_user.login}')

        # Lấy group Administrator
        admin_group = env['res.groups'].search([('name', 'ilike', 'Administrator')])
        if admin_group:
            print(f'✓ Tìm thấy group Administrator: {admin_group.name}')

            # Thêm user vào group Administrator
            if admin_group not in admin_user.groups_id:
                admin_user.write({'groups_id': [(4, admin_group.id)]})
                print('✓ Đã thêm admin vào group Administrator')
            else:
                print('✓ Admin đã có trong group Administrator')

        # Lấy group Technical Features
        tech_group = env['res.groups'].search([('name', 'ilike', 'Technical Features')])
        if tech_group:
            if tech_group not in admin_user.groups_id:
                admin_user.write({'groups_id': [(4, tech_group.id)]})
                print('✓ Đã thêm admin vào group Technical Features')
            else:
                print('✓ Admin đã có trong group Technical Features')

        # Lấy group Access Rights
        access_group = env['res.groups'].search([('name', 'ilike', 'Access Rights')])
        if access_group:
            if access_group not in admin_user.groups_id:
                admin_user.write({'groups_id': [(4, access_group.id)]})
                print('✓ Đã thêm admin vào group Access Rights')
            else:
                print('✓ Admin đã có trong group Access Rights')

        # Liệt kê tất cả groups của admin
        print('\n📋 Danh sách groups hiện tại của admin:')
        for group in admin_user.groups_id:
            print(f'  • {group.name}')

        print('\n✅ Hoàn thành! User admin đã có đầy đủ quyền Administrator.')
    else:
        print('❌ Không tìm thấy user admin!')