#!/usr/bin/env python3
import subprocess
import time
import sys

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", 1
    except Exception as e:
        return "", str(e), 1

print("=" * 50)
print("  KIỂM TRA VÀ SỬA LỖI ODOO")
print("=" * 50)

# 1. Kiểm tra Docker
print("\n[1/6] Kiểm tra Docker...")
stdout, stderr, code = run_cmd("docker info")
if code != 0:
    print("✖ Docker chưa chạy. Vui lòng khởi động Docker Desktop.")
    sys.exit(1)
print("✓ Docker đang chạy")

# 2. Kiểm tra containers
print("\n[2/6] Kiểm tra containers...")
stdout, stderr, code = run_cmd("cd /Users/nguyenhuucuong/Downloads/dockerodoo19 && docker compose ps")
print(stdout)
if "odoo-19-enterprise" not in stdout or "Up" not in stdout:
    print("\n[3/6] Containers chưa chạy, đang khởi động...")
    stdout, stderr, code = run_cmd("cd /Users/nguyenhuucuong/Downloads/dockerodoo19 && docker compose up -d")
    print(stdout)
    if stderr:
        print("STDERR:", stderr)
    print("Đang chờ containers khởi động (20 giây)...")
    time.sleep(20)
else:
    print("\n[3/6] Containers đang chạy")

# 4. Kiểm tra logs
print("\n[4/6] Kiểm tra logs Odoo...")
stdout, stderr, code = run_cmd("docker logs odoo-19-enterprise --tail 30 2>&1")
if stdout:
    print(stdout[-500:])  # Last 500 chars
if "ERROR" in stdout or "CRITICAL" in stdout:
    print("⚠ Có lỗi trong logs")

# 5. Kiểm tra kết nối
print("\n[5/6] Kiểm tra kết nối HTTP...")
stdout, stderr, code = run_cmd("curl -s -o /dev/null -w '%{http_code}' http://localhost:10019/web/login")
if stdout == "200":
    print("✓ Odoo đang phản hồi (HTTP 200)")
elif stdout == "000" or code != 0:
    print("✖ Odoo không phản hồi")
    print("Đang thử restart...")
    run_cmd("cd /Users/nguyenhuucuong/Downloads/dockerodoo19 && docker compose restart odoo")
    time.sleep(15)
    stdout, stderr, code = run_cmd("curl -s -o /dev/null -w '%{http_code}' http://localhost:10019/web/login")
    if stdout == "200":
        print("✓ Đã sửa! Odoo đang phản hồi")
    else:
        print(f"✖ Vẫn chưa được (HTTP {stdout})")
else:
    print(f"⚠ HTTP Status: {stdout}")

# 6. Thông tin đăng nhập
print("\n[6/6] Thông tin:")
print("=" * 50)
print("URL: http://localhost:10019/web/login")
print("Database: sgco1")
print("Tài khoản: nhd.hsevn@gmail.com")
print("Mật khẩu: admin")
print("=" * 50)

