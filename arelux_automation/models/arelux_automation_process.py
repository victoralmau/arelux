# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, fields, models, _
from odoo.exceptions import Warning as UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz
import random
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
        string='Mail Activity type'
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
        compute='_compute_total_records',
        string='Total records',
        store=False
    )

    @api.multi
    def _compute_total_records(self):
        for item in self:
            item.total_records = 0
            if item.model == 'crm.lead':
                item.total_records = len(item.crm_lead_ids)
            elif item.model == 'sale.order':
                item.total_records = len(item.sale_order_ids)

    @api.multi
    def action_calculate(self):
        for item in self:
            if item.state == 'draft':
                # checks
                allow_calculate = True
                # user_ids
                if len(item.user_ids) == 0:
                    allow_calculate = False
                    raise UserError(
                        _('It is necessary to define at least user for the assignment')
                    )
                # lead_type
                if item.model == 'crm.lead':
                    if item.lead_type == 'none':
                        allow_calculate = False
                        raise UserError(
                            _('It is necessary to define a type of lead')
                        )
                # mail_template_id
                if item.mail_template_id.id == 0:
                    allow_calculate = False
                    raise UserError(
                        _('It is necessary to define an email template')
                    )
                # mail_activity
                if item.mail_activity:
                    # mail_activity_type_id
                    if item.mail_activity_type_id.id == 0:
                        allow_calculate = False
                        raise UserError(
                            _('It is necessary to define an activity type')
                        )
                    # mail_activity_date_deadline_days
                    if item.mail_activity_date_deadline_days == 0:
                        allow_calculate = False
                        raise UserError(
                            _('It is necessary to define days for the activity')
                        )
                    # mail_activity_summary
                    if not item.mail_activity_summary:
                        allow_calculate = False
                        raise UserError(
                            _('It is necessary to define a summary of the activity')
                        )
                # lead_m2_to
                if item.model == 'sale.order':
                    if item.lead_m2_to == 0:
                        allow_calculate = False
                        raise UserError(
                            _('It is necessary to define a Lead m2 up to '
                              'greater than 0')
                        )
                # operations_real
                if allow_calculate:
                    # by_model
                    if item.model == 'crm.lead':
                        item.crm_lead_ids = self.env['crm.lead'].search(
                            [
                                ('type', '=', item.lead_type),
                                ('ar_qt_activity_type', '=', item.ar_qt_activity_type),
                                ('ar_qt_customer_type', '=', item.ar_qt_customer_type),
                                ('create_date', '>=', item.create_date_from),
                                ('create_date', '<=', item.create_date_to),
                                ('active', '=', True),
                                ('probability', '>', 0),
                                ('probability', '<', 100),
                                ('user_id', '=', False)
                            ]
                        )
                    elif item.model == 'sale.order':
                        item.sale_order_ids = self.env['sale.order'].search(
                            [
                                ('state', '=', 'draft'),
                                ('amount_total', '>', 0),
                                ('claim', '=', False),
                                ('ar_qt_activity_type', '=', item.ar_qt_activity_type),
                                ('ar_qt_customer_type', '=', item.ar_qt_customer_type),
                                ('create_date', '>=', item.create_date_from),
                                ('create_date', '<=', item.create_date_to),
                                ('opportunity_id', '!=', False),
                                ('opportunity_id.active', '=', True),
                                ('opportunity_id.type', '=', 'opportunity'),
                                ('opportunity_id.probability', '>', 0),
                                ('opportunity_id.user_id', '=', False),
                                ('opportunity_id.lead_m2', '>=', item.lead_m2_from),
                                ('opportunity_id.lead_m2', '<=', item.lead_m2_to)
                            ]
                        )
                    # update
                    item.state = 'calculate'

        return True

    @api.multi
    def action_run(self):
        for item in self:
            if item.state == 'calculate':
                if item.total_records == 0:
                    raise UserError(
                        _('It is necessary that there is a registry to be '
                          'able to execute the action')
                    )
                else:
                    # update
                    item.state = 'in_progress'
                    # mail_activity
                    if item.mail_activity:
                        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
                        activity_dd = current_date + relativedelta(
                            days=item.mail_activity_date_deadline_days
                        )
                        activity_dd_w = activity_dd.weekday()
                        # prevent saturday and sunday
                        if activity_dd_w == 5:  # saturday
                            activity_dd = activity_dd + relativedelta(days=2)
                        elif activity_dd_w == 6:  # sunday
                            activity_dd = activity_dd + relativedelta(days=1)
                    # user_ids
                    user_ids = []
                    for user_id in item.user_ids:
                        user_ids.append(int(user_id.id))
                    # logger
                    _logger.info('Total')
                    _logger.info(item.total_records)
                    # operations
                    if item.model == 'crm.lead':
                        # operations
                        count = 0
                        for crm_lead_id in item.crm_lead_ids:
                            count += 1
                            # user_id_random
                            user_id_random = int(random.choice(user_ids))
                            # automation_proces_vals
                            vals = {
                                'action_log': 'arelux_automation_process_%s' % item.id,
                                'user_id': user_id_random,
                                'mail_activity': item.mail_activity,
                                'mail_template_id': item.mail_template_id.id
                            }
                            # mail_activity
                            if item.mail_activity:
                                vals['mail_activity_type_id'] = \
                                    item.mail_activity_type_id.id
                                vals['mail_activity_date_deadline'] = activity_dd
                                vals['mail_activity_summary'] = \
                                    item.mail_activity_summary
                            # lead_stage_id
                            if item.stage_id:
                                vals['lead_stage_id'] = item.stage_id.id
                            # automation_proces
                            crm_lead_id.automation_proces(vals)
                            # logger_percent
                            percent = (float(count) / float(item.total_records)) * 100
                            percent = "{0:.2f}".format(percent)
                            _logger.info('%s%s (%s/%s)' % (
                                percent,
                                '%',
                                count,
                                item.total_records
                            ))
                    elif item.model == 'sale.order':
                        # operations
                        count = 0
                        for sale_order_id in item.sale_order_ids:
                            count += 1
                            # user_id_random
                            user_id_random = int(random.choice(user_ids))
                            # automation_proces_vals
                            vals = {
                                'action_log': 'arelux_automation_process_%s' % item.id,
                                'user_id': user_id_random,
                                'mail_activity': item.mail_activity,
                                'mail_template_id': item.mail_template_id.id
                            }
                            # mail_activity
                            if item.mail_activity:
                                vals['mail_activity_type_id'] = \
                                    item.mail_activity_type_id.id
                                vals['mail_activity_date_deadline'] = activity_dd
                                vals['mail_activity_summary'] = \
                                    item.mail_activity_summary
                            # sms_template_id
                            if item.sms_template_id:
                                vals['sms_template_id'] = item.sms_template_id.id
                            # lead_stage_id
                            if item.stage_id:
                                vals['lead_stage_id'] = item.stage_id.id
                            # automation_proces
                            sale_order_id.automation_proces(vals)
                            # logger_percent
                            percent = (float(count) / float(item.total_records)) * 100
                            percent = "{0:.2f}".format(percent)
                            _logger.info('%s%s (%s/%s)' % (
                                percent,
                                '%',
                                count,
                                item.total_records
                            ))
                    # update
                    item.state = 'done'
        return True

    @api.multi
    def action_change_to_draft(self):
        for item in self:
            if item.state == 'calculate':
                item.state = 'draft'
        return True
