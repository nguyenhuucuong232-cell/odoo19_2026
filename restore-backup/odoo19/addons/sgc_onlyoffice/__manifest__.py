# -*- coding: utf-8 -*-
{
    'name': 'SGC OnlyOffice Integration',
    'version': '19.0.1.0.0',
    'category': 'Document Management',
    'summary': 'Tích hợp OnlyOffice để chỉnh sửa tài liệu trực tuyến',
    'description': """
        Module tích hợp OnlyOffice Document Server:
        - Chỉnh sửa tài liệu Office trực tuyến (docx, xlsx, pptx)
        - Xem trước tài liệu
        - Cộng tác chỉnh sửa thời gian thực
    """,
    'author': 'SGC',
    'website': 'https://sgc.vn',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/ir_attachment_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sgc_onlyoffice/static/src/js/onlyoffice_widget.js',
            'sgc_onlyoffice/static/src/css/onlyoffice.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

