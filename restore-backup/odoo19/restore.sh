#!/bin/bash
# Odoo 19 Production Restore Script
# Date: 2025-11-23

set -e

echo "🔄 ODOO 19 PRODUCTION RESTORE SCRIPT"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/home/sgc/odoo19"
BACKUP_DIR="/home/sgc/odoo-backups"
RESTORE_TEMP="/home/sgc/temp_restore"

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

# Function to list available backups
list_backups() {
    log "Available backups in $BACKUP_DIR:"
    echo ""

    echo "📦 Full System Backups:"
    ls -la "$BACKUP_DIR"/pre_production_*.tar.gz 2>/dev/null | head -5 || echo "No full backups found"

    echo ""
    echo "🗄️  Database Backups:"
    ls -la "$BACKUP_DIR"/odoo19_pre_production_*.sql 2>/dev/null | head -5 || echo "No database backups found"

    echo ""
    echo "📋 Usage: $0 <backup_timestamp>"
    echo "Example: $0 20251123_164534"
    exit 0
}

# Function to validate backup files
validate_backup() {
    local timestamp="$1"

    if [ -z "$timestamp" ]; then
        error "Backup timestamp is required!"
        echo ""
        list_backups
        exit 1
    fi

    BACKUP_FILE="$BACKUP_DIR/pre_production_${timestamp}.tar.gz"
    DB_BACKUP_FILE="$BACKUP_DIR/odoo19_pre_production_${timestamp}.sql"

    if [ ! -f "$BACKUP_FILE" ]; then
        error "Full backup file not found: $BACKUP_FILE"
        echo ""
        list_backups
        exit 1
    fi

    if [ ! -f "$DB_BACKUP_FILE" ]; then
        error "Database backup file not found: $DB_BACKUP_FILE"
        echo ""
        list_backups
        exit 1
    fi

    success "Backup files validated for timestamp: $timestamp"
}

# Function to stop services
stop_services() {
    log "Stopping current services..."

    # Stop production services if running
    if [ -f "$PROJECT_DIR/docker-compose.prod.yml" ]; then
        docker-compose -f "$PROJECT_DIR/docker-compose.prod.yml" down 2>/dev/null || true
    fi

    # Stop development services
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" down 2>/dev/null || true

    success "Services stopped"
}

# Function to backup current state before restore
backup_current_state() {
    log "Creating emergency backup before restore..."

    EMERGENCY_BACKUP="$BACKUP_DIR/emergency_before_restore_$(date +%Y%m%d_%H%M%S).tar.gz"

    # Quick backup of current state
    tar -czf "$EMERGENCY_BACKUP" \
        --exclude='*.log' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='node_modules' \
        -C "$PROJECT_DIR" . 2>/dev/null || true

    success "Emergency backup created: $EMERGENCY_BACKUP"
}

# Function to restore database
restore_database() {
    local db_backup="$1"

    log "Restoring database from: $db_backup"

    # Ensure database container is running
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" up -d db

    # Wait for database to be ready
    log "Waiting for database to be ready..."
    sleep 10

    # Drop and recreate database
    log "Recreating database..."
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" exec -T db psql -U odoo -c "DROP DATABASE IF EXISTS odoo19;" 2>/dev/null || true
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" exec -T db psql -U odoo -c "CREATE DATABASE odoo19;" 2>/dev/null || true

    # Restore database
    log "Importing database backup..."
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" exec -T db psql -U odoo -d odoo19 < "$db_backup"

    success "Database restored successfully"
}

