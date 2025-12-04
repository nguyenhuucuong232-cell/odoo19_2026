{
    'name': 'Hợp đồng đã ký',
    'version': '19.0.1.1',
    'summary': 'Quản lý Hợp đồng đã ký (Odoo 19)',
    'description': """
        Module quản lý nghiệp vụ Hợp đồng đã ký:
        - Tùy chỉnh Báo giá (Quotation)
        - Tùy chỉnh Hợp đồng (Contract)
        - Tùy chỉnh Dự án (Project)
        - Các mẫu in ấn (Reports)
    """,
    'author': 'SGC Tech Team',
    'website': 'https://sgc.vn',
    'category': 'Sales/Sales',
    'depends': [
        'base',
        'sale_management',
        'project',
        'hr',
        'hr_expense',
        'sgc_activity_dashboard',
        'sgc_kpi',
        'sgc_document_management',
        'sgc_approval_management',
        'sgc_account_payment',
        'sgc_hr_reward_warning',
    ],
    'data': [
        # Security - phải load đầu tiên
        'security/security.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        
        # Data files
        'data/sequence_data.xml',
        'data/uom_data.xml',
        'data/account_tax_data.xml',
        'data/company_header_data.xml',
        'data/mail_template_data.xml',
        'data/crm_stage_data.xml',
        'data/process_template_data.xml',
        'data/customer_care_template_data.xml',
        
        # Views - load sau khi models đã được định nghĩa
        'views/res_company_views.xml',
        'views/crm_lead_views.xml',
        'views/signed_contract_views.xml',
        'views/sgc_expense_advance_views.xml',
        'views/sale_order_views.xml',
        'views/hr_expense_views.xml',
        'views/sgc_config_views.xml',
        'views/sgc_document_views.xml',
        'views/sgc_main_menus.xml',  # Menu chính - phải load trước menus.xml
        'views/menus.xml',
        'views/dashboard_views.xml',
        
        # Reports
        'report/report_sale_order_sgc.xml',
        'report/report_signed_contract_template.xml',
        'report/report_expense_advance_template.xml',
        'report/report_project_revenue.xml',
        'report/report_bg_mau_mtld_template.xml',
        'report/report_layout_sgc.xml',
        'report/report_actions.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sgc_management_core/static/src/scss/sgc_theme.scss',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
