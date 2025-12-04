#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to check all modules, workflows, and subsystems
"""

import subprocess
import sys

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
    sys.exit(1)

def run_sql(query):
    """Execute SQL query"""
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
        return result.stdout
    except subprocess.CalledProcessError as e:
        return None

print("=" * 80)
print("KIỂM TRA TOÀN BỘ MODULE, LUỒNG VÀ PHÂN HỆ")
print("=" * 80)
print()

# 1. Kiểm tra modules đã cài
print("1. TRẠNG THÁI CÁC MODULE SGC:")
print("-" * 80)
result = run_sql("""
    SELECT name, state, latest_version 
    FROM ir_module_module 
    WHERE name LIKE 'sgc_%' 
    ORDER BY name;
""")
if result:
    print(result)

# 2. Kiểm tra dependencies
print("\n2. KIỂM TRA DEPENDENCIES:")
print("-" * 80)
result = run_sql("""
    SELECT m.name, d.name as dependency, d.state as dep_state
    FROM ir_module_module m
    JOIN ir_module_module_dependency dep ON m.id = dep.module_id
    JOIN ir_module_module d ON dep.name = d.name
    WHERE m.name LIKE 'sgc_%' AND d.state != 'installed'
    ORDER BY m.name, d.name;
""")
if result and result.strip() and 'rows)' in result:
    print("  ⚠ Có dependencies chưa được cài:")
    print(result)
else:
    print("  ✓ Tất cả dependencies đã được cài đặt")

# 3. Kiểm tra models
print("\n3. KIỂM TRA MODELS:")
print("-" * 80)
result = run_sql("""
    SELECT model, COUNT(*) as count
    FROM ir_model
    WHERE model LIKE 'sgc.%'
    GROUP BY model
    ORDER BY model;
""")
if result:
    print(result)

# 4. Kiểm tra views
print("\n4. KIỂM TRA VIEWS:")
print("-" * 80)
result = run_sql("""
    SELECT model, type, COUNT(*) as count
    FROM ir_ui_view
    WHERE model LIKE 'sgc.%'
    GROUP BY model, type
    ORDER BY model, type;
""")
if result:
    print(result)

# 5. Kiểm tra actions
print("\n5. KIỂM TRA ACTIONS:")
print("-" * 80)
result = run_sql("""
    SELECT res_model, COUNT(*) as count
    FROM ir_actions_act_window
    WHERE res_model LIKE 'sgc.%'
    GROUP BY res_model
    ORDER BY res_model;
""")
if result:
    print(result)

# 6. Kiểm tra menus
print("\n6. KIỂM TRA MENUS:")
print("-" * 80)
result = run_sql("""
    SELECT complete_name, action
    FROM ir_ui_menu
    WHERE complete_name LIKE '%SGC%' OR complete_name LIKE '%sgc%'
    ORDER BY sequence
    LIMIT 20;
""")
if result:
    print(result)

# 7. Kiểm tra workflows (ir_actions_server)
print("\n7. KIỂM TRA WORKFLOWS (Server Actions):")
print("-" * 80)
result = run_sql("""
    SELECT name, model_name, state, COUNT(*) as count
    FROM ir_actions_server
    WHERE model_name LIKE 'sgc.%'
    GROUP BY name, model_name, state
    ORDER BY model_name;
""")
if result and result.strip() and 'rows)' in result:
    print(result)
else:
    print("  (Không có server actions)")

# 8. Kiểm tra cron jobs
print("\n8. KIỂM TRA CRON JOBS:")
print("-" * 80)
result = run_sql("""
    SELECT name, model_id, active, interval_number, interval_type
    FROM ir_cron
    WHERE model_id IN (SELECT id FROM ir_model WHERE model LIKE 'sgc.%')
    ORDER BY name;
""")
if result and result.strip() and 'rows)' in result:
    print(result)
else:
    print("  (Không có cron jobs)")

# 9. Kiểm tra security rules
print("\n9. KIỂM TRA SECURITY RULES:")
print("-" * 80)
result = run_sql("""
    SELECT name, model_id, active, COUNT(*) as count
    FROM ir_rule
    WHERE model_id IN (SELECT id FROM ir_model WHERE model LIKE 'sgc.%')
    GROUP BY name, model_id, active
    ORDER BY model_id;
""")
if result and result.strip() and 'rows)' in result:
    print(result)
else:
    print("  (Không có security rules)")

# 10. Kiểm tra lỗi trong database
print("\n10. KIỂM TRA LỖI TRONG DATABASE:")
print("-" * 80)
result = run_sql("""
    SELECT COUNT(*) as error_count
    FROM ir_ui_view
    WHERE arch_db IS NULL OR arch_db = '';
""")
if result:
    print(result)

print("\n" + "=" * 80)
print("KIỂM TRA HOÀN TẤT")
print("=" * 80)

