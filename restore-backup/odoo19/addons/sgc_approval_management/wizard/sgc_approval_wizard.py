# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SGCApprovalRefuseWizard(models.TransientModel):
    _name = 'sgc.approval.refuse.wizard'
    _description = 'Từ chối yêu cầu phê duyệt'

    request_id = fields.Many2one(
        'sgc.approval.request',
        string='Yêu cầu',
        required=True
    )
    reason = fields.Text(string='Lý do từ chối', required=True)

    def action_refuse(self):
        """Refuse the approval request"""
        self.ensure_one()
        current_user = self.env.user
        
        approver = self.request_id.approver_ids.filtered(
            lambda a: a.user_id == current_user and a.status == 'pending'
        )
        
        if approver:
            approver.write({
                'status': 'refused',
                'approve_date': fields.Datetime.now(),
                'note': self.reason
            })
        
        self.request_id.write({
            'state': 'refused',
            'rejection_reason': self.reason,
            'date_completed': fields.Datetime.now()
        })
        
        # Update sale order if linked
        if self.request_id.sale_order_id:
            self.request_id.sale_order_id.write({
                'sgc_approval_state': 'refused',
                'sgc_rejection_reason': self.reason
            })
        
        return {'type': 'ir.actions.act_window_close'}

