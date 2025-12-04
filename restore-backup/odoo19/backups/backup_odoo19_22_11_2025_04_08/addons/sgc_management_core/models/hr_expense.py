# -*- coding: utf-8 -*-
from odoo import models, fields


class HrExpense(models.Model):
    # Kế thừa Expense model (Odoo 19 uses hr.expense)
    _inherit = 'hr.expense'

    # Thêm Many2one tới đề nghị tạm ứng SGC
    sgc_advance_id = fields.Many2one(
        'sgc.expense.advance',
        string='Đề nghị Tạm ứng SGC',
        readonly=True,
        copy=False,
    )
