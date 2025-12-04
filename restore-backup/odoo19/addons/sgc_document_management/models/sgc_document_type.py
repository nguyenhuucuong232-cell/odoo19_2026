# -*- coding: utf-8 -*-
from odoo import fields, models


class SGCDocumentType(models.Model):
    _name = 'sgc.document.type'
    _description = 'Loại văn bản'

    name = fields.Char(string='Tên', required=True)
    description = fields.Text(string='Mô tả')

