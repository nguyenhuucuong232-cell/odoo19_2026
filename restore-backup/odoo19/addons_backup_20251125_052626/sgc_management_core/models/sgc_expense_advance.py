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

    # Approvers
    approver_l1_id = fields.Many2one(
        'res.users',
        string='Người duyệt cấp 1',
        readonly=True,
        tracking=True
    )
    approver_l2_id = fields.Many2one(
        'res.users',
        string='Người duyệt cấp 2',
        readonly=True,
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
        for advance in self:
            advance.state = 'submit'

            # Tự động tìm và gán approver L1 (Trưởng nhóm)
            approver_l1 = advance._find_approver_l1()
            if approver_l1:
                advance.write({'approver_l1_id': approver_l1.id})

            # Tạo activity cho approver L1
            advance._create_approval_activity('L1', approver_l1)

            # Gửi email thông báo
            template = self.env.ref('sgc_management_core.email_template_advance_submitted', raise_if_not_found=False)
            if template:
                template.send_mail(advance.id, force_send=True)

    def action_approve_l1(self):
        """Duyệt L1 và thông báo email cho Quản lý"""
        for advance in self:
            advance.state = 'approve_l1'

            # Tự động tìm và gán approver L2 (Quản lý)
            approver_l2 = advance._find_approver_l2()
            if approver_l2:
                advance.write({'approver_l2_id': approver_l2.id})

            # Tạo activity cho approver L2
            advance._create_approval_activity('L2', approver_l2)

            # Gửi email thông báo
            template = self.env.ref('sgc_management_core.email_template_advance_approved_l1', raise_if_not_found=False)
            if template:
                template.send_mail(advance.id, force_send=True)

    def action_approve_l2(self):
        """Duyệt L2 và thông báo email cho Nhân viên"""
        for advance in self:
            advance.state = 'approved'

            # Gửi email thông báo
            template = self.env.ref('sgc_management_core.email_template_advance_approved_l2', raise_if_not_found=False)
            if template:
                template.send_mail(advance.id, force_send=True)

    def action_refuse(self):
        """Từ chối và thông báo email cho Nhân viên"""
        for advance in self:
            advance.state = 'refuse'

            # Xóa activities liên quan
            advance._remove_approval_activities()

            # Gửi email thông báo
            template = self.env.ref('sgc_management_core.email_template_advance_refused', raise_if_not_found=False)
            if template:
                template.send_mail(advance.id, force_send=True)

    def action_reset_to_draft(self):
        for advance in self:
            advance.state = 'draft'
            # Xóa approvers và activities
            advance.write({
                'approver_l1_id': False,
                'approver_l2_id': False,
            })
            advance._remove_approval_activities()

    def _find_approver_l1(self):
        """Tìm approver cấp 1 (Trưởng nhóm)"""
        self.ensure_one()

        # Ưu tiên 1: Manager của employee
        if self.employee_id.parent_id and self.employee_id.parent_id.user_id:
            return self.employee_id.parent_id.user_id

        # Ưu tiên 2: Manager của department
        if self.employee_id.department_id and self.employee_id.department_id.manager_id and self.employee_id.department_id.manager_id.user_id:
            return self.employee_id.department_id.manager_id.user_id

        # Ưu tiên 3: Tìm user có group team leader trong cùng department
        team_leaders = self.env['res.users'].search([
            ('employee_id.department_id', '=', self.employee_id.department_id.id),
            ('has_group', '=', 'sgc_management_core.group_sgc_team_leader')
        ])
        if team_leaders:
            return team_leaders[0]

        return False

    def _find_approver_l2(self):
        """Tìm approver cấp 2 (Quản lý)"""
        self.ensure_one()

        # Tìm user có group manager
        managers = self.env['res.users'].search([
            ('has_group', '=', 'sgc_management_core.group_sgc_manager')
        ])
        if managers:
            return managers[0]

        return False

    def _create_approval_activity(self, level, approver):
        """Tạo activity cho approver"""
        if not approver:
            return

        activity_vals = {
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'summary': f'Duyệt đề nghị tạm ứng {self.name} (Cấp {level})',
            'note': f'Vui lòng duyệt đề nghị tạm ứng {self.amount} VNĐ của {self.employee_id.name}',
            'user_id': approver.id,
            'res_model_id': self.env['ir.model']._get_id('sgc.expense.advance'),
            'res_id': self.id,
            'date_deadline': fields.Date.context_today(self),
        }
        self.env['mail.activity'].create(activity_vals)

    def _remove_approval_activities(self):
        """Xóa các approval activities"""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'sgc.expense.advance'),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id)
        ])
        activities.unlink()
        
    # --- THÊM HÀM MỚI NÀY ---
    def action_paid(self):
        # Hàm này sẽ được gọi bởi Kế toán
        for advance in self:
            advance.state = 'paid'
            # Tự động tạo reimbursement nếu có expense sheets
            advance._auto_create_reimbursement()
    # --------------------------
    
    def _auto_create_reimbursement(self):
        """Tự động tạo reimbursement khi advance được paid"""
        self.ensure_one()

        if not self.expense_sheet_ids:
            return

        # Tính tổng tiền đã chi từ expense sheets
        total_expensed = sum(sheet.total_amount for sheet in self.expense_sheet_ids if sheet.state == 'done')

        if total_expensed > self.amount:
            # Tạo reimbursement cho phần vượt
            reimbursement_amount = total_expensed - self.amount

            # Tạo hr.expense.sheet mới cho reimbursement
            reimbursement_vals = {
                'name': f"Hoàn ứng cho {self.name}",
                'employee_id': self.employee_id.id,
                'sgc_advance_id': self.id,
                'state': 'draft',
            }

            reimbursement_sheet = self.env['hr.expense.sheet'].create(reimbursement_vals)

            # Tạo expense line cho reimbursement
            expense_line_vals = {
                'name': f"Hoàn ứng - vượt {reimbursement_amount} VNĐ",
                'employee_id': self.employee_id.id,
                'product_id': self._get_reimbursement_product().id,
                'total_amount': reimbursement_amount,
                'sheet_id': reimbursement_sheet.id,
            }

            self.env['hr.expense'].create(expense_line_vals)

            # Thông báo cho employee
            self.message_post(
                body=f"Đã tạo bảng kê hoàn ứng tự động với số tiền {reimbursement_amount} VNĐ",
                subtype_xmlid='mail.mt_note'
            )

        elif total_expensed < self.amount:
            # Tạo reimbursement cho phần còn lại (nếu cần)
            remaining_amount = self.amount - total_expensed

            # Có thể tạo expense sheet để thu hồi phần còn lại
            # Hoặc chỉ ghi chú
            self.message_post(
                body=f"Tạm ứng còn dư {remaining_amount} VNĐ. Vui lòng hoàn trả.",
                subtype_xmlid='mail.mt_note'
            )

    def _get_reimbursement_product(self):
        """Tìm product cho reimbursement"""
        # Tìm product có tên chứa "hoàn ứng" hoặc "reimbursement"
        product = self.env['product.product'].search([
            ('name', 'ilike', 'hoàn ứng'),
            ('can_be_expensed', '=', True)
        ], limit=1)

        if not product:
            # Tạo product mặc định nếu chưa có
            product_vals = {
                'name': 'Hoàn ứng',
                'type': 'service',
                'can_be_expensed': True,
                'standard_price': 0,
            }
            product = self.env['product.product'].create(product_vals)

        return product
    
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