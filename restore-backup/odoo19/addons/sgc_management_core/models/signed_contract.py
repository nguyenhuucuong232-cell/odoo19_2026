# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SignedContract(models.Model):
    _name = 'sgc.signed.contract'
    _description = 'Hợp đồng đã ký (SGC)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # ==========================================
    # TRƯỜNG CƠ BẢN - TITLE
    # ==========================================
    
    name = fields.Char(
        string='Số hợp đồng', 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: _('New'),
        tracking=True
    )
    
    # ==========================================
    # THÔNG TIN CHUNG (CỘT TRÁI - PHẦN TRÊN)
    # ==========================================
    
    internal_code = fields.Char(
        string='Mã hợp đồng nội bộ',
        tracking=True
    )
    
    template_id = fields.Many2one(
        'sgc.contract.template',
        string='Mẫu hợp đồng'
    )
    
    contract_type = fields.Selection([
        ('service', 'Dịch vụ'),
        ('product', 'Sản phẩm'),
        ('mixed', 'Hỗn hợp'),
    ], string='Loại hợp đồng', default='service')
    
    ref_order_id = fields.Many2one(
        'sale.order', 
        string='Đơn hàng tham chiếu'
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Nhân viên phụ trách',
        default=lambda self: self.env.user,
        tracking=True
    )
    
    description = fields.Text(
        string='Nội dung hợp đồng'
    )
    
    # ==========================================
    # NGÀY THÁNG (CỘT TRÁI - PHẦN DƯỚI)
    # ==========================================
    
    date_signed = fields.Date(
        string='Ngày ký hợp đồng', 
        tracking=True
    )
    
    date_end = fields.Date(
        string='Ngày kết thúc', 
        tracking=True
    )
    
    notice_days = fields.Integer(
        string='Số ngày thông báo',
        default=7
    )
    
    is_overdue = fields.Boolean(
        string='Quá hạn',
        compute='_compute_is_overdue',
        store=True
    )
    
    overdue_reason_id = fields.Many2one(
        'sgc.overdue.reason',
        string='Lý do quá hạn'
    )
    
    overdue_description = fields.Text(
        string='Mô tả chi tiết lý do quá hạn'
    )
    
    date_create = fields.Date(
        string='Ngày tạo',
        default=fields.Date.context_today,
        readonly=True
    )
    
    frequency = fields.Char(
        string='Tần suất'
    )
    
    # ==========================================
    # BÊN A - THUÊ DỊCH VỤ (KHÁCH HÀNG)
    # ==========================================
    
    partner_id = fields.Many2one(
        'res.partner', 
        string='Khách hàng', 
        required=True,
        tracking=True
    )
    
    partner_phone = fields.Char(
        string='Điện thoại liên hệ',
        related='partner_id.phone',
        readonly=True
    )
    
    representative_a = fields.Char(
        string='Đại diện'
    )
    
    bank_account_a = fields.Many2one(
        'res.partner.bank',
        string='Tài khoản thanh toán',
        domain="[('partner_id', '=', partner_id)]"
    )
    
    auth_number_a = fields.Char(
        string='Theo giấy ủy quyền số'
    )
    
    show_auth_a = fields.Boolean(
        string='Hiển thị giấy ủy quyền'
    )
    
    # ==========================================
    # BÊN B - CUNG CẤP DỊCH VỤ (CÔNG TY)
    # ==========================================
    
    company_id = fields.Many2one(
        'res.company', 
        string='Công ty', 
        default=lambda self: self.env.company,
        required=True
    )
    
    representative_b = fields.Char(
        string='Đại diện',
        default='Nguyễn Hữu Dương'
    )
    
    bank_account_b = fields.Many2one(
        'res.partner.bank',
        string='Tài khoản thanh toán'
    )
    
    auth_number_b = fields.Char(
        string='Theo giấy ủy quyền số'
    )
    
    show_auth_b = fields.Boolean(
        string='Hiển thị giấy ủy quyền'
    )
    
    # ==========================================
    # ĐIỀU KHOẢN HỢP ĐỒNG
    # ==========================================
    
    contract_product_desc = fields.Text(
        string='Sản phẩm của hợp đồng'
    )
    
    quality_desc = fields.Text(
        string='Chất lượng hợp đồng'
    )
    
    form_type = fields.Char(
        string='Hình thức hợp đồng'
    )
    
    show_signer = fields.Boolean(
        string='Hiển thị người ký'
    )
    
    sampling_location = fields.Char(
        string='Địa điểm lấy mẫu'
    )
    
    sampling_time = fields.Char(
        string='Thời gian lấy mẫu thực hiện'
    )
    
    duration_days = fields.Integer(
        string='Thời hạn thực hiện hợp đồng',
        help='Số ngày thực hiện hợp đồng'
    )
    
    payment_term_days = fields.Integer(
        string='Thời gian cho phép thanh toán',
        help='Số ngày cho phép thanh toán'
    )
    
    # ==========================================
    # ĐIỀU KHOẢN THANH TOÁN
    # ==========================================
    
    payment_condition = fields.Text(
        string='Điều kiện'
    )
    
    # ==========================================
    # CẤU HÌNH FILE IN
    # ==========================================
    
    line_spacing = fields.Float(
        string='Khoảng cách dòng',
        default=1.5
    )
    
    # ==========================================
    # TIỀN TỆ & GIÁ TRỊ
    # ==========================================
    
    currency_id = fields.Many2one(
        'res.currency', 
        string='Tiền tệ', 
        related='company_id.currency_id'
    )
    
    amount_total = fields.Monetary(
        string='Tổng giá trị', 
        currency_field='currency_id', 
        tracking=True,
        compute='_compute_amount_total',
        store=True
    )
    
    # ==========================================
    # TRẠNG THÁI
    # ==========================================
    
    state = fields.Selection([
        ('draft', 'Mới tạo'),
        ('in_progress', 'Đang thực hiện'),
        ('handover', 'Bàn giao'),
        ('acceptance', 'Nghiệm thu'),
        ('done', 'Hoàn tất'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='draft', tracking=True)

    active = fields.Boolean(
        default=True, 
        string="Hoạt động"
    )
    
    # ==========================================
    # LIÊN KẾT
    # ==========================================
    
    project_id = fields.Many2one(
        'project.project', 
        string='Dự án'
    )
    
    # Giữ lại để tương thích ngược
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Đơn hàng gốc',
        related='ref_order_id',
        store=True
    )
    
    # ==========================================
    # ONE2MANY - CHI TIẾT THANH TOÁN
    # ==========================================
    
    payment_line_ids = fields.One2many(
        'sgc.contract.payment.line',
        'contract_id',
        string='Chi tiết thanh toán'
    )
    
    # ==========================================
    # SMART BUTTON COUNTS
    # ==========================================
    
    acceptance_count = fields.Integer(
        string='Biên bản nghiệm thu',
        compute='_compute_document_counts'
    )
    
    handover_count = fields.Integer(
        string='Biên bản bàn giao',
        compute='_compute_document_counts'
    )
    
    sampling_count = fields.Integer(
        string='Biên bản lấy mẫu',
        compute='_compute_document_counts'
    )
    
    bbqt_count = fields.Integer(
        string='BBQT',
        compute='_compute_document_counts'
    )
    
    document_count = fields.Integer(
        string='Documents',
        compute='_compute_document_counts'
    )
    
    # ==========================================
    # COMPUTE METHODS
    # ==========================================
    
    @api.depends('date_end')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.date_end:
                record.is_overdue = record.date_end < today
            else:
                record.is_overdue = False
    
    @api.depends('payment_line_ids.price_subtotal')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.payment_line_ids.mapped('price_subtotal'))
    
    def _compute_document_counts(self):
        """Tính số lượng các biên bản liên quan"""
        for record in self:
            record.acceptance_count = self.env['sgc.acceptance.minutes'].search_count([
                ('contract_id', '=', record.id)
            ])
            record.handover_count = self.env['sgc.handover.minutes'].search_count([
                ('contract_id', '=', record.id)
            ])
            record.sampling_count = self.env['sgc.sampling.minutes'].search_count([
                ('contract_id', '=', record.id)
            ])
            record.bbqt_count = self.env['sgc.payment.request'].search_count([
                ('contract_id', '=', record.id)
            ])
            record.document_count = record.acceptance_count + record.handover_count + record.sampling_count + record.bbqt_count
    
    # ==========================================
    # ACTION METHODS - BUTTONS
    # ==========================================
    
    def action_start(self):
        """Bắt đầu hợp đồng"""
        for record in self:
            if record.state == 'draft':
                record.state = 'in_progress'
    
    def action_handover(self):
        """Chuyển sang trạng thái bàn giao"""
        for record in self:
            if record.state == 'in_progress':
                record.state = 'handover'
    
    def action_acceptance(self):
        """Chuyển sang trạng thái nghiệm thu"""
        for record in self:
            if record.state == 'handover':
                record.state = 'acceptance'
    
    def action_done(self):
        """Hoàn tất hợp đồng"""
        for record in self:
            if record.state == 'acceptance':
                record.state = 'done'
    
    def action_cancel(self):
        """Hủy hợp đồng"""
        for record in self:
            record.state = 'cancelled'
    
    def action_reset_draft(self):
        """Reset về trạng thái nháp"""
        for record in self:
            record.state = 'draft'
    
    def action_print_pdf(self):
        """In PDF hợp đồng"""
        return self.env.ref('sgc_management_core.action_report_signed_contract').report_action(self)
    
    def action_create_bbqt(self):
        """Tạo biên bản quyết toán"""
        # Placeholder - implement khi có model BBQT
        pass
    
    # ==========================================
    # SMART BUTTON ACTIONS
    # ==========================================
    
    def action_view_acceptance(self):
        """Xem biên bản nghiệm thu"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Biên bản nghiệm thu',
            'res_model': 'sgc.acceptance.minutes',
            'view_mode': 'list,form',
            'domain': [('contract_id', '=', self.id)],
            'context': {'default_contract_id': self.id},
        }
    
    def action_view_handover(self):
        """Xem biên bản bàn giao"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Biên bản bàn giao tài liệu',
            'res_model': 'sgc.handover.minutes',
            'view_mode': 'list,form',
            'domain': [('contract_id', '=', self.id)],
            'context': {'default_contract_id': self.id},
        }
    
    def action_view_sampling(self):
        """Xem biên bản lấy mẫu"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Biên bản lấy mẫu',
            'res_model': 'sgc.sampling.minutes',
            'view_mode': 'list,form',
            'domain': [('contract_id', '=', self.id)],
            'context': {'default_contract_id': self.id},
        }
    
    def action_view_bbqt(self):
        """Xem đề nghị thanh toán"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đề nghị thanh toán',
            'res_model': 'sgc.payment.request',
            'view_mode': 'list,form',
            'domain': [('contract_id', '=', self.id)],
            'context': {'default_contract_id': self.id},
        }
    
    def action_view_documents(self):
        """Xem tài liệu đính kèm"""
        # Placeholder
        pass
    
    # ==========================================
    # CRUD METHODS
    # ==========================================
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to generate sequence for contract name"""
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sgc.signed.contract') or _('New')
        return super(SignedContract, self).create(vals_list)
    
    def unlink(self):
        """Prevent deletion if project is active"""
        for contract in self:
            if contract.project_id and contract.project_id.active:
                raise UserError(_(
                    'Không thể xóa Hợp đồng "%s" vì Dự án "%s" đang hoạt động.\n'
                    'Vui lòng lưu trữ (archive) dự án trước khi xóa hợp đồng.'
                ) % (contract.name, contract.project_id.name))
        return super(SignedContract, self).unlink()
    
    # ==========================================
    # LEGACY METHODS (Giữ lại để tương thích)
    # ==========================================
    
    def action_confirm_contract(self):
        """Xác nhận và tạo dự án từ template"""
        self.ensure_one()
        
        template = self.env.ref('sgc_management_core.sgc_project_template', raise_if_not_found=False)
        if not template:
            raise UserError(_('Không tìm thấy "Dự án Mẫu". Vui lòng kiểm tra file project_data.xml'))

        new_project = template.copy({
            'name': f"{self.name} - {self.partner_id.name}",
            'is_template': False,
            'partner_id': self.partner_id.id,
            'contract_id': self.id,
            'sale_order_id': self.ref_order_id.id if self.ref_order_id else False,
        })

        self.write({
            'state': 'in_progress',
            'project_id': new_project.id
        })
        
        if self.ref_order_id:
            self.ref_order_id.with_context(sgc_skip_sales_permission=True).write({'sgc_project_id': new_project.id})
            self.ref_order_id._update_prj_flow_state('b2c_project')
            self.ref_order_id._update_prj_flow_state('b4_execute')
            self.ref_order_id._update_prj_flow_state('b5_tracking')
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'res_id': new_project.id,
            'view_mode': 'form',
            'target': 'current',
            'name': _('Dự án vừa tạo'),
        }

    def action_mark_as_done(self):
        """Đánh dấu hoàn thành"""
        self.state = 'done'
        template = self.env.ref('sgc_management_core.customer_care_template_default', raise_if_not_found=False)
        if template:
            for contract in self:
                template._schedule_customer_care(
                    partner=contract.partner_id,
                    care_type='completed',
                    contract=contract,
                    reference_date=contract.date_end or fields.Date.context_today(contract)
                )
                if contract.ref_order_id:
                    contract.ref_order_id._update_prj_flow_state('b7_contract_done')


class ContractPaymentLine(models.Model):
    _name = 'sgc.contract.payment.line'
    _description = 'Chi tiết thanh toán hợp đồng'
    _order = 'sequence, id'
    
    contract_id = fields.Many2one(
        'sgc.signed.contract',
        string='Hợp đồng',
        required=True,
        ondelete='cascade'
    )
    
    sequence = fields.Integer(
        string='STT',
        default=10
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Sản phẩm'
    )
    
    name = fields.Char(
        string='Diễn giải'
    )
    
    product_uom_qty = fields.Float(
        string='Số lượng',
        default=1.0
    )
    
    product_uom = fields.Many2one(
        'uom.uom',
        string='Đơn vị tính'
    )
    
    price_unit = fields.Float(
        string='Đơn giá'
    )
    
    frequency = fields.Char(
        string='Tần suất'
    )
    
    tax_ids = fields.Many2many(
        'account.tax',
        string='Thuế'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Tiền tệ',
        related='contract_id.currency_id'
    )
    
    price_subtotal = fields.Monetary(
        string='Thành tiền',
        currency_field='currency_id',
        compute='_compute_price_subtotal',
        store=True
    )
    
    @api.depends('product_uom_qty', 'price_unit', 'tax_ids')
    def _compute_price_subtotal(self):
        for line in self:
            subtotal = line.product_uom_qty * line.price_unit
            if line.tax_ids:
                taxes = line.tax_ids.compute_all(
                    line.price_unit,
                    currency=line.currency_id,
                    quantity=line.product_uom_qty,
                    product=line.product_id,
                )
                subtotal = taxes['total_included']
            line.price_subtotal = subtotal
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.product_uom = self.product_id.uom_id
            self.price_unit = self.product_id.list_price


class ContractTemplate(models.Model):
    _name = 'sgc.contract.template'
    _description = 'Mẫu hợp đồng'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    # ==========================================
    # THÔNG TIN CƠ BẢN
    # ==========================================
    
    name = fields.Char(
        string='Tên mẫu',
        required=True,
        tracking=True
    )
    
    code = fields.Char(
        string='Mã mẫu'
    )
    
    create_date = fields.Datetime(
        string='Ngày tạo',
        readonly=True
    )
    
    description = fields.Text(
        string='Diễn giải'
    )
    
    # ==========================================
    # THÔNG TIN HỢP ĐỒNG
    # ==========================================
    
    contract_type_id = fields.Many2one(
        'sgc.contract.type',
        string='Loại hợp đồng',
        tracking=True
    )
    
    contract_product_desc = fields.Text(
        string='Sản phẩm của hợp đồng'
    )
    
    quality_desc = fields.Text(
        string='Chất lượng hợp đồng'
    )
    
    form_type = fields.Char(
        string='Hình thức hợp đồng'
    )
    
    # ==========================================
    # NỘI DUNG MẪU
    # ==========================================
    
    content = fields.Html(
        string='Nội dung mẫu'
    )
    
    active = fields.Boolean(
        default=True,
        string='Hoạt động'
    )


class ContractType(models.Model):
    _name = 'sgc.contract.type'
    _description = 'Loại hợp đồng'
    _order = 'sequence, name'
    
    name = fields.Char(
        string='Loại hợp đồng',
        required=True
    )
    
    short_name = fields.Char(
        string='Tên viết tắt'
    )
    
    description = fields.Text(
        string='Diễn giải loại hợp đồng'
    )
    
    sequence = fields.Integer(
        string='Thứ tự',
        default=10
    )
    
    active = fields.Boolean(
        default=True,
        string='Hoạt động'
    )
