# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import api, fields, models


class MailActivity(models.Model):
    """Inherited mail.activity model mostly to add dashboard functionalities"""
    _inherit = "mail.activity"

    activity_tag_ids = fields.Many2many(
        'sgc.activity.tag',
        string='Activity Tags',
        help='Select activity tags.'
    )
    # Reminder fields (merged from sgc_activity_reminder)
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company
    )
    sgc_activity_alarm_ids = fields.Many2many(
        'sgc.activity.alarm',
        string='Nhắc nhở'
    )
    sgc_date_deadline = fields.Datetime(
        'Thời hạn nhắc nhở',
        default=lambda self: fields.Datetime.now()
    )
    state = fields.Selection([
        ('planned', 'Planned'),
        ('today', 'Today'),
        ('done', 'Done'),
        ('overdue', 'Overdue')
    ], string='State', help='State of the activity',
        compute='_compute_state', store=True)

    @api.onchange('date_deadline')
    def _onchange_sgc_date_deadline(self):
        for rec in self:
            if rec.date_deadline:
                # Set deadline datetime to end of day
                rec.sgc_date_deadline = fields.Datetime.to_datetime(rec.date_deadline)

    @api.depends('date_deadline', 'active')
    def _compute_state(self):
        """Compute the state based on date_deadline"""
        today = fields.Date.context_today(self)
        for activity in self:
            if not activity.active:
                activity.state = 'done'
            elif not activity.date_deadline:
                activity.state = 'planned'
            elif activity.date_deadline < today:
                activity.state = 'overdue'
            elif activity.date_deadline == today:
                activity.state = 'today'
            else:
                activity.state = 'planned'

    def _action_done(self, feedback=False, attachment_ids=None):
        """Override _action_done to mark as done instead of delete"""
        messages = self.env['mail.message']
        next_activities_values = []
        
        # Search for all attachments linked to the activities
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])
        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])
            
        for model, activity_data in self._classify_by_model().items():
            records = self.env[model].browse(activity_data['record_ids'])
            for record, activity in zip(records, activity_data['activities']):
                # extract value to generate next activities
                if activity.chaining_type == 'trigger':
                    vals = activity.with_context(
                        activity_previous_deadline=activity.date_deadline
                    )._prepare_next_activity_values()
                    next_activities_values.append(vals)
                    
                # post message on activity
                activity_message = record.message_post_with_source(
                    'mail.message_activity_done',
                    attachment_ids=attachment_ids,
                    render_values={
                        'activity': activity,
                        'feedback': feedback,
                        'display_assignee': activity.user_id != self.env.user
                    },
                    mail_activity_type_id=activity.activity_type_id.id,
                    subtype_xmlid='mail.mt_activities',
                )
                
                if activity.activity_type_id.keep_done:
                    attachment_ids_to_link = (attachment_ids or []) + activity_attachments.get(activity.id, [])
                    if attachment_ids_to_link:
                        activity.attachment_ids = attachment_ids_to_link
                        
                # Moving the attachments in the message
                if activity_attachments[activity.id]:
                    message_attachments = self.env['ir.attachment'].browse(
                        activity_attachments[activity.id]
                    )
                    if message_attachments:
                        message_attachments.write({
                            'res_id': activity_message.id,
                            'res_model': activity_message._name,
                        })
                        activity_message.attachment_ids = message_attachments
                messages += activity_message
                
        next_activities = self.env['mail.activity']
        if next_activities_values:
            next_activities = self.env['mail.activity'].create(next_activities_values)
            
        # Mark as done instead of deleting
        for rec in self:
            if rec.state != 'done':
                rec.state = 'done'
                rec.active = False
                
        return messages, next_activities

    def get_activity(self, activity_id):
        """Method for returning model and id of activity"""
        activity = self.browse(activity_id)
        if not activity.exists():
            return {'model': False, 'res_id': False}
        return {
            'model': activity.res_model,
            'res_id': activity.res_id
        }
