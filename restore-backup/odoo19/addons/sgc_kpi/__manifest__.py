# -*- coding: utf-8 -*-
{
    'name': 'SGC KPI Management',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Quản lý KPI nhân sự',
    'description': """
        Module quản lý KPI:
        - Định nghĩa tiêu chí KPI
        - Báo cáo KPI theo tháng
        - Theo dõi hiệu suất nhân viên
        - Hệ số thời gian và vị trí
    """,
    'author': 'SGC',
    'website': 'https://sgc.vn',
    'depends': ['base', 'hr', 'hr_recruitment'],
    'data': [
        'security/sgc_kpi_security.xml',
        'security/ir.model.access.csv',
        'data/sgc_kpi_cron.xml',
        'views/sgc_kpi_criteria_views.xml',
        'views/sgc_kpi_report_views.xml',
        'views/sgc_kpi_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

