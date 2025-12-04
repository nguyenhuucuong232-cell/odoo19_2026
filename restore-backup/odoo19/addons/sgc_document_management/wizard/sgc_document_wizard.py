# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SGCDocumentUserWizard(models.TransientModel):
    _name = 'sgc.document.user.wizard'
    _description = 'Chọn người xử lý văn bản'

    document_id = fields.Many2one('sgc.document', string='Văn bản', required=True)
    next_status_id = fields.Many2one('sgc.document.status', string='Trạng thái tiếp theo')
    user_ids = fields.Many2many('res.users', string='Người xử lý')
    response = fields.Text(string='Phản hồi')
    show_response = fields.Boolean(string='Hiển thị phản hồi')
    show_users = fields.Boolean(string='Hiển thị chọn người')

    def action_confirm(self):
        self.ensure_one()
        
        if self.show_users and self.user_ids:
            self.document_id.user_ids = [(6, 0, self.user_ids.ids)]
        elif self.next_status_id.user_ids:
            self.document_id.user_ids = [(6, 0, self.next_status_id.user_ids.ids)]
        
        self.document_id._log_history(
            self.document_id.status_id,
            self.response if self.show_response else None
        )
        self.document_id.status_id = self.next_status_id
        
        return {'type': 'ir.actions.act_window_close'}

