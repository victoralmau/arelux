# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import uuid
import pytz
_logger = logging.getLogger(__name__)


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'
    _rec_name = 'internal_name'

    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),
        ],
        size=15,
        string='Tipo de actividad'
    )
    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),
        ],
        string='Tipo de cliente',
    )
    survey_filter_installer = fields.Selection(
        [
            ('none', 'Todos'),
            ('without_installer', 'Sin instalador'),
            ('with_installer', 'Con instalador'),
        ],
        string='Filtro instalador',
        default='none'
    )

    @api.multi
    def get_sale_order_ids_satisfaction(self):
        self.ensure_one()
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        if self.automation_difference_days > 0:
            # date_filters
            date_done_picking_start = current_date + relativedelta(
                days=-self.automation_difference_days*2
            )
            date_done_picking_end = current_date + relativedelta(
                days=-self.automation_difference_days
            )
            # res_partner_sale_order_first_report_ids
            if self.survey_filter_installer == 'none':
                first_report_ids = self.env[
                    'res.partner.sale.order.first.report'
                ].search(
                    [ 
                        ('order_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                        ('order_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),                
                        ('date_done_picking', '!=', False),
                        (
                            'date_done_picking',
                            '>',
                            date_done_picking_start.strftime("%Y-%m-%d")
                        ),
                        (
                            'date_done_picking',
                            '<',
                            date_done_picking_end.strftime("%Y-%m-%d")
                        ),
                    ]
                )
            elif self.survey_filter_installer == 'without_installer':
                first_report_ids = self.env[
                    'res.partner.sale.order.first.report'
                ].search(
                    [ 
                        ('order_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                        ('order_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                        ('order_id.installer_id', '=', False),                
                        ('date_done_picking', '!=', False),
                        (
                            'date_done_picking',
                            '>',
                            date_done_picking_start.strftime("%Y-%m-%d")
                        ),
                        (
                            'date_done_picking',
                            '<',
                            date_done_picking_end.strftime("%Y-%m-%d")
                        ),
                    ]
                )
            elif self.survey_filter_installer == 'with_installer':
                first_report_ids = self.env[
                    'res.partner.sale.order.first.report'
                ].search(
                    [ 
                        ('order_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                        ('order_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                        ('order_id.installer_id', '!=', False),                
                        ('date_done_picking', '!=', False),
                        (
                            'date_done_picking',
                            '>',
                            date_done_picking_start.strftime("%Y-%m-%d")
                        ),
                        (
                            'date_done_picking',
                            '<',
                            date_done_picking_end.strftime("%Y-%m-%d")
                        ),
                    ]
                )            
            # operations
            if first_report_ids:
                order_ids_mapped = first_report_ids.mapped('order_id')
                # survey_user_input_ids
                user_input_ids = self.env['survey.user_input'].search(
                    [ 
                        ('survey_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                        ('survey_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                        ('survey_id.survey_type', '=', self.survey_type),
                        ('survey_id.survey_subtype', '=', self.survey_subtype),                                        
                        ('order_id', 'in', order_ids_mapped.ids)                
                    ]
                )
                if user_input_ids:
                    order_ids = self.env['sale.order'].search(
                        [ 
                            ('id', 'in', order_ids_mapped.ids),
                            ('id', 'not in', user_input_ids.mapped('order_id').ids)
                        ]
                    )
                else:
                    order_ids = self.env['sale.order'].search(
                        [
                            ('id', 'in', order_ids_mapped.ids)
                        ]
                    )
                
        return order_ids
        
    @api.multi
    def get_res_partner_ids_satisfaction_recurrent(self):
        self.ensure_one()
        # general
        survey_frequence_days = {
            'day': 1,
            'week': 7,
            'month': 30,
            'year': 365
        }
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        partner_ids = False
        if self.automation_difference_days > 0:
            # date_filters
            date_filter_end = current_date
            date_filter_start = current_date + relativedelta(
                days=-self.automation_difference_days
            )
            # others
            if self.ar_qt_customer_type == 'profesional':
                # res_partner_sale_order_report_ids
                if self.ar_qt_activity_type == 'arelux':
                    order_report_ids = self.env[
                        'res.partner.sale.order.report'
                    ].search(
                        [ 
                            ('partner_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                            ('partner_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                            ('partner_id.ar_qt_arelux_pf_customer_type', '!=', False),
                            ('partner_id.ar_qt_arelux_pf_customer_type', '!=', 'other'),                                        
                            ('date_done_picking', '!=', False),
                            (
                                'date_done_picking', '>',
                                date_filter_start.strftime("%Y-%m-%d")
                            ),
                            (
                                'date_done_picking',
                                '<',
                                date_filter_end.strftime("%Y-%m-%d")
                            ),
                        ]
                    )
                else:
                    order_report_ids = self.env[
                        'res.partner.sale.order.report'
                    ].search(
                        [ 
                            ('partner_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                            ('partner_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                            ('partner_id.ar_qt_todocesped_pf_customer_type', '!=', False),
                            ('partner_id.ar_qt_todocesped_pf_customer_type', '!=', 'other'),                                        
                            ('date_done_picking', '!=', False),
                            (
                                'date_done_picking',
                                '>',
                                date_filter_start.strftime("%Y-%m-%d")
                            ),
                            (
                                'date_done_picking',
                                '<',
                                date_filter_end.strftime("%Y-%m-%d"))
                            ,
                        ]
                    )
                # operations
                if order_report_ids:
                    # only >1
                    partner_ids_all = {}
                    for order_report_id in order_report_ids:
                        if order_report_id.partner_id.id not in partner_ids_all:
                            partner_ids_all[order_report_id.partner_id.id] = 0
                            
                        partner_ids_all[order_report_id.partner_id.id] += 1
                    
                    if len(partner_ids_all) > 0:
                        partner_ids_mapped = []
                        for partner_id_all in partner_ids_all:
                            partner_id_all_item = partner_ids_all[partner_id_all]
                            if partner_id_all_item > 1:
                                partner_ids_mapped.append(partner_id_all)
    
                        if len(partner_ids_mapped) > 0:
                            # operations
                            partner_ids_max_date_sui = {}
                            for partner_id_mapped in partner_ids_mapped:
                                if partner_id_mapped not in partner_ids_max_date_sui:
                                    partner_ids_max_date_sui[partner_id_mapped] = None
                            # survey_user_input_ids
                            user_input_ids = self.env['survey.user_input'].search(
                                [ 
                                    ('survey_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                                    ('survey_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                                    ('survey_id.survey_type', '=', self.survey_type),
                                    ('survey_id.survey_subtype', '=', self.survey_subtype),                                        
                                    ('partner_id', 'in', partner_ids_mapped)                                        
                                ]
                            )                                
                            if user_input_ids:
                                # operations
                                for input_id in user_input_ids:
                                    date_create_item_format = datetime.strptime(
                                        input_id.date_create,
                                        "%Y-%m-%d %H:%M:%S"
                                    ).strftime('%Y-%m-%d')
                                    
                                    if partner_ids_max_date_sui[input_id.partner_id.id] is None:
                                        partner_ids_max_date_sui[input_id.partner_id.id] = \
                                            date_create_item_format
                                    else:
                                        item_check = partner_ids_max_date_sui[input_id.partner_id.id]
                                        if date_create_item_format > item_check:
                                            partner_ids_max_date_sui[input_id.partner_id.id] = \
                                                date_create_item_format
                            # operations
                            partner_ids_final = []
                            b = datetime.strptime(date_filter_end.strftime("%Y-%m-%d"), "%Y-%m-%d")
                            frequence_days_item = survey_frequence_days[self.survey_frequence]
                            for partner_id in partner_ids_max_date_sui:
                                partner_id_item = res_partner_ids_max_date_sui[partner_id]
                                 # checks
                                if partner_id_item is None:
                                    partner_ids_final.append(partner_id)
                                else:
                                    a = datetime.strptime(partner_id_item, "%Y-%m-%d")                                
                                    delta = b - a
                                    difference_days = delta.days                                                                                                            
                                    if difference_days >= frequence_days_item:
                                        partner_ids_final.append(partner_id)
                            # final
                            partner_ids = self.env['res.partner'].search(
                                [
                                    ('id', 'in', partner_ids_final)
                                ]
                            )
        # return
        return res_partner_ids            
    
    @api.multi
    def send_survey_satisfaction_phone(self):
        self.ensure_one()
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        # deadline
        deadline = False                
        if self.deadline_days > 0:
            deadline = current_date + relativedelta(days=self.deadline_days)                
        # ANADIMOS LOS QUE CORRESPONDEN (NUEVOS)
        sale_order_ids = self.get_sale_order_ids_satisfaction()[0]
        if sale_order_ids:
            survey_survey_old_ids = self.env['survey.survey'].search(
                [
                    ('active', '=', False),
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type),
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type),
                    ('survey_subtype', '=', self.survey_subtype),
                    ('survey_filter_installer', '=', self.survey_filter_installer),
                    ('survey_type', '=', 'mail'),
                    ('survey_type_origin', '=', 'none'),
                    ('id', '<', 13)

                ]
            )
            if survey_survey_old_ids:
                survey_survey_old_id = survey_survey_old_ids[0]
                # results
                survey_user_input_ids = self.env['survey.user_input'].search(
                    [
                        ('survey_id', '=', survey_survey_old_id.id)
                    ]
                )
                if survey_user_input_ids:
                    sale_order_ids_new = self.env['sale.order'].search(
                        [
                            ('id', 'in', sale_order_ids.ids),
                            ('id', 'not in', survey_user_input_ids.mapped('order_id').ids)
                        ]
                    )
                    sale_order_ids = sale_order_ids_new
            # operations
            if sale_order_ids:
                for sale_order_id in sale_order_ids:
                    # creamos el registro personalizado SIN asignar a nadie
                    vals = {
                        'order_id': sale_order_id.id,
                        'lead_id': sale_order_id.opportunity_id.id,
                        'installer_id': sale_order_id.installer_id.id,
                        'state': 'skip',
                        'type': 'manually',
                        'token': uuid.uuid4().__str__(),
                        'survey_id': self.id,
                        'partner_id': sale_order_id.partner_id.id,
                        'test_entry': False
                    }
                    # deadline (if is need)
                    if deadline:
                        vals['deadline'] = deadline
                    # create
                    self.env['survey.user_input'].sudo().create(vals)
    
    @api.multi
    def send_survey_satisfaction_recurrent_phone(self):
        self.ensure_one()
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        # deadline
        deadline = False                
        if self.deadline_days > 0:
            deadline = current_date + relativedelta(days=self.deadline_days)                
        # ANADIMOS LOS QUE CORRESPONDEN (NUEVOS)
        res_partner_ids = self.get_res_partner_ids_satisfaction_recurrent()[0]
        if res_partner_ids:
            # operations
            for res_partner_id in res_partner_ids:
                # creamos el registro personalizado SIN asignar a nadie
                vals = {
                    'state': 'skip',
                    'type': 'manually',
                    'token': uuid.uuid4().__str__(),
                    'survey_id': self.id,
                    'partner_id': res_partner_id.id,
                    'test_entry': False
                }
                # deadline (if is need)
                if deadline:
                    vals['deadline'] = deadline
                # create
                self.env['survey.user_input'].sudo().create(vals)
    
    # mail NOT recurrent
    @api.multi
    def send_survey_real_satisfaction_mail(self):
        self.ensure_one()
        sale_order_ids = self.get_sale_order_ids_satisfaction()[0]
        if sale_order_ids:
            for sale_order_id in sale_order_ids:
                self.send_survey_real(self, sale_order_id)
    
    @api.multi
    def send_survey_satisfaction_mail(self, user_input_expired_ids):
        self.ensure_one()
        if len(user_input_expired_ids) > 0:
            # actual_results
            user_input_ids = self.env['survey.user_input'].search(
                [
                    ('survey_id', '=', self.id)
                ]
            )
            # query
            if user_input_ids:
                order_ids = self.env['sale.order'].search(
                    [ 
                        ('id', 'in', user_input_expired_ids.mapped('order_id').ids),
                        ('id', 'not in', user_input_ids.mapped('order_id').ids)
                    ]
                )
            else:
                order_ids = self.env['sale.order'].search(
                    [
                        ('id', 'in', user_input_expired_ids.mapped('order_id').ids)
                    ]
                )
            # operations
            if order_ids:
                for order_id in order_ids:
                    self.send_survey_real(self, order_id)
    
    # mail recurrent
    @api.multi
    def send_survey_real_satisfaction_recurrent_mail(self):
        self.ensure_one()
        order_ids = self.get_sale_order_ids_satisfaction()[0]
        if order_ids:
            for order_id in order_ids:
                self.send_survey_real(self, order_id)
    
    @api.multi
    def send_survey_satisfaction_recurrent_mail(self, user_input_expired_ids):
        self.ensure_one()
        if len(user_input_expired_ids) > 0:
            # actual_results
            user_input_ids = self.env['survey.user_input'].search(
                [
                    ('survey_id', '=', self.id)
                ]
            )
            # query
            if user_input_ids:
                order_ids = self.env['sale.order'].search(
                    [ 
                        ('id', 'in', user_input_expired_ids.mapped('order_id').ids),
                        ('id', 'not in', user_input_ids.mapped('order_id').ids)
                    ]
                )
            else:
                order_ids = self.env['sale.order'].search(
                    [
                        ('id', 'in', user_input_expired_ids.mapped('order_id').ids)
                    ]
                )
            # operations
            if order_ids:
                for order_id in order_ids:
                    self.send_survey_real(self, order_id)
                            
    @api.multi
    def get_phone_survey_surveys(self):
        self.ensure_one()
        return self.env['survey.survey'].search(
            [ 
                ('active', '=', True),
                ('ar_qt_activity_type', '=', self.ar_qt_activity_type),
                ('ar_qt_customer_type', '=', self.ar_qt_customer_type),                
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'phone'),
                ('survey_subtype', '=', self.survey_subtype),
                ('survey_filter_installer', '=', self.survey_filter_installer)                
            ]
        )                                                            
    
    @api.multi    
    def send_survey_real(self, survey_survey, sale_order):
        self.ensure_one()
        vals = {
            'auto_delete_message': False,
            'template_id': survey_survey.mail_template_id.id,
            'subject': survey_survey.mail_template_id.subject,
            'res_id': survey_survey.id,
            'body': survey_survey.mail_template_id.body_html,
            'record_name': survey_survey.title,
            'no_auto_thread': False,
            'public': 'email_private',
            'reply_to': survey_survey.mail_template_id.reply_to,
            'model': 'survey.survey',
            'survey_id': survey_survey.id,
            'message_type': 'comment',
            'email_from': survey_survey.mail_template_id.email_from,
            'partner_ids': []
        }
        # Fix
        partner_id_partial = (4, sale_order.partner_id.id)
        vals['partner_ids'].append(partner_id_partial)
        # survey_mail_compose_message_obj
        message_obj = self.env['survey.mail.compose.message'].sudo().create(vals)
        message_obj.arelux_send_partner_mails({
            sale_order.partner_id.id: sale_order
        })  