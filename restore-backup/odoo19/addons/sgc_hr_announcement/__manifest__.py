# -*- coding: utf-8 -*-
{
    'name': 'SGC HR Announcement',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Quản lý thông báo nhân sự',
    'description': """
        Module quản lý thông báo nhân sự:
        - Tạo thông báo cho nhân viên, phòng ban, vị trí công việc
        - Quy trình phê duyệt thông báo
        - Tự động hết hạn thông báo
        - Đính kèm tài liệu
    """,
    'author': 'SGC',
    'website': 'https://sgc.vn',
    'depends': ['hr', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/cron_data.xml',
        'views/hr_announcement_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}

