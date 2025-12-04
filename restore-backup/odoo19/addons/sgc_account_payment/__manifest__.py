# -*- coding: utf-8 -*-
{
    'name': 'SGC Account Payment',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Quản lý giao dịch thanh toán mở rộng',
    'description': """
        Module quản lý giao dịch thanh toán mở rộng:
        - Quản lý thanh toán thu/chi
        - Phân loại danh mục thanh toán
        - Theo dõi chi tiết từng dòng thanh toán
        - Báo cáo thanh toán
    """,
    'author': 'SGC',
    'website': 'https://sgc.vn',
    'depends': ['base', 'account', 'crm', 'analytic'],
    'data': [
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        'views/sgc_payment_views.xml',
        'views/sgc_item_category_views.xml',
        'views/sgc_item_detail_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
