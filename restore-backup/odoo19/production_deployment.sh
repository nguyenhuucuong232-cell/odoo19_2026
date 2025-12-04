#!/bin/bash
# Production Deployment Script for Odoo 19
# Date: 2025-11-23

set -e

echo "🚀 ODOO 19 PRODUCTION DEPLOYMENT SCRIPT"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/home/sgc/odoo19"
BACKUP_DIR="/home/sgc/odoo-backups"
DOMAIN="odoo.yourdomain.com"
EMAIL="admin@yourdomain.com"

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to backup current setup
backup_current_setup() {
    log "Creating backup before production deployment..."
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="$BACKUP_DIR/pre_production_$TIMESTAMP.tar.gz"

    mkdir -p "$BACKUP_DIR"

    # Backup database
    log "Backing up database..."
    docker-compose exec -T db pg_dump -U odoo odoo19 > "$BACKUP_DIR/odoo19_pre_production_$TIMESTAMP.sql"

    # Backup configuration and data
    log "Backing up configuration and data..."
    tar -czf "$BACKUP_FILE" \
        --exclude='*.log' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='postgresql' \
        --exclude='node_modules' \
        -C "$PROJECT_DIR" .

    success "Backup created: $BACKUP_FILE"
}

# Function to update production configuration
update_production_config() {
    log "Updating production configuration..."

    # Update docker-compose.yml for production
    cat > "$PROJECT_DIR/docker-compose.prod.yml" << EOF
version: '3.8'
services:
  db:
    image: postgres:18
    user: root
    environment:
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=${ODOO_DB_PASSWORD:-odoo19@2025}
      - POSTGRES_DB=odoo19
    restart: always
    volumes:
      - ./postgresql:/var/lib/postgresql/18/docker
      - ./postgresql/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "127.0.0.1:5432:5432"  # Only bind to localhost for security
    command: postgres -c shared_buffers=256MB -c work_mem=4MB -c maintenance_work_mem=64MB -c checkpoint_segments=32

  odoo19:
    image: odoo:19
    user: root
    depends_on:
      - db
    ports:
      - "127.0.0.1:8069:8069"  # Bind to localhost only
    tty: true
    command: --log-level=warn --workers=2 --max-cron-threads=1 --addons-path=/mnt/enterprise-addons,/mnt/extra-addons
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=${ODOO_DB_PASSWORD:-odoo19@2025}
      - PIP_BREAK_SYSTEM_PACKAGES=1
      - PYTHONUNBUFFERED=1
      - ODOO_SESSION_REDIS=1
    volumes:
      - ./entrypoint.sh:/entrypoint.sh
      - ./odoo-enterprise/src/odoo/addons:/mnt/enterprise-addons
      - ./addons:/mnt/extra-addons
      - ./etc:/etc/odoo
      - ./logs:/var/log/odoo
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8069/web/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - odoo19
    restart: always

  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - ./redis:/data
EOF

    success "Production docker-compose.yml created"
}

# Function to setup SSL certificates
setup_ssl() {
    log "Setting up SSL certificates..."

    mkdir -p "$PROJECT_DIR/nginx/ssl"

    # Create self-signed certificate for testing (replace with Let's Encrypt in production)
    if ! [ -f "$PROJECT_DIR/nginx/ssl/odoo.crt" ]; then
        log "Creating self-signed SSL certificate..."
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout "$PROJECT_DIR/nginx/ssl/odoo.key" \
            -out "$PROJECT_DIR/nginx/ssl/odoo.crt" \
            -subj "/C=VN/ST=HoChiMinh/L=HoChiMinh/O=SGC/OU=IT/CN=$DOMAIN"
        success "SSL certificate created"
    else
        success "SSL certificate already exists"
    fi
}

