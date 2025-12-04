# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrAnnouncement(models.Model):
    _name = 'sgc.hr.announcement'
    _description = 'Thông báo nhân sự'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Mã thông báo',
        readonly=True,
        copy=False,
        default=lambda self: _('New')
    )
    title = fields.Char(
        string='Tiêu đề',
        required=True,
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('to_approve', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
        ('expired', 'Hết hạn')
    ], string='Trạng thái', default='draft', tracking=True)
    
    requested_date = fields.Date(
        string='Ngày tạo',
        default=fields.Date.context_today,
        readonly=True
    )
    date_start = fields.Date(
        string='Ngày bắt đầu',
        default=fields.Date.context_today,
        required=True
    )
    date_end = fields.Date(
        string='Ngày kết thúc',
        default=fields.Date.context_today,
        required=True
    )
    
    is_general = fields.Boolean(
        string='Thông báo chung?',
        help='Thông báo cho tất cả nhân viên'
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
        string='Nhân viên'
    )
    department_ids = fields.Many2many(
        'hr.department',
        'sgc_announcement_department_rel',
        'announcement_id',
        'department_id',
        string='Phòng ban'
    )
    position_ids = fields.Many2many(
        'hr.job',
        'sgc_announcement_job_rel',
        'announcement_id',
        'job_id',
        string='Vị trí công việc'
    )
    
    content = fields.Html(
        string='Nội dung',
        sanitize_style=True
    )
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'sgc_announcement_attachment_rel',
        'announcement_id',
        'attachment_id',
        string='Đính kèm'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company,
        readonly=True
    )
    user_id = fields.Many2one(
        'res.users',
        string='Người tạo',
        default=lambda self: self.env.user,
        readonly=True
    )

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end:
                if record.date_start > record.date_end:
                    raise ValidationError(_("Ngày bắt đầu phải nhỏ hơn ngày kết thúc!"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_general'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.hr.announcement.general') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.hr.announcement') or _('New')
        return super().create(vals_list)

    def action_submit(self):
        """Gửi yêu cầu phê duyệt"""
        self.write({'state': 'to_approve'})

    def action_approve(self):
        """Phê duyệt thông báo"""
        self.write({'state': 'approved'})

    def action_reject(self):
        """Từ chối thông báo"""
        self.write({'state': 'rejected'})

    def action_reset_draft(self):
        """Đặt lại về nháp"""
        self.write({'state': 'draft'})

    @api.model
    def _cron_check_expiry(self):
        """Cron job kiểm tra và cập nhật thông báo hết hạn"""
        today = fields.Date.context_today(self)
        expired_announcements = self.search([
            ('state', '=', 'approved'),
            ('date_end', '<', today)
        ])
        expired_announcements.write({'state': 'expired'})

