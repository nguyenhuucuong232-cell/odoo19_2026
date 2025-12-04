#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để kích hoạt các module Odoo từ hình ảnh (trừ Zalo)
"""

import xmlrpc.client

# Thông tin kết nối Odoo
url = 'http://localhost:10019'
db = 'odoo19'
username = 'admin'
password = 'admin'

# Kết nối đến Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("❌ Không thể kết nối đến Odoo!")
    exit(1)

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Danh sách các module cần kích hoạt (từ hình ảnh, trừ Zalo)
modules_to_install = [
    # Core modules
    'base',
    'web',
    'mail',
    
    # Activities & Overview
    'mail_activity',
    'board',  # Trang tổng quan
    
    # Accounting & Finance
    'account',
    'account_accountant',
    'account_reports',
    
    # HR & Payroll
    'hr',
    'hr_payroll',
    'hr_recruitment',
    'hr_holidays',
    'hr_attendance',
    'hr_timesheet',
    'hr_expense',
    
    # Sales & CRM
    'crm',
    'sale',
    'sale_management',
    'sale_crm',
    
    # Documents & Knowledge
    'documents',
    'knowledge',
    
    # Projects
    'project',
    'project_timesheet',
    
    # Inventory & Purchases
    'stock',
    'purchase',
    'stock_barcode',
    
    # Website
    'website',
    'website_sale',
    
    # Marketing (trừ Zalo)
    'marketing_automation',
    'mass_mailing',
    'sms',
    'whatsapp',
    
    # Communication
    'im_livechat',
    'mail',
    'discuss',
    
    # Calendar & Planning
    'calendar',
    'calendar_sms',
    'planning',
    
    # Appointments
    'appointment',
    'appointment_crm',
    
    # Support
    'helpdesk',
    'helpdesk_timesheet',
    
    # E-learning
    'website_slides',
    
    # Events & Surveys
    'event',
    'event_sale',
    'survey',
    
    # Fleet
    'fleet',
    
    # Maintenance & Repairs
    'maintenance',
    'repair',
    
    # Contacts
    'contacts',
    
    # Reports
    'account_reports',
    
    # To-do
    'project_todo',
    
    # KPI Dashboard
    'spreadsheet_dashboard',
    
    # Signed Contracts (SGC custom)
    'sgc_management_core',
]

# Loại trừ các module Zalo
excluded_modules = ['zalo', 'zalo_marketing', 'zalo_crm', 'zalo_sale']

# Lọc bỏ các module Zalo
modules_to_install = [m for m in modules_to_install if not any(zalo in m.lower() for zalo in excluded_modules)]

print("="*80)
print("🔄 BẮT ĐẦU KÍCH HOẠT CÁC MODULE")
print("="*80)
print(f"📋 Tổng số module cần kích hoạt: {len(modules_to_install)}")
print(f"🚫 Đã loại trừ: Zalo modules")
print()

# Kiểm tra và cài đặt từng module
installed_count = 0
failed_modules = []

for module_name in modules_to_install:
    try:
        # Kiểm tra module có tồn tại không
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[('name', '=', module_name)]])
        
        if not module_ids:
            print(f"⚠️  Module '{module_name}' không tồn tại, bỏ qua...")
            continue
        
        module = models.execute_kw(db, uid, password,
            'ir.module.module', 'read',
            [module_ids], {'fields': ['name', 'state']})[0]
        
        if module['state'] == 'installed':
            print(f"✓ {module_name}: Đã được cài đặt")
            installed_count += 1
        elif module['state'] == 'uninstalled':
            print(f"📦 {module_name}: Đang cài đặt...")
            models.execute_kw(db, uid, password,
                'ir.module.module', 'button_immediate_install',
                [[module_ids[0]]])
            print(f"✅ {module_name}: Đã cài đặt thành công")
            installed_count += 1
        else:
            print(f"ℹ️  {module_name}: Trạng thái '{module['state']}'")
            
    except Exception as e:
        print(f"❌ {module_name}: Lỗi - {str(e)}")
        failed_modules.append(module_name)

print()
print("="*80)
print("📊 KẾT QUẢ")
print("="*80)
print(f"✅ Đã cài đặt thành công: {installed_count} module")
if failed_modules:
    print(f"❌ Module lỗi: {len(failed_modules)}")
    for m in failed_modules:
        print(f"   - {m}")
print("="*80)


