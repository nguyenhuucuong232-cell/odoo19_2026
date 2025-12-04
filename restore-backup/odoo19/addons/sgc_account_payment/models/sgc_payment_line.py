# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SGCPaymentLine(models.Model):
    _name = 'sgc.payment.line'
    _inherit = "analytic.mixin"
    _description = 'Chi tiết thanh toán'

    payment_id = fields.Many2one('sgc.payment', string='Thanh toán', ondelete='cascade')
    item_detail_id = fields.Many2one('sgc.item.detail', string='Khoản mục')
    account_id = fields.Many2one('account.account', string='Tài khoản')
    description = fields.Char(string='Mô tả')
    amount = fields.Float(string='Số tiền', digits=(18, 0))
    team_id = fields.Many2one('crm.team', string='Nhóm bán hàng')

    @api.onchange('item_detail_id')
    def _onchange_item_detail_id(self):
        for rec in self:
            if rec.item_detail_id:
                rec.account_id = rec.item_detail_id.account_id.id

