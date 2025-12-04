# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SgcExpenseAdvance(models.Model):
    _name = 'sgc.expense.advance'
    _description = 'Đề nghị Tạm ứng SGC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Số Đề nghị', 
        required=True, 
        copy=False, 
        readonly=True, 
        default='Mới'
    )
    
    # Liên kết với nhân viên (hr.employee)
    employee_id = fields.Many2one(
        'hr.employee', 
        string='Nhân viên', 
        required=True,
        default=lambda self: self.env.user.employee_id
    )
    
    # Liên kết với Dự án
    project_id = fields.Many2one(
        'project.project', 
        string='Dự án'
    )
    
    # Liên kết với Hợp đồng
    contract_id = fields.Many2one(
        'sgc.signed.contract', 
        string='Hợp đồng SGC'
    )

    reason = fields.Text(
        string='Lý do Tạm ứng', 
        required=True
    )
    
    company_id = fields.Many2one(
        'res.company', 
        string='Công ty', 
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        'res.currency', 
        string='Tiền tệ', 
        related='company_id.currency_id'
    )
    amount = fields.Monetary(
        string='Số tiền Tạm ứng', 
        currency_field='currency_id', 
        required=True,
        tracking=True
    )

    # Quy trình phê duyệt
    state = fields.Selection(
        [
            ('draft', 'Nháp'),
            ('submit', 'Chờ Trưởng nhóm (L1)'),
            ('approve_l1', 'Chờ Quản lý (L2)'),
            ('approved', 'Đã duyệt (Chờ chi tiền)'),
            ('paid', 'Đã chi tiền'),
            ('done', 'Hoàn thành'),
            ('refuse', 'Từ chối'),
        ], 
        string='Trạng thái', 
        default='draft', 
        tracking=True
    )

    # --- THÊM CÁC TRƯỜNG MỚI NÀY ---
    # Liên kết "Một-đến-Nhiều" để xem các Bảng kê Hoàn ứng
    expense_sheet_ids = fields.One2many(
        'hr.expense', 
        'sgc_advance_id', 
        string='Bảng kê Hoàn ứng'
    )
    
    # Trường tính toán (compute) để đếm số Bảng kê
    expense_sheet_count = fields.Integer(
        compute='_compute_expense_sheet_count'
    )
    
    # Hàm tính toán
    def _compute_expense_sheet_count(self):
        for advance in self:
            advance.expense_sheet_count = len(advance.expense_sheet_ids)
    # -----------------------------------

    # --- Hàm (Methods) ---
    def action_submit(self):
        """Gửi đề nghị và thông báo email cho Trưởng nhóm"""
        self.state = 'submit'
        # Gửi email thông báo
        template = self.env.ref('sgc_management_core.email_template_advance_submitted', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

    def action_approve_l1(self):
        """Duyệt L1 và thông báo email cho Quản lý"""
        self.state = 'approve_l1'
        # Gửi email thông báo
        template = self.env.ref('sgc_management_core.email_template_advance_approved_l1', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

    def action_approve_l2(self):
        """Duyệt L2 và thông báo email cho Nhân viên"""
        self.state = 'approved'
        # Gửi email thông báo
        template = self.env.ref('sgc_management_core.email_template_advance_approved_l2', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

    def action_refuse(self):
        """Từ chối và thông báo email cho Nhân viên"""
        self.state = 'refuse'
        # Gửi email thông báo
        template = self.env.ref('sgc_management_core.email_template_advance_refused', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

    def action_reset_to_draft(self):
        self.state = 'draft'
        
    # --- THÊM HÀM MỚI NÀY ---
    def action_paid(self):
        # Hàm này sẽ được gọi bởi Kế toán
        self.state = 'paid'
    # --------------------------
    
    # --- THÊM CÁC HÀM MỚI NÀY (CHO NÚT BẤM) ---
    
    def action_create_reconciliation(self):
        # Nút "Tạo Hoàn ứng"
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.expense',
            'view_mode': 'form',
            'target': 'current',
            'name': _('Tạo Hoàn ứng'),
            # Truyền giá trị mặc định vào form Hoàn ứng
            'context': {
                'default_employee_id': self.employee_id.id,
                'default_sgc_advance_id': self.id,
                'default_name': f"Hoàn ứng cho [ {self.name} ]",
            }
        }

    def action_view_reconciliations(self):
        # Nút "thông minh" (smart button)
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.expense',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.expense_sheet_ids.ids)],
            'target': 'current',
            'name': _('Các Bảng kê Hoàn ứng'),
        }