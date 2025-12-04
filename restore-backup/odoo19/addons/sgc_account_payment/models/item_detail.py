# -*- coding: utf-8 -*-
from odoo import fields, models


class ItemDetail(models.Model):
    _name = 'sgc.item.detail'
    _description = 'Chi tiết khoản mục'
    _order = 'category_id, name'

    name = fields.Char(string='Tên khoản mục', required=True)
    code = fields.Char(string='Mã khoản mục')
    description = fields.Text(string='Mô tả')
    account_id = fields.Many2one(
        'account.account',
        string='Tài khoản kế toán',
        required=True
    )
    category_id = fields.Many2one(
        'sgc.item.category',
        string='Danh mục',
        required=True
    )
    active = fields.Boolean(string='Hoạt động', default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )

