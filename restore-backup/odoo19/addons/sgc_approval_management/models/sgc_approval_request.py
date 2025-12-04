# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SGCApprovalRequest(models.Model):
    _name = 'sgc.approval.request'
    _description = 'Yêu cầu phê duyệt'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Mã',
        default=lambda self: _('New'),
        readonly=True,
        copy=False
    )
    category_id = fields.Many2one(
        'sgc.approval.category',
        string='Loại phê duyệt',
        required=True
    )
    request_owner_id = fields.Many2one(
        'res.users',
        string='Người yêu cầu',
        default=lambda self: self.env.user,
        required=True
    )
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('pending', 'Chờ phê duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('refused', 'Từ chối'),
        ('cancel', 'Hủy')
    ], string='Trạng thái', default='draft', tracking=True)
    
    date = fields.Date(string='Ngày yêu cầu', default=fields.Date.today)
    date_deadline = fields.Date(string='Hạn chót')
    date_confirmed = fields.Datetime(string='Ngày gửi')
    date_completed = fields.Datetime(string='Ngày hoàn thành')
    
    reason = fields.Text(string='Lý do')
    rejection_reason = fields.Text(string='Lý do từ chối')
    
    # Related to Sale Order
    sale_order_id = fields.Many2one('sale.order', string='Đơn bán hàng')
    amount_total = fields.Monetary(
        string='Tổng tiền',
        related='sale_order_id.amount_total',
        store=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Khách hàng',
        related='sale_order_id.partner_id',
        store=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id
    )
    
    approver_ids = fields.One2many(
        'sgc.approval.approver',
        'request_id',
        string='Người phê duyệt'
    )
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.approval.request') or _('New')
        return super().create(vals_list)

    def action_submit(self):
        """Submit request for approval"""
        self.ensure_one()
        
        if not self.approver_ids:
            # Auto-create approvers from category
            for cat_approver in self.category_id.approver_ids:
                self.env['sgc.approval.approver'].create({
                    'request_id': self.id,
                    'user_id': cat_approver.user_id.id,
                    'level': cat_approver.level,
                    'sequence': cat_approver.sequence,
                    'required': cat_approver.required,
                    'status': 'pending' if cat_approver.level == 1 else 'waiting',
                })
        
        if not self.approver_ids:
            raise UserError(_('Vui lòng thêm người phê duyệt.'))
        
        self.write({
            'state': 'pending',
            'date_confirmed': fields.Datetime.now()
        })
        
        # Create activities for first level approvers
        first_level_approvers = self.approver_ids.filtered(lambda a: a.status == 'pending')
        for approver in first_level_approvers:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=approver.user_id.id,
                summary=_('Yêu cầu phê duyệt: %s') % self.name
            )

    def action_approve(self):
        """Approve the request"""
        self.ensure_one()
        current_user = self.env.user
        
        approver = self.approver_ids.filtered(
            lambda a: a.user_id == current_user and a.status == 'pending'
        )
        if not approver:
            raise UserError(_('Bạn không có quyền phê duyệt yêu cầu này.'))
        
        approver.write({
            'status': 'approved',
            'approve_date': fields.Datetime.now()
        })
        
        # Check if all required approvers approved
        pending_approvers = self.approver_ids.filtered(
            lambda a: a.status == 'pending' and a.required
        )
        
        if not pending_approvers:
            # Activate next level if exists
            waiting_approvers = self.approver_ids.filtered(lambda a: a.status == 'waiting')
            if waiting_approvers:
                min_level = min(waiting_approvers.mapped('level'))
                next_level = waiting_approvers.filtered(lambda a: a.level == min_level)
                next_level.write({'status': 'pending'})
                for app in next_level:
                    self.activity_schedule(
                        'mail.mail_activity_data_todo',
                        user_id=app.user_id.id,
                        summary=_('Yêu cầu phê duyệt: %s') % self.name
                    )
            else:
                # All approved
                self.write({
                    'state': 'approved',
                    'date_completed': fields.Datetime.now()
                })
                # Update sale order if linked
                if self.sale_order_id:
                    self.sale_order_id.write({'sgc_approval_state': 'approved'})

    def action_refuse(self):
        """Refuse the request"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Từ chối yêu cầu'),
            'res_model': 'sgc.approval.refuse.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_request_id': self.id}
        }

    def action_cancel(self):
        """Cancel the request"""
        self.write({'state': 'cancel'})
        if self.sale_order_id:
            self.sale_order_id.write({'sgc_approval_state': 'cancel'})

    def action_draft(self):
        """Reset to draft"""
        self.write({'state': 'draft'})
        self.approver_ids.write({'status': 'new'})

