# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    sgc_stage_key = fields.Selection([
        ('lead', 'Bước 1 - Khách hàng tiềm năng'),
        ('opportunity', 'Bước 2 - Cơ hội'),
        ('research', 'Bước 3 - Đang tìm hiểu'),
        ('need', 'Bước 4 - Có nhu cầu'),
        ('quotation', 'Bước 5 - Báo giá'),
        ('pending', 'Bước 6 - Pending'),
        ('success', 'Bước 7a - Thành công'),
        ('fail', 'Bước 7b - Thất bại'),
    ], string='SGC Stage', copy=False)
    sgc_description = fields.Text(string='Mô tả SGC')
    sgc_sales_tasks = fields.Text(string='Công việc NV Kinh doanh')
    sgc_marketing_tasks = fields.Text(string='Công việc Marketing')
    sgc_reference = fields.Char(string='Tham chiếu quy trình')


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sgc_stage_key = fields.Selection(related='stage_id.sgc_stage_key', string="Bước CRM", store=True, readonly=True)
    sgc_stage_description = fields.Text(related='stage_id.sgc_description', readonly=True)
    sgc_stage_sales_tasks = fields.Text(related='stage_id.sgc_sales_tasks', readonly=True)
    sgc_stage_marketing_tasks = fields.Text(related='stage_id.sgc_marketing_tasks', readonly=True)
    sgc_stage_reference = fields.Char(related='stage_id.sgc_reference', readonly=True)

    def _post_stage_message(self, new_stage):
        self.ensure_one()
        if not new_stage.sgc_stage_key:
            return
        body = "<p><b>%s</b></p>" % (new_stage.display_name)
        if new_stage.sgc_description:
            body += "<p>%s</p>" % new_stage.sgc_description
        if new_stage.sgc_sales_tasks:
            body += "<p><b>NV Kinh doanh:</b><br/>%s</p>" % new_stage.sgc_sales_tasks.replace('\n', '<br/>')
        if new_stage.sgc_marketing_tasks:
            body += "<p><b>Marketing:</b><br/>%s</p>" % new_stage.sgc_marketing_tasks.replace('\n', '<br/>')
        if new_stage.sgc_reference:
            body += "<p><b>Tham chiếu:</b> %s</p>" % new_stage.sgc_reference
        self.message_post(body=body, subtype_xmlid='mail.mt_note')

    def write(self, vals):
        stage_before = {}
        if 'stage_id' in vals:
            stage_before = {lead.id: lead.stage_id for lead in self}
        res = super().write(vals)
        if 'stage_id' in vals:
            for lead in self:
                prev_stage = stage_before.get(lead.id)
                if prev_stage != lead.stage_id and lead.stage_id:
                    lead._post_stage_message(lead.stage_id)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for lead in records:
            if lead.stage_id:
                lead._post_stage_message(lead.stage_id)
        return records

