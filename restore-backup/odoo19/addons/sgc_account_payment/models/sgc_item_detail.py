# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SGCItemDetail(models.Model):
    _name = 'sgc.item.detail'
    _description = 'Chi tiết khoản mục'

    name = fields.Char(string='Tên', required=True)
    code = fields.Char(string='Mã')
    description = fields.Char(string='Mô tả')
    account_id = fields.Many2one('account.account', string='Tài khoản', required=True)
    category_id = fields.Many2one('sgc.item.category', string='Danh mục', required=True)

