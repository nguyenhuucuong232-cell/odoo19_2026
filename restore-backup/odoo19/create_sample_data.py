#!/usr/bin/env python3
# Script to create sample data for Odoo 19
# Run with: docker-compose exec odoo19 odoo shell -d odoo19 -c /etc/odoo/odoo.conf < create_sample_data.py
# Or run directly: python create_sample_data.py

import random
import sys
import os
from datetime import datetime, timedelta

# Check if running in Odoo shell or directly
try:
    # Try to access env - if it exists, we're in Odoo shell
    env
    IN_ODOO_SHELL = True
except NameError:
    # env not defined, need to initialize Odoo
    IN_ODOO_SHELL = False

if not IN_ODOO_SHELL:
    # Initialize Odoo when running directly
    import odoo
    from odoo.api import Environment
    from odoo.tools import config

    # Load configuration
    config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'odoo19'])

    # Initialize Odoo
    odoo.cli.main.setup()

    # Get database connection
    dbname = config['db_name'] or 'odoo19'
    registry = odoo.registry(dbname)

    # Create environment
    with registry.cursor() as cr:
        env = Environment(cr, 1, {})  # uid=1 (admin user)
else:
    # Already in Odoo shell, env is available
    pass

def create_sample_data():
    # In Odoo shell, 'env' is available in the global scope
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

    # Commit projects to database
    env.cr.commit()
    print("Projects created and committed successfully!")

    # Skip purchase requisitions - not available in community edition
    print("Skipping purchase requisitions - not available in community edition")

    # Create sample stock pickings (receipts)
    print("Creating sample stock pickings...")
    picking_types = env['stock.picking.type'].search([('code', '=', 'incoming')])
    print(f"Found {len(picking_types)} incoming picking types")
    if picking_types:
        picking_type = picking_types[0]
        print(f"Using picking type: {picking_type.name} (ID: {picking_type.id})")

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
            try:
                # Random state: draft, waiting, confirmed, assigned, done, cancel
                states = ['draft', 'waiting', 'confirmed', 'assigned', 'done', 'cancel']
                state = random.choice(states)

                # Get locations with fallbacks
                supplier_location = env['stock.location'].search([('usage', '=', 'supplier')], limit=1)
                internal_location = env['stock.location'].search([('usage', '=', 'internal')], limit=1)

                if not supplier_location:
                    print(f"Warning: No supplier location found, skipping picking {name}")
                    continue
                if not internal_location:
                    print(f"Warning: No internal location found, skipping picking {name}")
                    continue

                picking_data = {
                    'name': f"{name} #{i}",
                    'picking_type_id': picking_type.id,
                    'state': state,
                    'scheduled_date': (datetime.now() + timedelta(days=random.randint(0, 14))).strftime('%Y-%m-%d %H:%M:%S'),
                    'origin': f"PO{i:03d}",
                    'partner_id': random.choice(partner_ids) if random.choice([True, False]) else False,
                    'location_id': supplier_location.id,
                    'location_dest_id': internal_location.id,
                }

                picking = env['stock.picking'].create(picking_data)
                print(f"Created stock picking: {picking.name} (State: {picking.state})")
            except Exception as e:
                print(f"Error creating picking {name}: {str(e)}")

        # Commit pickings to database
        env.cr.commit()
        print("Stock pickings created and committed successfully!")

    else:
        print("No incoming picking types found!")

    print("Stock pickings creation completed!")

    print("Sample data creation completed!")

def main():
    """Main function to run the script"""
    if not IN_ODOO_SHELL:
        # When running directly, we need to handle the database transaction
        with registry.cursor() as cr:
            env = Environment(cr, 1, {})  # uid=1 (admin user)
            create_sample_data()
            cr.commit()
    else:
        # When in Odoo shell, just run the function
        create_sample_data()

if __name__ == '__main__':
    main()
else:
    # Run the function when executed through Odoo shell
    create_sample_data()