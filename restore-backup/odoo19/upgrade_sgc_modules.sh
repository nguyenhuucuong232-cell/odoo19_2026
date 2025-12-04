#!/bin/bash
# Script to upgrade all SGC modules

MODULES=(
    "sgc_activity_dashboard"
    "sgc_activity_reminder"
    "sgc_hr_reward_warning"
    "sgc_crm_sale"
    "sgc_account_payment"
    "sgc_approval_management"
    "sgc_document_management"
    "sgc_onlyoffice"
    "sgc_kpi"
)

echo "Upgrading SGC modules..."

for module in "${MODULES[@]}"; do
    echo "Upgrading $module..."
    docker exec odoo19_odoo_1 /mnt/extra-addons/odoo-src/odoo-bin -c /mnt/extra-addons/etc/odoo.conf -u "$module" --stop-after-init 2>&1 | tail -20
done

echo "Done!"

