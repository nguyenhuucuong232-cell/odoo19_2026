# -*- coding: utf-8 -*-
{
    'license': 'LGPL-3',
    'name': "Quản lý Văn bản",
    'summary': "Hệ thống quản lý văn bản doanh nghiệp",
    'author': "SGC Team",
    'website': "https://sgc.vn",
    'support': 'support@sgc.vn',
    'category': 'Document Management',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'views/document.xml',
    ],
    'images': [
        'static/description/main_screenshot.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}