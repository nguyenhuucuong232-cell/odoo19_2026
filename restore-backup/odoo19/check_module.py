from odoo import modules
print('Module state:', modules.get_module_info('sgc_management_core')['state'])