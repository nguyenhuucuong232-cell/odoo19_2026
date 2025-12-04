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

        # 1. Tìm project template phù hợp
        template = self._find_project_template()
        if not template:
            # Nếu không tìm thấy template, báo lỗi
            raise models.UserError('Không tìm thấy "Dự án Mẫu" phù hợp. Vui lòng kiểm tra cấu hình sản phẩm.')

        # 2. Sao chép (copy) template để tạo Dự án mới
        new_project = template.copy({
            'name': f"{self.name} - {self.partner_id.name}", # Tên dự án mới
            'is_template': False,           # Đánh dấu đây là dự án thật
            'partner_id': self.partner_id.id,
            'contract_id': self.id,         # Liên kết dự án với Hợp đồng này
            'sale_order_id': self.sale_order_id.id,
        })

        # 3. Phân công nhân sự cho dự án
        self._assign_project_team(new_project)

        # 4. Cập nhật Hợp đồng:
        # - Gán 'project_id' trỏ đến dự án vừa tạo
        # - Chuyển trạng thái
        self.write({
            'state': 'active',
            'project_id': new_project.id
        })

        # 5. Cập nhật Sale Order
        if self.sale_order_id:
            self.sale_order_id.with_context(sgc_skip_sales_permission=True).write({'sgc_project_id': new_project.id})
            self.sale_order_id._update_prj_flow_state('b2c_project')
            self.sale_order_id._update_prj_flow_state('b4_execute')
            self.sale_order_id._update_prj_flow_state('b5_tracking')

        # 6. Trả về hành động để mở Dự án vừa tạo
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'res_id': new_project.id,
            'view_mode': 'form',
            'target': 'current',
            'name': _('Dự án vừa tạo'),
        }

    def _find_project_template(self):
        """Tìm project template phù hợp dựa trên sản phẩm trong sale order"""
        self.ensure_one()

        # Ưu tiên 1: Tìm theo product template trong sale order lines
        if self.sale_order_id and self.sale_order_id.order_line:
            for line in self.sale_order_id.order_line:
                if line.product_id and line.product_id.project_template_id:
                    return line.product_id.project_template_id
                elif line.product_template_id and line.product_template_id.project_template_id:
                    return line.product_template_id.project_template_id

        # Ưu tiên 2: Tìm theo category của sản phẩm chính
        if self.sale_order_id and self.sale_order_id.order_line:
            main_product = self.sale_order_id.order_line[0].product_id
            if main_product and main_product.categ_id:
                category_name = main_product.categ_id.name.lower()
                if 'quan trắc' in category_name or 'môi trường' in category_name:
                    return self.env.ref('sgc_management_core.sgc_project_template', raise_if_not_found=False)

        # Ưu tiên 3: Dùng template mặc định
        return self.env.ref('sgc_management_core.sgc_project_template', raise_if_not_found=False)

    def _assign_project_team(self, project):
        """Phân công team cho dự án dựa trên sale order"""
        self.ensure_one()

        if not self.sale_order_id:
            return

        # Tìm PM từ user tạo sale order hoặc team leader
        pm_user = self.sale_order_id.user_id
        if self.sale_order_id.team_id and self.sale_order_id.team_id.user_id:
            pm_user = self.sale_order_id.team_id.user_id

        if pm_user:
            # Thêm PM vào project
            project.write({
                'user_id': pm_user.id,  # Project Manager
            })

        # Tìm kỹ thuật viên từ department
        tech_department = self.env['hr.department'].search([
            ('name', 'ilike', 'kỹ thuật'),
            ('name', 'ilike', 'thí nghiệm'),
        ], limit=1)

        if tech_department:
            tech_users = self.env['res.users'].search([
                ('employee_id.department_id', '=', tech_department.id),
                ('employee_id', '!=', False)
            ], limit=3)  # Lấy tối đa 3 kỹ thuật viên

            for tech_user in tech_users:
                # Thêm kỹ thuật viên vào project team (nếu có module project_role)
                pass  # Có thể mở rộng sau

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