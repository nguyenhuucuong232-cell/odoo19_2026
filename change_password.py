#!/usr/bin/env python3
import sys
import psycopg2
import hashlib
import binascii
import secrets

def change_password(dbname, username, new_password):
    """Đổi password cho user trong Odoo database"""
    try:
        # Kết nối database
        conn = psycopg2.connect(
            host='db',
            port=5432,
            user='odoo',
            password='odoo',
            database=dbname
        )
        cur = conn.cursor()
        
        # Tạo password hash theo format Odoo (pbkdf2_sha256)
        salt = secrets.token_hex(16)
        iterations = 600000
        
        password_bytes = new_password.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        
        dk = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, iterations)
        hash_hex = binascii.hexlify(dk).decode('utf-8')
        
        password_hash = f'pbkdf2_sha256${iterations}${salt}${hash_hex}'
        
        # Đổi password
        cur.execute("UPDATE res_users SET password = %s WHERE login = %s OR id = 2", (password_hash, username))
        rows_updated = cur.rowcount
        conn.commit()
        
        if rows_updated > 0:
            print(f"✓ Đã đổi password thành công!")
            print(f"  Database: {dbname}")
            print(f"  Username: {username}")
            print(f"  Password: {new_password}")
        else:
            print(f"⚠ Không tìm thấy user: {username}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

if __name__ == '__main__':
    # Đổi password cho database sgco1
    change_password('sgco1', 'nhd.hsevn@gmail.com', 'admin')
    
    # Đổi password cho database odoo (nếu có)
    try:
        change_password('odoo', 'admin', 'admin')
    except:
        pass

