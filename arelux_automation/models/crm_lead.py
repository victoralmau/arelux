# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def automation_proces(self, params):
        self.ensure_one()
        _logger.info('Aplicando automatizaciones del flujo')
        _logger.info(self.id)
        # example params
        '''
        params = {
            'action_log': 'custom_17_18_19_enero_2020',
            'user_id': 1,
            'mail_activity': True,
            'mail_activity_type_id': 3,
            'mail_activity_date_deadline': '2020-01-01',
            'mail_activity_summary': 'Revisar flujo automatico',
            'mail_template_id': 133
            'lead_stage_id': 2
        }
        '''
        # special_log
        if 'action_log' in params:
            vals = {
                'model': 'crm.lead',
                'res_id': self.id,
                'category': 'crm_lead',
                'action': str(params['action_log']),
            }
            self.env['automation.log'].sudo().create(vals)
        # check_user_id crm_lead
        if 'user_id' in params:
            if self.user_id.id == 0:
                user_id_random = int(params['user_id'])
                # write
                self.write({
                    'user_id': user_id_random
                })
                # save_log
                vals = {
                    'model': 'crm.lead',
                    'res_id': self.id,
                    'category': 'crm_lead',
                    'action': 'asign_user_id',
                }
                self.env['automation.log'].sudo().create(vals)
                # fix change user_id res.partner
                if self.partner_id.user_id.id == 0:
                    self.partner_id.user_id = user_id_random
        # mail_activity
        if 'mail_activity' in params:
            if params['mail_activity']:
                if self.user_id:
                    # search
                    mail_activity_ids = self.env['mail.activity'].sudo().search(
                        [
                            ('activity_type_id', '=', params['mail_activity_type_id']),
                            (
                                'date_deadline',
                                '=',
                                params['next_activity_date_action'].strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                )
                            ),
                            ('res_model_id.model', '=', 'crm.lead'),
                            ('res_id', '=', self.id)
                        ]
                    )
                    if len(mail_activity_ids) == 0:
                        # search
                        ir_model_ids = self.env['ir.model'].sudo().search(
                            [
                                ('model', '=', 'crm.lead')
                            ]
                        )
                        if ir_model_ids:
                            ir_model_id = ir_model_ids[0]
                            # create
                            vals = {
                                'activity_type_id': params['mail_activity_type_id'],
                                'date_deadline':
                                    params['next_activity_date_action'].strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                'user_id': self.user_id.id,
                                'summary': str(params['mail_activity_summary']),
                                'res_model_id': ir_model_id.id,
                                'res_id': self.id
                            }
                            self.env['mail.activity'].sudo(
                                self.create_uid.id
                            ).create(vals)
                            # save_log
                            vals = {
                                'model': 'crm.lead',
                                'res_id': self.id,
                                'category': 'crm_lead',
                                'action': 'mail_activity_type_id_%s'
                                          % params['mail_activity_type_id'],
                            }
                            self.env['automation.log'].sudo().create(vals)
        # send_mail
        if 'mail_template_id' in params:
            self.action_send_mail_with_template_id(
                int(params['mail_template_id'])
            )
            # save_log
            vals = {
                'model': 'crm.lead',
                'res_id': self.id,
                'category': 'crm_lead',
                'action': 'send_mail',
            }
            self.env['automation.log'].sudo().create(vals)
        # update crm.lead stage_id
        if 'lead_stage_id' in params:
            self.stage_id = int(params['lead_stage_id'])
            # save_log
            vals = {
                'model': 'crm.lead',
                'res_id': self.id,
                'category': 'crm_lead',
                'action': 'change_stage_id',
            }
            self.env['automation.log'].sudo().create(vals)

    @api.one
    def action_send_mail_with_template_id(self, template_id=False):
        if template_id:
            mail_template_item = self.env['mail.template'].browse(
                template_id
            )
            vals = {
                'author_id': 1,
                'record_name': self.name
            }
            # Fix user_id
            if self.user_id:
                vals['author_id'] = self.user_id.partner_id.id
                message_obj = self.env['mail.compose.message'].sudo(
                    self.user_id.id
                ).create(vals)
            else:
                message_obj = self.env['mail.compose.message'].sudo().create(vals)

            res = message_obj.onchange_template_id(
                mail_template_item.id,
                'comment',
                'crm.lead',
                self.id
            )
            # mail_compose_message_obj_vals
            vals = {
                'author_id': vals['author_id'],
                'template_id': mail_template_item.id,
                'composition_mode': 'comment',
                'model': 'crm.lead',
                'res_id': self.id,
                'body': res['value']['body'],
                'subject': res['value']['subject'],
                'record_name': vals['record_name'],
                'no_auto_thread': False,
            }
            # partner_ids
            if 'email_from' in res['value']:
                vals['email_from'] = res['value']['email_from']
            # partner_ids
            if 'partner_ids' in res['value']:
                vals['partner_ids'] = res['value']['partner_ids']
            # update
            message_obj.update(vals)
            # send_mail_action
            message_obj.send_mail_action()
            # return
            return True

    @api.model
    def cron_automation_todocesped_profesional_potenciales(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        partners = {}
        res_partner_ids = self.env['res.partner'].search(
            [
                ('active', '=', True),
                ('type', '=', 'contact'),
                ('ar_qt_activity_type', '=', 'todocesped'),
                ('ar_qt_customer_type', '=', 'profesional'),
                ('user_id', '!=', False),
                ('create_date', '<', '2018-01-01')
            ]
        )
        if res_partner_ids:
            partner_ids_potencial = []
            for res_partner_id in res_partner_ids:
                if res_partner_id.ref:
                    partner_ids_potencial.append(res_partner_id.id)
                    partners[res_partner_id.id] = res_partner_id
            # account_invoice
            invoice_ids = self.env['account.invoice'].search(
                [
                    ('state', 'in', ('open', 'paid')),
                    ('amount_total', '>', 0),
                    ('type', '=', 'out_invoice'),
                    ('partner_id', 'in', partner_ids_potencial)
                ]
            )
            if invoice_ids:
                for invoice_id in invoice_ids:
                    if invoice_id.partner_id.id in partner_ids_potencial:
                        partner_ids_potencial.remove(invoice_id.partner_id.id)

            if partner_ids_potencial:
                # crm_lead_6_months
                start_date = current_date + relativedelta(months=-6)
                end_date = current_date
                for partner_id_potencial in partner_ids_potencial:
                    partner_item = partners[partner_id_potencial]
                    crm_activity_report_ids = self.env['crm.activity.report'].search(
                        [
                            ('subtype_id', 'in', (1, 2, 4)),
                            ('partner_id', '=', partner_item.id),
                            ('lead_id', '!=', False),
                            ('date', '>=', start_date.strftime("%Y-%m-%d")),
                            ('date', '<=', end_date.strftime("%Y-%m-%d"))
                        ]
                    )
                    if len(crm_activity_report_ids) == 0:
                        crm_lead_ids = self.env['crm.lead'].search(
                            [
                                ('active', '=', True),
                                ('probability', '<', 100),
                                ('partner_id', '=', partner_item.id),
                                (
                                    'ar_qt_activity_type',
                                    '=',
                                    partner_item.ar_qt_activity_type
                                ),
                                (
                                    'ar_qt_customer_type',
                                    '=',
                                    partner_item.ar_qt_customer_type
                                ),
                            ]
                        )
                        if len(crm_lead_ids) == 0:
                            # Auto-create lead
                            vals = {
                                'active': True,
                                'type': 'opportunity',
                                'stage_id': 1,
                                'name': partner_item.name,
                                'partner_id': partner_item.id,
                                'ar_qt_activity_type':
                                    partner_item.ar_qt_activity_type,
                                'ar_qt_customer_type':
                                    partner_item.ar_qt_customer_type,
                                'user_id': partner_item.user_id.id
                            }
                            crm_lead_obj = self.env['crm.lead'].sudo(
                                partner_item.user_id.id
                            ).create(vals)
                            crm_lead_obj._onchange_partner_id()

    @api.model
    def cron_automation_todocesped_profesional_potenciales_activo(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        partners = {}
        res_partner_ids = self.env['res.partner'].search(
            [
                ('active', '=', True),
                ('type', '=', 'contact'),
                ('ar_qt_activity_type', '=', 'todocesped'),
                ('ar_qt_customer_type', '=', 'profesional'),
                ('user_id', '!=', False),
                ('ref', '=', False),
                ('create_date', '>=', '2018-01-01')
            ]
        )
        if res_partner_ids:
            partner_ids_potencial_activo = []
            for res_partner_id in res_partner_ids:
                partner_ids_potencial_activo.append(res_partner_id.id)
                partners[res_partner_id.id] = res_partner_id
            # account_invoice
            invoice_ids = self.env['account.invoice'].search(
                [
                    ('state', 'in', ('open', 'paid')),
                    ('amount_total', '>', 0),
                    ('type', '=', 'out_invoice'),
                    ('partner_id', 'in', partner_ids_potencial_activo)
                ]
            )
            if invoice_ids:
                for invoice_id in invoice_ids:
                    if invoice_id.partner_id.id in partner_ids_potencial_activo:
                        partner_ids_potencial_activo.remove(
                            invoice_id.partner_id.id
                        )

            if partner_ids_potencial_activo:
                # crm_lead_3_months
                start_date = current_date + relativedelta(months=-3)
                end_date = current_date
                for partner_id_potencial_activo in partner_ids_potencial_activo:
                    partner_item = partners[partner_id_potencial_activo]
                    crm_activity_report_ids = self.env['crm.activity.report'].search(
                        [
                            ('subtype_id', 'in', (1, 2, 4)),
                            ('partner_id', '=', partner_item.id),
                            ('lead_id', '!=', False),
                            ('date', '>=', start_date.strftime("%Y-%m-%d")),
                            ('date', '<=', end_date.strftime("%Y-%m-%d"))
                        ]
                    )
                    if len(crm_activity_report_ids) == 0:
                        crm_lead_ids = self.env['crm.lead'].search(
                            [
                                ('active', '=', True),
                                ('probability', '<', 100),
                                ('partner_id', '=', partner_item.id),
                                (
                                    'ar_qt_activity_type',
                                    '=',
                                    partner_item.ar_qt_activity_type
                                ),
                                (
                                    'ar_qt_customer_type',
                                    '=',
                                    partner_item.ar_qt_customer_type
                                ),
                            ]
                        )
                        if len(crm_lead_ids) == 0:
                            # Auto-create lead
                            vals = {
                                'active': True,
                                'type': 'opportunity',
                                'stage_id': 1,
                                'name': partner_item.name,
                                'partner_id': partner_item.id,
                                'ar_qt_activity_type':
                                    partner_item.ar_qt_activity_type,
                                'ar_qt_customer_type':
                                    partner_item.ar_qt_customer_type,
                                'user_id': partner_item.user_id.id
                            }
                            crm_lead_obj = self.env['crm.lead'].sudo(
                                partner_item.user_id.id
                            ).create(vals)
                            crm_lead_obj._onchange_partner_id()

    @api.model
    def cron_automation_todocesped_profesional_puntuales(self):
        _logger.info('cron_automation_todocesped_profesional_puntuales')

    @api.model
    def cron_automation_todocesped_profesional_recurrentes(self):
        _logger.info('cron_automation_todocesped_profesional_recurrentes')

    @api.model
    def cron_automation_todocesped_profesional_fidelizados(self):
        _logger.info('cron_automation_todocesped_profesional_fidelizados')

    @api.model
    def cron_automation_todocesped_profesional(self):
        # potenciales
        # self.cron_automation_todocesped_profesional_potenciales()
        # potenciales_activo
        # self.cron_automation_todocesped_profesional_potenciales_activo()
        # puntuales
        # self.cron_automation_todocesped_profesional_puntuales()
        # recurrentes
        # self.cron_automation_todocesped_profesional_recurrentes()
        # fidelizados
        # self.cron_automation_todocesped_profesional_fidelizados()
        _logger.info('cron_automation_todocesped_profesional')
