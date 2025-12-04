# -*- coding: utf-8 -*-
from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    # Thêm trường liên kết ngược lại Hợp đồng
    contract_id = fields.Many2one(
        'sgc.signed.contract',
        string='Hợp đồng SGC',
        readonly=True
    )
    department_id = fields.Many2one(
        'hr.department',
        string="Phòng phụ trách",
        default=lambda self: self.env.user.employee_id.department_id.id
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Đơn bán hàng',
        readonly=True
    )

    def write(self, vals):
        res = super().write(vals)
        if 'stage_id' in vals:
            for project in self:
                if project.sale_order_id and project.stage_id and project.stage_id.fold:
                    project.sale_order_id._update_prj_flow_state('b6_complete')
        return res