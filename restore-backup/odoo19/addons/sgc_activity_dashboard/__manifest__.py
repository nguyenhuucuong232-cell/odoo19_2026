# -*- coding: utf-8 -*-
{
    'name': 'SGC Activity Dashboard',
    'version': '19.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Dashboard quản lý hoạt động công việc và nhắc nhở',
    'description': """
        Module quản lý và theo dõi hoạt động (Activities) với Dashboard trực quan.
        - Xem tổng quan các hoạt động: đã lên kế hoạch, hôm nay, quá hạn, hoàn thành
        - Lọc theo người dùng, phòng ban, khoảng thời gian
        - Quản lý Activity Tags
        - Thiết lập nhắc nhở trước khi hoạt động đến hạn
        - Gửi thông báo qua Email hoặc Popup
        - Tự động nhắc nhở theo lịch trình
    """,
    'author': 'SGC',
    'website': 'https://sgc.vn',
    'depends': ['base_setup', 'mail', 'hr'],
    'data': [
        'security/sgc_activity_alarm_rules.xml',
        'security/ir.model.access.csv',
        'views/activity_tag_views.xml',
        'views/sgc_activity_alarm_views.xml',
        'views/mail_activity_views.xml',
        'views/res_config_settings_views.xml',
        'views/activity_dashboard_views.xml',
        'data/sgc_activity_alarm_data.xml',
        'data/sgc_activity_reminder_mail_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sgc_activity_dashboard/static/src/css/dashboard.css',
            'sgc_activity_dashboard/static/src/css/style.scss',
            'sgc_activity_dashboard/static/src/js/activity_dashboard.js',
            'sgc_activity_dashboard/static/src/xml/activity_dashboard_template.xml',
            'sgc_activity_dashboard/static/src/xml/search_header.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
