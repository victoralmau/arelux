# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import Warning

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz
import random

import logging
_logger = logging.getLogger(__name__)

class AreluxAutomationProcess(models.Model):
    _name = 'arelux.automation.process'
    _description = 'Arelux Automation Process'

    model = fields.Selection(
        selection=[
            ('crm.lead', 'Lead / Opportunity'),
            ('sale.order', 'Sale')
        ],
        default='sale.order',
        string='Model'
    )
    lead_type = fields.Selection(
        selection=[
            ('none', 'Ninguno'),
            ('lead', 'Lead'),
            ('opportunity', 'Opportunity')
        ],
        default='none',
        string='Lead type'
    )
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),
        ],
        default='todocesped',
        size=15,
        string='Activity type'
    )

    ar_qt_activity_type_upper = fields.Char(
        store=False
    )

    @api.onchange('ar_qt_activity_type')
    def _get_ar_qt_activity_type_upper(self):
        for obj in self:
            obj.ar_qt_activity_type_upper = obj.ar_qt_activity_type.capitalize()

    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),
        ],
        default='particular',
        string='Customer type',
    )
    user_ids = fields.Many2many(
        'res.users',
        column1='user_id',
        column2='arelux_automation_process_id',
        string='Users'
    )
    create_date_from = fields.Datetime(
        string='Date from'
    )
    create_date_to = fields.Datetime(
        string='Date to'
    )
    lead_m2_from = fields.Integer(
        string='Lead M2 from'
    )
    lead_m2_to = fields.Integer(
        string='Lead M2 to'
    )
    mail_activity = fields.Boolean(
        string='Activity'
    )
    mail_activity_type_id = fields.Many2one(
        comodel_name='mail.activity.type',
        string='Activity type'
    )
    mail_activity_date_deadline_days = fields.Integer(
        string='Activity date deadline days'
    )
    mail_activity_summary = fields.Char(
        string='Activity summary'
    )
    mail_template_id = fields.Many2one(
        comodel_name='mail.template',
        string='Template id'
    )
    sms_template_id = fields.Many2one(
        comodel_name='sms.template',
        string='Sms template'
    )
    stage_id = fields.Many2one(
        comodel_name='crm.stage',
        string='Stage'
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('calculate', 'Calculate'),
            ('in_progress', 'In progress'),
            ('done', 'Done')
        ],
        size=15,
        default='draft',
        string='State'
    )
    crm_lead_ids = fields.Many2many(
        'crm.lead',
        column1='crm_lead_id',
        column2='arelux_automation_process_id',
        string='Crm Lead Ids'
    )
    sale_order_ids = fields.Many2many(
        'sale.order',
        column1='sale_order_id',
        column2='arelux_automation_process_id',
        string='Sale Order Ids'
    )
    total_records = fields.Integer(
        compute='_get_total_records',
        string='Total records',
        store=False
    )

    @api.one
    def _get_total_records(self):
        for obj in self:
            obj.total_records = 0
            if obj.model == 'crm.lead':
                obj.total_records = len(obj.crm_lead_ids)
            elif obj.model == 'sale.order':
                obj.total_records = len(obj.sale_order_ids)

    @api.multi
    def action_calculate(self):
        for obj in self:
            if obj.state == 'draft':
                # checks
                allow_calculate = True
                # user_ids
                if len(obj.user_ids) == 0:
                    allow_calculate = False
                    raise Warning(_('It is necessary to define at least user for the assignment'))
                # lead_type
                if obj.model == 'crm.lead':
                    if obj.lead_type == 'none':
                        allow_calculate = False
                        raise Warning(_('It is necessary to define a type of lead'))
                # mail_template_id
                if obj.mail_template_id.id == 0:
                    allow_calculate = False
                    raise Warning(_('It is necessary to define an email template'))
                # mail_activity
                if obj.mail_activity:
                    # mail_activity_type_id
                    if obj.mail_activity_type_id.id == 0:
                        allow_calculate = False
                        raise Warning(_('It is necessary to define an activity type'))
                    # mail_activity_date_deadline_days
                    if obj.mail_activity_date_deadline_days == 0:
                        allow_calculate = False
                        raise Warning(_('It is necessary to define days for the activity'))
                    # mail_activity_summary
                    if not obj.mail_activity_summary:
                        allow_calculate = False
                        raise Warning(_('It is necessary to define a summary of the activity'))
                # lead_m2_to
                if obj.model == 'sale.order':
                    if obj.lead_m2_to == 0:
                        allow_calculate = False
                        raise Warning(_('It is necessary to define a Lead m2 up to greater than 0'))
                # operations_real
                if allow_calculate:
                    # by_model
                    if obj.model == 'crm.lead':
                        obj.crm_lead_ids = self.env['crm.lead'].search(
                            [
                                ('type', '=', obj.lead_type),
                                ('ar_qt_activity_type', '=', obj.ar_qt_activity_type),
                                ('ar_qt_customer_type', '=', obj.ar_qt_customer_type),
                                ('create_date', '>=', obj.create_date_from),
                                ('create_date', '<=', obj.create_date_to),
                                ('active', '=', True),
                                ('probability', '>', 0),
                                ('probability', '<', 100),
                                ('user_id', '=', False)
                            ]
                        )
                    elif obj.model == 'sale.order':
                        obj.sale_order_ids = self.env['sale.order'].search(
                            [
                                ('state', '=', 'draft'),
                                ('amount_total', '>', 0),
                                ('claim', '=', False),
                                ('ar_qt_activity_type', '=', obj.ar_qt_activity_type),
                                ('ar_qt_customer_type', '=', obj.ar_qt_customer_type),
                                ('create_date', '>=', obj.create_date_from),
                                ('create_date', '<=', obj.create_date_to),
                                ('opportunity_id', '!=', False),
                                ('opportunity_id.active', '=', True),
                                ('opportunity_id.type', '=', 'opportunity'),
                                ('opportunity_id.probability', '>', 0),
                                ('opportunity_id.user_id', '=', False),
                                ('opportunity_id.lead_m2', '>=', obj.lead_m2_from),
                                ('opportunity_id.lead_m2', '<=', obj.lead_m2_to)
                            ]
                        )
                    # update
                    obj.state = 'calculate'

        return True

    @api.multi
    def action_run(self):
        for obj in self:
            if obj.state == 'calculate':
                if obj.total_records == 0:
                    raise Warning(_('It is necessary that there is a registry to be able to execute the action'))
                else:
                    # update
                    obj.state = 'in_progress'
                    # mail_activity
                    if obj.mail_activity:
                        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
                        mail_activity_date_deadline_action = current_date + relativedelta(days=obj.mail_activity_date_deadline_days)
                        mail_activity_date_deadline_action_weekday = mail_activity_date_deadline_action.weekday()
                        # prevent saturday and sunday
                        if mail_activity_date_deadline_action_weekday == 5:  # saturday
                            mail_activity_date_deadline_action = mail_activity_date_deadline_action + relativedelta(days=2)
                        elif mail_activity_date_deadline_action_weekday == 6:  # sunday
                            mail_activity_date_deadline_action = mail_activity_date_deadline_action + relativedelta(days=1)
                    # user_ids
                    user_ids = []
                    for user_id in obj.user_ids:
                        user_ids.append(int(user_id.id))
                    # logger
                    _logger.info('Total')
                    _logger.info(obj.total_records)
                    # operations
                    if obj.model == 'crm.lead':
                        # operations
                        count = 0
                        for crm_lead_id in obj.crm_lead_ids:
                            count += 1
                            # user_id_random
                            user_id_random = int(random.choice(user_ids))
                            # automation_proces_vals
                            vals = {
                                'action_log': 'arelux_automation_process_' + str(obj.id),
                                'user_id': user_id_random,
                                'mail_activity': obj.mail_activity,
                                'mail_template_id': obj.mail_template_id.id
                            }
                            # mail_activity
                            if obj.mail_activity:
                                vals['mail_activity_type_id'] = obj.mail_activity_type_id.id
                                vals['mail_activity_date_deadline'] = mail_activity_date_deadline_action
                                vals['mail_activity_summary'] = obj.mail_activity_summary
                            # lead_stage_id
                            if obj.stage_id:
                                vals['lead_stage_id'] = obj.stage_id.id
                            # automation_proces
                            crm_lead_id.automation_proces(vals)
                            # logger_percent
                            percent = (float(count) / float(obj.total_records)) * 100
                            percent = "{0:.2f}".format(percent)
                            _logger.info('%s%s (%s/%s)' % (
                                percent,
                                '%',
                                count,
                                obj.total_records
                            ))

                    elif obj.model == 'sale.order':
                        # operations
                        count = 0
                        for sale_order_id in obj.sale_order_ids:
                            count += 1
                            # user_id_random
                            user_id_random = int(random.choice(user_ids))
                            # automation_proces_vals
                            vals = {
                                'action_log': 'arelux_automation_process_'+str(obj.id),
                                'user_id': user_id_random,
                                'mail_activity': obj.mail_activity,
                                'mail_template_id': obj.mail_template_id.id
                            }
                            # mail_activity
                            if obj.mail_activity:
                                vals['mail_activity_type_id'] = obj.mail_activity_type_id.id
                                vals['mail_activity_date_deadline'] = mail_activity_date_deadline_action
                                vals['mail_activity_summary'] = obj.mail_activity_summary
                            # sms_template_id
                            if obj.sms_template_id:
                                vals['sms_template_id'] = obj.sms_template_id.id
                            # lead_stage_id
                            if obj.stage_id:
                                vals['lead_stage_id'] = obj.stage_id.id
                            # automation_proces
                            sale_order_id.automation_proces(vals)
                            # logger_percent
                            percent = (float(count) / float(obj.total_records)) * 100
                            percent = "{0:.2f}".format(percent)
                            _logger.info('%s%s (%s/%s)' % (
                                percent,
                                '%',
                                count,
                                obj.total_records
                            ))
                    # update
                    obj.state = 'done'
        return True

    @api.multi
    def action_change_to_draft(self):
        for obj in self:
            if obj.state == 'calculate':
                obj.state = 'draft'
        return True