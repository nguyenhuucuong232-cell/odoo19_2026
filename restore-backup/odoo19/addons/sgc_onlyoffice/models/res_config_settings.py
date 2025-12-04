# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sgc_onlyoffice_url = fields.Char(
        string='OnlyOffice Server URL',
        help='URL của OnlyOffice Document Server (ví dụ: https://documentserver.example.com)'
    )
    sgc_onlyoffice_secret = fields.Char(
        string='OnlyOffice JWT Secret',
        help='JWT Secret để xác thực với OnlyOffice'
    )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sgc_onlyoffice_url = fields.Char(
        string='OnlyOffice Server URL',
        related='company_id.sgc_onlyoffice_url',
        readonly=False
    )
    sgc_onlyoffice_secret = fields.Char(
        string='OnlyOffice JWT Secret',
        related='company_id.sgc_onlyoffice_secret',
        readonly=False
    )

