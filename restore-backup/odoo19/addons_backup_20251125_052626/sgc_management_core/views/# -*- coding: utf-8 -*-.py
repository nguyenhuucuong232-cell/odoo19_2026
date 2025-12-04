# -*- coding: utf-8 -*-
{
    'name': "Quản lý hợp đồng đã ký",

    'summary': """
        Module quản lý hợp đồng đã ký giữa công ty và khách hàng""",

    'description': """
        Module này giúp theo dõi và quản lý các hợp đồng đã ký giữa công ty và khách hàng. 
        Các tính năng chính bao gồm:
        - Tạo mới, chỉnh sửa, xóa hợp đồng đã ký.
        - Theo dõi trạng thái hợp đồng (Đã ký, Đang hoạt động, Hoàn thành).
        - Liên kết hợp đồng với đơn bán hàng và dự án.
        - Quản lý thời gian và giá trị hợp đồng.
    """,

    'author': "Công ty TNHH ABC",
    'website': "http://www.example.com",

    'category': 'Quản lý',
    'version': '1.0',

    'depends': [
        'base',
        'mail',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/signed_contract_views.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}