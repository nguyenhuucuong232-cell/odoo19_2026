# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class PaymentTransaction(models.Model):
    _name = 'sgc.payment.transaction'
    _description = 'Giao dịch thanh toán'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Mã giao dịch",
        default=lambda self: _('New'),
        copy=False,
        readonly=True
    )
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('posted', 'Đã ghi sổ'),
        ('cancel', 'Đã hủy')
    ], string='Trạng thái', default='draft', tracking=True)
    
    payment_type = fields.Selection([
        ('inbound', 'Thu'),
        ('outbound', 'Chi')
    ], string='Loại giao dịch', required=True, default='outbound')
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Đối tác'
    )
    payment_person_id = fields.Many2one(
        'res.partner',
        string='Người thanh toán'
    )
    payment_person = fields.Char(string='Tên người thanh toán')
    
    date = fields.Date(
        string='Ngày',
        required=True,
        default=fields.Date.context_today
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Sổ nhật ký',
        domain="[('type', 'in', ['bank', 'cash'])]",
        required=True
    )
    previous_journal_id = fields.Many2one(
        'account.journal',
        string='Sổ nhật ký trước',
        readonly=True,
        copy=False
    )
    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Tài khoản ngân hàng'
    )
    
    line_ids = fields.One2many(
        'sgc.payment.line',
        'payment_id',
        string='Chi tiết thanh toán'
    )
    move_id = fields.Many2one(
        'account.move',
        string='Bút toán kế toán',
        readonly=True
    )
    
    total_amount = fields.Monetary(
        string='Tổng tiền',
        compute='_compute_total_amount',
        store=True,
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Tiền tệ',
        default=lambda self: self.env.company.currency_id
    )
    description = fields.Char(
        string='Mô tả',
        compute='_compute_description',
        store=True
    )
    
    team_id = fields.Many2one(
        'crm.team',
        string='Nhóm kinh doanh'
    )
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
            if rec.line_ids:
                rec.description = rec.line_ids[0].description
            else:
                rec.description = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.payment.transaction') or _('New')
            if 'journal_id' in vals:
                vals['previous_journal_id'] = vals['journal_id']
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            if 'journal_id' in vals and record.state != 'draft':
                raise ValidationError(_('Không thể thay đổi sổ nhật ký khi không ở trạng thái nháp.'))
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'posted':
                raise UserError(_('Không thể xóa giao dịch đã ghi sổ. Vui lòng hủy trước.'))
            if rec.move_id:
                rec.move_id.unlink()
        return super().unlink()

    def action_post(self):
        """Ghi sổ giao dịch"""
        for rec in self:
            if rec.previous_journal_id and rec.previous_journal_id != rec.journal_id:
                raise ValidationError(_('Sổ nhật ký đã bị thay đổi!'))
            
            # Tạo bút toán kế toán
            if not rec.move_id:
                rec._create_account_move()
            
            rec.state = 'posted'
            if rec.move_id:
                rec.move_id.action_post()

    def action_cancel(self):
        """Hủy giao dịch"""
        for rec in self:
            rec.state = 'cancel'
            if rec.move_id:
                rec.move_id.button_cancel()

    def action_draft(self):
        """Đặt lại về nháp"""
        for rec in self:
            rec.previous_journal_id = rec.journal_id
            rec.state = 'draft'
            if rec.move_id:
                rec.move_id.button_draft()

    def _create_account_move(self):
        """Tạo bút toán kế toán từ giao dịch thanh toán"""
        self.ensure_one()
        
        move_lines = []
        for line in self.line_ids:
            # Debit/Credit tùy theo loại giao dịch
            if self.payment_type == 'outbound':
                move_lines.append((0, 0, {
                    'account_id': line.account_id.id,
                    'name': line.description or self.name,
                    'debit': line.amount,
                    'credit': 0,
                    'partner_id': self.partner_id.id,
                    'analytic_distribution': line.analytic_distribution,
                }))
            else:
                move_lines.append((0, 0, {
                    'account_id': line.account_id.id,
                    'name': line.description or self.name,
                    'debit': 0,
                    'credit': line.amount,
                    'partner_id': self.partner_id.id,
                    'analytic_distribution': line.analytic_distribution,
                }))
        
        # Thêm dòng đối ứng từ journal
        journal_account = self.journal_id.default_account_id
        if journal_account:
            if self.payment_type == 'outbound':
                move_lines.append((0, 0, {
                    'account_id': journal_account.id,
                    'name': self.name,
                    'debit': 0,
                    'credit': self.total_amount,
                    'partner_id': self.partner_id.id,
                }))
            else:
                move_lines.append((0, 0, {
                    'account_id': journal_account.id,
                    'name': self.name,
                    'debit': self.total_amount,
                    'credit': 0,
                    'partner_id': self.partner_id.id,
                }))
        
        move = self.env['account.move'].create({
            'move_type': 'entry',
            'date': self.date,
            'journal_id': self.journal_id.id,
            'ref': self.name,
            'partner_id': self.partner_id.id,
            'line_ids': move_lines,
        })
        
        self.move_id = move

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        if self.journal_id:
            related_bank = self.env['res.partner.bank'].search([
                ('journal_id', '=', self.journal_id.id)
            ], limit=1)
            self.partner_bank_id = related_bank or False

    def copy(self, default=None):
        default = default or {}
        default.update({
            'payment_type': self.payment_type,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id if self.partner_bank_id else False,
            'journal_id': self.journal_id.id,
            'internal_transfer': self.internal_transfer,
            'line_ids': [(0, 0, {
                'amount': line.amount,
                'account_id': line.account_id.id,
                'description': line.description,
                'analytic_distribution': line.analytic_distribution,
                'item_detail_id': line.item_detail_id.id if line.item_detail_id else False,
                'team_id': line.team_id.id if line.team_id else False,
            }) for line in self.line_ids],
        })
        return super().copy(default)

