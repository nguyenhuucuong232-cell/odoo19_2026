# -*- coding: utf-8 -*-
from odoo import fields, models, api


class CrmStage(models.Model):
    _inherit = "crm.stage"

    sgc_auto_change = fields.Boolean(
        string="Tự động chuyển giai đoạn",
        default=False,
        help="Bật để tự động chuyển giai đoạn sau thời gian định trước"
    )
    sgc_stage_days = fields.Integer(
        string="Số ngày",
        help="Số ngày trước khi tự động chuyển giai đoạn"
    )
    sgc_next_stage_id = fields.Many2one(
        'crm.stage',
        string="Giai đoạn tiếp theo",
        help="Giai đoạn sẽ chuyển đến sau khi hết thời gian"
    )
    sgc_notification = fields.Char(
        string="Thông báo",
        help="Nội dung thông báo khi gần hết hạn"
    )

    def write(self, vals):
        if 'sgc_auto_change' in vals and not vals['sgc_auto_change']:
            vals['sgc_stage_days'] = False
            vals['sgc_next_stage_id'] = False
        return super().write(vals)
