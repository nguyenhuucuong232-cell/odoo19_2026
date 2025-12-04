# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SGCKpiCriteria(models.Model):
    _name = 'sgc.kpi.criteria'
    _description = 'Tiêu chí KPI'

    code = fields.Char(string='Mã', required=True)
    name = fields.Char(string='Tên tiêu chí', required=True)
    description = fields.Text(string='Mô tả')
    
    default_target = fields.Float(string='Chỉ tiêu mặc định', required=True)
    unit = fields.Char(string='Đơn vị đo', required=True)
    weight = fields.Float(
        string='Trọng số',
        help="Trọng số của tiêu chí trong tổng KPI (0-1)"
    )
    
    department_id = fields.Many2one(
        'hr.department',
        string='Phòng ban',
        required=True
    )
    
    calculation_method = fields.Selection([
        ('sum', 'Tổng'),
        ('count', 'Đếm'),
        ('average', 'Trung bình')
    ], string='Phương pháp tính', default='sum')
    
    target_type = fields.Selection([
        ('fixed', 'Cố định'),
        ('dynamic', 'Động')
    ], string='Loại chỉ tiêu', default='fixed', required=True)
    
    # Time coefficients for each month
    month_01 = fields.Float(string='Tháng 1', default=1.0)
    month_02 = fields.Float(string='Tháng 2', default=1.0)
    month_03 = fields.Float(string='Tháng 3', default=1.0)
    month_04 = fields.Float(string='Tháng 4', default=1.0)
    month_05 = fields.Float(string='Tháng 5', default=1.0)
    month_06 = fields.Float(string='Tháng 6', default=1.0)
    month_07 = fields.Float(string='Tháng 7', default=1.0)
    month_08 = fields.Float(string='Tháng 8', default=1.0)
    month_09 = fields.Float(string='Tháng 9', default=1.0)
    month_10 = fields.Float(string='Tháng 10', default=1.0)
    month_11 = fields.Float(string='Tháng 11', default=1.0)
    month_12 = fields.Float(string='Tháng 12', default=1.0)
    
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Mã tiêu chí phải là duy nhất!')
    ]

    @api.constrains('weight')
    def _check_weight(self):
        for record in self:
            if record.weight < 0 or record.weight > 1:
                raise ValidationError(_('Trọng số phải từ 0 đến 1'))

    def get_month_coefficient(self, month):
        """Get coefficient for a specific month (1-12)"""
        self.ensure_one()
        field_name = f'month_{str(month).zfill(2)}'
        return getattr(self, field_name, 1.0)

