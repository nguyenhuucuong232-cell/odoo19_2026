from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError
from odoo.tools import format_amount

PRJ_FLOW_SEQUENCE = {
    'b1_create': 10,
    'b2_review': 20,
    'b2a_cancel': 25,
    'b2b_contract': 30,
    'b3_sign': 35,
    'b2c_project': 40,
    'b4_execute': 50,
    'b5_tracking': 60,
    'b6_complete': 70,
    'b7_contract_done': 80,
    'b8_payment': 90,
}

PRJ_FLOW_META = {
    'b1_create': {
        'title': 'Bước 1: Tạo đơn bán hàng',
        'description': 'Bộ phận kinh doanh tạo Đơn bán hàng, ghi nhận đầy đủ nhu cầu và tài liệu khách hàng.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Nhập thông tin khách hàng, sản phẩm, lịch trình dự kiến.\n- Đính kèm tài liệu yêu cầu.',
    },
    'b2_review': {
        'title': 'Bước 2: Kiểm tra & gửi phê duyệt',
        'description': 'NVKD gửi yêu cầu phê duyệt hợp đồng tới trưởng phòng và Ban lãnh đạo.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Kiểm tra nội dung báo giá.\n- Gửi yêu cầu duyệt tới Trưởng phòng/Giám đốc.\n- Theo dõi kết quả duyệt.',
    },
    'b2a_cancel': {
        'title': 'Bước 2a: Hủy đơn hàng',
        'description': 'Đơn bán hàng không được phê duyệt và bị hủy.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Ghi lý do hủy.\n- Thông báo cho các bên liên quan.\n- Lưu lịch sử để chăm sóc lại nếu cần.',
    },
    'b2b_contract': {
        'title': 'Bước 2b: Tạo hợp đồng mới',
        'description': 'Sau khi đơn được duyệt, tạo bản ghi Hợp đồng để trình ký.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Sinh hợp đồng từ đơn bán hàng.\n- Chuẩn bị hồ sơ trình ký.',
    },
    'b3_sign': {
        'title': 'Bước 3: Trình ký & cập nhật tài liệu',
        'description': 'In ấn, trình ký hợp đồng và lưu trữ tài liệu chính thức.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Trình ký hợp đồng.\n- Cập nhật bản scan/tài liệu lên hệ thống.',
    },
    'b2c_project': {
        'title': 'Bước 2c: Tạo dự án & nhiệm vụ',
        'description': 'Sinh dự án mới dựa trên mẫu dịch vụ tương ứng.',
        'department': 'Quản lý dự án',
        'tasks': '- Tạo dự án, cấu trúc nhiệm vụ theo template.\n- Phân công nhân sự liên quan.',
    },
    'b4_execute': {
        'title': 'Bước 4: Triển khai dự án',
        'description': 'Các bộ phận triển khai dự án theo kế hoạch.',
        'department': 'Các bộ phận dự án',
        'tasks': '- Thực hiện các nhiệm vụ triển khai.\n- Cập nhật tiến độ, phát sinh trong dự án.',
    },
    'b5_tracking': {
        'title': 'Bước 5-6-7: Cập nhật trạng thái hợp đồng & dự án',
        'description': 'Theo dõi trạng thái dự án, nghiệm thu từng giai đoạn và thông báo về phòng kinh doanh.',
        'department': 'Quản lý dự án / Phòng kinh doanh',
        'tasks': '- Update trạng thái dự án trong Odoo.\n- Nghiệm thu từng phần, ghi chú vấn đề.\n- Gửi báo cáo cho kinh doanh/ban lãnh đạo.',
    },
    'b6_complete': {
        'title': 'Bước 6: Hoàn thành dự án',
        'description': 'Dự án đã nghiệm thu, chuyển sang giai đoạn kết thúc.',
        'department': 'Quản lý dự án',
        'tasks': '- Hoàn tất biên bản nghiệm thu.\n- Đóng dự án và bàn giao hồ sơ.',
    },
    'b7_contract_done': {
        'title': 'Bước 7: Cập nhật trạng thái hợp đồng',
        'description': 'Cập nhật hợp đồng sang trạng thái hoàn thành/đóng, chuẩn bị công tác thanh toán.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Cập nhật trạng thái hợp đồng.\n- Chuẩn bị hồ sơ thanh lý.',
    },
    'b8_payment': {
        'title': 'Bước 8: Thanh toán & thu hồi công nợ',
        'description': 'Bộ phận kế toán xuất hóa đơn, thu hồi công nợ, kết thúc quy trình.',
        'department': 'Bộ phận kế toán & kinh doanh',
        'tasks': '- Xuất hóa đơn, theo dõi thanh toán.\n- Đối soát công nợ và cập nhật kết quả.',
    },
}

