# Hướng Dẫn Backup và Restore Odoo 19

## Tổng Quan
Hệ thống backup tự động tạo snapshot đầy đủ của Odoo 19 bao gồm:
- Database PostgreSQL
- Filestore (file đính kèm)
- Addons tùy chỉnh
- Cấu hình Docker

## Cấu Trúc Backup
```
bakup_odoo19_DD_MM_YYYY_HH_MM/
├── odoo19_backup_YYYYMMDD_HHMMSS.sql    # Database dump
├── filestore/                            # Thư mục file đính kèm
├── addons/                              # Addons tùy chỉnh
├── etc/                                 # Cấu hình Odoo
└── docker-compose.yml                   # Cấu hình Docker
```

## Cách Sử Dụng

### 1. Tạo Backup
```bash
cd /home/sgc/odoo19
./backup_full.sh
```

### 2. Restore Thủ Công

#### Restore Database
```bash
cd /home/sgc/odoo19
# Dừng Odoo trước khi restore
docker-compose stop odoo19

# Restore database
docker-compose exec -T db psql -U odoo -d odoo < path/to/backup/odoo19_backup_YYYYMMDD_HHMMSS.sql

# Khởi động lại Odoo
docker-compose start odoo19
```

#### Restore Filestore
```bash
cp -r path/to/backup/filestore ../odoo-backups/
```

#### Restore Addons
```bash
cp -r path/to/backup/addons ../odoo19/
```

### 3. Kiểm Tra Backup
```bash
# Kiểm tra kích thước backup
du -sh /home/sgc/file\ luu\ trữ/bakup_odoo19_*

# Kiểm tra file database
head -20 /path/to/backup/odoo19_backup_*.sql
```

## Lưu Ý
- Backup được lưu trong thư mục `/home/sgc/file luu trữ/`
- Tên thư mục có format: `bakup_odoo19_DD_MM_YYYY_HH_MM`
- Luôn backup trước khi thực hiện thay đổi lớn
- Test restore trên môi trường dev trước khi áp dụng production

## Automation
Có thể thêm cron job để backup tự động:
```bash
# Backup hàng ngày lúc 2:00 AM
0 2 * * * /home/sgc/odoo19/backup_full.sh
```