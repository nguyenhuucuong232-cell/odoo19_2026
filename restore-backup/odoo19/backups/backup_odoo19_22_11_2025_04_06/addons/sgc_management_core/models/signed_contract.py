# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

# Định nghĩa một model Odoo mới
# _name là tên kỹ thuật của model (tên bảng trong CSDL)
# _inherit = ['mail.thread'] thêm tính năng chatter (lịch sử, theo dõi) ở cuối form
class SignedContract(models.Model):
    _name = 'sgc.signed.contract'
    _description = 'Hợp đồng đã ký (SGC)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # --- Trường (Fields) Cơ bản ---
    
    # 'name' là trường tiêu đề chính, có 'required=True' (bắt buộc nhập)
    # Sử dụng sequence tự động
    name = fields.Char(
        string='Mã Hợp đồng', 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: _('New')
    )
    
    # Liên kết "Nhiều-đến-Một" tới model Khách hàng (res.partner)
    partner_id = fields.Many2one(
        'res.partner', 
        string='Khách hàng', 
        required=True
    )
    
    # Liên kết "Nhiều-đến-Một" tới model Đơn hàng (sale.order)
    sale_order_id = fields.Many2one(
        'sale.order', 
        string='Đơn hàng Gốc'
    )
    
    # Liên kết "Nhiều-đến-Một" tới model Dự án (project.project)
    project_id = fields.Many2one(
        'project.project', 
        string='Dự án'
    )
    
    # Trường ngày, có 'tracking=True' để tự động ghi lịch sử (chatter) khi thay đổi
    sign_date = fields.Date(
        string='Ngày ký', 
        tracking=True
    )
    
    start_date = fields.Date(
        string='Ngày hiệu lực', 
        tracking=True
    )
    
    end_date = fields.Date(
        string='Ngày kết thúc', 
        tracking=True
    )
    
    # Trường tiền tệ
    # Cần 'company_id' và 'currency_id' để Odoo biết dùng đơn vị tiền tệ nào
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
    
    contract_value = fields.Monetary(
        string='Giá trị Hợp đồng', 
        currency_field='currency_id', 
        tracking=True
    )

    # Thanh trạng thái (statusbar)
    state = fields.Selection(
        [
            ('draft', 'Nháp'),
            ('active', 'Đang thực hiện'),
            ('done', 'Hoàn thành'),
            ('cancel', 'Hủy bỏ'),
        ], 
        string='Trạng thái', 
        default='draft', 
        tracking=True
    )

    # Thêm trường 'active' để có thể Lưu trữ (Archive)
    active = fields.Boolean(
        default=True, 
        string="Hoạt động"
    )

    # --- Hàm (Methods) ---
    
    # Chúng ta sẽ thêm các hàm (như nút bấm) ở Giai đoạn 6
    def action_confirm_contract(self):
        self.ensure_one()
        
        # 1. Tìm "Dự án Mẫu" mà chúng ta đã tạo ở Bước 7.1
        # Lưu ý: 'sgc_management_core.sgc_project_template' là XML ID
        template = self.env.ref('sgc_management_core.sgc_project_template', raise_if_not_found=False)
        if not template:
            # Nếu không tìm thấy template, báo lỗi
            raise models.UserError('Không tìm thấy "Dự án Mẫu". Vui lòng kiểm tra file project_data.xml')

        # 2. Sao chép (copy) template để tạo Dự án mới
        new_project = template.copy({
            'name': f"{self.name} - {self.partner_id.name}", # Tên dự án mới
            'is_template': False,           # Đánh dấu đây là dự án thật
            'partner_id': self.partner_id.id,
            'contract_id': self.id,         # Liên kết dự án với Hợp đồng này
            'sale_order_id': self.sale_order_id.id,
        })

        # 3. Cập nhật Hợp đồng:
        # - Gán 'project_id' trỏ đến dự án vừa tạo
        # - Chuyển trạng thái
        self.write({
            'state': 'active',
            'project_id': new_project.id
        })
        if self.sale_order_id:
            self.sale_order_id.with_context(sgc_skip_sales_permission=True).write({'sgc_project_id': new_project.id})
            self.sale_order_id._update_prj_flow_state('b2c_project')
            self.sale_order_id._update_prj_flow_state('b4_execute')
            self.sale_order_id._update_prj_flow_state('b5_tracking')
        
        # 4. Trả về hành động để mở Dự án vừa tạo
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'res_id': new_project.id,
            'view_mode': 'form',
            'target': 'current',
            'name': _('Dự án vừa tạo'),
        }

    def action_mark_as_done(self):
        # (Chưa làm gì vội)
        self.state = 'done'
        template = self.env.ref('sgc_management_core.customer_care_template_default', raise_if_not_found=False)
        if template:
            for contract in self:
                template._schedule_customer_care(
                    partner=contract.partner_id,
                    care_type='completed',
                    contract=contract,
                    reference_date=contract.end_date or fields.Date.context_today(contract)
                )
                if contract.sale_order_id:
                    contract.sale_order_id._update_prj_flow_state('b7_contract_done')
    
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
                raise models.UserError(_(
                    'Không thể xóa Hợp đồng "%s" vì Dự án "%s" đang hoạt động.\n'
                    'Vui lòng lưu trữ (archive) dự án trước khi xóa hợp đồng.'
                ) % (contract.name, contract.project_id.name))
        return super(SignedContract, self).unlink()