# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime


class SGCDocument(models.Model):
    _name = 'sgc.document'
    _description = 'Văn bản'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Tiêu đề', required=True)
    in_number = fields.Char(string='Số công văn đến')
    out_number = fields.Char(string='Số công văn đi', readonly=True)
    
    type = fields.Selection([
        ('in', 'Công văn đến'),
        ('out', 'Công văn đi')
    ], string='Loại', required=True, default='in')
    
    partner_id = fields.Many2one('res.partner', string='Người nhận')
    send_partner_id = fields.Many2one('res.partner', string='Người gửi')
    sign_user_id = fields.Many2one('res.partner', string='Người ký')
    signing_date = fields.Datetime(string='Ngày ký')
    received_date = fields.Datetime(
        string='Ngày nhận',
        default=fields.Datetime.now
    )
    
    document_type_id = fields.Many2one('sgc.document.type', string='Loại văn bản')
    document_body = fields.Html(string='Nội dung')
    document_summary = fields.Html(string='Tóm tắt')
    
    priority = fields.Selection([
        ('0', 'Bình thường'),
        ('1', 'Trung bình'),
        ('2', 'Cao'),
    ], string='Độ ưu tiên', default='0')
    
    effective_date = fields.Datetime(string='Ngày hiệu lực')
    expiry_date = fields.Datetime(string='Ngày hết hạn')
    department_id = fields.Many2one('hr.department', string='Nơi lưu trữ')
    
    user_ids = fields.Many2many(
        'res.users',
        'sgc_document_users_implementer_rel',
        string='Người xử lý'
    )
    follower_ids = fields.Many2many(
        'res.users',
        'sgc_document_users_follower_rel',
        string='Người theo dõi'
    )
    
    status_id = fields.Many2one(
        'sgc.document.status',
        string='Trạng thái',
        tracking=True,
        required=True
    )
    
    file = fields.Binary(string='Tệp đính kèm')
    file_name = fields.Char(string='Tên tệp')
    
    display_number = fields.Char(
        string='Số văn bản',
        compute='_compute_display_number',
        store=True
    )
    
    history_ids = fields.One2many(
        'sgc.document.history',
        'document_id',
        string='Lịch sử xử lý'
    )
    
    # Status helpers
    is_show_1 = fields.Boolean(related="status_id.is_show_1")
    is_show_2 = fields.Boolean(related="status_id.is_show_2")
    is_show_response = fields.Boolean(related="status_id.is_show_response")
    name_1 = fields.Char(related="status_id.name_1")
    name_2 = fields.Char(related="status_id.name_2")
    is_won = fields.Boolean(related="status_id.is_won")
    is_print_pdf = fields.Boolean(related="status_id.is_print_pdf")
    
    related_document_id = fields.Many2one('sgc.document', string='Văn bản liên quan')
    related_document_count = fields.Integer(
        string='Số văn bản liên quan',
        compute='_compute_related_document'
    )
    description = fields.Html(string='Mô tả')
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )
    
    # Additional fields for Odoo 17 compatibility
    recipient_name = fields.Html(string='Tên người nhận')
    department_name = fields.Char(
        string='Tên phòng ban',
        related='department_id.name',
        store=False
    )
    user_process_id = fields.Many2one(
        'res.users',
        string='Người xử lý chính',
        compute='_compute_user_process_id',
        store=False
    )
    
    @api.depends('user_ids')
    def _compute_user_process_id(self):
        for rec in self:
            if rec.user_ids:
                rec.user_process_id = rec.user_ids[0]
            else:
                rec.user_process_id = False

    @api.depends('type', 'in_number', 'out_number')
    def _compute_display_number(self):
        for rec in self:
            if rec.type == 'in' and rec.in_number:
                rec.display_number = rec.in_number
            elif rec.type == 'out' and rec.out_number:
                rec.display_number = rec.out_number
            else:
                rec.display_number = ''

    def _compute_related_document(self):
        for rec in self:
            rec.related_document_count = self.search_count([
                ('related_document_id', '=', rec.id)
            ])

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        context = self.env.context
        
        if context.get('is_out_document'):
            result['type'] = 'out'
            status = self.env['sgc.document.status'].search([
                ('type', '=', 'out'),
                ('is_default', '=', True),
                ('active', '=', True)
            ], limit=1)
            if status:
                result['status_id'] = status.id
        elif context.get('is_in_document'):
            result['type'] = 'in'
            status = self.env['sgc.document.status'].search([
                ('type', '=', 'in'),
                ('is_default', '=', True),
                ('active', '=', True)
            ], limit=1)
            if status:
                result['status_id'] = status.id
        
        result['user_ids'] = [(6, 0, [self.env.user.id])]
        return result

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            ctx = self.env.context
            if ctx.get('is_out_document') and not vals.get('out_number'):
                today = datetime.datetime.today()
                year = today.strftime('%Y')
                seq = self.env['ir.sequence'].next_by_code('sgc.document.out')
                vals['out_number'] = f"{seq}/{year}/SGC"
        return super().create(vals_list)

    def _log_history(self, status, response=None):
        for rec in self:
            self.env['sgc.document.history'].create({
                'document_id': rec.id,
                'user_id': self.env.user.id,
                'status_id': status.id,
                'type': rec.type,
                'date': fields.Datetime.now(),
                'response': response,
            })

    def _check_permission(self, current_status):
        self.ensure_one()
        if self.env.user.id not in self.user_ids.ids:
            raise UserError(_("Bạn không có quyền thực hiện hành động này."))

    def next_status_action01(self):
        self.ensure_one()
        self._check_permission(self.status_id)
        return self._action_update_status(
            self.status_id,
            self.status_id.next_stage_1
        )

    def next_status_action02(self):
        self.ensure_one()
        self._check_permission(self.status_id)
        return self._action_update_status(
            self.status_id,
            self.status_id.next_stage_2
        )

    def _action_update_status(self, current_status, next_status):
        self.ensure_one()
        
        if not next_status:
            raise UserError(_("Không tìm thấy trạng thái tiếp theo."))
        
        # Check if need to select users or show response
        if next_status.select_responsive_user or current_status.is_show_response:
            return {
                'name': _('Chọn người xử lý'),
                'type': 'ir.actions.act_window',
                'res_model': 'sgc.document.user.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_document_id': self.id,
                    'default_next_status_id': next_status.id,
                    'default_show_response': current_status.is_show_response,
                    'default_show_users': next_status.select_responsive_user,
                },
            }
        
        # Direct update
        if next_status.user_ids:
            self.user_ids = [(6, 0, next_status.user_ids.ids)]
        else:
            self.user_ids = [(6, 0, [self.create_uid.id])]
        
        self._log_history(current_status)
        self.status_id = next_status
        
        return True

    def action_view_related_documents(self):
        return {
            'name': _('Văn bản liên quan'),
            'type': 'ir.actions.act_window',
            'res_model': 'sgc.document',
            'view_mode': 'list,form',
            'domain': [('related_document_id', '=', self.id)],
        }

