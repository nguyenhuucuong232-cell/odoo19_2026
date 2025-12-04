# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PaymentLine(models.Model):
    _name = 'sgc.payment.line'
    _description = 'Dòng thanh toán'

    payment_id = fields.Many2one(
        'sgc.payment.transaction',
        string='Giao dịch thanh toán',
        ondelete='cascade'
    )
    item_detail_id = fields.Many2one(
        'sgc.item.detail',
        string='Khoản mục'
    )
    account_id = fields.Many2one(
        'account.account',
        string='Tài khoản kế toán'
    )
    description = fields.Char(string='Mô tả')
    amount = fields.Monetary(
        string='Số tiền',
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Tiền tệ',
        related='payment_id.currency_id',
        store=True
    )
    team_id = fields.Many2one(
        'crm.team',
        string='Nhóm kinh doanh'
    )
    analytic_distribution = fields.Json(
        string='Phân bổ phân tích'
    )

    @api.onchange('item_detail_id')
    def _onchange_item_detail_id(self):
        if self.item_detail_id:
            self.account_id = self.item_detail_id.account_id