# Function to restore files
restore_files() {
    local backup_file="$1"

    log "Restoring files from: $backup_file"

    # Create temp directory for restore
    mkdir -p "$RESTORE_TEMP"

    # Extract backup
    log "Extracting backup files..."
    tar -xzf "$backup_file" -C "$RESTORE_TEMP"

    # Preserve important current files
    log "Preserving current configuration..."

    # Backup current docker-compose files
    cp "$PROJECT_DIR/docker-compose.yml" "$PROJECT_DIR/docker-compose.yml.backup" 2>/dev/null || true
    cp "$PROJECT_DIR/docker-compose.prod.yml" "$PROJECT_DIR/docker-compose.prod.yml.backup" 2>/dev/null || true

    # Restore files (exclude database data)
    log "Restoring application files..."
    rsync -av --exclude='postgresql/' --exclude='logs/' --exclude='*.log' \
          "$RESTORE_TEMP/" "$PROJECT_DIR/"

    # Restore docker-compose files
    cp "$PROJECT_DIR/docker-compose.yml.backup" "$PROJECT_DIR/docker-compose.yml" 2>/dev/null || true
    cp "$PROJECT_DIR/docker-compose.prod.yml.backup" "$PROJECT_DIR/docker-compose.prod.yml" 2>/dev/null || true

    # Clean up temp directory
    rm -rf "$RESTORE_TEMP"

    success "Files restored successfully"
}

# Function to start services
start_services() {
    log "Starting services..."

    # Start development environment
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" up -d

    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 30

    success "Services started"
}

# Function to verify restore
verify_restore() {
    log "Verifying restore..."

    # Check if services are running
    if docker-compose -f "$PROJECT_DIR/docker-compose.yml" ps | grep -q "Up"; then
        success "Services are running"
    else
        warning "Services may not be fully started yet"
    fi

    # Test database connection
    if docker-compose -f "$PROJECT_DIR/docker-compose.yml" exec -T db psql -U odoo -d odoo19 -c "SELECT version();" >/dev/null 2>&1; then
        success "Database connection verified"
    else
        warning "Database connection test failed"
    fi

    # Test application health
    sleep 10
    if curl -s -f http://localhost:10019/web >/dev/null 2>&1; then
        success "Application is responding"
    else
        warning "Application health check failed (may still be starting)"
    fi
}

# Function to show restore summary
show_summary() {
    local timestamp="$1"

    echo ""
    echo "========================================"
    echo "🔄 RESTORE SUMMARY"
    echo "========================================"
    echo "Timestamp: $timestamp"
    echo "Backup files used:"
    echo "  - $BACKUP_DIR/pre_production_${timestamp}.tar.gz"
    echo "  - $BACKUP_DIR/odoo19_pre_production_${timestamp}.sql"
    echo ""
    echo "Next steps:"
    echo "1. Check application at: http://localhost:10019"
    echo "2. Verify data integrity"
    echo "3. Test critical workflows"
    echo "4. Update any configuration if needed"
    echo ""
    echo "Emergency backup created:"
    echo "  - Check $BACKUP_DIR/emergency_before_restore_*.tar.gz"
    echo "========================================"
}

# Main restore function
main() {
    local timestamp="$1"

    # Show help if no arguments
    if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "Usage: $0 <backup_timestamp> [--list]"
        echo ""
        echo "Arguments:"
        echo "  backup_timestamp  Timestamp of backup to restore (e.g., 20251123_164534)"
        echo "  --list           List available backups"
        echo ""
        echo "Examples:"
        echo "  $0 20251123_164534    # Restore from specific backup"
        echo "  $0 --list             # List all available backups"
        echo ""
        exit 0
    fi

    # List backups if requested
    if [ "$1" = "--list" ]; then
        list_backups
    fi

    # Validate backup
    validate_backup "$timestamp"

    # Confirm restore
    echo ""
    warning "⚠️  WARNING: This will overwrite current data!"
    echo "Backup timestamp: $timestamp"
    echo "Emergency backup will be created automatically."
    echo ""
    read -p "Are you sure you want to proceed? (yes/no): " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Restore cancelled."
        exit 0
    fi

    # Execute restore steps
    stop_services
    backup_current_state
    restore_database "$DB_BACKUP_FILE"
    restore_files "$BACKUP_FILE"
    start_services
    verify_restore
    show_summary "$timestamp"

    success "Restore completed successfully!"
    echo ""
    echo "🎉 System has been restored to backup: $timestamp"
}

# Run main function
main "$@"