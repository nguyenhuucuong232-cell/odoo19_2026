# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SGCItemCategory(models.Model):
    _name = 'sgc.item.category'
    _description = 'Danh mục khoản mục'

    name = fields.Char(string='Tên', required=True)
    description = fields.Char(string='Mô tả')
    is_internal = fields.Boolean(string="Nội bộ", default=False)

