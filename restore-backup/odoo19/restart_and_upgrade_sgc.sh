#!/bin/bash
# Script to restart Odoo and upgrade SGC modules

echo "=== Restarting Odoo container ==="
docker restart odoo19_odoo_1

echo "Waiting for Odoo to start..."
sleep 10

echo "=== Upgrading SGC Activity Dashboard ==="
docker exec odoo19_odoo_1 /mnt/extra-addons/odoo-src/odoo-bin -c /mnt/extra-addons/etc/odoo.conf -u sgc_activity_dashboard --stop-after-init

echo ""
echo "=== Done! ==="
echo "Please check Odoo interface to verify the fix."
echo "If errors persist, check:"
echo "1. Browser console (F12)"
echo "2. Odoo logs: docker logs odoo19_odoo_1"

