# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    # Thông tin người đại diện
    representative_name = fields.Char(
        string='Tên người đại diện',
        help='Tên người đại diện pháp luật của công ty'
    )
    
    representative_position = fields.Char(
        string='Chức vụ người đại diện',
        default='Giám đốc',
        help='Chức vụ của người đại diện (VD: Giám đốc, Tổng Giám đốc...)'
    )
    
    representative_signature = fields.Binary(
        string='Chữ ký người đại diện',
        help='Hình ảnh chữ ký của người đại diện (khuyến nghị: PNG 200x100px, nền trong suốt)',
        attachment=True
    )
    
    # Thông tin bổ sung cho report
    tax_code = fields.Char(
        string='Mã số thuế',
        help='Mã số thuế của công ty'
    )
    
    business_license = fields.Char(
        string='Số ĐKKD',
        help='Số đăng ký kinh doanh'
    )
    
    hotline = fields.Char(
        string='Hotline',
        help='Số hotline của công ty'
    )
    
    fax = fields.Char(
        string='Fax',
        help='Số fax của công ty'
    )
    
    # Header Report
    report_header_image = fields.Binary(
        string='Hình ảnh Header Report',
        help='Banner/Logo hiển thị ở đầu báo cáo (khuyến nghị: PNG/JPG 1200x300px)',
        attachment=True
    )
    
    report_header_text = fields.Html(
        string='Header report',
        help='Nội dung header report hiển thị ở đầu các báo cáo',
        translate=True
    )

    sale_double_approval_amount = fields.Monetary(
        string='Ngưỡng duyệt báo giá cấp 2',
        currency_field='currency_id',
        default=5000000.0,
        help='Đơn hàng có giá trị lớn hơn ngưỡng này phải phê duyệt thêm bởi Ban Giám Đốc.'
    )