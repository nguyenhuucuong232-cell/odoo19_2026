{
    'name': 'SGC Management Core',
    'version': '1.0',
    'summary': 'Core Business Logic for SGC (Odoo 19)',
    'description': """
        Module quản lý nghiệp vụ cốt lõi của SGC:
        - Tùy chỉnh Báo giá (Quotation)
        - Tùy chỉnh Hợp đồng (Contract)
        - Tùy chỉnh Dự án (Project)
        - Các mẫu in ấn (Reports)
    """,
    'author': 'SGC Tech Team',
    'website': 'https://sgc.vn',
    'category': 'Sales/Sales',
    'depends': ['base', 'sale_management', 'project', 'hr', 'hr_expense'],
    'data': [
        # Security - phải load đầu tiên
        'security/security.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        
        # Data files
        'data/sequence_data.xml',
        'data/uom_data.xml',
        'data/company_header_data.xml',
        'data/mail_template_data.xml',
        'data/crm_stage_data.xml',
        'data/process_template_data.xml',
        'data/customer_care_template_data.xml',
        'data/purchase_approval_rules_data.xml',
        
        # Views - load sau khi models đã được định nghĩa
        'views/res_company_views.xml',
        'views/crm_lead_views.xml',
        'views/signed_contract_views.xml',
        'views/sgc_expense_advance_views.xml',
        'views/sale_order_views.xml',
        'views/hr_expense_views.xml',
        'views/menus.xml',  # Phải load trước dashboard_views.xml
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
