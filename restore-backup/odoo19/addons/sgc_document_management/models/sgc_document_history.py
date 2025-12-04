# -*- coding: utf-8 -*-
from odoo import fields, models


class SGCDocumentHistory(models.Model):
    _name = 'sgc.document.history'
    _description = 'Lịch sử xử lý văn bản'
    _order = 'date desc'

    document_id = fields.Many2one(
        'sgc.document',
        string='Văn bản',
        required=True,
        ondelete='cascade'
    )
    user_id = fields.Many2one('res.users', string='Người xử lý')
    status_id = fields.Many2one('sgc.document.status', string='Trạng thái')
    type = fields.Selection([
        ('in', 'Công văn đến'),
        ('out', 'Công văn đi')
    ], string='Loại')
    date = fields.Datetime(string='Ngày xử lý', default=fields.Datetime.now)
    response = fields.Text(string='Phản hồi')

