# -*- coding: utf-8 -*-
from odoo import models, fields, api


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

    @api.model_create_multi
    def create(self, vals_list):
        """Override create để tự động liên kết với advance nếu có context"""
        records = super().create(vals_list)

        for record in records:
            # Nếu có sgc_advance_id trong context, tự động gán
            if self.env.context.get('default_sgc_advance_id'):
                record.sgc_advance_id = self.env.context.get('default_sgc_advance_id')

        return records

    def write(self, vals):
        """Override write để cập nhật trạng thái advance khi expense được approve"""
        res = super().write(vals)

        if vals.get('state') == 'approved':
            for expense in self:
                if expense.sgc_advance_id and expense.sgc_advance_id.state == 'paid':
                    # Tự động tạo reimbursement nếu cần
                    expense.sgc_advance_id._auto_create_reimbursement()

        return res
