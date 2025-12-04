# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """
        Ghi đè phương thức xác nhận phiếu nhập kho.
        Mục đích: Chặn việc nhập kho nếu đơn hàng mua tương ứng có yêu cầu tạm ứng
        nhưng khoản tạm ứng đó chưa được thanh toán.

        Quy tắc:
        1. Chỉ áp dụng cho phiếu nhập kho (picking_type_code == 'incoming').
        2. Phiếu phải được tạo từ một đơn mua hàng (purchase_id).
        3. Hệ thống sẽ tìm các hóa đơn nhà cung cấp (vendor bill) liên quan đến đơn mua hàng đó.
        4. Nếu có bất kỳ hóa đơn nào là hóa đơn đặt cọc (down payment),
           hệ thống sẽ kiểm tra trạng thái thanh toán của nó.
        5. Nếu hóa đơn đặt cọc chưa được thanh toán ('paid'), hệ thống sẽ báo lỗi và không cho nhập kho.
        """
        for picking in self:
            # Chỉ kiểm tra cho các phiếu nhập kho từ đơn mua hàng
            if picking.picking_type_code == 'incoming' and picking.purchase_id:
                purchase_order = picking.purchase_id

                # Tìm các hóa đơn đặt cọc liên quan đến đơn hàng
                # Hóa đơn đặt cọc được nhận diện bằng cách các dòng của nó được đánh dấu is_downpayment = True
                down_payment_bills = purchase_order.invoice_ids.filtered(
                    lambda bill: bill.move_type == 'in_invoice' and 
                                 any(line.is_downpayment for line in bill.invoice_line_ids)
                )

                if down_payment_bills:
                    # Nếu có hóa đơn đặt cọc, kiểm tra xem có cái nào chưa được thanh toán không
                    if any(bill.payment_state != 'paid' for bill in down_payment_bills):
                        raise UserError(_(
                            "Không thể nhận hàng cho Đơn hàng %s. "
                            "Hóa đơn đặt cọc liên quan chưa được thanh toán."
                        ) % (purchase_order.name))
                else:
                    # Nếu theo quy định bắt buộc phải có tạm ứng,
                    # mà lại không tìm thấy hóa đơn đặt cọc nào thì cũng chặn lại.
                    # Ghi chú: Logic này giả định mọi đơn hàng đều cần tạm ứng.
                    # Nếu có trường hợp không cần, cần phải có một trường để đánh dấu trên đơn hàng.
                    raise UserError(_(
                        "Không thể nhận hàng cho Đơn hàng %s. "
                        "Chưa có hóa đơn đặt cọc nào được tạo cho đơn hàng này theo quy định."
                    ) % (purchase_order.name))

        # Nếu tất cả kiểm tra đều qua, gọi đến hàm validate gốc.
        return super(StockPicking, self).button_validate()

