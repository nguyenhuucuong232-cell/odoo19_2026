# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ItemCategory(models.Model):
    _name = 'sgc.item.category'
    _description = 'Danh mục khoản mục'
    _order = 'sequence, name'

    name = fields.Char(string='Tên danh mục', required=True)
    code = fields.Char(string='Mã')
    description = fields.Text(string='Mô tả')
    is_internal = fields.Boolean(string="Nội bộ", default=False)
    sequence = fields.Integer(string='Thứ tự', default=10)
    active = fields.Boolean(string='Hoạt động', default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )
    item_detail_ids = fields.One2many(
        'sgc.item.detail',
        'category_id',
        string='Chi tiết khoản mục'
    )
    item_count = fields.Integer(
        string='Số khoản mục',
        compute='_compute_item_count'
    )

    @api.depends('item_detail_ids')
    def _compute_item_count(self):
        for category in self:
            category.item_count = len(category.item_detail_ids)

