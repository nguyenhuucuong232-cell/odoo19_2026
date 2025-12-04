# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SGCApprovalCategory(models.Model):
    _name = 'sgc.approval.category'
    _description = 'Loại phê duyệt'

    name = fields.Char(string='Tên', required=True)
    description = fields.Text(string='Mô tả')
    approval_type = fields.Selection([
        ('sale_order', 'Đơn bán hàng'),
        ('purchase_order', 'Đơn mua hàng'),
        ('general', 'Chung')
    ], string='Loại', default='general', required=True)
    
    approve_by_level = fields.Boolean(
        string='Phê duyệt theo cấp',
        default=False,
        help="Nếu bật, người phê duyệt sẽ duyệt theo thứ tự cấp độ"
    )
    approval_minimum = fields.Integer(
        string='Số người phê duyệt tối thiểu',
        default=1
    )
    approver_ids = fields.One2many(
        'sgc.approval.category.approver',
        'category_id',
        string='Người phê duyệt'
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )


class SGCApprovalCategoryApprover(models.Model):
    _name = 'sgc.approval.category.approver'
    _description = 'Người phê duyệt theo danh mục'
    _order = 'level, sequence'

    category_id = fields.Many2one(
        'sgc.approval.category',
        string='Loại phê duyệt',
        required=True,
        ondelete='cascade'
    )
    user_id = fields.Many2one(
        'res.users',
        string='Người phê duyệt',
        required=True
    )
    level = fields.Integer(string='Cấp độ', default=1)
    sequence = fields.Integer(string='Thứ tự', default=10)
    required = fields.Boolean(string='Bắt buộc', default=True)

