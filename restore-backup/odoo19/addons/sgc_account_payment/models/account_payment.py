# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    sgc_payment_person_id = fields.Many2one(
        'res.partner',
        string='Người thanh toán',
        store=True,
        readonly=False
    )
