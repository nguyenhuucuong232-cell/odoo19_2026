#!/usr/bin/env python3
# Script to test UoM configuration after module update

import sys
import os

# Add Odoo to path
sys.path.insert(0, '/usr/lib/python3/dist-packages')

try:
    import odoo
    from odoo.api import Environment
    from odoo.modules.registry import RegistryManager

    # Database connection
    DB_NAME = 'odoo19'
    registry = RegistryManager.get(DB_NAME)
    with registry.cursor() as cr:
        env = Environment(cr, odoo.SUPERUSER_ID, {})

        print("Testing UoM configuration...")

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
                print(f"  - {uom.name} ({uom.uom_type})")
        except Exception as e:
            print(f"✗ Error searching UoM records: {e}")
            sys.exit(1)

        # Test 3: Check if category_id field is removed (should not exist)
        try:
            # Try to access category_id - this should fail if field was removed
            test_uom = uoms[0] if uoms else None
            if test_uom:
                category_id = getattr(test_uom, 'category_id', None)
                if category_id is not None:
                    print("✗ Field category_id still exists - XML fix may not be applied")
                    sys.exit(1)
                else:
                    print("✓ Field category_id successfully removed")
        except Exception as e:
            print(f"✗ Error checking category_id field: {e}")

        print("UoM configuration test completed successfully!")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)