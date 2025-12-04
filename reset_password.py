#!/usr/bin/env python3
import sys
import os

# Add Odoo to path
sys.path.insert(0, '/usr/lib/python3/dist-packages')

import odoo
from odoo import api, SUPERUSER_ID

# Parse config
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'sgco1'])

# Initialize database
odoo.service.db.exp_db()
registry = odoo.registry(odoo.tools.config['db_name'])

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    user = env['res.users'].browse(2)
    user.password = 'admin'
    cr.commit()
    print(f"✓ Đã đổi password cho user '{user.login}' thành 'admin'")

