#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cải tiến để kích hoạt các module Odoo với retry logic
"""

import xmlrpc.client
import time

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
    'mail_activity',
    'board',
    
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
    'project_todo',
    
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
    
    # KPI Dashboard
    'spreadsheet_dashboard',
    
    # Signed Contracts (SGC custom)
    'sgc_management_core',
]

# Loại trừ các module Zalo
excluded_modules = ['zalo', 'zalo_marketing', 'zalo_crm', 'zalo_sale']
modules_to_install = [m for m in modules_to_install if not any(zalo in m.lower() for zalo in excluded_modules)]

def install_module(module_name, retry_count=3):
    """Cài đặt module với retry logic"""
    for attempt in range(retry_count):
        try:
            # Kiểm tra module có tồn tại không
            module_ids = models.execute_kw(db, uid, password,
                'ir.module.module', 'search',
                [[('name', '=', module_name)]])
            
            if not module_ids:
                return False, f"Module không tồn tại"
            
            module = models.execute_kw(db, uid, password,
                'ir.module.module', 'read',
                [module_ids], {'fields': ['name', 'state']})[0]
            
            if module['state'] == 'installed':
                return True, "Đã được cài đặt"
            
            if module['state'] == 'uninstalled':
                # Đợi một chút trước khi cài đặt
                if attempt > 0:
                    wait_time = 5 * attempt
                    print(f"   ⏳ Đợi {wait_time}s trước khi thử lại...")
                    time.sleep(wait_time)
                
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'button_immediate_install',
                    [[module_ids[0]]])
                return True, "Đã cài đặt thành công"
            
            return False, f"Trạng thái: {module['state']}"
            
        except Exception as e:
            error_msg = str(e)
            if 'LockNotAvailable' in error_msg or 'scheduled action' in error_msg.lower():
                if attempt < retry_count - 1:
                    wait_time = 10 * (attempt + 1)
                    print(f"   ⏳ Odoo đang xử lý scheduled action, đợi {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                return False, "Odoo đang xử lý scheduled action, vui lòng thử lại sau"
            return False, error_msg
    
    return False, "Đã thử lại nhiều lần nhưng vẫn lỗi"

print("="*80)
print("🔄 BẮT ĐẦU KÍCH HOẠT CÁC MODULE (Với Retry Logic)")
print("="*80)
print(f"📋 Tổng số module cần kích hoạt: {len(modules_to_install)}")
print(f"🚫 Đã loại trừ: Zalo modules")
print()

installed_count = 0
already_installed = 0
failed_modules = []
pending_modules = []

for module_name in modules_to_install:
    print(f"📦 {module_name}...", end=" ")
    success, message = install_module(module_name)
    
    if success:
        if "Đã được cài đặt" in message:
            print(f"✓ {message}")
            already_installed += 1
        else:
            print(f"✅ {message}")
            installed_count += 1
        # Đợi một chút giữa các module để tránh lock
        time.sleep(2)
    else:
        if "scheduled action" in message.lower():
            print(f"⏸️  {message}")
            pending_modules.append(module_name)
        else:
            print(f"❌ {message}")
            failed_modules.append((module_name, message))

print()
print("="*80)
print("📊 KẾT QUẢ")
print("="*80)
print(f"✅ Đã cài đặt mới: {installed_count} module")
print(f"✓ Đã được cài đặt trước đó: {already_installed} module")
if pending_modules:
    print(f"⏸️  Module cần thử lại sau (do scheduled action): {len(pending_modules)}")
    for m in pending_modules:
        print(f"   - {m}")
if failed_modules:
    print(f"❌ Module lỗi: {len(failed_modules)}")
    for m, err in failed_modules:
        print(f"   - {m}: {err[:100]}")
print("="*80)
print()
if pending_modules:
    print("💡 Để cài đặt các module còn lại, chạy lại script sau vài phút:")
    print("   python3 activate_modules_v2.py")

