# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    sgc_position_coefficient = fields.Float(
        string='Hệ số vị trí',
        default=1.0,
        help='Hệ số dùng để tính chỉ tiêu KPI theo vị trí công việc'
    )

