# -*- coding: utf-8 -*-
from odoo import models, fields, api

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

    @api.onchange('categ_id', 'name')
    def _onchange_auto_assign_project_template(self):
        """Tự động gán project template dựa trên category hoặc tên sản phẩm"""
        if not self.categ_id:
            return

        # Tìm project template phù hợp dựa trên category
        template = self._find_project_template_by_category(self.categ_id)
        if template:
            self.project_template_id = template.id
        else:
            # Nếu không tìm thấy theo category, thử tìm theo tên
            template = self._find_project_template_by_name(self.name)
            if template:
                self.project_template_id = template.id

    def _find_project_template_by_category(self, category):
        """Tìm project template dựa trên product category"""
        self.ensure_one()

        # Mapping category name với template (có thể mở rộng)
        category_mappings = {
            'quan trắc': 'sgc_management_core.sgc_project_template',
            'môi trường': 'sgc_management_core.sgc_project_template',
            'sức khỏe': 'sgc_management_core.sgc_project_template',
        }

        category_name = category.name.lower() if category.name else ''
        for key, template_xml_id in category_mappings.items():
            if key in category_name:
                template = self.env.ref(template_xml_id, raise_if_not_found=False)
                if template:
                    return template

        return False

    def _find_project_template_by_name(self, product_name):
        """Tìm project template dựa trên tên sản phẩm"""
        self.ensure_one()
        if not product_name:
            return False

        product_name_lower = product_name.lower()

        # Mapping tên sản phẩm với template
        name_mappings = {
            'quan trắc': 'sgc_management_core.sgc_project_template',
            'môi trường': 'sgc_management_core.sgc_project_template',
            'sức khỏe': 'sgc_management_core.sgc_project_template',
            'nước': 'sgc_management_core.sgc_project_template',
            'không khí': 'sgc_management_core.sgc_project_template',
            'tiếng ồn': 'sgc_management_core.sgc_project_template',
        }

        for key, template_xml_id in name_mappings.items():
            if key in product_name_lower:
                template = self.env.ref(template_xml_id, raise_if_not_found=False)
                if template:
                    return template

        return False

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Thêm trường liên kết với Project Template
    project_template_id = fields.Many2one(
        'project.project',
        string='Mẫu dự án',
        domain="[('is_template', '=', True)]",
        help='Mẫu dự án sử dụng khi bán sản phẩm này',
        related='product_tmpl_id.project_template_id',
        readonly=False
    )