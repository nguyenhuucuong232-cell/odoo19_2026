#!/bin/bash
# Odoo Production Monitoring Script

echo "=== ODOO PRODUCTION MONITORING ==="
echo "Time: $(date)"

# Check services
echo ""
echo "🔍 Service Status:"
docker-compose -f docker-compose.prod.yml ps

# Check database connections
echo ""
echo "🗄️  Database Status:"
DB_CONNECTIONS=$(docker-compose -f docker-compose.prod.yml exec -T db psql -U odoo -d odoo19 -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';" -t)
echo "Active DB connections: $DB_CONNECTIONS"

# Check disk usage
echo ""
echo "💾 Disk Usage:"
df -h | grep -E "(Filesystem|/home)"

# Check memory usage
echo ""
echo "🧠 Memory Usage:"
free -h

# Check Odoo logs for errors
echo ""
echo "📋 Recent Errors (last 10):"
docker-compose -f docker-compose.prod.yml logs --tail=10 odoo19 2>&1 | grep -i error || echo "No recent errors found"

# Check response time
echo ""
echo "⏱️  Response Time Test:"
RESPONSE_TIME=$(curl -s -w "%{time_total}\n" -o /dev/null http://localhost/health 2>/dev/null || echo "N/A")
echo "Health check response time: ${RESPONSE_TIME}s"

echo ""
echo "=== MONITORING COMPLETE ==="
