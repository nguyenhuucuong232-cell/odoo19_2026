#!/bin/bash

echo "=== Setting admin password and Installing SGC Modules ==="

# Step 1: Set password using Odoo shell
echo "Step 1: Setting password for admin user..."
docker exec odoo19_odoo19_1 odoo shell -d odoo19 --stop-after-init << 'PYEOF'
user = env['res.users'].browse(2)
user.password = 'admin'
env.cr.commit()
print(f"Password set for user: {user.login}")
PYEOF

# Step 2: Update module list
echo "Step 2: Updating module list..."
docker exec odoo19_odoo19_1 odoo -d odoo19 --stop-after-init -u base

# Step 3: Install all SGC modules
echo "Step 3: Installing SGC modules..."
MODULES="sgc_management_core,sgc_activity_dashboard,sgc_approval_management,sgc_account_payment,sgc_crm_sale,sgc_document_management,sgc_hr_announcement,sgc_hr_reward_warning,sgc_kpi,sgc_onlyoffice"

docker exec odoo19_odoo19_1 odoo -d odoo19 -i $MODULES --stop-after-init

# Step 4: Restart Odoo
echo "Step 4: Restarting Odoo..."
docker restart odoo19_odoo19_1

echo ""
echo "=== DONE! ==="
echo ""
echo "Login info:"
echo "  Username: nhd.hsevn@gmail.com"
echo "  Password: admin"
echo ""
echo "Access Odoo at: http://100.122.93.102:10019"

