# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api, _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _sgc_auto_stage_conversion(self):
        """
        Cron job to automatically convert stages based on time settings.
        Also sends notifications before deadline.
        """
        now = datetime.now()
        today = now.date()
        
        # Get leads with auto-change enabled stages
        leads = self.search([
            ('stage_id.sgc_auto_change', '=', True),
            ('active', '=', True)
        ])
        
        if not leads:
            return
        
        # Get stage change history from mail.tracking.value
        tracking_vals = self.env['mail.tracking.value'].search([
            ('field_id.name', '=', 'stage_id'),
            ('mail_message_id.model', '=', 'crm.lead'),
            ('mail_message_id.res_id', 'in', leads.ids),
        ])
        
        # Build dict of lead_id -> last stage change date
        stage_change_dates = {}
        for val in tracking_vals:
            lead_id = val.mail_message_id.res_id
            change_date = val.mail_message_id.date
            lead = self.browse(lead_id)
            
            if not lead.exists():
                continue
                
            current_stage_id = lead.stage_id.id
            
            # Check if new value matches current stage
            if val.new_value_integer == current_stage_id:
                if lead_id not in stage_change_dates or change_date > stage_change_dates[lead_id]:
                    stage_change_dates[lead_id] = change_date
        
        model_obj = self.env['ir.model'].search([('model', '=', 'crm.lead')], limit=1)
        
        # Check each lead for deadline
        for lead in leads:
            stage_date = stage_change_dates.get(lead.id)
            if not stage_date:
                continue
            
            elapsed_days = (today - stage_date.date()).days
            stage_days = lead.stage_id.sgc_stage_days or 0
            
            if stage_days <= 0:
                continue
            
            # Check if deadline reached
            if elapsed_days >= stage_days:
                self._sgc_process_stage_deadline(lead, model_obj, today)
            
            # Check if approaching deadline (1 day before)
            elif elapsed_days == stage_days - 1:
                self._sgc_notify_approaching_deadline(lead, model_obj, today)

    def _sgc_process_stage_deadline(self, lead, model_obj, today):
        """Process lead when stage deadline is reached"""
        # Mark existing activities as done
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'crm.lead'),
            ('res_id', '=', lead.id),
            ('active', '=', True)
        ])
        for activity in activities:
            activity.action_done()
        
        # Move to next stage if configured
        if lead.stage_id.sgc_next_stage_id:
            lead.write({'stage_id': lead.stage_id.sgc_next_stage_id.id})
            
            # Create activity notification
            self.env['mail.activity'].create({
                'res_model_id': model_obj.id,
                'res_id': lead.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': _('Cơ hội đã quá hạn chăm sóc và chuyển sang giai đoạn khác, vui lòng kiểm tra'),
                'user_id': lead.user_id.id or self.env.uid,
                'date_deadline': today,
            })
        
        # Or just send notification if configured
        elif lead.stage_id.sgc_notification:
            self.env['mail.activity'].create({
                'res_model_id': model_obj.id,
                'res_id': lead.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                'note': lead.stage_id.sgc_notification,
                'user_id': lead.user_id.id or self.env.uid,
                'date_deadline': today,
            })

    def _sgc_notify_approaching_deadline(self, lead, model_obj, today):
        """Notify when deadline is approaching (1 day before)"""
        self.env['mail.activity'].create({
            'res_model_id': model_obj.id,
            'res_id': lead.id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
            'note': _('Giai đoạn này đang gần hết hạn ngày chăm sóc, vui lòng kiểm tra lại cơ hội!'),
            'user_id': lead.user_id.id or self.env.uid,
            'date_deadline': today,
        })
