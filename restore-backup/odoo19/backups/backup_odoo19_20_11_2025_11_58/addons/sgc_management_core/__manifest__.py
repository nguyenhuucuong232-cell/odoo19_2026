{
    'name': 'Nghiệp vụ SGC',
    'summary': """
        Module nghiệp vụ SGC.
        (Xây dựng mới cho Odoo 19)
    """,
    'version': '19.0.1.0.0',
    'author': 'hsevn.com.vn',
    'website': 'https://hsevn.com.vn/',
    'category': 'Services',         # Sửa category thành chuẩn

    # Icon cho ứng dụng SGC (sử dụng file có sẵn icon_sgc.png)
    # Odoo tìm kiếm static/description/icon.png mặc định; module đã có icon_sgc.png
    # => Chỉ đổi đường dẫn để dùng file hiện hữu
    # Default location Odoo expects
    # Use module-prefixed path for manifest icon so update_list writes it
    'icon': '/sgc_management_core/static/description/icon.png',
    # Also provide web_icon to support menu icon references and studio
    # Use the module's static/src/img path for the app/menu icon
    'web_icon': 'sgc_management_core,static/src/img/icon.png',

    # Các module Odoo mà module này cần để chạy
    'depends': [
        'base',
        'mail',                 # Cần cho tính năng chatter (lịch sử trao đổi)
        'crm',                  # Cần để liên kết với Lead/Cơ hội
        'sale_management',      # Cần để liên kết với Đơn hàng (Sale Order)
        'sale_project',         # Cần để liên kết product.template -> project.template
        'project',              # Cần cho nghiệp vụ dự án (từ file thiết kế)
        'hr_expense',           # Cần cho Tạm ứng
        'account',              # Cần cho nghiệp vụ kế toán (từ file thiết kế)
        'hr',                   # Cần để liên kết với hr.employee
    ],

    # Các file dữ liệu/giao diện sẽ được tải (hiện tại chỉ có file security)
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        # Data files
        'data/sequence_data.xml',
        'data/project_data.xml',
        'data/product_service_data.xml',
        'data/product_environment_data.xml',
        'data/company_data.xml',
        'data/department_data.xml',
        'data/mail_template_data.xml',
        'data/bulk_employees_data.xml',

        # Report Actions & Templates
        'report/report_layout_sgc.xml',
        'report/report_actions.xml',
        'report/report_signed_contract_template.xml',
        'report/report_expense_advance_template.xml',
        'report/report_project_revenue.xml',

        # Views
        'views/res_company_views.xml',
        'views/signed_contract_views.xml',
        'views/sgc_expense_advance_views.xml',
        'views/sale_order_views.xml',
        'views/project_project_views.xml',
        'views/hr_expense_views.xml',
        'views/product_views.xml',
        'views/dashboard_views.xml',
        'views/menus.xml',
    ],

    'installable': True,
    'application': True,        # Đánh dấu đây là một "Ứng dụng"
    'license': 'LGPL-3',
}