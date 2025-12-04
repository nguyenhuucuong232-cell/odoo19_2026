# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SGCHRAnnouncement(models.Model):
    _name = 'sgc.hr.announcement'
    _description = 'HR Announcement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Mã số',
        readonly=True,
        copy=False,
        help="Mã số thông báo"
    )
    title = fields.Text(
        string='Tiêu đề',
        required=True,
        help="Tiêu đề thông báo"
    )
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('to_approve', 'Chờ phê duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('rejected', 'Từ chối'),
        ('expired', 'Hết hạn')
    ], string='Trạng thái', default='draft', tracking=True)
    
    requested_date = fields.Date(
        string='Ngày tạo',
        default=fields.Date.today,
        readonly=True,
        help="Ngày tạo thông báo"
    )
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'sgc_announcement_attachment_rel',
        'announcement_id',
        'attachment_id',
        string="Đính kèm",
        help='Đính kèm tài liệu'
    )
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company,
        readonly=True
    )
    is_general = fields.Boolean(
        string='Thông báo chung?',
        help="Đánh dấu là thông báo chung cho tất cả"
    )
    announcement_type = fields.Selection([
        ('employee', 'Theo nhân viên'),
        ('department', 'Theo phòng ban'),
        ('job_position', 'Theo vị trí công việc')
    ], string='Loại thông báo')
    
    employee_ids = fields.Many2many(
        'hr.employee',
        'sgc_announcement_employee_rel',
        'announcement_id',
        'employee_id',
        string='Nhân viên',
        help="Nhân viên nhận thông báo"
    )
    department_ids = fields.Many2many(
        'hr.department',
        'sgc_announcement_department_rel',
        'announcement_id',
        'department_id',
        string='Phòng ban',
        help="Phòng ban nhận thông báo"
    )
    position_ids = fields.Many2many(
        'hr.job',
        'sgc_announcement_job_rel',
        'announcement_id',
        'job_id',
        string='Vị trí công việc',
        help="Vị trí công việc nhận thông báo"
    )
    content = fields.Html(
        string='Nội dung',
        help="Nội dung thông báo"
    )
    date_start = fields.Date(
        string='Ngày bắt đầu',
        default=fields.Date.today,
        required=True,
        help="Ngày bắt đầu hiển thị thông báo"
    )
    date_end = fields.Date(
        string='Ngày kết thúc',
        default=fields.Date.today,
        required=True,
        help="Ngày kết thúc hiển thị thông báo"
    )

    def action_send_for_approval(self):
        """Send announcement for approval"""
        self.write({'state': 'to_approve'})

    def action_approve(self):
        """Approve announcement"""
        self.write({'state': 'approved'})

    def action_reject(self):
        """Reject announcement"""
        self.write({'state': 'rejected'})

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start > record.date_end:
                raise ValidationError(_("Ngày bắt đầu phải nhỏ hơn ngày kết thúc"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_general'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.hr.announcement.general')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.hr.announcement')
        return super().create(vals_list)

    @api.model
    def _cron_check_expiry(self):
        """Cron job to check and expire announcements"""
        today = fields.Date.today()
        expired_announcements = self.search([
            ('state', 'not in', ['rejected', 'expired']),
            ('date_end', '<', today)
        ])
        expired_announcements.write({'state': 'expired'})

