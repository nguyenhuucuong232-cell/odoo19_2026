module = env['ir.module.module'].search([('name', '=', 'sgc_management_core')])
if module:
    print('Module state:', module.state)
else:
    print('Module not found')