SALE_FLOW_SEQUENCE = {
    'sale_b1_quote': 10,
    'sale_b2_plan': 20,
    'sale_b3_approval': 30,
    'sale_b4_send': 40,
    'sale_b5_confirm': 50,
    'sale_b6_contract': 60,
    'sale_b7_fail': 70,
}

SALE_FLOW_META = {
    'sale_b1_quote': {
        'title': 'Bước 1: Tạo báo giá',
        'description': 'Từ CRM, NVKD tạo báo giá mới trên hệ thống.',
        'department': 'NVKD',
        'tasks': '- Lấy dữ liệu khách hàng từ CRM.\n- Lên danh sách dịch vụ, số lượng, giá.',
    },
    'sale_b2_plan': {
        'title': 'Bước 2: Xây dựng phương án kinh doanh',
        'description': 'NVKD trao đổi với khách về chi phí triển khai, tỷ lệ lợi nhuận, kế hoạch nhân sự.',
        'department': 'NVKD / Khách hàng',
        'tasks': '- Thỏa thuận chi phí, nguồn lực.\n- Chuẩn bị tài liệu PAKD (phương án kinh doanh).',
    },
    'sale_b3_approval': {
        'title': 'Bước 3: Gửi yêu cầu phê duyệt',
        'description': 'PAKD được gửi đến Ban quản lý phê duyệt (1 hoặc 2 cấp tùy giá trị).',
        'department': 'NVKD / Người duyệt',
        'tasks': '- Gửi yêu cầu duyệt.\n- Theo dõi kết quả, chỉnh sửa phương án nếu bị trả lại.',
    },
    'sale_b4_send': {
        'title': 'Bước 4: Gửi báo giá cho khách',
        'description': 'Báo giá đã duyệt được gửi cho khách hàng.',
        'department': 'NVKD',
        'tasks': '- Gửi báo giá và lưu lịch sử gửi.\n- Hẹn thời gian phản hồi.',
    },
    'sale_b5_confirm': {
        'title': 'Bước 5: Khách xác nhận đơn hàng',
        'description': 'Khách đồng ý báo giá, NVKD xác nhận đơn hàng trên hệ thống.',
        'department': 'NVKD / Khách hàng',
        'tasks': '- Cập nhật kết quả đàm phán.\n- Chuẩn bị hồ sơ để lập hợp đồng.',
    },
    'sale_b6_contract': {
        'title': 'Bước 6: Lên hợp đồng & dự án',
        'description': 'Tạo hợp đồng và triển khai theo PRJ.01.',
        'department': 'NVKD / Quản lý dự án',
        'tasks': '- Sinh hợp đồng, trình ký.\n- Bàn giao sang quy trình dự án.',
    },
    'sale_b7_fail': {
        'title': 'Bước 7: Cập nhật trạng thái thất bại',
        'description': 'Báo giá không được duyệt hoặc khách không đồng ý.',
        'department': 'NVKD',
        'tasks': '- Ghi nhận lý do thất bại.\n- Lên kế hoạch chăm sóc lại nếu cần.',
    },
}

SALE_APPROVAL_STATE = [
    ('none', 'Không yêu cầu'),
    ('waiting', 'Đang chờ'),
    ('approved', 'Đã duyệt'),
    ('rejected', 'Từ chối'),
]

