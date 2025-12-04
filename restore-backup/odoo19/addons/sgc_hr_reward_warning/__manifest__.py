# -*- coding: utf-8 -*-
{
    'name': 'SGC HR Reward & Warning',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Quản lý khen thưởng, kỷ luật và thông báo nhân sự',
    'description': """
        Module quản lý thông báo, khen thưởng và kỷ luật nhân sự.
        - Tạo và quản lý thông báo chung
        - Thông báo theo nhân viên, phòng ban hoặc vị trí công việc
        - Quy trình phê duyệt thông báo
        - Tự động hết hạn thông báo
    """,
    'author': 'SGC',
    'website': 'https://sgc.vn',
    'depends': ['base', 'hr', 'mail', 'sgc_hr_announcement'],
    'data': [
        'security/sgc_reward_security.xml',
        'security/ir.model.access.csv',
        # Thông báo nhân sự sử dụng model/view từ module sgc_hr_announcement
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}