# Function to create nginx configuration
create_nginx_config() {
    log "Creating Nginx configuration..."

    mkdir -p "$PROJECT_DIR/nginx"

    cat > "$PROJECT_DIR/nginx/nginx.conf" << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    upstream odoo {
        server odoo19:8069;
    }

    server {
        listen 80;
        server_name _;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name _;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/odoo.crt;
        ssl_certificate_key /etc/nginx/ssl/odoo.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';" always;

        # Proxy settings
        proxy_read_timeout 720s;
        proxy_connect_timeout 720s;
        proxy_send_timeout 720s;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Handle static files
        location /web/static/ {
            proxy_pass http://odoo;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Rate limit for API calls
        location /web/dataset/call_kw {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://odoo;
        }

        # Rate limit for login attempts
        location /web/login {
            limit_req zone=login burst=10 nodelay;
            proxy_pass http://odoo;
        }

        # Main proxy
        location / {
            proxy_pass http://odoo;
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF

    success "Nginx configuration created"
}

# Function to create systemd service
create_systemd_service() {
    log "Creating systemd service..."

    # Only create if we have sudo access
    if sudo -n true 2>/dev/null; then
        cat > "/tmp/odoo19.service" << EOF
[Unit]
Description=Odoo 19 Production Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
ExecReload=/usr/bin/docker-compose -f docker-compose.prod.yml restart
TimeoutStartSec=300
TimeoutStopSec=60

[Install]
WantedBy=multi-user.target
EOF
        sudo mv "/tmp/odoo19.service" "/etc/systemd/system/odoo19.service"
        success "Systemd service created"
    else
        warning "No sudo access - skipping systemd service creation"
        cat > "$PROJECT_DIR/odoo19.service" << EOF
[Unit]
Description=Odoo 19 Production Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
ExecReload=/usr/bin/docker-compose -f docker-compose.prod.yml restart
TimeoutStartSec=300
TimeoutStopSec=60

[Install]
WantedBy=multi-user.target
EOF
        success "Systemd service template created (run with sudo to install)"
    fi
}

# Function to create monitoring script
create_monitoring_script() {
    log "Creating monitoring script..."

    cat > "$PROJECT_DIR/monitor.sh" << 'EOF'
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
EOF

    chmod +x "$PROJECT_DIR/monitor.sh"
    success "Monitoring script created"
}

# Function to create backup script
create_backup_script() {
    log "Creating automated backup script..."

    cat > "$PROJECT_DIR/backup.sh" << EOF
#!/bin/bash
# Automated Backup Script for Odoo Production

BACKUP_DIR="$BACKUP_DIR"
TIMESTAMP=\$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="\$BACKUP_DIR/odoo19_backup_\$TIMESTAMP.tar.gz"
DB_BACKUP="\$BACKUP_DIR/odoo19_db_\$TIMESTAMP.sql"

echo "🔄 Starting automated backup: \$TIMESTAMP"

# Create backup directory
mkdir -p "\$BACKUP_DIR"

# Backup database
echo "📦 Backing up database..."
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U odoo odoo19 > "\$DB_BACKUP"

# Backup filestore and configuration
echo "📦 Backing up files and configuration..."
tar -czf "\$BACKUP_FILE" \\
    --exclude='*.log' \\
    --exclude='__pycache__' \\
    --exclude='.git' \\
    -C "$PROJECT_DIR" .

# Compress database backup
gzip "\$DB_BACKUP"

# Cleanup old backups (keep last 7 days)
echo "🧹 Cleaning up old backups..."
find "\$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
find "\$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete

echo "✅ Backup completed: \$BACKUP_FILE"
echo "📊 Backup size: \$(du -sh "\$BACKUP_FILE" | cut -f1)"
EOF

    chmod +x "$PROJECT_DIR/backup.sh"
    success "Backup script created"
}

# Function to create deployment checklist
create_deployment_checklist() {
    log "Creating deployment checklist..."

    cat > "$PROJECT_DIR/PRODUCTION_CHECKLIST.md" << 'EOF'
# 🚀 ODOO 19 PRODUCTION DEPLOYMENT CHECKLIST

## Pre-Deployment Checklist
- [ ] Database backup completed
- [ ] SSL certificates configured
- [ ] Domain DNS configured
- [ ] Firewall rules updated
- [ ] Server security hardened
- [ ] Monitoring tools configured

## Deployment Steps
1. [ ] Run backup script: `./backup.sh`
2. [ ] Stop development environment: `docker-compose down`
3. [ ] Start production environment: `docker-compose -f docker-compose.prod.yml up -d`
4. [ ] Verify services are running: `docker-compose -f docker-compose.prod.yml ps`
5. [ ] Test application access: `curl -k https://yourdomain.com/health`
6. [ ] Configure automated backups: `crontab -e` (add: `0 2 * * * /path/to/backup.sh`)
7. [ ] Setup monitoring: `crontab -e` (add: `*/5 * * * * /path/to/monitor.sh`)

## Post-Deployment Verification
- [ ] Application loads correctly
- [ ] Database connections working
- [ ] SSL certificate valid
- [ ] Email notifications working
- [ ] Scheduled jobs running
- [ ] Backup system operational
- [ ] Monitoring alerts configured

## Security Checklist
- [ ] Admin password changed
- [ ] Debug mode disabled
- [ ] Default accounts removed
- [ ] File permissions correct
- [ ] Database access restricted
- [ ] Firewall configured
- [ ] SSL/TLS enabled
- [ ] Security headers set

## Performance Optimization
- [ ] Database indexes optimized
- [ ] Caching configured
- [ ] CDN setup for static files
- [ ] Load balancer configured (if needed)
- [ ] Monitoring dashboards created

## Emergency Contacts
- System Administrator: admin@yourdomain.com
- Database Administrator: dba@yourdomain.com
- Hosting Provider: support@hosting.com

## Rollback Plan
1. Stop production services: `docker-compose -f docker-compose.prod.yml down`
2. Restore from backup: `./restore.sh <backup_file>`
3. Start development environment: `docker-compose up -d`
4. Verify rollback successful

---
*Generated on: 2025-11-23*
EOF

    success "Deployment checklist created"
}

# Main deployment function
main() {
    log "Starting Odoo 19 Production Deployment..."

    # Pre-deployment checks
    if [ ! -d "$PROJECT_DIR" ]; then
        error "Project directory $PROJECT_DIR does not exist!"
        exit 1
    fi

    # Execute deployment steps
    backup_current_setup
    update_production_config
    setup_ssl
    create_nginx_config
    create_systemd_service
    create_monitoring_script
    create_backup_script
    create_deployment_checklist

    success "Production deployment preparation completed!"
    echo ""
    warning "Next steps:"
    echo "1. Review and customize the generated configuration files"
    echo "2. Update domain name and SSL certificates"
    echo "3. Test the configuration: docker-compose -f docker-compose.prod.yml config"
    echo "4. Run the deployment checklist: cat PRODUCTION_CHECKLIST.md"
    echo "5. Execute deployment when ready"
}

# Run main function
main "$@"
EOF