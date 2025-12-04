#!/usr/bin/env python3

import sys
import os

# Thêm đường dẫn Odoo
sys.path.insert(0, '/usr/lib/python3/dist-packages')
sys.path.insert(0, '/mnt/extra-addons')

# Import Odoo
import odoo
from odoo import api, SUPERUSER_ID
from odoo.api import Environment

# Khởi tạo Odoo
odoo.tools.config.parse_config(['--config', '/etc/odoo/odoo.conf'])
odoo.service.server.start(preload=[], stop=True)

# Tạo environment
with api.Environment.manage():
    env = api.Environment(odoo.registry('odoo').cursor(), SUPERUSER_ID, {})

    # Tìm user admin
    admin_user = env['res.users'].search([('login', '=', 'admin')])
    if admin_user:
        print(f'Found admin user: {admin_user.id}')

        # Tìm nhóm Quản trị viên (ID 24)
        admin_group = env['res.groups'].browse(24)
        print(f'Found admin group: {admin_group.id} - {admin_group.name}')

        # Kiểm tra xem admin đã trong nhóm chưa
        existing_relations = env['res.groups.users.rel'].search([
            ('uid', '=', admin_user.id),
            ('gid', '=', admin_group.id)
        ])

        if not existing_relations:
            # Thêm user vào nhóm
            env['res.groups.users.rel'].create({
                'uid': admin_user.id,
                'gid': admin_group.id
            })
            print('Đã thêm user admin vào nhóm Quản trị viên')
        else:
            print('User admin đã có trong nhóm Quản trị viên')
    else:
        print('Không tìm thấy user admin')

print('Hoàn thành')