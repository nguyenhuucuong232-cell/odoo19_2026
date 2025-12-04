# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    # Kế thừa model 'sale.order'
    _inherit = 'sale.order'

    def action_confirm(self):
        # Gọi method gốc trước
        result = super(SaleOrder, self).action_confirm()

        # Tự động tạo project từ product template
        for order in self:
            for line in order.order_line:
                if line.product_id.type == 'service' and line.product_id.project_template_id:
                    # Tạo project từ template
                    template = line.product_id.project_template_id

                    # Tạo tên project
                    project_name = f"{order.name} - {line.product_id.name}"

                    # Copy project từ template
                    new_project = template.copy({
                        'name': project_name,
                        'partner_id': order.partner_id.id,
                        'sale_order_id': order.id,
                        'is_template': False,
                    })

                    # Liên kết sale order line với project
                    line.write({'project_id': new_project.id})

                    # Copy tasks từ template
                    for task in template.task_ids:
                        task.copy({
                            'project_id': new_project.id,
                            'sale_order_id': order.id,
                            'partner_id': order.partner_id.id,
                        })

        return result

    # Hàm này sẽ được gọi bằng nút bấm
    def action_create_sgc_contract(self):
        # Đảm bảo chỉ chạy cho 1 đơn hàng mỗi lần
        self.ensure_one()

        # Kiểm tra xem hợp đồng đã được tạo trước đó chưa
        existing_contract = self.env['sgc.signed.contract'].search([
            ('sale_order_id', '=', self.id)
        ], limit=1)

        if existing_contract:
            # Nếu có, báo lỗi cho người dùng
            raise UserError(_("Hợp đồng SGC đã tồn tại cho Đơn hàng này."))

        # Nếu chưa, chuẩn bị dữ liệu để tạo Hợp đồng mới
        contract_vals = {
            'partner_id': self.partner_id.id,
            'sale_order_id': self.id,
            'contract_value': self.amount_total, # Lấy tổng giá trị từ Đơn hàng
            'sign_date': fields.Date.today(),   # Lấy ngày hôm nay
            'name': f"{self.name} - HĐ",        # Tạo Mã HĐ (ví dụ: S00001 - HĐ)
            'state': 'draft',
            # (Bạn có thể thêm các trường khác ở đây)
        }

        # Tạo bản ghi Hợp đồng mới
        new_contract = self.env['sgc.signed.contract'].create(contract_vals)

        # Trả về một hành động để Odoo mở Form view của Hợp đồng vừa tạo
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sgc.signed.contract',
            'res_id': new_contract.id,
            'view_mode': 'form',
            'target': 'current',
            'name': _('Hợp đồng SGC vừa tạo'),
        }