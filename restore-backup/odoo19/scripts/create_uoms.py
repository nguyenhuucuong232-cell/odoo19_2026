#!/usr/bin/env python3
# Script to create missing UoMs in Odoo 19

import odoo
from odoo import api, SUPERUSER_ID
from odoo.api import Environment

# Connect to Odoo
odoo.tools.config.parse_config(['--config', '/etc/odoo/odoo.conf'])
db_name = 'odoo19'  # Replace with your DB name
with api.Environment.manage():
    registry = odoo.registry(db_name)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Get UoM categories
        unit_category = env['uom.category'].search([('name', '=', 'Unit')], limit=1)
        if not unit_category:
            unit_category = env['uom.category'].create({'name': 'Unit'})

        weight_category = env['uom.category'].search([('name', '=', 'Weight')], limit=1)
        if not weight_category:
            weight_category = env['uom.category'].create({'name': 'Weight'})

        # Create missing UoMs
        uoms_to_create = [
            {'name': 'Lần', 'category_id': unit_category.id, 'uom_type': 'reference', 'factor': 1.0, 'rounding': 1.0},
            {'name': 'Chỉ tiêu', 'category_id': unit_category.id, 'uom_type': 'reference', 'factor': 1.0, 'rounding': 1.0},
            {'name': 'Mẫu', 'category_id': unit_category.id, 'uom_type': 'reference', 'factor': 1.0, 'rounding': 1.0},
            {'name': 'Gói', 'category_id': unit_category.id, 'uom_type': 'reference', 'factor': 1.0, 'rounding': 1.0},
        ]

        for uom_data in uoms_to_create:
            if not env['uom.uom'].search([('name', '=', uom_data['name'])]):
                env['uom.uom'].create(uom_data)
                print(f"Created UoM: {uom_data['name']}")

        print("UoM creation completed.")