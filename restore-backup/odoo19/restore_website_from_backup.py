#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to restore website data from backup SQL file
Extracts website-related tables and imports them into current database
"""

import subprocess
import sys
import re
from datetime import datetime

BACKUP_FILE = '/home/sgc/odoo19/backups/odoo19_db_20251124_082003.sql'
DB_NAME = 'odoo19'
DB_USER = 'odoo'
DB_HOST = 'db'
DB_PORT = '5432'

# Tables to restore (in order due to foreign keys)
TABLES = [
    'ir_ui_view',
    'website_page',
    'website_menu',
    'ir_attachment',  # Only website-related attachments
]

def extract_table_data(sql_file, table_name):
    """Extract COPY data for a specific table from SQL backup"""
    print(f"Extracting {table_name}...")
    
    # Find the line number where COPY starts
    result = subprocess.run(
        ['grep', '-n', f'COPY public.{table_name}', sql_file],
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        print(f"  Warning: {table_name} not found in backup")
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

def delete_website_data(table_name):
    """Delete website-related data from current database"""
    print(f"Deleting old {table_name} data...")
    
    if table_name == 'ir_ui_view':
        # Delete only website views
        query = "DELETE FROM ir_ui_view WHERE website_id IS NOT NULL OR type = 'qweb';"
    elif table_name == 'website_page':
        query = "DELETE FROM website_page;"
    elif table_name == 'website_menu':
        query = "DELETE FROM website_menu;"
    elif table_name == 'ir_attachment':
        # Delete only website attachments
        query = "DELETE FROM ir_attachment WHERE website_id IS NOT NULL;"
    else:
        query = f"DELETE FROM {table_name};"
    
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
        print("  Error: Could not find database container")
        return False
    
    cmd = [
        'docker', 'exec', '-i', db_container,
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
        print(f"  Deleted from {table_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error deleting {table_name}: {e.stderr}")
        return False

def import_table_data(table_data):
    """Import table data into database"""
    if not table_data:
        return False
    
    print("Importing data...")
    
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
        print("  Error: Could not find database container")
        return False
    
    cmd = [
        'docker', 'exec', '-i', db_container,
        'psql', '-U', DB_USER, '-d', DB_NAME
    ]
    
    try:
        result = subprocess.run(
            cmd,
            input=table_data,
            capture_output=True,
            text=True,
            check=True
        )
        print("  Import successful")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error importing: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("Website Data Restore Script")
    print("=" * 60)
    print(f"Backup file: {BACKUP_FILE}")
    print(f"Database: {DB_NAME}")
    print()
    
    # Step 1: Extract and import each table
    for table in TABLES:
        print(f"\n--- Processing {table} ---")
        
        # Extract data from backup
        table_data = extract_table_data(BACKUP_FILE, table)
        
        if table_data:
            # Delete old data
            if not delete_website_data(table):
                print(f"  Warning: Failed to delete old {table} data")
                continue
            
            # Import new data
            if import_table_data(table_data):
                print(f"  ✓ {table} restored successfully")
            else:
                print(f"  ✗ Failed to restore {table}")
        else:
            print(f"  ✗ No data found for {table}")
    
    print("\n" + "=" * 60)
    print("Restore process completed!")
    print("=" * 60)
    print("\nPlease restart Odoo server to see the changes.")
    print("You may need to clear browser cache (Ctrl+F5)")

if __name__ == '__main__':
    main()

