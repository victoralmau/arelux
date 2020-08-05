# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz
import random
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_send_sms_automatic(self,
                                  sms_template_id=False,
                                  need_check_date_order_send_sms=True
                                  ):
        self.ensure_one()
        super(SaleOrder, self).action_send_sms_automatic(
            sms_template_id,
            need_check_date_order_send_sms
        )
        return True

    @api.multi
    def action_generate_sale_order_link_tracker(self):
        self.ensure_one()
        super(SaleOrder, self).action_generate_sale_order_link_tracker()
        return True

    @api.multi
    def automation_proces(self, params):
        self.ensure_one()
        _logger.info(
            _('Aplicando automatizaciones del pedido %s') % self.id
        )
        # special_log
        if 'action_log' in params:
            vals = {
                'model': 'sale.order',
                'res_id': self.id,
                'category': 'sale_order',
                'action': str(params['action_log'])
            }
            self.env['automation.log'].sudo().create(vals)
        # check_user_id sale_order
        if 'user_id' in params:
            if self.user_id.id == 0:
                user_id_random = int(params['user_id'])
                if self.opportunity_id.user_id.id == 0:
                    self.opportunity_id.write({
                        'user_id': user_id_random
                    })
                    # save_log
                    vals = {
                        'model': 'crm.lead',
                        'res_id': self.opportunity_id.id,
                        'category': 'crm_lead',
                        'action': 'asign_user_id'
                    }
                    self.env['automation.log'].sudo().create(vals)
                    # fix change user_id res.partner
                    if self.partner_id.user_id.id == 0:
                        self.partner_id.user_id = user_id_random
                else:
                    self.user_id.id = user_id_random
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
                            ('res_model_id.model', '=', 'sale.order'),
                            ('res_id', '=', self.id)
                        ]
                    )
                    if len(mail_activity_ids) == 0:
                        # search
                        ir_model_ids = self.env['ir.model'].sudo().search(
                            [
                                ('model', '=', 'sale.order')
                            ]
                        )
                        if ir_model_ids:
                            ir_model_id = ir_model_ids[0]
                            # create
                            vals = {
                                'activity_type_id': params['mail_activity_type_id'],
                                'date_deadline':
                                    params['next_activity_date_action'].strftime(
                                        "%Y-%m-%d %H:%M:%S")
                                ,
                                'user_id': self.user_id.id,
                                'summary': str(params['mail_activity_summary']),
                                'res_model_id': ir_model_id.id,
                                'res_id': self.id
                            }
                            self.env['mail.activity'].sudo(
                                self.create_uid.id
                            ).create(ir_model_ids)
                            # save_log
                            vals = {
                                'model': 'sale.prder',
                                'res_id': self.opportunity_id.id,
                                'category': 'sale_order',
                                'action': 'mail_activity_type_id_%s' %
                                          params['mail_activity_type_id'],
                            }
                            self.env['automation.log'].sudo().create(vals)
        # send_mail
        if 'mail_template_id' in params:
            self.action_send_mail_with_template_id(
                int(params['mail_template_id'])
            )
            # save_log
            vals = {
                'model': 'sale.order',
                'res_id': self.id,
                'category': 'sale_order',
                'action': 'send_mail'
            }
            self.env['automation.log'].sudo().create(vals)
            # update
            self.write({
                'state': 'sent',
                'date_order_send_mail': fields.datetime.now()
            })
        # send_sms
        if 'sms_template_id' in params:
            self.action_generate_sale_order_link_tracker()  # Fix generate link-tracker
            self.action_send_sms_automatic(
                int(params['sms_template_id']),
                True
            )
            # save_log
            vals = {
                'model': 'sale.order',
                'res_id': self.id,
                'category': 'sale_order',
                'action': 'send_sms_done'
            }
            self.env['automation.log'].sudo().create(vals)
        # update crm.lead stage_id
        if 'lead_stage_id' in params:
            self.opportunity_id.stage_id = int(params['lead_stage_id'])
            # save_log
            vals = {
                'model': 'crm.lead',
                'res_id': self.opportunity_id.id,
                'category': 'crm_lead',
                'action': 'change_stage_id'
            }
            self.env['automation.log'].sudo().create(vals)

    @api.model
    def cron_automation_profesional_sale_orders_sens_sms(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        # skip_cron
        skip_cron = True
        weekday = current_date.weekday()
        current_date_hour = current_date.strftime("%H")
        hours_allow_by_weekday = {
            '0': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '1': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '2': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '3': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '4': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
        }
        if str(weekday) in hours_allow_by_weekday:
            hours_allow = hours_allow_by_weekday[str(weekday)]
            if current_date_hour in hours_allow:
                skip_cron = False

        if not skip_cron:
            sms_template_id_todocesped = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_prof_so_sms_template_id_todocesped'
                )
            )
            sms_template_id_arelux = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_prof_so_sms_template_id_arelux'
                )
            )
            sms_template_id_both = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_prof_so_sms_template_id_both'
                )
            )
            # retira_cliente
            sms_template_id_rc_todocesped = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_prof_so_sms_template_id_rc_todocesped'
                )
            )
            sms_template_id_rc_arelux = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_prof_so_sms_template_id_rc_arelux'
                )
            )
            sms_template_id_rc_both = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_prof_so_sms_template_id_rc_both'
                )
            )

            automation_log_ids = self.env['automation.log'].search(
                [
                    ('model', '=', 'sale.order'),
                    ('category', '=', 'sale_order'),
                    ('action', '=', 'send_sms_done')
                ]
            )
            sale_order_ids_get_not_in = automation_log_ids.mapped('res_id')
            # confirmation_date
            confirmation_date_start = current_date + relativedelta(days=-5)
            confirmation_date_end = current_date + relativedelta(hours=-4)

            sale_order_ids = self.env['sale.order'].search(
                [
                    ('state', 'in', ['sale', 'done']),
                    ('amount_total', '>', 0),
                    ('claim', '=', False),
                    ('ar_qt_customer_type', '=', 'profesional'),
                    ('create_date', '>', '2019-06-18 00:00:00'),
                    (
                        'confirmation_date',
                        '>',
                        confirmation_date_start.strftime("%Y-%m-%d %H:%M:%S")
                    ),
                    (
                        'confirmation_date',
                        '<',
                        confirmation_date_end.strftime("%Y-%m-%d %H:%M:%S")
                    ),
                    ('partner_id.mobile', '!=', False),
                    ('partner_id.mobile_code_res_country_id', '!=', False),
                    ('id', 'not in', sale_order_ids_get_not_in)
                ]
            )
            if sale_order_ids:
                for sale_order_id in sale_order_ids:
                    if sale_order_id.carrier_id.id == 6:
                        if sale_order_id.ar_qt_activity_type == 'todocesped':
                            sms_template_id = sms_template_id_rc_todocesped
                        elif sale_order_id.ar_qt_activity_type == 'arelux':
                            sms_template_id = sms_template_id_rc_arelux
                        else:
                            sms_template_id = sms_template_id_rc_both
                    else:
                        if sale_order_id.ar_qt_activity_type == 'todocesped':
                            sms_template_id = sms_template_id_todocesped
                        elif sale_order_id.ar_qt_activity_type == 'arelux':
                            sms_template_id = sms_template_id_arelux
                        else:
                            sms_template_id = sms_template_id_both
                    # send_sms
                    sale_order_id.action_generate_sale_order_link_tracker()
                    sale_order_id.action_send_sms_automatic(sms_template_id, True)
                    # save_log
                    vals = {
                        'model': 'sale.order',
                        'res_id': sale_order_id.id,
                        'category': 'sale_order',
                        'action': 'send_sms_done'
                    }
                    self.env['automation.log'].sudo().create(vals)

    @api.model
    def cron_automation_todocesped_particular_sale_orders(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        # skip_cron
        skip_cron = True
        weekday = current_date.weekday()
        current_date_hour = current_date.strftime("%H")
        hours_allow_by_weekday = {
            '0': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '1': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '2': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '3': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '4': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '5': ['11', '12', '13', '14'],
        }
        if str(weekday) in hours_allow_by_weekday:
            hours_allow = hours_allow_by_weekday[str(weekday)]
            if current_date_hour in hours_allow:
                skip_cron = False

        if not skip_cron:
            so_qty_from = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_qty_from'
                )
            )
            so_qty_to = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_qty_to'
                )
            )
            so_hours_since_creation = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_hours_since_creation'
                )
            )
            so_user_ids = self.env['ir.config_parameter'].sudo().get_param(
                'arelux_automation_tc_part_sale_orders_user_ids'
            )
            so_team_id = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_team_id'
                )
            )
            so_stage_id = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_check_stage_id'
                )
            )
            so_change_stage_id = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_change_stage_id'
                )
            )
            so_template_id = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_mail_template_id'
                )
            )
            so_template_id_less_15_m = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_mail_template_id_less_15_m'
                )
            )
            so_sms_template_id = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_sms_template_id'
                )
            )

            if ',' in so_user_ids:
                user_ids = so_user_ids.split(',')
            else:
                user_ids = [so_user_ids]

            date_now_hours_diference = current_date + relativedelta(
                hours=-so_hours_since_creation
            )
            order_ids = self.env['sale.order'].search(
                [
                    ('state', '=', 'draft'),
                    ('amount_total', '>', 0),
                    ('team_id', '=', so_team_id),
                    ('claim', '=', False),
                    ('ar_qt_activity_type', '=', 'todocesped'),
                    ('ar_qt_customer_type', '=', 'particular'),
                    ('create_date', '>', '2019-03-15 00:00:00'),
                    (
                        'create_date',
                        '<',
                        date_now_hours_diference.strftime("%Y-%m-%d %H:%M:%S")
                    ),
                    ('opportunity_id', '!=', False),
                    ('opportunity_id.active', '=', True),
                    ('opportunity_id.type', '=', 'opportunity'),
                    ('opportunity_id.probability', '>', 0),
                    ('opportunity_id.stage_id', '=', so_stage_id),
                    ('opportunity_id.lead_m2', '>=', so_qty_from),
                    ('opportunity_id.lead_m2', '<=', so_qty_to),
                    ('opportunity_id.user_id', '=', False)
                ]
            )
            if order_ids:
                for order_id in order_ids:
                    user_id_random = int(random.choice(user_ids))
                    # params
                    sale_order_params = {
                        'user_id': user_id_random,
                        'next_activity': False,
                        'mail_template_id': so_template_id,
                        'sms_template_id': so_sms_template_id,
                        'lead_stage_id': so_change_stage_id
                    }
                    # Fix 15m
                    if order_id.opportunity_id.lead_m2 < 15:
                        sale_order_params['mail_template_id'] = so_template_id_less_15_m
                    # automation_proces
                    order_id.automation_proces(sale_order_params)

    @api.model
    def cron_automation_todocesped_particular_sale_orders_mail2(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        # skip_cron
        skip_cron = True
        weekday = current_date.weekday()
        current_date_hour = current_date.strftime("%H")
        hours_allow_by_weekday = {
            '0': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '1': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '2': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '3': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '4': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            '5': ['11', '12', '13', '14', '15', '16'],
        }
        if str(weekday) in hours_allow_by_weekday:
            hours_allow = hours_allow_by_weekday[str(weekday)]
            if current_date_hour in hours_allow:
                skip_cron = False

        if not skip_cron:
            mail_template_id = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_automation_tc_part_sale_orders_mail2_mail_template_id'
                )
            )
            # automation_log_ids_send_mail send_mail
            log_ids_send_mail = self.env['automation.log'].search(
                [
                    ('category', '=', 'sale_order'),
                    ('action', '=', 'send_mail')
                ]
            )
            order_ids_get_in = log_ids_send_mail.mapped('res_id')
            # automation_log_ids_send_mail2 previously send_mail2
            log_ids_send_mail2 = self.env['automation.log'].search(
                [
                    ('category', '=', 'sale_order'),
                    ('action', '=', 'send_mail2')
                ]
            )
            order_ids_get_not_in = log_ids_send_mail2.mapped('res_id')
            # sale_orders
            current_date = datetime.today()
            date_order_management_filter = current_date + relativedelta(
                days=-2,
                minutes=-5
            )
            order_ids = self.env['sale.order'].search(
                [
                    ('state', '=', 'sent'),
                    ('claim', '=', False),
                    ('id', 'in', order_ids_get_in),
                    ('id', 'not in', order_ids_get_not_in),
                    (
                        'date_order_management',
                        '<=', date_order_management_filter.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    ),
                    ('opportunity_id', '!=', False),
                    ('opportunity_id.probability', '>', 0),
                    ('opportunity_id.probability', '<', 100)
                ]
            )
            if order_ids:
                for order_id in order_ids:
                    order_id.action_sale_order_mail2(mail_template_id)

    @api.model
    def cron_automation_todocesped_particular_repaso_mail(self):
        _logger.info('cron_automation_todocesped_particular_repaso_mail')
        # def
        current_date = datetime.today()
        shipping_expedition_date = current_date + relativedelta(days=-4)
        # crm_lead
        lead_ids = self.env['crm.lead'].sudo().search(
            [
                ('type', '=', 'opportunity'),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100),
                ('ar_qt_activity_type', '=', 'todocesped'),
                ('ar_qt_customer_type', '=', 'particular'),
                ('stage_id', '=', 2)
            ]
        )
        if lead_ids:
            # sale_order
            _logger.info('crm_lead_ids')
            _logger.info(lead_ids.ids)
            order_ids = self.env['sale.order'].sudo().search(
                [
                    ('opportunity_id', 'in', lead_ids.ids),
                    ('claim', '=', False),
                    ('amount_total', '=', 0),
                    ('carrier_id.carrier_type', '=', 'nacex')
                ]
            )
            if order_ids:
                # stock.picking
                _logger.info('sale_order_ids')
                _logger.info(order_ids.ids)
                picking_ids = self.env['stock.picking'].sudo().search(
                    [
                        ('sale_id', 'in', order_ids.ids),
                        ('state', '=', 'done'),
                        ('carrier_id.carrier_type', '=', 'nacex'),
                        ('shipping_expedition_id', '!=', False),
                        ('shipping_expedition_id.state', '=', 'delivered'),
                        (
                            'shipping_expedition_id.date',
                            '<=',
                            shipping_expedition_date.strftime("%Y-%m-%d")
                        )
                    ]
                )
                _logger.info('stock_picking_ids')
                _logger.info(picking_ids.ids)
                if picking_ids:
                    lead_ids = []
                    for picking_id in picking_ids:
                        if picking_id.sale_id:
                            if picking_id.sale_id.opportunity_id:
                                if picking_id.sale_id.opportunity_id.id not in lead_ids:
                                    lead_ids.append(
                                        int(picking_id.sale_id.opportunity_id.id)
                                    )
                    # sale_order (with_sent_item)
                    order_ids_operations = self.env['sale.order'].sudo().search(
                        [
                            ('opportunity_id', 'in', lead_ids),
                            ('claim', '=', False),
                            ('amount_total', '>', 0),
                            ('state', '=', 'sent')
                        ]
                    )
                    if order_ids_operations:
                        lead_ids_operations = self.env['crm.lead'].sudo().search(
                            [
                                (
                                    'id',
                                    'in',
                                    order_ids_operations.mapped('opportunity_id').ids
                                )
                            ]
                        )
                        _logger.info(
                            _('Total items aplicados %s') % len(lead_ids_operations)
                        )
                        for lead_id in lead_ids_operations:
                            order_ids_operations = self.env['sale.order'].sudo().search(
                                [
                                    ('opportunity_id', '=', lead_id.id),
                                    ('claim', '=', False),
                                    ('amount_total', '>', 0),
                                    ('state', '=', 'sent')
                                ]
                            )
                            if order_ids_operations:
                                order_id_operations = order_ids_operations[0]
                                # send_mail (sale.order)
                                # change state_id (opportunity_id)
                                _logger.info(
                                    _('Operaciones del presupuesto %s')
                                    % order_id_operations.name
                                )

    @api.multi
    def action_sale_order_mail2(self, template_id=False):
        self.ensure_one()
        need_send_mail = False
        automation_log_ids = self.env['automation.log'].search(
            [
                ('category', '=', 'sale_order'),
                ('action', '=', 'send_mail2'),
                ('res_id', '=', self.id)
            ]
        )
        if len(automation_log_ids) == 0:
            if not self.claim and self.state == 'sent' and self.amount_untaxed > 0:
                current_date = datetime.today()
                date_order_management_filter = current_date + relativedelta(
                    days=-2, minutes=-5
                )

                if self.date_order_management <= date_order_management_filter.strftime(
                        "%Y-%m-%d %H:%M:%S"
                ):
                    need_send_mail = True

                    date_order_management_check = datetime.strptime(
                        self.date_order_management,
                        "%Y-%m-%d %H:%M:%S"
                    ) + relativedelta(minutes=5)
                    # 1- Que no exista un email enviado por nosotros desde el flujo
                    # o pto > fecha gestion
                    if self.user_id:
                        message_ids = self.env['mail.message'].search(
                            [
                                ('model', '=', 'sale.order'),
                                ('res_id', '=', self.id),
                                ('subtype_id', '=', 1),
                                ('author_id', '=', self.user_id.partner_id.id),
                                ('date', '>', date_order_management_check.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ))
                            ]
                        )
                        if message_ids:
                            need_send_mail = False

                        if self.opportunity_id and need_send_mail:
                            message_ids = self.env['mail.message'].search(
                                [
                                    ('model', '=', 'crm.lead'),
                                    ('res_id', '=', self.opportunity_id.id),
                                    ('subtype_id', '=', 1),
                                    ('author_id', '=', self.user_id.partner_id.id),
                                    ('date', '>', date_order_management_check.strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ))
                                ]
                            )
                            if message_ids:
                                need_send_mail = False
                    # 2- Que no exista un email creado por el cliente (author_id)
                    # > a la fecha gestion
                    if need_send_mail:
                        message_ids = self.env['mail.message'].search(
                            [
                                ('model', '=', 'sale.order'),
                                ('res_id', '=', self.id),
                                ('author_id', '=', self.partner_id.id),
                                ('message_type', '=', 'email'),
                                ('date', '>', date_order_management_check.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ))
                            ]
                        )
                        if message_ids:
                            need_send_mail = False
                    # 3- Que no exista ninguna llamada en el flujo > a la
                    # fecha gestion
                    if self.opportunity_id and need_send_mail:
                        message_ids = self.env['mail.message'].search(
                            [
                                ('model', '=', 'crm.lead'),
                                ('res_id', '=', self.opportunity_id.id),
                                ('subtype_id', '=', 5),
                                ('date', '>', date_order_management_check.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ))
                            ]
                        )
                        if message_ids:
                            need_send_mail = False

        if need_send_mail:
            self.action_send_mail_with_template_id(template_id)
            # save_log
            vals = {
                'model': 'sale.order',
                'res_id': self.id,
                'category': 'sale_order',
                'action': 'send_mail2'
            }
            self.env['automation.log'].sudo().create(vals)

    @api.multi
    def action_send_mail_with_template_id(self, template_id=False):
        self.ensure_one()
        if template_id:
            mail_template_item = self.env['mail.template'].search(
                [
                    ('id', '=', template_id)
                ]
            )[0]
            vals = {
                'author_id': self.user_id.partner_id.id,
                'record_name': self.name
            }
            message_obj = self.env['mail.compose.message'].with_context().sudo(
                self.user_id.id
            ).create(vals)
            res = message_obj.onchange_template_id(
                mail_template_item.id,
                'comment',
                'sale.order',
                self.id
            )
            vals = {
                'author_id': vals['author_id'],
                'template_id': mail_template_item.id,
                'composition_mode': 'comment',
                'model': 'sale.order',
                'res_id': self.id,
                'body': res['value']['body'],
                'subject': res['value']['subject'],
                'record_name': vals['record_name'],
                'no_auto_thread': False,
            }
            # email_from
            if 'email_from' in res['value']:
                vals['email_from'] = res['value']['email_from']
            # partner_ids
            if 'partner_ids' in res['value']:
                vals['partner_ids'] = res['value']['partner_ids']
            # update
            message_obj.update(vals)
            message_obj.send_mail_action()
            return True
