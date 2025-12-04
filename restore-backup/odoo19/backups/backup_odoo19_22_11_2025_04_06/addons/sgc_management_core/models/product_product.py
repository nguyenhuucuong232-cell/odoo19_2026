# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Thêm trường liên kết với Project Template
    project_template_id = fields.Many2one(
        'project.project',
        string='Mẫu dự án',
        domain="[('is_template', '=', True)]",
        help='Mẫu dự án sử dụng khi bán sản phẩm này'
    )
    
    # Thêm trường Thẻ mẫu sản phẩm
    product_tag_ids = fields.Many2many(
        'product.tag',
        string='Thẻ mẫu sản phẩm',
        help='Các thẻ phân loại sản phẩm'
    )
    
    # Thêm trường Công ty
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Thêm trường liên kết với Project Template
    project_template_id = fields.Many2one(
        'project.project',
        string='Mẫu dự án',
        domain="[('is_template', '=', True)]",
        help='Mẫu dự án sử dụng khi bán sản phẩm này'
    )