# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    department_id = fields.Many2one(
        'hr.department',
        string="Phòng ban",
        related='employee_id.department_id',
        store=True,
        readonly=True
    )

