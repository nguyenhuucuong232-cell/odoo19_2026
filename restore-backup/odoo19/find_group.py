#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host="db",
    database="odoo19",
    user="odoo",
    password="odoo19@2025"
)
cur = conn.cursor()
cur.execute("SELECT id, name FROM res_groups WHERE name LIKE %s", ('%Quản lý Tài liệu%',))
rows = cur.fetchall()
for row in rows:
    print(row)
cur.close()
conn.close()