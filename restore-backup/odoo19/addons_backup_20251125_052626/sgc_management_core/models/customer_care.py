# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError

CARE_ACTIVITY_SELECTION = [
    ('email', 'Email Marketing'),
    ('zalo', 'Zalo / Social'),
    ('event', 'Sự kiện / Hội thảo'),
    ('program', 'Thông báo chương trình'),
    ('call', 'Gọi điện'),
    ('survey', 'Khảo sát'),
    ('other', 'Khác'),
]

class CustomerCareTemplate(models.Model):
    _name = 'sgc.customer.care.template'
    _description = 'Customer Care Template'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    step_ids = fields.One2many('sgc.customer.care.template.step', 'template_id', string='Steps')

    def _schedule_customer_care(self, partner, care_type='success', sale_order=None, contract=None, reference_date=None):
        self.ensure_one()
        if not partner:
            return
        reference_date = reference_date or date.today()
        log_obj = self.env['sgc.customer.care.log']
        domain = [('template_id', '=', self.id),
                  ('care_type', '=', care_type)]
        if sale_order:
            domain.append(('sale_order_id', '=', sale_order.id))
        if contract:
            domain.append(('contract_id', '=', contract.id))
        if log_obj.search_count(domain):
            return

        user = sale_order.user_id if sale_order else (contract.sale_order_id.user_id if contract else False)
        vals_list = []
        for step in self.step_ids:
            planned_date = reference_date + relativedelta(days=step.lead_time_days or 0)
            vals = {
                'name': "%s - %s" % (self.code, step.name),
                'partner_id': partner.id,
                'sale_order_id': sale_order.id if sale_order else False,
                'contract_id': contract.id if contract else False,
                'template_id': self.id,
                'template_step_id': step.id,
                'activity_type': step.activity_type,
                'planned_date': planned_date,
                'care_type': care_type,
                'responsible_id': user.id,
                'description': step.description,
            }
            vals_list.append(vals)
        if vals_list:
            log_obj.create(vals_list)


class CustomerCareTemplateStep(models.Model):
    _name = 'sgc.customer.care.template.step'
    _description = 'Customer Care Template Step'
    _order = 'sequence, id'

    template_id = fields.Many2one('sgc.customer.care.template', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    description = fields.Text()
    activity_type = fields.Selection(CARE_ACTIVITY_SELECTION, default='email', required=True)
    lead_time_days = fields.Integer(default=0, help="Số ngày sau mốc tạo để thực hiện bước này.")


class CustomerCareLog(models.Model):
    _name = 'sgc.customer.care.log'
    _description = 'Customer Care Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'planned_date, id'

    name = fields.Char(required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', required=True, tracking=True)
    sale_order_id = fields.Many2one('sale.order', tracking=True)
    contract_id = fields.Many2one('sgc.signed.contract', tracking=True)
    template_id = fields.Many2one('sgc.customer.care.template', readonly=True)
    template_step_id = fields.Many2one('sgc.customer.care.template.step', readonly=True)
    activity_type = fields.Selection(CARE_ACTIVITY_SELECTION, string='Loại hoạt động', tracking=True)
    care_type = fields.Selection([
        ('success', 'Sau bán hàng'),
        ('completed', 'Hoàn tất hợp đồng'),
        ('lost', 'Khách hàng rớt'),
    ], default='success', tracking=True)
    planned_date = fields.Date(default=lambda self: fields.Date.context_today(self), tracking=True)
    completed_date = fields.Date(tracking=True)
    responsible_id = fields.Many2one('res.users', string='Phụ trách', tracking=True)
    description = fields.Text()
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('in_progress', 'Đang làm'),
        ('done', 'Hoàn tất'),
        ('approved', 'Đã duyệt'),
    ], default='draft', tracking=True)
    locked = fields.Boolean(default=False)
    approve_user_id = fields.Many2one('res.users', string='Người duyệt', tracking=True, readonly=True)

    def _check_editable(self):
        if not self:
            return
        if self.env.user.has_group('sgc_management_core.group_sgc_sales_director'):
            return
        if any(log.locked or log.state == 'approved' for log in self):
            raise UserError(_('Log CSKH đã được khóa. Liên hệ Ban Giám Đốc để mở khóa.'))

    def write(self, vals):
        if any(field in vals for field in ['name', 'description', 'planned_date', 'state', 'completed_date']):
            self._check_editable()
        return super().write(vals)

    def unlink(self):
        self._check_editable()
        return super().unlink()

    def action_start(self):
        self._check_editable()
        self.write({'state': 'in_progress'})

    def action_done(self):
        self._check_editable()
        today = fields.Date.context_today(self)
        self.write({'state': 'done', 'completed_date': today})

    def action_approve(self):
        director_group = self.env.user.has_group('sgc_management_core.group_sgc_sales_director')
        if not director_group:
            raise UserError(_('Chỉ Ban Giám Đốc được phép duyệt log CSKH.'))
        self.write({'state': 'approved', 'locked': True, 'approve_user_id': self.env.user.id})

    def action_unlock(self):
        if not self.env.user.has_group('sgc_management_core.group_sgc_sales_director'):
            raise UserError(_('Chỉ Ban Giám Đốc mới mở khóa được log đã duyệt.'))
        self.write({'locked': False, 'state': 'in_progress'})

