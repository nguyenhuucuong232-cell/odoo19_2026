# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class SGCActivityAlarm(models.Model):
    _name = "sgc.activity.alarm"
    _description = "Activity Alarm Reminder"

    name = fields.Char(string="Tên", compute='_compute_name', store=True)
    type = fields.Selection([
        ('email', 'Email'),
        ('popup', 'Popup')
    ], string="Loại", required=True, default='email')
    remind_before = fields.Integer(string="Nhắc trước")
    reminder_unit = fields.Selection([
        ('hours', 'Giờ'),
        ('minutes', 'Phút'),
        ('seconds', 'Giây')
    ], string="Đơn vị", default='hours', required=True)
    company_id = fields.Many2one(
        'res.company',
        'Công ty',
        default=lambda self: self.env.company
    )

    @api.constrains('remind_before', 'reminder_unit')
    def _check_remind_before(self):
        for alarm in self:
            if alarm.reminder_unit == 'minutes' and alarm.remind_before < 5:
                raise ValidationError(_("Không thể đặt nhắc nhở dưới 5 phút."))
            elif alarm.reminder_unit == 'seconds' and alarm.remind_before < 300:
                raise ValidationError(_("Không thể đặt nhắc nhở dưới 300 giây."))
            elif alarm.reminder_unit == 'hours' and alarm.remind_before < 1:
                raise ValidationError(_("Không thể đặt nhắc nhở dưới 1 giờ."))

    @api.depends('remind_before', 'reminder_unit', 'type')
    def _compute_name(self):
        unit_labels = {
            'hours': 'Giờ',
            'minutes': 'Phút',
            'seconds': 'Giây'
        }
        type_labels = {
            'email': 'Email',
            'popup': 'Popup'
        }
        for alarm in self:
            unit_label = unit_labels.get(alarm.reminder_unit, '')
            type_label = type_labels.get(alarm.type, '')
            alarm.name = f"{alarm.remind_before} {unit_label} [{type_label}]"

    @api.model
    def _run_activity_reminder(self):
        """Scheduled action to send activity reminders"""
        if not self.env.company.sgc_display_activity_reminder:
            return
            
        alarm_ids = self.sudo().search([])
        for alarm in alarm_ids:
            activity_ids = self.env['mail.activity'].sudo().search([
                ('sgc_activity_alarm_ids', 'in', [alarm.id]),
                ('active', '=', True)
            ])
            
            for activity in activity_ids:
                if not activity.sgc_date_deadline:
                    continue
                    
                # Calculate reminder time
                deadline_date = activity.sgc_date_deadline
                if alarm.reminder_unit == 'hours':
                    reminder_time = deadline_date - timedelta(hours=alarm.remind_before)
                elif alarm.reminder_unit == 'minutes':
                    reminder_time = deadline_date - timedelta(minutes=alarm.remind_before)
                else:  # seconds
                    reminder_time = deadline_date - timedelta(seconds=alarm.remind_before)
                
                now = fields.Datetime.now()
                
                # Check if it's time to send reminder (within 1 minute window)
                if abs((reminder_time - now).total_seconds()) <= 60:
                    if alarm.type == 'popup':
                        self._send_popup_reminder(activity)
                    elif alarm.type == 'email':
                        self._send_email_reminder(activity)

    def _send_popup_reminder(self, activity):
        """Send popup notification for activity"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        message = f'{base_url}/web#id={activity.res_id}&model={activity.res_model}'
        
        if activity.user_id:
            self.env['bus.bus']._sendone(
                activity.user_id.partner_id,
                'simple_notification',
                {
                    'title': _("Nhắc nhở hoạt động: %s") % activity.activity_type_id.name,
                    'message': message,
                    'sticky': True,
                }
            )

    def _send_email_reminder(self, activity):
        """Send email reminder for activity"""
        template = self.env.ref(
            'sgc_activity_dashboard.sgc_activity_reminder_mail_template',
            raise_if_not_found=False
        )
        if template and activity.user_id:
            template.sudo().send_mail(
                activity.id,
                force_send=True,
                email_layout_xmlid='mail.mail_notification_light'
            )

