#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to fix website attachments by converting store_fname to db_datas
or removing broken file references
"""

import subprocess

DB_NAME = 'odoo19'
DB_USER = 'odoo'
DB_CONTAINER = 'odoo19-db-1'

def run_sql(query):
    """Execute SQL query"""
    cmd = [
        'docker', 'exec', '-i', DB_CONTAINER,
        'psql', '-U', DB_USER, '-d', DB_NAME
    ]
    
    try:
        result = subprocess.run(
            cmd,
            input=query,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

print("=" * 60)
print("Fixing Website Attachments")
print("=" * 60)

# Step 1: Count attachments with store_fname
print("\nStep 1: Checking attachments...")
result = run_sql("SELECT COUNT(*) FROM ir_attachment WHERE website_id IS NOT NULL AND store_fname IS NOT NULL;")
if result:
    print(result.strip())

# Step 2: Update attachments to remove store_fname (force Odoo to use db_datas or regenerate)
print("\nStep 2: Removing store_fname from website attachments...")
result = run_sql("""
    UPDATE ir_attachment 
    SET store_fname = NULL 
    WHERE website_id IS NOT NULL 
    AND store_fname IS NOT NULL
    AND (db_datas IS NOT NULL OR type = 'url');
""")
if result:
    print("  Updated attachments")

# Step 3: Delete attachments that have neither db_datas nor valid store_fname
print("\nStep 3: Cleaning up broken attachments...")
result = run_sql("""
    DELETE FROM ir_attachment 
    WHERE website_id IS NOT NULL 
    AND store_fname IS NOT NULL 
    AND db_datas IS NULL 
    AND type != 'url';
""")
if result:
    print("  Cleaned up broken attachments")

# Step 4: Verify
print("\nStep 4: Verifying...")
result = run_sql("SELECT COUNT(*) FROM ir_attachment WHERE website_id IS NOT NULL AND store_fname IS NOT NULL;")
if result:
    count = result.strip().split()[-1]
    print(f"  Remaining attachments with store_fname: {count}")

print("\n" + "=" * 60)
print("Fix completed!")
print("=" * 60)
print("\nPlease restart Odoo to rebuild assets.")

