user = env['res.users'].sudo().search([('login', '=', 'admin')], limit=1)
if user:
    user.sudo().write({'password': 'admin'})
    env.cr.commit()
    print(f"✓ Password reset thành công!")
    print(f"  Tài khoản: {user.login}")
    print(f"  Mật khẩu: admin")
else:
    print("✖ Không tìm thấy user admin")

