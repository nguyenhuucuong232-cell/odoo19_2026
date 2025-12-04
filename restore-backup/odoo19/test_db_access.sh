#!/bin/bash
# Script test truy cập database odoo19_web

echo "=== TEST TRUY CẬP DATABASE odoo19_web ==="
echo ""

# Test 1: Kiểm tra database tồn tại
echo "1. Kiểm tra database tồn tại..."
EXISTS=$(docker exec odoo19-db-1 psql -U odoo -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='odoo19_web';" 2>&1)
if [ "$EXISTS" = "1" ]; then
    echo "   ✓ Database tồn tại"
else
    echo "   ✗ Database không tồn tại"
    exit 1
fi

# Test 2: Kiểm tra có bảng
echo "2. Kiểm tra database đã init..."
TABLES=$(docker exec odoo19-db-1 psql -U odoo -d odoo19_web -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>&1)
if [ "$TABLES" -gt "0" ]; then
    echo "   ✓ Database đã init ($TABLES bảng)"
else
    echo "   ✗ Database chưa init"
    exit 1
fi

# Test 3: Kiểm tra có user admin
echo "3. Kiểm tra user admin..."
ADMIN=$(docker exec odoo19-db-1 psql -U odoo -d odoo19_web -tAc "SELECT COUNT(*) FROM res_users WHERE login='admin' AND active=true;" 2>&1)
if [ "$ADMIN" = "1" ]; then
    echo "   ✓ User admin tồn tại"
else
    echo "   ✗ User admin không tồn tại"
    exit 1
fi

# Test 4: Test truy cập Odoo
echo "4. Test truy cập Odoo..."
RESPONSE=$(docker exec odoo19_odoo19_1 curl -s -o /dev/null -w "%{http_code}" "http://localhost:8069/web?db=odoo19_web" 2>&1)
if [ "$RESPONSE" = "200" ] || [ "$RESPONSE" = "303" ] || [ "$RESPONSE" = "302" ]; then
    echo "   ✓ Odoo phản hồi (HTTP $RESPONSE)"
else
    echo "   ✗ Odoo không phản hồi (HTTP $RESPONSE)"
fi

echo ""
echo "=== KẾT QUẢ ==="
echo "Database odoo19_web đã sẵn sàng!"
echo ""
echo "URL truy cập: http://100.122.93.102:10019/web?db=odoo19_web"
echo "Username: admin"
echo "Password: admin"

