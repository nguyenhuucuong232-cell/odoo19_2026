#!/usr/bin/env python3
# Script to create UoMs in Odoo
# Run with: docker-compose exec odoo19 odoo shell -d odoo19 < create_uoms.py

# Find or create Unit category
unit_category = env['uom.category'].search([('name', '=', 'Unit')], limit=1)
if not unit_category:
    unit_category = env['uom.category'].create({'name': 'Unit'})

# Create UoMs
uoms_to_create = [
    {'name': 'Lần', 'category_id': unit_category.id, 'uom_type': 'reference', 'factor': 1.0},
    {'name': 'Chỉ tiêu', 'category_id': unit_category.id, 'uom_type': 'reference', 'factor': 1.0},
    {'name': 'Mẫu', 'category_id': unit_category.id, 'uom_type': 'reference', 'factor': 1.0},
    {'name': 'Gói', 'category_id': unit_category.id, 'uom_type': 'reference', 'factor': 1.0}
]

for uom_data in uoms_to_create:
    env['uom.uom'].create(uom_data)

print('UoM created successfully')