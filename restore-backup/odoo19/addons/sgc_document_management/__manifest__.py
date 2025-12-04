# -*- coding: utf-8 -*-
{
    'name': 'SGC Document Management',
    'version': '19.0.1.0.0',
    'category': 'Document Management',
    'summary': 'Quản lý văn bản, công văn đi/đến',
    'description': """
        Module quản lý văn bản, công văn:
        - Quản lý công văn đi/đến
        - Workflow xử lý văn bản
        - Theo dõi lịch sử xử lý
        - Tích hợp OnlyOffice để chỉnh sửa tài liệu
    """,
    'author': 'SGC',
    'website': 'https://sgc.vn',
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'data/sgc_document_sequence.xml',
        'security/ir.model.access.csv',
        'wizard/sgc_document_wizard_views.xml',
        'views/sgc_document_status_views.xml',
        'views/sgc_document_type_views.xml',
        'views/sgc_document_views.xml',
        'views/sgc_document_dashboard_views.xml',
        'views/sgc_document_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sgc_document_management/static/src/js/document_dashboard.js',
            'sgc_document_management/static/src/xml/document_dashboard_template.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

