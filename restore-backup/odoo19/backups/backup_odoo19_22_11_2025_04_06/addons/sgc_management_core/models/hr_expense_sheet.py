# -*- coding: utf-8 -*-
from odoo import models, fields

class HrExpense(models.Model):
    # Kế thừa Expense model (Odoo 19 uses hr.expense)
    _inherit = 'hr.expense'

    # Thêm trường liên kết "Nhiều-đến-Một"
    # Một "Đề nghị Tạm ứng" có thể có nhiều "Bảng kê Hoàn ứng"
    sgc_advance_id = fields.Many2one(
        'sgc.expense.advance', 
        string='Đề nghị Tạm ứng SGC',
        readonly=True,
        copy=False # Không sao chép liên kết này khi nhân bản
    )