# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SGCDocumentStatus(models.Model):
    _name = 'sgc.document.status'
    _description = 'Trạng thái văn bản'
    _order = "priority ASC"

    name = fields.Char(string='Tên trạng thái', required=True)
    code = fields.Char(string='Mã', required=True)
    priority = fields.Integer(string='Thứ tự', default=1)
    
    type = fields.Selection([
        ('in', 'Công văn đến'),
        ('out', 'Công văn đi')
    ], required=True, string='Loại')
    
    user_ids = fields.Many2many(
        'res.users',
        string='Người xử lý',
        domain=[('share', '=', False)]
    )
    
    is_default = fields.Boolean(string='Mặc định')
    is_won = fields.Boolean(string='Hoàn thành')
    active = fields.Boolean(string='Hoạt động', default=True)
    
    # Button 1
    is_show_1 = fields.Boolean(string='Hiển thị nút 1')
    name_1 = fields.Char(string='Tên nút 1')
    next_stage_1 = fields.Many2one(
        'sgc.document.status',
        string='Trạng thái tiếp theo 1'
    )
    
    # Button 2
    is_show_2 = fields.Boolean(string='Hiển thị nút 2')
    name_2 = fields.Char(string='Tên nút 2')
    next_stage_2 = fields.Many2one(
        'sgc.document.status',
        string='Trạng thái tiếp theo 2'
    )
    
    select_responsive_user = fields.Boolean(string='Chọn người xử lý')
    is_print_pdf = fields.Boolean(string='In PDF')
    is_show_response = fields.Boolean(string='Hiển thị phản hồi')
    is_processing_status = fields.Boolean(string='Đang xử lý')
    
    # UI
    text_color = fields.Char(string='Màu chữ', default='#ffffff')
    background_color = fields.Char(string='Màu nền', default='#714B67')

    @api.constrains('code')
    def _check_unique_code(self):
        for rec in self:
            if rec.code:
                domain = [('code', '=', rec.code), ('id', '!=', rec.id)]
                if self.search_count(domain):
                    raise ValidationError(_("Mã '%s' đã tồn tại.") % rec.code)

    @api.constrains('is_default', 'type')
    def _check_only_one_default_per_type(self):
        for rec in self:
            if rec.is_default:
                domain = [
                    ('is_default', '=', True),
                    ('type', '=', rec.type),
                    ('id', '!=', rec.id)
                ]
                if self.search_count(domain):
                    raise ValidationError(
                        _("Chỉ được đặt 1 trạng thái mặc định cho loại '%s'.") % rec.type
                    )

    @api.onchange('type')
    def _onchange_type(self):
        return {
            'domain': {
                'next_stage_1': [('type', '=', self.type)],
                'next_stage_2': [('type', '=', self.type)],
            }
        }

