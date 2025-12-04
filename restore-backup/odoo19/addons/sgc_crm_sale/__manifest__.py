# -*- coding: utf-8 -*-
{
    'name': 'SGC CRM Sale',
    'version': '19.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Tự động chuyển giai đoạn CRM và thông báo',
    'description': """
        Module mở rộng CRM với các tính năng:
        - Tự động chuyển giai đoạn sau thời gian định trước
        - Thông báo nhắc nhở trước khi hết hạn giai đoạn
        - Quản lý workflow CRM linh hoạt
    """,
    'author': 'SGC',
    'website': 'https://sgc.vn',
    'depends': ['base', 'crm', 'mail'],
    'data': [
        'views/crm_stage_views.xml',
        'data/ir_cron.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
