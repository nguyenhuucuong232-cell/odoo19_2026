#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/usr/lib/python3/dist-packages')

import odoo
from odoo import api

# Setup
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'sgco1'])
odoo.service.db.exp_db()

registry = odoo.registry('sgco1')
with registry.cursor() as cr:
    env = api.Environment(cr, 1, {})
    user = env['res.users'].browse(2)
    user.password = 'admin'
    cr.commit()
    print(f"✓ Đã đổi password cho user '{user.login}' thành 'admin'")

