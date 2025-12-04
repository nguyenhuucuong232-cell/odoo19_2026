# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    sgc_announcement_count = fields.Integer(
        compute='_compute_announcement_count',
        string='Số thông báo'
    )

    def _compute_announcement_count(self):
        """Compute count of announcements for employee"""
        today = fields.Date.today()
        Announcement = self.env['sgc.hr.announcement'].sudo()
        
        for employee in self:
            # General announcements
            general = Announcement.search([
                ('is_general', '=', True),
                ('state', '=', 'approved'),
                ('date_start', '<=', today),
                ('date_end', '>=', today)
            ])
            
            # Announcements for this employee
            by_employee = Announcement.search([
                ('employee_ids', 'in', employee.id),
                ('state', '=', 'approved'),
                ('date_start', '<=', today),
                ('date_end', '>=', today)
            ])
            
            # Announcements for employee's department
            by_department = Announcement.search([
                ('department_ids', 'in', employee.department_id.id),
                ('state', '=', 'approved'),
                ('date_start', '<=', today),
                ('date_end', '>=', today)
            ]) if employee.department_id else Announcement

            # Announcements for employee's job position
            by_job = Announcement.search([
                ('position_ids', 'in', employee.job_id.id),
                ('state', '=', 'approved'),
                ('date_start', '<=', today),
                ('date_end', '>=', today)
            ]) if employee.job_id else Announcement

            # Combine all announcements (unique)
            all_announcements = general | by_employee | by_department | by_job
            employee.sgc_announcement_count = len(all_announcements)

    def action_view_announcements(self):
        """Open announcements for this employee"""
        self.ensure_one()
        today = fields.Date.today()
        Announcement = self.env['sgc.hr.announcement'].sudo()
        
        # Collect all applicable announcements
        general = Announcement.search([
            ('is_general', '=', True),
            ('state', '=', 'approved'),
            ('date_start', '<=', today),
            ('date_end', '>=', today)
        ])
        
        by_employee = Announcement.search([
            ('employee_ids', 'in', self.id),
            ('state', '=', 'approved'),
            ('date_start', '<=', today),
            ('date_end', '>=', today)
        ])
        
        by_department = Announcement.search([
            ('department_ids', 'in', self.department_id.id),
            ('state', '=', 'approved'),
            ('date_start', '<=', today),
            ('date_end', '>=', today)
        ]) if self.department_id else Announcement
        
        by_job = Announcement.search([
            ('position_ids', 'in', self.job_id.id),
            ('state', '=', 'approved'),
            ('date_start', '<=', today),
            ('date_end', '>=', today)
        ]) if self.job_id else Announcement
        
        all_announcements = general | by_employee | by_department | by_job
        
        if len(all_announcements) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Thông báo'),
                'res_model': 'sgc.hr.announcement',
                'view_mode': 'form',
                'res_id': all_announcements.id,
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Thông báo'),
                'res_model': 'sgc.hr.announcement',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', all_announcements.ids)],
            }

