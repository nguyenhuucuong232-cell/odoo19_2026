# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    department_id = fields.Many2one(
        'hr.department',
        string="Phòng phụ trách",
        related='project_id.department_id',
        store=True,
        readonly=False
    )

