# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SGCApprovalApprover(models.Model):
    _name = 'sgc.approval.approver'
    _description = 'Người phê duyệt'
    _order = 'level, sequence'

    request_id = fields.Many2one(
        'sgc.approval.request',
        string='Yêu cầu',
        required=True,
        ondelete='cascade'
    )
    user_id = fields.Many2one(
        'res.users',
        string='Người phê duyệt',
        required=True
    )
    status = fields.Selection([
        ('new', 'Mới'),
        ('pending', 'Chờ duyệt'),
        ('waiting', 'Đang chờ'),
        ('approved', 'Đã duyệt'),
        ('refused', 'Từ chối')
    ], string='Trạng thái', default='new')
    
    level = fields.Integer(string='Cấp độ', default=1)
    sequence = fields.Integer(string='Thứ tự', default=10)
    required = fields.Boolean(string='Bắt buộc', default=True)
    approve_date = fields.Datetime(string='Ngày phê duyệt')
    note = fields.Text(string='Ghi chú')

