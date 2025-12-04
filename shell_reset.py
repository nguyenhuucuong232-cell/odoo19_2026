env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
user = env['res.users'].sudo().search([('login', '=', 'nhd.hsevn@gmail.com')], limit=1)
if user:
    user.sudo().write({'password': 'admin'})
    cr.commit()
    print(f"✓ Password reset thành công!")
    print(f"  Tài khoản: {user.login}")
    print(f"  Mật khẩu: admin")
else:
    print("✖ Không tìm thấy user")
    all_users = env['res.users'].sudo().search([])
    print("\nDanh sách users:")
    for u in all_users:
        print(f"  - {u.login} (ID: {u.id}, Active: {u.active})")

