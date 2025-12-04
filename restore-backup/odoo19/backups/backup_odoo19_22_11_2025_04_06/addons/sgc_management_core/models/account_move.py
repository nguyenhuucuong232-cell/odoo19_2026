# -*- coding: utf-8 -*-
from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _update_sgc_sale_orders(self):
        orders = self.mapped('invoice_line_ids.sale_line_ids.order_id')
        if orders:
            orders._check_prj_payment_completion()

    def action_post(self):
        res = super().action_post()
        self._update_sgc_sale_orders()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'payment_state' in vals or 'state' in vals:
            self._update_sgc_sale_orders()
        return res

