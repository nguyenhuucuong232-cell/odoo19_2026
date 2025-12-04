# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_double_approval_amount = fields.Monetary(
        related='company_id.sale_double_approval_amount',
        readonly=False,
        currency_field='company_currency_id',
        string='Ngưỡng duyệt báo giá cấp 2'
    )

