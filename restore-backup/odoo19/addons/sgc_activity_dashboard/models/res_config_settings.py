# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sgc_display_activity_reminder = fields.Boolean(
        'Bật nhắc nhở hoạt động',
        default=True
    )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sgc_display_activity_reminder = fields.Boolean(
        'Bật nhắc nhở hoạt động',
        related='company_id.sgc_display_activity_reminder',
        readonly=False
    )

