# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Thêm các trường cho tab "Nghiệp vụ SGC"
    sgc_customer_type = fields.Selection([
        ('individual', 'Cá nhân'),
        ('company', 'Công ty'),
        ('government', 'Chính phủ'),
        ('other', 'Khác'),
    ], string='Loại khách hàng SGC', default='company')

    sgc_industry = fields.Char(string='Ngành nghề SGC')
    sgc_business_scale = fields.Selection([
        ('small', 'Doanh nghiệp nhỏ'),
        ('medium', 'Doanh nghiệp vừa'),
        ('large', 'Doanh nghiệp lớn'),
        ('enterprise', 'Tập đoàn'),
    ], string='Quy mô SGC')

    # Liên kết với các model SGC
    sgc_contract_ids = fields.One2many(
        'sgc.signed.contract',
        'partner_id',
        string='Hợp đồng SGC'
    )
    sgc_contract_count = fields.Integer(
        compute='_compute_sgc_contract_count',
        string='Số hợp đồng SGC'
    )

    sgc_project_ids = fields.One2many(
        'project.project',
        'partner_id',
        string='Dự án SGC'
    )
    sgc_project_count = fields.Integer(
        compute='_compute_sgc_project_count',
        string='Số dự án SGC'
    )

    sgc_sale_order_ids = fields.One2many(
        'sale.order',
        'partner_id',
        string='Đơn bán hàng SGC'
    )
    sgc_sale_order_count = fields.Integer(
        compute='_compute_sgc_sale_order_count',
        string='Số đơn hàng SGC'
    )

    # Thông tin bổ sung
    sgc_contact_person = fields.Char(string='Người liên hệ SGC')
    sgc_contact_phone = fields.Char(string='SĐT liên hệ SGC')
    sgc_contact_email = fields.Char(string='Email liên hệ SGC')

    sgc_notes = fields.Text(string='Ghi chú SGC')

    def _compute_sgc_contract_count(self):
        for partner in self:
            partner.sgc_contract_count = len(partner.sgc_contract_ids)

    def _compute_sgc_project_count(self):
        for partner in self:
            partner.sgc_project_count = len(partner.sgc_project_ids)

    def _compute_sgc_sale_order_count(self):
        for partner in self:
            partner.sgc_sale_order_count = len(partner.sgc_sale_order_ids)