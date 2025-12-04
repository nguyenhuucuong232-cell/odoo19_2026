# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


# ============================================
# BIÊN BẢN BÀN GIAO TÀI LIỆU
# ============================================
class SgcHandoverMinutes(models.Model):
    _name = 'sgc.handover.minutes'
    _description = 'Biên bản bàn giao tài liệu'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char(
        string='Số biên bản',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    
    create_date = fields.Datetime(
        string='Ngày tạo',
        readonly=True
    )
    
    project_name = fields.Char(
        string='Dự án'
    )
    
    contract_id = fields.Many2one(
        'sgc.signed.contract',
        string='Hợp đồng ký kết',
        tracking=True
    )
    
    receiving_org = fields.Char(
        string='Cơ quan nhận tài liệu'
    )
    
    state = fields.Selection([
        ('draft', 'Mới tạo'),
        ('confirmed', 'Đã xác nhận'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='draft', tracking=True)
    
    handover_form_id = fields.Many2one(
        'sgc.handover.form',
        string='Hình thức bàn giao'
    )
    
    document_ids = fields.Many2many(
        'sgc.document.handover.config',
        string='Tài liệu bàn giao'
    )
    
    notes = fields.Text(
        string='Ghi chú'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'sgc_handover_minutes_attachment_rel',
        'minutes_id',
        'attachment_id',
        string='File đính kèm'
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.handover.minutes') or _('New')
        return super().create(vals_list)
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_done(self):
        self.write({'state': 'done'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_draft(self):
        self.write({'state': 'draft'})


# ============================================
# BIÊN BẢN LẤY MẪU
# ============================================
class SgcSamplingMinutes(models.Model):
    _name = 'sgc.sampling.minutes'
    _description = 'Biên bản lấy mẫu'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char(
        string='Số biên bản',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    
    create_date = fields.Datetime(
        string='Ngày tạo',
        readonly=True
    )
    
    contract_id = fields.Many2one(
        'sgc.signed.contract',
        string='Hợp đồng ký kết',
        tracking=True
    )
    
    sampling_date = fields.Datetime(
        string='Ngày lấy mẫu'
    )
    
    sampling_location = fields.Char(
        string='Địa điểm lấy mẫu'
    )
    
    sampler_id = fields.Many2one(
        'res.users',
        string='Người lấy mẫu',
        default=lambda self: self.env.user
    )
    
    sample_description = fields.Text(
        string='Mô tả mẫu'
    )
    
    state = fields.Selection([
        ('draft', 'Mới tạo'),
        ('confirmed', 'Đã xác nhận'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='draft', tracking=True)
    
    notes = fields.Text(
        string='Ghi chú'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'sgc_sampling_minutes_attachment_rel',
        'minutes_id',
        'attachment_id',
        string='File đính kèm'
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.sampling.minutes') or _('New')
        return super().create(vals_list)
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_done(self):
        self.write({'state': 'done'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_draft(self):
        self.write({'state': 'draft'})


# ============================================
# BIÊN BẢN NGHIỆM THU
# ============================================
class SgcAcceptanceMinutes(models.Model):
    _name = 'sgc.acceptance.minutes'
    _description = 'Biên bản nghiệm thu'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char(
        string='Số biên bản',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    
    create_date = fields.Datetime(
        string='Ngày tạo',
        readonly=True
    )
    
    contract_id = fields.Many2one(
        'sgc.signed.contract',
        string='Hợp đồng ký kết',
        tracking=True
    )
    
    acceptance_date = fields.Date(
        string='Ngày nghiệm thu'
    )
    
    acceptor_id = fields.Many2one(
        'res.users',
        string='Người nghiệm thu',
        default=lambda self: self.env.user
    )
    
    result = fields.Selection([
        ('pass', 'Đạt'),
        ('fail', 'Không đạt'),
        ('conditional', 'Đạt có điều kiện'),
    ], string='Kết quả', default='pass')
    
    state = fields.Selection([
        ('draft', 'Mới tạo'),
        ('confirmed', 'Đã xác nhận'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='draft', tracking=True)
    
    notes = fields.Text(
        string='Ghi chú'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'sgc_acceptance_minutes_attachment_rel',
        'minutes_id',
        'attachment_id',
        string='File đính kèm'
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.acceptance.minutes') or _('New')
        return super().create(vals_list)
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_done(self):
        self.write({'state': 'done'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_draft(self):
        self.write({'state': 'draft'})


# ============================================
# ĐỀ NGHỊ THANH TOÁN
# ============================================
class SgcPaymentRequest(models.Model):
    _name = 'sgc.payment.request'
    _description = 'Đề nghị thanh toán'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char(
        string='Số đề nghị',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    
    create_date = fields.Datetime(
        string='Ngày tạo',
        readonly=True
    )
    
    contract_id = fields.Many2one(
        'sgc.signed.contract',
        string='Hợp đồng ký kết',
        tracking=True
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Khách hàng',
        related='contract_id.partner_id',
        store=True
    )
    
    amount = fields.Monetary(
        string='Số tiền đề nghị',
        currency_field='currency_id'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Tiền tệ',
        default=lambda self: self.env.company.currency_id
    )
    
    payment_method_id = fields.Many2one(
        'sgc.payment.method',
        string='Phương thức thanh toán'
    )
    
    due_date = fields.Date(
        string='Ngày đến hạn'
    )
    
    state = fields.Selection([
        ('draft', 'Mới tạo'),
        ('submitted', 'Đã gửi'),
        ('approved', 'Đã duyệt'),
        ('paid', 'Đã thanh toán'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='draft', tracking=True)
    
    notes = fields.Text(
        string='Ghi chú'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'sgc_payment_request_attachment_rel',
        'request_id',
        'attachment_id',
        string='File đính kèm'
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.payment.request') or _('New')
        return super().create(vals_list)
    
    def action_submit(self):
        self.write({'state': 'submitted'})
    
    def action_approve(self):
        self.write({'state': 'approved'})
    
    def action_paid(self):
        self.write({'state': 'paid'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_draft(self):
        self.write({'state': 'draft'})

