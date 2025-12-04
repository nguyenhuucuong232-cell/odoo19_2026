#!/bin/bash
# Script backup report template

REPORT_FILE="/home/sgc/odoo19/addons/sgc_management_core/report/report_sale_order_sgc.xml"
BACKUP_DIR="/home/sgc/odoo19/backups/reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$BACKUP_DIR"

# Backup
cp "$REPORT_FILE" "$BACKUP_DIR/report_sale_order_sgc_${TIMESTAMP}.xml"

echo "✅ Đã backup report template vào:"
echo "   $BACKUP_DIR/report_sale_order_sgc_${TIMESTAMP}.xml"
echo ""
echo "Để restore lại:"
echo "   cp $BACKUP_DIR/report_sale_order_sgc_${TIMESTAMP}.xml $REPORT_FILE"
echo "   python3 scripts/upgrade_sgc_module.py"

