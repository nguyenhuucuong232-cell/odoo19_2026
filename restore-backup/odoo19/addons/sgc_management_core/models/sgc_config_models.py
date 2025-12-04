# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


# ============================================
# CẤU HÌNH - HÌNH THỨC BÀN GIAO
# ============================================
class SgcHandoverForm(models.Model):
    _name = 'sgc.handover.form'
    _description = 'Hình thức bàn giao'
    _order = 'sequence, name'
    
    name = fields.Char(
        string='Hình thức bàn giao',
        required=True
    )
    
    code = fields.Char(
        string='Mã'
    )
    
    sequence = fields.Integer(
        string='Thứ tự',
        default=10
    )
    
    active = fields.Boolean(
        default=True,
        string='Hoạt động'
    )


# ============================================
# CẤU HÌNH - BÀN GIAO TÀI LIỆU
# ============================================
class SgcDocumentHandoverConfig(models.Model):
    _name = 'sgc.document.handover.config'
    _description = 'Bàn giao tài liệu'
    _order = 'sequence, name'
    
    name = fields.Char(
        string='Tên tài liệu',
        required=True
    )
    
    code = fields.Char(
        string='Mã'
    )
    
    sequence = fields.Integer(
        string='Thứ tự',
        default=10
    )
    
    active = fields.Boolean(
        default=True,
        string='Hoạt động'
    )


# ============================================
# CẤU HÌNH - GIẤY ỦY QUYỀN
# ============================================
class SgcPowerOfAttorney(models.Model):
    _name = 'sgc.power.of.attorney'
    _description = 'Giấy ủy quyền'
    _order = 'date desc, name'
    
    name = fields.Char(
        string='Số giấy ủy quyền',
        required=True
    )
    
    date = fields.Date(
        string='Ngày ký'
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Bên ủy quyền'
    )
    
    authorized_person = fields.Char(
        string='Người được ủy quyền'
    )
    
    content = fields.Text(
        string='Nội dung ủy quyền'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='File đính kèm'
    )
    
    active = fields.Boolean(
        default=True,
        string='Hoạt động'
    )


# ============================================
# CẤU HÌNH - PHƯƠNG THỨC THANH TOÁN
# ============================================
class SgcPaymentMethod(models.Model):
    _name = 'sgc.payment.method'
    _description = 'Phương thức thanh toán'
    _order = 'sequence, name'
    
    name = fields.Char(
        string='Phương thức thanh toán',
        required=True
    )
    
    code = fields.Char(
        string='Mã'
    )
    
    description = fields.Text(
        string='Mô tả'
    )
    
    sequence = fields.Integer(
        string='Thứ tự',
        default=10
    )
    
    active = fields.Boolean(
        default=True,
        string='Hoạt động'
    )


# ============================================
# CẤU HÌNH - LÝ DO QUÁ HẠN HĐ
# ============================================
class SgcOverdueReason(models.Model):
    _name = 'sgc.overdue.reason'
    _description = 'Lý do quá hạn HĐ'
    _order = 'sequence, name'
    
    name = fields.Char(
        string='Lý do quá hạn',
        required=True
    )
    
    code = fields.Char(
        string='Mã'
    )
    
    description = fields.Text(
        string='Mô tả chi tiết'
    )
    
    sequence = fields.Integer(
        string='Thứ tự',
        default=10
    )
    
    active = fields.Boolean(
        default=True,
        string='Hoạt động'
    )