SALE_CUSTOMER_RESPONSE = [
    ('pending', 'Chưa phản hồi'),
    ('accepted', 'Khách đồng ý'),
    ('rejected', 'Khách từ chối'),
]

PRJ_FLOW_SEQUENCE = {
    'b1_create': 10,
    'b2_review': 20,
    'b2a_cancel': 25,
    'b2b_contract': 30,
    'b3_sign': 35,
    'b2c_project': 40,
    'b4_execute': 50,
    'b5_tracking': 60,
    'b6_complete': 70,
    'b7_contract_done': 80,
    'b8_payment': 90,
}

PRJ_FLOW_META = {
    'b1_create': {
        'title': 'Bước 1: Tạo đơn bán hàng',
        'description': 'Bộ phận kinh doanh tạo Đơn bán hàng, ghi nhận đầy đủ nhu cầu và tài liệu khách hàng.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Nhập thông tin khách hàng, sản phẩm, lịch trình dự kiến.\n- Đính kèm tài liệu yêu cầu.',
    },
    'b2_review': {
        'title': 'Bước 2: Kiểm tra & gửi phê duyệt',
        'description': 'NVKD gửi yêu cầu phê duyệt hợp đồng tới trưởng phòng và Ban lãnh đạo.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Kiểm tra nội dung báo giá.\n- Gửi yêu cầu duyệt tới Trưởng phòng/ Giám đốc.\n- Theo dõi kết quả duyệt.',
    },
    'b2a_cancel': {
        'title': 'Bước 2a: Hủy đơn hàng',
        'description': 'Đơn bán hàng không được phê duyệt và bị hủy.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Ghi lý do hủy.\n- Thông báo cho các bên liên quan.\n- Lưu lịch sử để chăm sóc lại nếu cần.',
    },
    'b2b_contract': {
        'title': 'Bước 2b: Tạo hợp đồng mới',
        'description': 'Sau khi đơn được duyệt, tạo bản ghi Hợp đồng để trình ký.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Sinh hợp đồng từ đơn bán hàng.\n- Chuẩn bị hồ sơ trình ký.',
    },
    'b3_sign': {
        'title': 'Bước 3: Trình ký & cập nhật tài liệu',
        'description': 'In ấn, trình ký hợp đồng và lưu trữ tài liệu chính thức.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Trình ký hợp đồng.\n- Cập nhật bản scan/tài liệu lên hệ thống.',
    },
    'b2c_project': {
        'title': 'Bước 2c: Tạo dự án & nhiệm vụ',
        'description': 'Sinh dự án mới dựa trên mẫu dịch vụ tương ứng.',
        'department': 'Quản lý dự án',
        'tasks': '- Tạo dự án, cấu trúc nhiệm vụ theo template.\n- Phân công nhân sự liên quan.',
    },
    'b4_execute': {
        'title': 'Bước 4: Triển khai dự án',
        'description': 'Các bộ phận triển khai dự án theo kế hoạch.',
        'department': 'Các bộ phận dự án',
        'tasks': '- Thực hiện các nhiệm vụ triển khai.\n- Cập nhật tiến độ, phát sinh trong dự án.',
    },
    'b5_tracking': {
        'title': 'Bước 5-6-7: Cập nhật trạng thái hợp đồng & dự án',
        'description': 'Theo dõi trạng thái dự án, nghiệm thu từng giai đoạn và thông báo về phòng kinh doanh.',
        'department': 'Quản lý dự án / Phòng kinh doanh',
        'tasks': '- Update trạng thái dự án trong Odoo.\n- Nghiệm thu từng phần, ghi chú vấn đề.\n- Gửi báo cáo cho kinh doanh/ban lãnh đạo.',
    },
    'b6_complete': {
        'title': 'Bước 6: Hoàn thành dự án',
        'description': 'Dự án đã nghiệm thu, chuyển sang giai đoạn kết thúc.',
        'department': 'Quản lý dự án',
        'tasks': '- Hoàn tất biên bản nghiệm thu.\n- Đóng dự án và bàn giao hồ sơ.',
    },
    'b7_contract_done': {
        'title': 'Bước 7: Cập nhật trạng thái hợp đồng',
        'description': 'Cập nhật hợp đồng sang trạng thái hoàn thành/đóng, chuẩn bị công tác thanh toán.',
        'department': 'Bộ phận kinh doanh',
        'tasks': '- Cập nhật trạng thái hợp đồng.\n- Chuẩn bị hồ sơ thanh lý.',
    },
    'b8_payment': {
        'title': 'Bước 8: Thanh toán & thu hồi công nợ',
        'description': 'Bộ phận kế toán xuất hóa đơn, thu hồi công nợ, kết thúc quy trình.',
        'department': 'Bộ phận kế toán & kinh doanh',
        'tasks': '- Xuất hóa đơn, theo dõi thanh toán.\n- Đối soát công nợ và cập nhật kết quả.',
    },
}

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ==========================================
    # THÔNG TIN BÁO GIÁ (Giống hình mẫu gốc)
    # ==========================================
    
    # -- Người liên hệ --
    contact_id = fields.Many2one(
        'res.partner', 
        string="Người liên hệ",
        domain="[('parent_id', '=', partner_id)]"
    )
    
    # -- Mẫu báo giá --
    quote_template_id = fields.Many2one(
        'sale.order.template',
        string="Mẫu báo giá"
    )
    
    # -- Nội dung báo giá --
    quote_content = fields.Text(
        string="Nội dung báo giá", 
        default="Kính gửi Quý Khách hàng bảng báo giá dịch vụ..."
    )
    
    # -- Tần suất --
    have_frequency = fields.Boolean(
        string="Tần suất?", 
        default=False,
        help="Có hiển thị cột Tần suất trong báo giá không?"
    )
    
    # -- Độ ưu tiên --
    priority = fields.Selection([
        ('0', 'Thấp'),
        ('1', 'Trung bình'),
        ('2', 'Cao'),
        ('3', 'Rất cao'),
    ], string="Độ ưu tiên", default='1')
    
    # -- Loại nhiệm vụ --
    task_type = fields.Selection([
        ('task', 'Task'),
        ('project', 'Project'),
        ('service', 'Service'),
    ], string="Loại nhiệm vụ", default='task')
    
    # -- Tiến triển --
    progress = fields.Integer(string="Tiến triển", default=0)
    
    # -- Màu sắc --
    color = fields.Integer(string="Màu", default=0)
    
    # -- Kết quả đạt được --
    result_achieved = fields.Text(string="Kết quả đạt được")
    
    # -- State Old Order (Trạng thái cũ) --
    state_old_order = fields.Char(string="State Old Order", readonly=True)
    
    # -- Loại đơn hàng --
    order_type = fields.Selection([
        ('normal', 'Bình thường'),
        ('urgent', 'Khẩn cấp'),
        ('vip', 'VIP'),
    ], string="Loại đơn hàng", default='normal')
    
    # -- Hoa hồng dự chi --
    commission_budget = fields.Monetary(
        string="Hoa hồng dự chi", 
        currency_field='currency_id',
        default=0
    )
    
    # -- Đã thêm vị --
    is_added_position = fields.Boolean(string="Đã Thêm Vị", default=False)
    
    # -- CTV (Cộng tác viên) --
    ctv_id = fields.Many2one('res.partner', string="CTV")
    
    # -- Người được giới thiệu --
    referred_by_id = fields.Many2one('res.partner', string="Người được giới thiệu")
    
    # -- Services (Dịch vụ) --
    service_ids = fields.Many2many(
        'product.product',
        'sale_order_service_rel',
        'order_id',
        'product_id',
        string="Services",
        domain="[('type', '=', 'service')]"
    )
    
    # -- Nhà cung cấp --
    supplier_id = fields.Many2one('res.partner', string="Nhà cung cấp")
    
    # -- Đơn mua hàng liên kết --
    purchase_order_id = fields.Many2one('purchase.order', string="Đơn mua hàng")

    # -- Discount Logic --
    customer_discount = fields.Monetary(
        string="Chiết khấu khách hàng", 
        currency_field='currency_id'
    )
    price_after_discount = fields.Monetary(
        string="Sau chiết khấu", 
        compute='_compute_price_after_discount'
    )

    # -- QR Code --
    order_qr_code = fields.Binary(string="QR Code Đơn hàng")
    # SALE flow tracking
    sale_flow_state = fields.Selection(
        [(key, meta['title']) for key, meta in SALE_FLOW_META.items()],
        string='Trạng thái SALE.01',
        default='sale_b1_quote',
        tracking=True,
        copy=False,
    )
    sale_flow_title = fields.Char(string='Bước SALE hiện tại', copy=False)
    sale_flow_description = fields.Text(string='Diễn giải SALE', copy=False)
    sale_flow_department = fields.Char(string='Bộ phận thực hiện (SALE)', copy=False)
    sale_flow_tasks = fields.Text(string='Công việc SALE', copy=False)
    sale_flow_need_second_level = fields.Boolean(string='Cần duyệt cấp 2', copy=False)
    sale_flow_lvl1_state = fields.Selection(
        SALE_APPROVAL_STATE, default='none', copy=False, string='Trạng thái duyệt cấp 1'
    )
    sale_flow_lvl2_state = fields.Selection(
        SALE_APPROVAL_STATE, default='none', copy=False, string='Trạng thái duyệt cấp 2'
    )
    sale_flow_lvl1_user_id = fields.Many2one('res.users', string='Người duyệt cấp 1', copy=False, readonly=True)
    sale_flow_lvl2_user_id = fields.Many2one('res.users', string='Người duyệt cấp 2', copy=False, readonly=True)
    sale_flow_customer_response = fields.Selection(
        SALE_CUSTOMER_RESPONSE, default='pending', copy=False, string='Phản hồi khách hàng'
    )
    prj_flow_state = fields.Selection(
        [(key, meta['title']) for key, meta in PRJ_FLOW_META.items()],
        string='Trạng thái PRJ.01',
        default='b1_create',
        tracking=True,
        copy=False,
    )
    prj_flow_title = fields.Char(string="Bước hiện tại", copy=False)
    prj_flow_description = fields.Text(string="Diễn giải bước", copy=False)
    prj_flow_department = fields.Char(string="Bộ phận thực hiện", copy=False)
    prj_flow_tasks = fields.Text(string="Công việc cần làm", copy=False)
    sgc_contract_id = fields.Many2one('sgc.signed.contract', string='Hợp đồng SGC', copy=False, tracking=True)
    sgc_project_id = fields.Many2one('project.project', string='Dự án SGC', copy=False, tracking=True)

    @api.depends('amount_untaxed', 'customer_discount')
    def _compute_price_after_discount(self):
        for order in self:
            order.price_after_discount = order.amount_untaxed - order.customer_discount

    # -- Helper Methods for Report --
    def intToRoman(self, num):
        # Simple converter for report numbering
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        roman_num = ''
        i = 0
        while  num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i]
                num -= val[i]
            i += 1
        return roman_num

    def format_float_number(self, value):
        return "{:,.0f}".format(value).replace(",", ".")

    def get_lines(self, doc):
        # Group lines logic simulation (Needs real implementation based on sections)
        # Returns a dictionary grouping lines by Section
        res = {}
        current_section = '/'
        res[current_section] = {'lines': [], 'total': 0}
        
        for line in doc.order_line:
            if line.display_type == 'line_section':
                current_section = line.name
                res[current_section] = {'lines': [], 'total': 0}
            else:
                res[current_section]['lines'].append(line)
                res[current_section]['total'] += line.price_subtotal
        return res

    def get_line_tax(self, doc):
        # Group taxes
        tax_groups = {}
        for line in doc.order_line:
            for tax in line.tax_id:
                if tax.id not in tax_groups:
                    tax_groups[tax.id] = {'tax_group_name': tax.name, 'tax_group_amount': 0}
                tax_groups[tax.id]['tax_group_amount'] += (line.price_subtotal * tax.amount / 100)
        return tax_groups.values()

    def get_total(self, doc):
        return doc.amount_total

    def amount_to_text(self, amount):
        # Simple placeholder, better use library or Odoo's built-in if available for VN
        return doc.currency_id.amount_to_text(amount)

    # -------------------------------------------------------------------------
    # Permission helpers
    # -------------------------------------------------------------------------
    def _user_is_sales_director(self):
        return self.env.user.has_group('sgc_management_core.group_sgc_sales_director') or \
            self.env.user.has_group('sgc_management_core.group_sgc_sales_manager')

    def _user_is_sales_lead(self):
        return self.env.user.has_group('sgc_management_core.group_sgc_sales_lead')

    def _user_is_sales_staff(self):
        return self.env.user.has_group('sgc_management_core.group_sgc_sales_staff')

    def _check_sales_permissions(self):
        """Ensure non-manager users only edit their allowed quotations."""
        if not (self._user_is_sales_staff() or self._user_is_sales_lead() or self._user_is_sales_director()):
            return

        allowed_states = ('draft', 'sent')
        user = self.env.user
        for order in self:
            if order.state not in allowed_states and not self._user_is_sales_director():
                raise UserError(_("Bạn chỉ có thể chỉnh sửa hoặc xóa báo giá ở trạng thái Nháp hoặc Đã gửi."))

            if self._user_is_sales_director():
                continue

            if self._user_is_sales_lead():
                if order.user_id == user:
                    continue
                team = order.team_id
                if not team:
                    continue
                if team.user_id == user:
                    continue
                if user in team.member_ids:
                    continue
                raise AccessError(_("Bạn chỉ có thể thao tác trên báo giá của đội bạn quản lý."))

            elif self._user_is_sales_staff():
                if order.user_id != user:
                    raise AccessError(_("Bạn chỉ có thể thao tác trên báo giá của chính mình."))

    def action_confirm(self):
        for order in self:
            if order.prj_flow_state == 'b1_create':
                order._update_prj_flow_state('b2_review')
        res = super().action_confirm()
        for order in self:
            order._update_prj_flow_state('b2b_contract')
            contract = order._ensure_sgc_contract()
            if contract:
                order._update_prj_flow_state('b3_sign')
                order._update_sale_flow_state('sale_b6_contract', allow_backward=True)
            elif order.sale_flow_state not in ('sale_b6_contract', 'sale_b7_fail'):
                order._update_sale_flow_state('sale_b6_contract', allow_backward=True)
        self._schedule_customer_care_logs('success')
        return res

    def action_cancel(self):
        res = super().action_cancel()
        for order in self:
            order._update_prj_flow_state('b2a_cancel')
            order._update_sale_flow_state('sale_b7_fail', allow_backward=True)
        self._schedule_customer_care_logs('lost')
        return res

    def _schedule_customer_care_logs(self, care_type='success'):
        template = self.env.ref('sgc_management_core.customer_care_template_default', raise_if_not_found=False)
        if not template:
            return
        for order in self:
            template._schedule_customer_care(
                partner=order.partner_id,
                care_type=care_type,
                sale_order=order,
                reference_date=order.date_order.date() if order.date_order else fields.Date.context_today(order)
            )

    # -------------------------------------------------------------------------
    # SALE.01 Flow helpers
    # -------------------------------------------------------------------------
    def action_sale_flow_prepare_plan(self):
        self._update_sale_flow_state('sale_b2_plan', allow_backward=True)

    def action_sale_flow_revise_plan(self):
        self.with_context(sgc_skip_sales_permission=True).write({
            'sale_flow_lvl1_state': 'none',
            'sale_flow_lvl2_state': 'none',
            'sale_flow_lvl1_user_id': False,
            'sale_flow_lvl2_user_id': False,
            'sale_flow_need_second_level': False,
        })
        self._update_sale_flow_state('sale_b2_plan', allow_backward=True)

    def action_sale_flow_request_approval(self):
        today = fields.Date.context_today(self)
        for order in self:
            need_second = order._sale_flow_need_second_level()
            vals = {
                'sale_flow_need_second_level': need_second,
                'sale_flow_lvl1_state': 'waiting',
                'sale_flow_lvl1_user_id': False,
                'sale_flow_lvl2_state': 'waiting' if need_second else 'none',
                'sale_flow_lvl2_user_id': False,
            }
            super(SaleOrder, order.with_context(sgc_skip_sales_permission=True)).write(vals)
        self._update_sale_flow_state('sale_b3_approval')

    def _sale_flow_need_second_level(self):
        self.ensure_one()
        threshold = self.company_id.sale_double_approval_amount or 5000000.0
        company_currency = self.company_id.currency_id
        amount_company = self.currency_id._convert(
            self.amount_total, company_currency, self.company_id, fields.Date.context_today(self)
        )
        return amount_company >= threshold

    def action_sale_flow_approve_level1(self, approve=True):
        self._sale_flow_handle_approval(level=1, approve=approve)

    def action_sale_flow_approve_level2(self, approve=True):
        self._sale_flow_handle_approval(level=2, approve=approve)

    def action_sale_flow_reject_level1(self):
        self._sale_flow_handle_approval(level=1, approve=False)

    def action_sale_flow_reject_level2(self):
        self._sale_flow_handle_approval(level=2, approve=False)

    def _sale_flow_handle_approval(self, level=1, approve=True):
        self.ensure_one()
        if level == 1 and not self.env.user.has_group('sgc_management_core.group_sgc_sales_manager'):
            raise UserError(_('Bạn không có quyền duyệt cấp 1.'))
        if level == 2 and not self.env.user.has_group('sgc_management_core.group_sgc_sales_director'):
            raise UserError(_('Bạn không có quyền duyệt cấp 2.'))
        field_state = f'sale_flow_lvl{level}_state'
        field_user = f'sale_flow_lvl{level}_user_id'
        if getattr(self, field_state) != 'waiting':
            raise UserError(_('Bước duyệt không ở trạng thái chờ.'))
        state_value = 'approved' if approve else 'rejected'
        values = {
            field_state: state_value,
            field_user: self.env.user.id,
        }
        super(SaleOrder, self.with_context(sgc_skip_sales_permission=True)).write(values)
        if not approve:
            self._update_sale_flow_state('sale_b7_fail', allow_backward=True)
            self.action_cancel()
            return
        if level == 1 and self.sale_flow_need_second_level:
            return
        if level == 2 or not self.sale_flow_need_second_level:
            if self.sale_flow_lvl1_state == 'approved' and (not self.sale_flow_need_second_level or self.sale_flow_lvl2_state == 'approved'):
                self._update_sale_flow_state('sale_b4_send')

    def action_sale_flow_send_quote(self):
        for order in self:
            if order.sale_flow_state != 'sale_b3_approval':
                raise UserError(_('Bước hiện tại chưa sẵn sàng gửi báo giá.'))
            if order.sale_flow_lvl1_state != 'approved':
                raise UserError(_('Chưa có duyệt cấp 1.'))
            if order.sale_flow_need_second_level and order.sale_flow_lvl2_state != 'approved':
                raise UserError(_('Chưa có duyệt cấp 2.'))
        self._update_sale_flow_state('sale_b4_send')

    def action_sale_flow_customer_accept(self):
        self.with_context(sgc_skip_sales_permission=True).write({'sale_flow_customer_response': 'accepted'})
        self._update_sale_flow_state('sale_b5_confirm')
        to_confirm = self.filtered(lambda so: so.state in ('draft', 'sent'))
        if to_confirm:
            to_confirm.action_confirm()

    def action_sale_flow_customer_reject(self):
        self.with_context(sgc_skip_sales_permission=True).write({'sale_flow_customer_response': 'rejected'})
        self._update_sale_flow_state('sale_b7_fail', allow_backward=True)
        self.action_cancel()

    def _update_sale_flow_state(self, new_state, allow_backward=False):
        meta = SALE_FLOW_META.get(new_state)
        if not meta:
            return
        for order in self:
            current_seq = SALE_FLOW_SEQUENCE.get(order.sale_flow_state or '', 0)
            if not allow_backward and SALE_FLOW_SEQUENCE.get(new_state, 0) < current_seq:
                continue
            vals = {
                'sale_flow_state': new_state,
                'sale_flow_title': meta['title'],
                'sale_flow_description': meta['description'],
                'sale_flow_department': meta['department'],
                'sale_flow_tasks': meta['tasks'],
            }
            super(SaleOrder, order.with_context(sgc_skip_sales_permission=True)).write(vals)
            body = "<p><b>%s</b></p><p>%s</p><p><b>Bộ phận:</b> %s</p><p><b>Công việc:</b><br/>%s</p>" % (
                meta['title'],
                meta['description'],
                meta['department'],
                meta['tasks'].replace('\n', '<br/>'),
            )
            order.message_post(body=body, subtype_xmlid='mail.mt_note')

    def write(self, vals):
        if not self.env.context.get('sgc_skip_sales_permission'):
            self._check_sales_permissions()
        return super().write(vals)

    def unlink(self):
        if not self.env.context.get('sgc_skip_sales_permission'):
            self._check_sales_permissions()
        return super().unlink()

    def action_request_prj_approval(self):
        self._update_prj_flow_state('b2_review')
        return True

    def _update_prj_flow_state(self, new_state):
        meta = PRJ_FLOW_META.get(new_state)
        if not meta:
            return
        for order in self:
            current_seq = PRJ_FLOW_SEQUENCE.get(order.prj_flow_state or '', 0)
            if order.prj_flow_state == 'b2a_cancel' and PRJ_FLOW_SEQUENCE.get(new_state, 0) <= current_seq:
                continue
            if PRJ_FLOW_SEQUENCE.get(new_state, 0) < current_seq:
                continue
            vals = {
                'prj_flow_state': new_state,
                'prj_flow_title': meta['title'],
                'prj_flow_description': meta['description'],
                'prj_flow_department': meta['department'],
                'prj_flow_tasks': meta['tasks'],
            }
            super(SaleOrder, order.with_context(sgc_skip_sales_permission=True)).write(vals)
            body = "<p><b>%s</b></p><p>%s</p><p><b>Bộ phận:</b> %s</p><p><b>Công việc:</b><br/>%s</p>" % (
                meta['title'],
                meta['description'],
                meta['department'],
                meta['tasks'].replace('\n', '<br/>'),
            )
            order.message_post(body=body, subtype_xmlid='mail.mt_note')

    def _ensure_sgc_contract(self):
        self.ensure_one()
        if self.sgc_contract_id:
            return self.sgc_contract_id
        contract_vals = {
            'partner_id': self.partner_id.id,
            'sale_order_id': self.id,
            'company_id': self.company_id.id,
            'sign_date': fields.Date.context_today(self),
            'start_date': fields.Date.context_today(self),
            'contract_value': self.amount_total,
        }
        contract = self.env['sgc.signed.contract'].create(contract_vals)
        super(SaleOrder, self.with_context(sgc_skip_sales_permission=True)).write({'sgc_contract_id': contract.id})
        self._update_sale_flow_state('sale_b6_contract', allow_backward=True)
        return contract

    def _check_prj_payment_completion(self):
        for order in self:
            if PRJ_FLOW_SEQUENCE.get(order.prj_flow_state or '', 0) >= PRJ_FLOW_SEQUENCE['b8_payment']:
                continue
            invoices = order.invoice_ids.filtered(lambda inv: inv.move_type in ('out_invoice', 'out_refund') and inv.state == 'posted')
            if invoices and all(inv.payment_state == 'paid' for inv in invoices if inv.move_type == 'out_invoice'):
                order._update_prj_flow_state('b8_payment')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    frequency = fields.Integer(string="Tần suất", default=1)
