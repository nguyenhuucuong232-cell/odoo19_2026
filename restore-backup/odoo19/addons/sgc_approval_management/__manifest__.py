# -*- coding: utf-8 -*-
{
    'name': 'SGC Approval Management',
    'version': '19.0.1.0.0',
    'category': 'Approvals',
    'summary': 'Quản lý phê duyệt đơn hàng và yêu cầu',
    'description': """
        Module quản lý phê duyệt:
        - Phê duyệt đơn bán hàng
        - Phê duyệt theo cấp độ
        - Quy trình phê duyệt linh hoạt
        - Theo dõi lịch sử phê duyệt
    """,
    'author': 'SGC',
    'website': 'https://sgc.vn',
    'depends': ['base', 'sale_management', 'mail', 'hr'],
    'data': [
        'security/sgc_approval_security.xml',
        'security/ir.model.access.csv',
        'data/sgc_approval_data.xml',
        'wizard/sgc_approval_wizard_views.xml',
        'views/sgc_approval_category_views.xml',
        'views/sgc_approval_request_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

