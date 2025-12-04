#!/usr/bin/env python3
# Script to create sample data for Odoo 19
# Run with: docker-compose exec odoo19 odoo shell -d odoo19 -c /etc/odoo/odoo.conf < create_sample_data.py

import random
from datetime import datetime, timedelta

# This script runs in Odoo shell context where 'env' is available

# Get valid user IDs
user_ids = env['res.users'].search([]).ids
if not user_ids:
    user_ids = [1]  # fallback

# Get valid partner IDs
partner_ids = env['res.partner'].search([]).ids
if not partner_ids:
    partner_ids = [1]  # fallback

# Create sample projects (15 projects)
print("Creating 15 sample projects...")
project_names = [
    "Dự án Phát triển Phần mềm ERP",
    "Dự án Tư vấn CNTT",
    "Dự án Thiết kế Website",
    "Dự án Mobile App",
    "Dự án AI/ML",
    "Dự án Blockchain",
    "Dự án IoT",
    "Dự án Cloud Migration",
    "Dự án DevOps",
    "Dự án QA Testing",
    "Dự án Data Analytics",
    "Dự án Cybersecurity",
    "Dự án E-commerce",
    "Dự án CRM System",
    "Dự án HR Management"
]

for i, name in enumerate(project_names, 1):
    # Random status - projects don't have state field, just create with different dates
    project_data = {
        'name': f"{name} #{i}",
        'date_start': (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
        'date': (datetime.now() + timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d'),
        'user_id': random.choice(user_ids),  # Random valid user
        'partner_id': random.choice(partner_ids) if random.choice([True, False]) else False,  # Random partner
        'company_id': 1,  # Set company to main company
    }

    project = env['project.project'].create(project_data)
    print(f"Created project: {project.name}")

print("Projects created successfully!")

# Skip purchase requisitions - not available in community edition
print("Skipping purchase requisitions - not available in community edition")

# Create sample stock pickings (receipts)
print("Creating sample stock pickings...")
picking_types = env['stock.picking.type'].search([('code', '=', 'incoming')])
if picking_types:
    picking_type = picking_types[0]

    picking_names = [
        "Nhập kho máy tính",
        "Nhập kho phần mềm",
        "Nhập kho thiết bị mạng",
        "Nhập kho văn phòng phẩm",
        "Nhập kho server",
        "Nhập kho license",
        "Nhập kho thiết bị bảo mật",
        "Nhập kho dụng cụ",
        "Nhập kho sách kỹ thuật",
        "Nhập kho training materials"
    ]

    for i, name in enumerate(picking_names, 1):
        # Random state: draft, waiting, confirmed, assigned, done, cancel
        states = ['draft', 'waiting', 'confirmed', 'assigned', 'done', 'cancel']
        state = random.choice(states)

        picking_data = {
            'name': f"{name} #{i}",
            'picking_type_id': picking_type.id,
            'state': state,
            'scheduled_date': (datetime.now() + timedelta(days=random.randint(0, 14))).strftime('%Y-%m-%d %H:%M:%S'),
            'origin': f"PO{i:03d}",
            'partner_id': random.choice(partner_ids) if random.choice([True, False]) else False,
            'location_id': env['stock.location'].search([('usage', '=', 'supplier')], limit=1).id,
            'location_dest_id': env['stock.location'].search([('usage', '=', 'internal')], limit=1).id,
        }

        picking = env['stock.picking'].create(picking_data)
        print(f"Created stock picking: {picking.name} (State: {picking.state})")

print("Stock pickings created successfully!")

print("Sample data creation completed!")