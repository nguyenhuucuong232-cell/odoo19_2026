# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from calendar import monthrange


class SGCKpiReport(models.Model):
    _name = 'sgc.kpi.report'
    _description = 'Báo cáo KPI'
    _order = 'year desc, month desc'

    name = fields.Char(string='Tên báo cáo', compute='_compute_name', store=True)
    criteria_id = fields.Many2one(
        'sgc.kpi.criteria',
        string='Tiêu chí',
        required=True,
        ondelete='cascade'
    )
    
    month = fields.Selection([
        ('01', 'Tháng 1'),
        ('02', 'Tháng 2'),
        ('03', 'Tháng 3'),
        ('04', 'Tháng 4'),
        ('05', 'Tháng 5'),
        ('06', 'Tháng 6'),
        ('07', 'Tháng 7'),
        ('08', 'Tháng 8'),
        ('09', 'Tháng 9'),
        ('10', 'Tháng 10'),
        ('11', 'Tháng 11'),
        ('12', 'Tháng 12')
    ], string='Tháng', required=True)
    
    year = fields.Char(string='Năm', required=True, default=lambda self: str(datetime.now().year))
    department_id = fields.Many2one(
        'hr.department',
        string='Phòng ban',
        required=True
    )
    
    from_date = fields.Date(string='Từ ngày', compute='_compute_date_range', store=True)
    to_date = fields.Date(string='Đến ngày', compute='_compute_date_range', store=True)
    
    line_ids = fields.One2many(
        'sgc.kpi.report.line',
        'report_id',
        string='Chi tiết'
    )
    note = fields.Text(string='Ghi chú')
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('approved', 'Đã duyệt')
    ], string='Trạng thái', default='draft')
    
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )

    @api.depends('criteria_id', 'month', 'year')
    def _compute_name(self):
        for rec in self:
            if rec.criteria_id and rec.month and rec.year:
                rec.name = f"{rec.criteria_id.name} - Tháng {rec.month}/{rec.year}"
            else:
                rec.name = _('Báo cáo KPI mới')

    @api.depends('month', 'year')
    def _compute_date_range(self):
        for rec in self:
            if rec.month and rec.year:
                try:
                    month_num = int(rec.month)
                    year_int = int(rec.year)
                    rec.from_date = datetime(year_int, month_num, 1).date()
                    rec.to_date = datetime(
                        year_int, month_num,
                        monthrange(year_int, month_num)[1]
                    ).date()
                except Exception:
                    rec.from_date = False
                    rec.to_date = False
            else:
                rec.from_date = False
                rec.to_date = False

    def action_generate_lines(self):
        """Generate report lines for employees in department"""
        self.ensure_one()
        
        if not self.criteria_id or not self.department_id:
            raise UserError(_('Vui lòng chọn tiêu chí và phòng ban.'))
        
        # Get all employees in department and child departments
        all_dept_ids = self.env['hr.department'].search([
            ('id', 'child_of', self.department_id.id)
        ]).ids
        
        employees = self.env['hr.employee'].search([
            ('department_id', 'in', all_dept_ids),
            ('active', '=', True)
        ])
        
        # Clear existing lines
        self.line_ids.unlink()
        
        # Get month coefficient
        month_coef = self.criteria_id.get_month_coefficient(int(self.month))
        
        for emp in employees:
            position_coef = emp.sgc_position_coefficient or 1.0
            target = self.criteria_id.default_target * position_coef * month_coef
            
            self.env['sgc.kpi.report.line'].create({
                'report_id': self.id,
                'employee_id': emp.id,
                'department_id': emp.department_id.id,
                'target': target,
                'actual': 0,
            })

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_draft(self):
        self.write({'state': 'draft'})


class SGCKpiReportLine(models.Model):
    _name = 'sgc.kpi.report.line'
    _description = 'Chi tiết báo cáo KPI'

    report_id = fields.Many2one(
        'sgc.kpi.report',
        string='Báo cáo',
        required=True,
        ondelete='cascade'
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Nhân viên',
        required=True
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Phòng ban'
    )
    
    target = fields.Float(string='Chỉ tiêu')
    actual = fields.Float(string='Thực tế')
    ratio = fields.Float(
        string='Tỷ lệ (%)',
        compute='_compute_ratio',
        store=True
    )
    note = fields.Text(string='Ghi chú')

    @api.depends('target', 'actual')
    def _compute_ratio(self):
        for line in self:
            if line.target:
                line.ratio = round((line.actual / line.target) * 100, 2)
            else:
                line.ratio = 0

