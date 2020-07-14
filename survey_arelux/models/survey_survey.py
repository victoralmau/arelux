# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, exceptions, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime

import uuid
import pytz

import logging
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
    
    @api.one    
    def get_sale_order_ids_satisfaction(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        sale_order_ids = False
        
        if self.automation_difference_days>0:
            #date_filters
            date_done_picking_start = current_date + relativedelta(days=-self.automation_difference_days*2)
            date_done_picking_end = current_date + relativedelta(days=-self.automation_difference_days)            
            #res_partner_sale_order_first_report_ids
            if self.survey_filter_installer=='none':
                res_partner_sale_order_first_report_ids = self.env['res.partner.sale.order.first.report'].search(
                    [ 
                        ('order_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                        ('order_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),                
                        ('date_done_picking', '!=', False),
                        ('date_done_picking', '>', date_done_picking_start.strftime("%Y-%m-%d")),
                        ('date_done_picking', '<', date_done_picking_end.strftime("%Y-%m-%d")),                
                    ]
                )
            elif self.survey_filter_installer=='without_installer':
                res_partner_sale_order_first_report_ids = self.env['res.partner.sale.order.first.report'].search(
                    [ 
                        ('order_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                        ('order_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                        ('order_id.installer_id', '=', False),                
                        ('date_done_picking', '!=', False),
                        ('date_done_picking', '>', date_done_picking_start.strftime("%Y-%m-%d")),
                        ('date_done_picking', '<', date_done_picking_end.strftime("%Y-%m-%d")),                
                    ]
                )
            elif self.survey_filter_installer=='with_installer':
                res_partner_sale_order_first_report_ids = self.env['res.partner.sale.order.first.report'].search(
                    [ 
                        ('order_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                        ('order_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                        ('order_id.installer_id', '!=', False),                
                        ('date_done_picking', '!=', False),
                        ('date_done_picking', '>', date_done_picking_start.strftime("%Y-%m-%d")),
                        ('date_done_picking', '<', date_done_picking_end.strftime("%Y-%m-%d")),                
                    ]
                )            
            #operations
            if len(res_partner_sale_order_first_report_ids)>0:                
                order_ids_mapped = res_partner_sale_order_first_report_ids.mapped('order_id')
                #survey_user_input_ids
                survey_user_input_ids = self.env['survey.user_input'].search(
                    [ 
                        ('survey_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                        ('survey_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                        ('survey_id.survey_type', '=', self.survey_type),
                        ('survey_id.survey_subtype', '=', self.survey_subtype),                                        
                        ('order_id', 'in', order_ids_mapped.ids)                
                    ]
                )
                if len(survey_user_input_ids)>0:
                    sale_order_ids = self.env['sale.order'].search(
                        [ 
                            ('id', 'in', order_ids_mapped.ids),
                            ('id', 'not in', survey_user_input_ids.mapped('order_id').ids)                                                
                        ]
                    )
                else:
                    sale_order_ids = self.env['sale.order'].search([('id', 'in', order_ids_mapped.ids)])
                
        return sale_order_ids
        
    @api.one    
    def get_res_partner_ids_satisfaction_recurrent(self):
        #general
        survey_frequence_days = {
            'day': 1,
            'week': 7,
            'month': 30,
            'year': 365
        }
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        res_partner_ids = False
        
        if self.automation_difference_days>0:
            #date_filters
            date_filter_end = current_date
            date_filter_start = current_date + relativedelta(days=-self.automation_difference_days)
            #others
            if self.ar_qt_customer_type=='profesional':                                
                #res_partner_sale_order_report_ids
                if self.ar_qt_activity_type=='arelux':
                    res_partner_sale_order_report_ids = self.env['res.partner.sale.order.report'].search(
                        [ 
                            ('partner_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                            ('partner_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                            ('partner_id.ar_qt_arelux_pf_customer_type', '!=', False),
                            ('partner_id.ar_qt_arelux_pf_customer_type', '!=', 'other'),                                        
                            ('date_done_picking', '!=', False),
                            ('date_done_picking', '>', date_filter_start.strftime("%Y-%m-%d")),
                            ('date_done_picking', '<', date_filter_end.strftime("%Y-%m-%d")),                
                        ]
                    )
                else:
                    res_partner_sale_order_report_ids = self.env['res.partner.sale.order.report'].search(
                        [ 
                            ('partner_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                            ('partner_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                            ('partner_id.ar_qt_todocesped_pf_customer_type', '!=', False),
                            ('partner_id.ar_qt_todocesped_pf_customer_type', '!=', 'other'),                                        
                            ('date_done_picking', '!=', False),
                            ('date_done_picking', '>', date_filter_start.strftime("%Y-%m-%d")),
                            ('date_done_picking', '<', date_filter_end.strftime("%Y-%m-%d")),                
                        ]
                    )
                #operations
                if len(res_partner_sale_order_report_ids)>0:                
                    #only >1
                    partner_ids_all = {}
                    for res_partner_sale_order_report_id in res_partner_sale_order_report_ids:
                        if res_partner_sale_order_report_id.partner_id.id not in partner_ids_all:
                            partner_ids_all[res_partner_sale_order_report_id.partner_id.id] = 0
                            
                        partner_ids_all[res_partner_sale_order_report_id.partner_id.id] += 1
                    
                    if len(partner_ids_all)>0:
                        partner_ids_mapped = []
                        for partner_id_all in partner_ids_all:
                            partner_id_all_item = partner_ids_all[partner_id_all]
                            if partner_id_all_item>1:
                                partner_ids_mapped.append(partner_id_all)
    
                        if len(partner_ids_mapped)>0:
                            #operations
                            res_partner_ids_max_date_survey_user_input = {}
                            for partner_id_mapped in partner_ids_mapped:
                                if partner_id_mapped not in res_partner_ids_max_date_survey_user_input:
                                    res_partner_ids_max_date_survey_user_input[partner_id_mapped] = None                                                   
                            #survey_user_input_ids
                            survey_user_input_ids = self.env['survey.user_input'].search(
                                [ 
                                    ('survey_id.ar_qt_activity_type', '=', self.ar_qt_activity_type),
                                    ('survey_id.ar_qt_customer_type', '=', self.ar_qt_customer_type),
                                    ('survey_id.survey_type', '=', self.survey_type),
                                    ('survey_id.survey_subtype', '=', self.survey_subtype),                                        
                                    ('partner_id', 'in', partner_ids_mapped)                                        
                                ]
                            )                                
                            if len(survey_user_input_ids)>0:
                                #operations
                                for survey_user_input_id in survey_user_input_ids:
                                    date_create_item_format = datetime.strptime(survey_user_input_id.date_create, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')
                                    
                                    if res_partner_ids_max_date_survey_user_input[survey_user_input_id.partner_id.id]==None:
                                        res_partner_ids_max_date_survey_user_input[survey_user_input_id.partner_id.id] = date_create_item_format
                                    else:
                                        if date_create_item_format>res_partner_ids_max_date_survey_user_input[survey_user_input_id.partner_id.id]:
                                            res_partner_ids_max_date_survey_user_input[survey_user_input_id.partner_id.id] = date_create_item_format                        
                            #operations
                            res_partner_ids_final = []                            
                            b = datetime.strptime(date_filter_end.strftime("%Y-%m-%d"), "%Y-%m-%d")
                            survey_frequence_days_item = survey_frequence_days[self.survey_frequence]
                            for partner_id in res_partner_ids_max_date_survey_user_input:
                                partner_id_item = res_partner_ids_max_date_survey_user_input[partner_id]
                                #checks
                                if partner_id_item==None:
                                    res_partner_ids_final.append(partner_id)
                                else:
                                    a = datetime.strptime(partner_id_item, "%Y-%m-%d")                                
                                    delta = b - a
                                    difference_days = delta.days                                                                                                            
                                    if difference_days>=survey_frequence_days_item:
                                        res_partner_ids_final.append(partner_id)                                                                                                                                       
                            #final
                            res_partner_ids = self.env['res.partner'].search([('id', 'in', res_partner_ids_final)])
        #return                            
        return res_partner_ids            
    
    @api.one    
    def send_survey_satisfaction_phone(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        #deadline
        deadline = False                
        if self.deadline_days>0:
            deadline = current_date + relativedelta(days=self.deadline_days)                
        #ANADIMOS LOS QUE CORRESPONDEN (NUEVOS)
        sale_order_ids = self.get_sale_order_ids_satisfaction()[0]#Fix multi
        if sale_order_ids!=False:
            if len(sale_order_ids)>0:
                #buscamos los de encuestas viejas "raros" (los que no pasaron por la de telefono y en el pasado se hicieron de email directamente)
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
                if len(survey_survey_old_ids)>0:
                    survey_survey_old_id = survey_survey_old_ids[0]
                    #results
                    survey_user_input_ids = self.env['survey.user_input'].search([('survey_id', '=', survey_survey_old_id.id)])
                    if len(survey_user_input_ids)>0:
                        sale_order_ids_new = self.env['sale.order'].search(
                            [ 
                                ('id', 'in', sale_order_ids.ids),
                                ('id', 'not in', survey_user_input_ids.mapped('order_id').ids)                                                
                            ]
                        )
                        sale_order_ids = sale_order_ids_new                                                                                                            
                #operations                        
                if len(sale_order_ids)>0:
                    for sale_order_id in sale_order_ids:
                        #token
                        token = uuid.uuid4().__str__()                                        
                        #creamos el registro personalizado SIN asignar a nadie
                        survey_user_input_vals = {
                            'order_id': sale_order_id.id,
                            'lead_id': sale_order_id.opportunity_id.id,
                            #'user_id': sale_order_id.user_id.id,#Fix prevent assign 'incorrectly'
                            'installer_id': sale_order_id.installer_id.id,
                            'state': 'skip',
                            'type': 'manually',
                            'token': token,
                            'survey_id': self.id,
                            'partner_id': sale_order_id.partner_id.id,
                            'test_entry': False
                        }
                        #deadline (if is need)
                        if deadline!=False:
                            survey_user_input_vals['deadline'] = deadline
                        #create
                        survey_user_input_obj = self.env['survey.user_input'].sudo().create(survey_user_input_vals)
    
    @api.one    
    def send_survey_satisfaction_recurrent_phone(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        #deadline
        deadline = False                
        if self.deadline_days>0:
            deadline = current_date + relativedelta(days=self.deadline_days)                
        #ANADIMOS LOS QUE CORRESPONDEN (NUEVOS)
        res_partner_ids = self.get_res_partner_ids_satisfaction_recurrent()[0]#Fix multi
        if res_partner_ids!=False:
            if len(res_partner_ids)>0:                        
                #operations
                for res_partner_id in res_partner_ids:                
                    #token
                    token = uuid.uuid4().__str__()                                        
                    #creamos el registro personalizado SIN asignar a nadie
                    survey_user_input_vals = {
                        #'user_id': sale_order_id.user_id.id,#Fix prevent assign 'incorrectly'
                        'state': 'skip',
                        'type': 'manually',
                        'token': token,
                        'survey_id': self.id,
                        'partner_id': res_partner_id.id,
                        'test_entry': False
                    }
                    #deadline (if is need)
                    if deadline!=False:
                        survey_user_input_vals['deadline'] = deadline
                    #create
                    survey_user_input_obj = self.env['survey.user_input'].sudo().create(survey_user_input_vals)
    
    #mail NOT recurrent
    @api.one    
    def send_survey_real_satisfaction_mail(self):
        sale_order_ids = self.get_sale_order_ids_satisfaction()[0]#Fix multi                                        
        #operations
        if sale_order_ids!=False:
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    self.send_survey_real(self, sale_order_id)
    
    @api.one    
    def send_survey_satisfaction_mail(self, survey_survey_input_expired_ids):
        if len(survey_survey_input_expired_ids)>0:
            #actual_results
            survey_survey_input_ids = self.env['survey.user_input'].search([('survey_id', '=', self.id)])
            #query
            if len(survey_survey_input_expired_ids)>0:
                sale_order_ids = self.env['sale.order'].search(
                    [ 
                        ('id', 'in', survey_survey_input_expired_ids.mapped('order_id').ids),
                        ('id', 'not in', survey_survey_input_ids.mapped('order_id').ids)                                                
                    ]
                )
            else:
                sale_order_ids = self.env['sale.order'].search([('id', 'in', survey_survey_input_expired_ids.mapped('order_id').ids)])
            #operations
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:                                
                    self.send_survey_real(self, sale_order_id)
    
    #mail recurrent                                                                                                        
    @api.one    
    def send_survey_real_satisfaction_recurrent_mail(self):
        sale_order_ids = self.get_sale_order_ids_satisfaction()[0]#Fix multi                                        
        #operations
        if sale_order_ids!=False:
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    self.send_survey_real(self, sale_order_id)
    
    @api.one    
    def send_survey_satisfaction_recurrent_mail(self, survey_survey_input_expired_ids):
        if len(survey_survey_input_expired_ids)>0:
            #actual_results
            survey_survey_input_ids = self.env['survey.user_input'].search([('survey_id', '=', self.id)])
            #query
            if len(survey_survey_input_expired_ids)>0:
                sale_order_ids = self.env['sale.order'].search(
                    [ 
                        ('id', 'in', survey_survey_input_expired_ids.mapped('order_id').ids),
                        ('id', 'not in', survey_survey_input_ids.mapped('order_id').ids)                                                
                    ]
                )
            else:
                sale_order_ids = self.env['sale.order'].search([('id', 'in', survey_survey_input_expired_ids.mapped('order_id').ids)])
            #operations
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:                                
                    self.send_survey_real(self, sale_order_id)
                            
    @api.one
    def get_phone_survey_surveys(self):
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
        #survey_mail_compose_message_vals                                                                                                                                                    
        survey_mail_compose_message_vals = {
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
        #Fix
        partner_id_partial = (4, sale_order.partner_id.id)
        survey_mail_compose_message_vals['partner_ids'].append(partner_id_partial)            
        #survey_mail_compose_message_obj                                                                                                    
        survey_mail_compose_message_obj = self.env['survey.mail.compose.message'].sudo().create(survey_mail_compose_message_vals)                
        survey_mail_compose_message_obj.arelux_send_partner_mails({
            sale_order.partner_id.id: sale_order
        })  