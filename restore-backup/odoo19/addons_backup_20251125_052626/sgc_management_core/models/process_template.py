# -*- coding: utf-8 -*-
from odoo import fields, models


class ProcessTemplate(models.Model):
    _name = 'sgc.process.template'
    _description = 'SGC Process Template'
    _order = 'sequence, code'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    module_area = fields.Selection([
        ('crm', 'CRM'),
        ('project', 'Project'),
        ('sale', 'Sales'),
        ('purchase', 'Purchase'),
        ('stock', 'Inventory'),
        ('account', 'Accounting'),
        ('expense', 'Expense'),
    ], required=True)
    sequence = fields.Integer(default=10)
    cloudmedia_status = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Review'),
        ('approved', 'Approved'),
    ], default='review')
    sgc_status = fields.Selection([
        ('new', 'Mới'),
        ('in_progress', 'Đang rà soát'),
        ('done', 'Hoàn tất'),
    ], default='new', string="Trạng thái SGC")
    cloudmedia_note = fields.Text(string='CloudMedia Note')
    sgc_note = fields.Text(string='SGC Note')
    step_ids = fields.One2many('sgc.process.step', 'template_id', string='Steps')
    active = fields.Boolean(default=True)


class ProcessStep(models.Model):
    _name = 'sgc.process.step'
    _description = 'SGC Process Step'
    _order = 'sequence, id'

    template_id = fields.Many2one('sgc.process.template', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    description = fields.Text()

