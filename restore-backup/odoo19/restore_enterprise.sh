#!/bin/bash

echo "=== Restoring Odoo 19 Enterprise Database ==="

# Step 1: Stop Odoo
echo "Step 1: Stopping Odoo..."
docker stop odoo19_odoo19_1

# Step 2: Extract dump
echo "Step 2: Extracting dump file..."
rm -rf /tmp/odoo_restore
mkdir -p /tmp/odoo_restore
cd /tmp/odoo_restore
unzip -o "/home/sgc/file luu trữ/sgco1.dump.zip"

# Step 3: Drop and recreate database
echo "Step 3: Recreating database..."
docker exec odoo19-db-1 psql -U odoo -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'odoo19' AND pid <> pg_backend_pid();"
docker exec odoo19-db-1 psql -U odoo -d postgres -c "DROP DATABASE IF EXISTS odoo19;"
docker exec odoo19-db-1 psql -U odoo -d postgres -c "CREATE DATABASE odoo19 WITH OWNER odoo ENCODING 'UTF8' TEMPLATE template0;"

# Step 4: Restore database
echo "Step 4: Restoring database from dump..."
docker cp /tmp/odoo_restore/dump.sql odoo19-db-1:/tmp/dump.sql
docker exec odoo19-db-1 psql -U odoo -d odoo19 -f /tmp/dump.sql > /dev/null 2>&1

# Step 5: Copy filestore
echo "Step 5: Copying filestore..."
rm -rf /home/sgc/odoo19/data/filestore/odoo19
mkdir -p /home/sgc/odoo19/data/filestore
cp -r /tmp/odoo_restore/filestore /home/sgc/odoo19/data/filestore/odoo19

# Step 6: Check original user
echo "Step 6: Checking original user account..."
docker exec odoo19-db-1 psql -U odoo -d odoo19 -c "SELECT id, login FROM res_users WHERE active = true;"

# Step 7: Set password for original user (id=2)
echo "Step 7: Setting password 'admin' for main user..."
docker exec odoo19-db-1 psql -U odoo -d odoo19 -c "UPDATE res_users SET password = 'admin' WHERE id = 2;"

# Step 8: Cleanup
echo "Step 8: Cleaning up..."
rm -rf /tmp/odoo_restore
docker exec odoo19-db-1 rm -f /tmp/dump.sql

# Step 9: Start Odoo
echo "Step 9: Starting Odoo..."
docker start odoo19_odoo19_1

echo ""
echo "=== DONE! ==="
echo "Please wait 10 seconds for Odoo to start..."
sleep 10

# Show login info
echo ""
echo "=== LOGIN INFO ==="
docker exec odoo19-db-1 psql -U odoo -d odoo19 -c "SELECT login as 'Username' FROM res_users WHERE id = 2;"
echo "Password: admin"
echo ""
echo "Access Odoo at: http://100.122.93.102:10019"

