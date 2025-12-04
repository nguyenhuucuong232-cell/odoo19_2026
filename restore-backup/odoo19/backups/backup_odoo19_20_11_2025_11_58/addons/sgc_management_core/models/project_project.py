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