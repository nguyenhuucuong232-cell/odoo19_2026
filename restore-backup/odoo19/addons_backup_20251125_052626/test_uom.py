#!/usr/bin/env python3
# Script to test UoM configuration after module update

import sys
import os

try:
    import odoo
    from odoo.api import Environment
    from odoo import tools
    from odoo.service import db

    # Set up configuration
    config = tools.config
    config['db_name'] = 'odoo19'
    config['db_host'] = 'db'
    config['db_user'] = 'odoo'
    config['db_password'] = 'odoo19@2025'

    print("Testing UoM configuration...")

    # Test with registry
    with db.cursor() as cr:
        env = Environment(cr, odoo.SUPERUSER_ID, {})

        # Test 1: Check if uom.uom model exists
        try:
            uom_model = env['uom.uom']
            print("✓ Model uom.uom exists")
        except Exception as e:
            print(f"✗ Model uom.uom error: {e}")
            sys.exit(1)

        # Test 2: Check if we can search UoM records
        try:
            uoms = env['uom.uom'].search([], limit=5)
            print(f"✓ Found {len(uoms)} UoM records")
            for uom in uoms:
                print(f"  - {uom.name} ({getattr(uom, 'uom_type', 'N/A')})")
        except Exception as e:
            print(f"✗ Error searching UoM records: {e}")
            sys.exit(1)

        # Test 3: Check if category_id field is removed
        try:
            test_uom = uoms[0] if uoms else None
            if test_uom:
                # Check if category_id field exists
                if hasattr(test_uom, 'category_id'):
                    print("✗ Field category_id still exists - XML fix may not be applied")
                    sys.exit(1)
                else:
                    print("✓ Field category_id successfully removed")
        except Exception as e:
            print(f"✗ Error checking category_id field: {e}")

        print("UoM configuration test completed successfully!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)