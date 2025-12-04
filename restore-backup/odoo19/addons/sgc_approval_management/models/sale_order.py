# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sgc_approval_request_id = fields.Many2one(
        'sgc.approval.request',
        string='Yêu cầu phê duyệt',
        copy=False
    )
    sgc_approval_state = fields.Selection([
        ('none', 'Không cần duyệt'),
        ('pending', 'Chờ phê duyệt'),
        ('approved', 'Đã duyệt'),
        ('refused', 'Từ chối'),
        ('cancel', 'Hủy')
    ], string='Trạng thái phê duyệt', default='none', tracking=True)
    
    sgc_approval_category_id = fields.Many2one(
        'sgc.approval.category',
        string='Loại phê duyệt'
    )
    sgc_approve_date_deadline = fields.Date(string='Hạn chót phê duyệt')
    sgc_rejection_reason = fields.Text(string='Lý do từ chối', readonly=True)

    def action_send_approval_request(self):
        """Send sale order for approval"""
        self.ensure_one()
        
        if not self.sgc_approval_category_id:
            raise UserError(_('Vui lòng chọn loại phê duyệt.'))
        
        # Create approval request
        approval_request = self.env['sgc.approval.request'].create({
            'category_id': self.sgc_approval_category_id.id,
            'sale_order_id': self.id,
            'date_deadline': self.sgc_approve_date_deadline,
            'reason': _('Yêu cầu phê duyệt đơn hàng %s') % self.name,
        })
        
        self.write({
            'sgc_approval_request_id': approval_request.id,
            'sgc_approval_state': 'pending'
        })
        
        # Submit the request
        approval_request.action_submit()
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Yêu cầu phê duyệt'),
            'res_model': 'sgc.approval.request',
            'view_mode': 'form',
            'res_id': approval_request.id,
        }

    def action_view_approval_request(self):
        """View the approval request"""
        self.ensure_one()
        if not self.sgc_approval_request_id:
            raise UserError(_('Không có yêu cầu phê duyệt.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Yêu cầu phê duyệt'),
            'res_model': 'sgc.approval.request',
            'view_mode': 'form',
            'res_id': self.sgc_approval_request_id.id,
        }

