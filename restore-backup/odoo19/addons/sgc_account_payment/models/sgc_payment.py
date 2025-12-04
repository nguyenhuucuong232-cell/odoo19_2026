# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class SGCPayment(models.Model):
    _name = 'sgc.payment'
    _order = 'create_date desc'
    _description = 'Giao dịch thanh toán'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Mã",
        default=lambda self: _('New'),
        copy=False,
        readonly=True
    )
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('posted', 'Đã xác nhận'),
        ('cancel', 'Đã hủy')
    ], string='Trạng thái', readonly=True, copy=False, index=True, default='draft', tracking=True)
    
    payment_type = fields.Selection([
        ('inbound', 'Thu'),
        ('outbound', 'Chi')
    ], string='Loại', required=True, copy=False, default='outbound')
    
    partner_id = fields.Many2one('res.partner', string='Đối tác')
    total_amount = fields.Float(
        string='Tổng tiền',
        readonly=True,
        compute='_compute_total_amount',
        digits=(18, 0),
        store=True
    )
    date = fields.Date(
        string='Ngày',
        required=True,
        default=lambda self: fields.Date.today()
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Sổ nhật ký',
        domain=[('type', 'in', ['bank', 'cash'])],
        required=True
    )
    previous_journal_id = fields.Many2one(
        'account.journal',
        string='Sổ nhật ký trước',
        readonly=True,
        copy=False
    )
    partner_bank_id = fields.Many2one('res.partner.bank', string='Tài khoản ngân hàng')
    payment_person_id = fields.Many2one('res.partner', string='Người thanh toán')
    line_ids = fields.One2many('sgc.payment.line', 'payment_id', string='Chi tiết thanh toán')
    move_id = fields.Many2one('account.move', string='Bút toán')
    description = fields.Char(string='Mô tả', compute="_compute_description", store=True)
    team_id = fields.Many2one('crm.team', string='Nhóm bán hàng')
    internal_transfer = fields.Boolean(string='Chuyển nội bộ')
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )

    @api.depends('line_ids.amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('amount'))

    @api.depends('line_ids.description')
    def _compute_description(self):
        for rec in self:
            rec.description = rec.line_ids and rec.line_ids[0].description or False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.payment.sequence') or _('New')
            if 'journal_id' in vals:
                vals['previous_journal_id'] = vals['journal_id']
        return super().create(vals_list)

    def copy(self, default=None):
        if default is None:
            default = {}
        default.update({
            'payment_type': self.payment_type,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'journal_id': self.journal_id.id,
            'internal_transfer': self.internal_transfer,
            'line_ids': [(0, 0, {
                'amount': line.amount,
                'account_id': line.account_id.id,
                'description': line.description,
                'analytic_distribution': line.analytic_distribution,
                'item_detail_id': line.item_detail_id.id,
                'team_id': line.team_id.id,
            }) for line in self.line_ids]
        })
        return super().copy(default)

    def unlink(self):
        for rec in self:
            if rec.state == 'posted':
                raise UserError(_('Không thể xóa thanh toán đã xác nhận. Vui lòng chuyển về nháp trước.'))
            if rec.move_id:
                rec.move_id.unlink()
        return super().unlink()

    def write(self, vals):
        for record in self:
            if 'journal_id' in vals and record.state != 'draft':
                raise ValidationError(_('Không thể thay đổi sổ nhật ký khi không ở trạng thái nháp.'))
        return super().write(vals)

    def action_post(self):
        for rec in self:
            if rec.previous_journal_id and rec.previous_journal_id.id != rec.journal_id.id:
                raise ValidationError(_('Sổ nhật ký đã bị thay đổi!'))
            rec.state = 'posted'
            if rec.move_id:
                rec.move_id.action_post()

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
            if rec.move_id:
                rec.move_id.button_cancel()

    def action_draft(self):
        for rec in self:
            rec.previous_journal_id = rec.journal_id
            rec.state = 'draft'
            if rec.move_id:
                rec.move_id.button_draft()

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        if self.journal_id:
            related_bank = self.env['res.partner.bank'].search([
                ('journal_id', '=', self.journal_id.id)
            ], limit=1)
            self.partner_bank_id = related_bank or False

