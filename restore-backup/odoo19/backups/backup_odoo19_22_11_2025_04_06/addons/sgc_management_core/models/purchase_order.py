# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import UserError, AccessError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_submit_approval_level1(self):
        self.write({
            'approval_level1_state': 'waiting',
            'approval_level1_user_id': False,
            'approval_level2_state': 'none',
            'approval_level2_user_id': False,
        })

    def action_approve_level1(self):
        if not self.env.user.has_group('sgc_management_core.group_sgc_purchase_manager'):
            raise AccessError('Bạn không có quyền duyệt cấp 1.')
        self.write({
            'approval_level1_state': 'approved',
            'approval_level1_user_id': self.env.user.id,
            'approval_level2_state': 'waiting',
            'approval_level2_user_id': False,
        })

    def action_reject_level1(self):
        if not self.env.user.has_group('sgc_management_core.group_sgc_purchase_manager'):
            raise AccessError('Bạn không có quyền từ chối cấp 1.')
        self.write({
            'approval_level1_state': 'rejected',
            'approval_level1_user_id': self.env.user.id,
            'approval_level2_state': 'none',
            'approval_level2_user_id': False,
        })

    def action_approve_level2(self):
        if not self.env.user.has_group('sgc_management_core.group_sgc_purchase_director'):
            raise AccessError('Bạn không có quyền duyệt cấp 2.')
        self.write({
            'approval_level2_state': 'approved',
            'approval_level2_user_id': self.env.user.id,
        })

    def action_reject_level2(self):
        if not self.env.user.has_group('sgc_management_core.group_sgc_purchase_director'):
            raise AccessError('Bạn không có quyền từ chối cấp 2.')
        self.write({
            'approval_level2_state': 'rejected',
            'approval_level2_user_id': self.env.user.id,
            'approval_level1_state': 'waiting',
        })

    def action_send_rfq(self):
        # Giả lập gửi báo giá cho nhiều NCC, chuyển trạng thái
        self.write({'rfq_sent_state': 'sent'})

        # Trạng thái duyệt cấp 1
        approval_level1_state = fields.Selection([
            ('none', 'Không yêu cầu'),
            ('waiting', 'Đang chờ'),
            ('approved', 'Đã duyệt'),
            ('rejected', 'Từ chối'),
        ], default='none', string='Trạng thái duyệt cấp 1', copy=False)

        # Người duyệt cấp 1
        approval_level1_user_id = fields.Many2one('res.users', string='Người duyệt cấp 1', copy=False, readonly=True)

        # Trạng thái duyệt cấp 2
        approval_level2_state = fields.Selection([
            ('none', 'Không yêu cầu'),
            ('waiting', 'Đang chờ'),
            ('approved', 'Đã duyệt'),
            ('rejected', 'Từ chối'),
        ], default='none', string='Trạng thái duyệt cấp 2', copy=False)

        # Người duyệt cấp 2
        approval_level2_user_id = fields.Many2one('res.users', string='Người duyệt cấp 2', copy=False, readonly=True)

        # Trạng thái gửi báo giá
        rfq_sent_state = fields.Selection([
            ('none', 'Chưa gửi'),
            ('sent', 'Đã gửi'),
            ('responded', 'Đã phản hồi'),
        ], default='none', string='Trạng thái gửi báo giá', copy=False)

    def _user_is_purchase_director(self):
        return self.env.user.has_group('sgc_management_core.group_sgc_purchase_director') or \
            self.env.user.has_group('sgc_management_core.group_sgc_purchase_manager')

    def _user_is_purchase_manager(self):
        return self.env.user.has_group('sgc_management_core.group_sgc_purchase_manager')

    def _user_is_purchase_staff(self):
        return self.env.user.has_group('sgc_management_core.group_sgc_purchase_staff')

    def _check_purchase_permissions(self):
        if not (self._user_is_purchase_staff() or self._user_is_purchase_manager() or self._user_is_purchase_director()):
            return

        allowed_states = ('draft', 'sent')
        user = self.env.user
        for order in self:
            if order.state not in allowed_states and not self._user_is_purchase_director():
                raise UserError(_("Chỉ được chỉnh sửa/xóa đơn mua ở trạng thái Nháp hoặc Đã gửi."))

            if self._user_is_purchase_director():
                continue

            if self._user_is_purchase_manager():
                manager_department = user.employee_id.department_id
                vendor_department = order.user_id.employee_id.department_id
                if manager_department and vendor_department and manager_department != vendor_department:
                    continue
                # allow managers to handle đơn không có department xác định
                continue

            if self._user_is_purchase_staff():
                if order.user_id != user:
                    raise AccessError(_("Bạn chỉ có thể thao tác với đơn mua của chính mình."))

    def write(self, vals):
        self._check_purchase_permissions()
        return super().write(vals)

    def unlink(self):
        self._check_purchase_permissions()
        return super().unlink()

