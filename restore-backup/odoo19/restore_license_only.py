#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to restore only license-related data from dump file
Keeps all existing modules and data intact
"""

import subprocess
import re

DUMP_FILE = '/home/sgc/odoo19/backups/sgco1_dump_extracted/dump.sql'
DB_NAME = 'odoo19'
DB_USER = 'odoo'

# Find database container
result = subprocess.run(
    ['docker', 'ps', '--format', '{{.Names}}'],
    capture_output=True,
    text=True
)
containers = result.stdout.strip().split('\n')
db_container = None
for c in containers:
    if 'db' in c.lower() or 'postgres' in c.lower():
        db_container = c
        break

if not db_container:
    print("Error: Could not find database container")
    exit(1)

def extract_table_data(sql_file, table_name):
    """Extract COPY data for a specific table from SQL dump"""
    print(f"Extracting {table_name}...")
    
    # Find the line number where COPY starts
    result = subprocess.run(
        ['grep', '-n', f'COPY public.{table_name}', sql_file],
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        print(f"  Warning: {table_name} not found in dump")
        return None
    
    start_line = int(result.stdout.split(':')[0])
    
    # Read the SQL file and extract COPY block
    with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    # Find the COPY statement
    copy_start = None
    for i, line in enumerate(lines[start_line-1:], start=start_line-1):
        if f'COPY public.{table_name}' in line:
            copy_start = i
            break
    
    if copy_start is None:
        print(f"  Error: Could not find COPY statement for {table_name}")
        return None
    
    # Extract COPY block (from COPY to \.)
    copy_lines = []
    in_copy = False
    
    for i in range(copy_start, len(lines)):
        line = lines[i]
        if f'COPY public.{table_name}' in line:
            in_copy = True
            copy_lines.append(line)
        elif in_copy:
            copy_lines.append(line)
            if line.strip() == '\\.':
                break
    
    return ''.join(copy_lines)

def update_license_data(table_name, table_data):
    """Update license data in database"""
    if not table_data:
        return False
    
    print(f"Updating {table_name}...")
    
    # For ir_config_parameter, we'll update only license-related keys
    if table_name == 'ir_config_parameter':
        # Extract license keys from dump (all database.* keys)
        license_keys = ['database.enterprise_code', 'database.expiration_date', 
                       'database.uuid', 'database.expiration_reason', 'database.secret',
                       'database.create_date', 'database.already_linked_email',
                       'database.already_linked_send_mail_url', 'database.already_linked_subscription_url']
        
        # Delete existing license keys (all database.* keys)
        delete_query = """
            DELETE FROM ir_config_parameter 
            WHERE key LIKE 'database.%';
        """
        
        cmd = [
            'docker', 'exec', '-i', db_container,
            'psql', '-U', DB_USER, '-d', DB_NAME
        ]
        
        try:
            subprocess.run(cmd, input=delete_query, capture_output=True, text=True, check=True)
            print("  Deleted existing license keys")
        except subprocess.CalledProcessError as e:
            print(f"  Error deleting: {e.stderr}")
            return False
        
        # Extract and insert only license-related rows (all database.* keys)
        lines = table_data.split('\n')
        license_rows = []
        in_data = False
        
        for line in lines:
            if 'COPY public.ir_config_parameter' in line:
                in_data = True
                license_rows.append(line)
            elif in_data and line.strip() and not line.strip().startswith('\\'):
                # Check if this row contains database.* key
                if '\tdatabase.' in line or line.startswith('database.'):
                    license_rows.append(line)
            elif in_data and line.strip() == '\\.':
                license_rows.append(line)
                break
        
        if len(license_rows) > 1:
            license_data = '\n'.join(license_rows)
            try:
                result = subprocess.run(
                    cmd,
                    input=license_data,
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"  ✓ License keys restored")
                return True
            except subprocess.CalledProcessError as e:
                print(f"  Error importing: {e.stderr}")
                return False
        else:
            print("  No license keys found in dump")
            return False
    
    elif table_name == 'res_company':
        # For res_company, we might need to update license info
        # But be careful not to overwrite company data
        print("  Skipping res_company (to preserve current company data)")
        return True
    
    return False

def main():
    print("=" * 60)
    print("Restore License Data Only")
    print("=" * 60)
    print(f"Dump file: {DUMP_FILE}")
    print(f"Database: {DB_NAME}")
    print()
    
    # Step 1: Extract ir_config_parameter (contains license keys)
    print("\n--- Processing License Data ---")
    
    table_data = extract_table_data(DUMP_FILE, 'ir_config_parameter')
    
    if table_data:
        if update_license_data('ir_config_parameter', table_data):
            print("  ✓ License data restored successfully")
        else:
            print("  ✗ Failed to restore license data")
    else:
        print("  ✗ No license data found in dump")
    
    print("\n" + "=" * 60)
    print("Restore completed!")
    print("=" * 60)
    print("\nPlease restart Odoo server to apply license changes.")
    print("You may need to clear browser cache (Ctrl+F5)")

if __name__ == '__main__':
    main()

