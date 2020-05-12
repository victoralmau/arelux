# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz

import random

class SaleOrder(models.Model):
    _inherit = 'sale.order'        
    
    @api.one
    def action_send_sms_automatic(self, sms_template_id=False, need_check_date_order_send_sms=True):
        res = super(SaleOrder, self).action_send_sms_automatic(sms_template_id, need_check_date_order_send_sms)
        return True
        
    @api.one    
    def automation_proces(self, params):
        _logger.info('Aplicando automatizaciones del pedido')
        _logger.info(self.id)
        #example params
        '''
        params = {
            'action_log': 'custom_17_18_19_enero_2020',
            'user_id': 1,            
            'mail_template_id': 133
            'sms_template_id': 1,
            'lead_stage_id': 2
        }
        '''
        #special_log
        if 'action_log' in params:
            automation_log_vals = {                    
                'model': 'sale.order',
                'res_id': self.id,
                'category': 'sale_order',
                'action': str(params['action_log']),                                                                                                                                                                                           
            }
            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        #check_user_id sale_order
        if 'user_id' in params:
            if self.user_id.id==0:            
                user_id_random = int(params['user_id'])
                #check_user_id crm_lead (write event and function user_id change in crm_lead, sale_orders and res_partner if need)    
                if self.opportunity_id.user_id.id==0:
                    self.opportunity_id.write({
                        'user_id': user_id_random
                    })
                    #save_log
                    automation_log_vals = {                    
                        'model': 'crm.lead',
                        'res_id': self.opportunity_id.id,
                        'category': 'crm_lead',
                        'action': 'asign_user_id',                                                                                                                                                                                           
                    }
                    automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
                    #fix change user_id res.partner
                    if self.partner_id.user_id.id==0:
                        self.partner_id.user_id = user_id_random
                else:                        
                    self.user_id.id = user_id_random        
        #send_mail
        if 'mail_template_id' in params:
            self.action_send_mail_with_template_id(int(params['mail_template_id']))
            #save_log
            automation_log_vals = {                    
                'model': 'sale.order',
                'res_id': self.id,
                'category': 'sale_order',
                'action': 'send_mail',                                                                                                                                                                                           
            }
            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
            #update
            self.write({
                'state': 'sent',
                'date_order_send_mail': fields.datetime.now()
            })                    
        #send_sms
        if 'sms_template_id' in params:
            self.action_send_sms_automatic(int(params['sms_template_id']), True)
        #update crm.lead stage_id
        if 'lead_stage_id' in params:
            self.opportunity_id.stage_id = int(params['lead_stage_id'])
            #save_log
            automation_log_vals = {                    
                'model': 'crm.lead',
                'res_id': self.opportunity_id.id,
                'category': 'crm_lead',
                'action': 'change_stage_id',                                                                                                                                                                                           
            }
            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)        
    
    @api.model    
    def cron_automation_profesional_sale_orders_sens_sms(self):    
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))        
        #skip_cron
        skip_cron = True
        
        weekday = current_date.weekday()
        current_date_hour = current_date.strftime("%H")    
                        
        hours_allow_by_weekday = {
            '0': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Lunes
            '1': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Martes
            '2': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Miercoles
            '3': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Jueves
            '4': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Viernes
        }

        if str(weekday) in hours_allow_by_weekday:
            hours_allow = hours_allow_by_weekday[str(weekday)]        
            if current_date_hour in hours_allow:            
                skip_cron = False                      
        
        if skip_cron==False:
            arelux_automation_tc_prof_sale_orders_sms_template_id_todocesped = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_prof_sale_orders_sms_template_id_todocesped'))
            arelux_automation_tc_prof_sale_orders_sms_template_id_arelux = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_prof_sale_orders_sms_template_id_arelux'))
            arelux_automation_tc_prof_sale_orders_sms_template_id_both = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_prof_sale_orders_sms_template_id_both'))
            #retira_cliente
            arelux_automation_tc_prof_sale_orders_sms_template_id_retira_cliente_todocesped = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_prof_sale_orders_sms_template_id_retira_cliente_todocesped'))
            arelux_automation_tc_prof_sale_orders_sms_template_id_retira_cliente_arelux = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_prof_sale_orders_sms_template_id_retira_cliente_arelux'))
            arelux_automation_tc_prof_sale_orders_sms_template_id_retira_cliente_both = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_prof_sale_orders_sms_template_id_retira_cliente_both'))
            
            automation_log_ids = self.env['automation.log'].search([('model', '=', 'sale.order'),('category', '=', 'sale_order'),('action', '=', 'send_sms_done')])
            sale_order_ids_get_not_in = automation_log_ids.mapped('res_id')
            
            #confirmation_date
            confirmation_date_start = current_date + relativedelta(days=-5)
            confirmation_date_end = current_date + relativedelta(hours=-4)            
                    
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('state', 'in', ['sale', 'done']),
                    ('amount_total', '>', 0),
                    ('claim', '=', False),
                    ('ar_qt_customer_type', '=', 'profesional'),
                    ('create_date', '>', '2019-06-18 00:00:00'),
                    ('confirmation_date', '>', confirmation_date_start.strftime("%Y-%m-%d %H:%M:%S")),
                    ('confirmation_date', '<', confirmation_date_end.strftime("%Y-%m-%d %H:%M:%S")),
                    ('partner_id.mobile', '!=', False),
                    ('partner_id.mobile_code_res_country_id', '!=', False),
                    ('id', 'not in', sale_order_ids_get_not_in)                    
                 ]
            )
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    
                    if sale_order_id.carrier_id.id==6:#Fix retira_cliente
                        if sale_order_id.ar_qt_activity_type=='todocesped':
                            arelux_automation_tc_prof_sale_orders_sms_template_id = arelux_automation_tc_prof_sale_orders_sms_template_id_retira_cliente_todocesped
                        elif sale_order_id.ar_qt_activity_type=='arelux':
                            arelux_automation_tc_prof_sale_orders_sms_template_id = arelux_automation_tc_prof_sale_orders_sms_template_id_retira_cliente_arelux
                        else:
                            arelux_automation_tc_prof_sale_orders_sms_template_id = arelux_automation_tc_prof_sale_orders_sms_template_id_retira_cliente_both
                    else:                
                        if sale_order_id.ar_qt_activity_type=='todocesped':
                            arelux_automation_tc_prof_sale_orders_sms_template_id = arelux_automation_tc_prof_sale_orders_sms_template_id_todocesped
                        elif sale_order_id.ar_qt_activity_type=='arelux':
                            arelux_automation_tc_prof_sale_orders_sms_template_id = arelux_automation_tc_prof_sale_orders_sms_template_id_arelux
                        else:
                            arelux_automation_tc_prof_sale_orders_sms_template_id = arelux_automation_tc_prof_sale_orders_sms_template_id_both
                    
                    #send_sms
                    sale_order_id.action_send_sms_automatic(arelux_automation_tc_prof_sale_orders_sms_template_id, True)
                    #save_log
                    automation_log_vals = {                    
                        'model': 'sale.order',
                        'res_id': sale_order_id.id,
                        'category': 'sale_order',
                        'action': 'send_sms_done',                                                                                                                                                                                           
                    }
                    automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
                                
    @api.model    
    def cron_automation_todocesped_particular_sale_orders(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        #skip_cron
        skip_cron = True
        
        weekday = current_date.weekday()
        current_date_hour = current_date.strftime("%H")
                        
        hours_allow_by_weekday = {
            '0': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Lunes
            '1': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Martes
            '2': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Miercoles
            '3': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Jueves
            '4': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Viernes
            '5': ['11', '12', '13', '14'],#Sabado
        }

        if str(weekday) in hours_allow_by_weekday:
            hours_allow = hours_allow_by_weekday[str(weekday)]        
            if current_date_hour in hours_allow:            
                skip_cron = False                      
        
        if skip_cron==False:
            arelux_automation_tc_part_sale_orders_qty_from = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_qty_from'))            
            arelux_automation_tc_part_sale_orders_qty_to = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_qty_to'))
            arelux_automation_tc_part_sale_orders_hours_since_creation = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_hours_since_creation'))
            arelux_automation_tc_part_sale_orders_user_ids = self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_user_ids')                    
            arelux_automation_tc_part_sale_orders_team_id = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_team_id'))
            arelux_automation_tc_part_sale_orders_check_stage_id = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_check_stage_id'))
            arelux_automation_tc_part_sale_orders_change_stage_id = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_change_stage_id'))
            arelux_automation_tc_part_sale_orders_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_mail_template_id'))
            arelux_automation_tc_part_sale_orders_mail_template_id_less_15_m = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_mail_template_id_less_15_m'))            
            arelux_automation_tc_part_sale_orders_sms_template_id = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_sms_template_id'))            
            
            if ',' in arelux_automation_tc_part_sale_orders_user_ids:
                user_ids = arelux_automation_tc_part_sale_orders_user_ids.split(',')
            else:
                user_ids = [arelux_automation_tc_part_sale_orders_user_ids]                
                                                
            date_now_hours_diference = current_date + relativedelta(hours=-arelux_automation_tc_part_sale_orders_hours_since_creation)
            
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('state', '=', 'draft'),
                    ('amount_total', '>', 0),
                    ('team_id', '=', arelux_automation_tc_part_sale_orders_team_id),
                    ('claim', '=', False),
                    ('ar_qt_activity_type', '=', 'todocesped'),
                    ('ar_qt_customer_type', '=', 'particular'),
                    ('create_date', '>', '2019-03-15 00:00:00'),
                    ('create_date', '<', date_now_hours_diference.strftime("%Y-%m-%d %H:%M:%S")),
                    ('opportunity_id', '!=', False),
                    ('opportunity_id.active', '=', True),
                    ('opportunity_id.type', '=', 'opportunity'),                    
                    ('opportunity_id.probability', '>', 0),
                    ('opportunity_id.stage_id', '=', arelux_automation_tc_part_sale_orders_check_stage_id),
                    ('opportunity_id.lead_m2', '>=', arelux_automation_tc_part_sale_orders_qty_from),
                    ('opportunity_id.lead_m2', '<=', arelux_automation_tc_part_sale_orders_qty_to),
                    ('opportunity_id.user_id', '=', False)
                 ]
            )        
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    user_id_random = int(random.choice(user_ids))
                    #params
                    sale_order_params = {
                        'user_id': user_id_random,
                        'next_activity': False,                        
                        'mail_template_id': arelux_automation_tc_part_sale_orders_mail_template_id,
                        'sms_template_id': arelux_automation_tc_part_sale_orders_sms_template_id,
                        'lead_stage_id': arelux_automation_tc_part_sale_orders_change_stage_id
                    }                    
                    #Fix 15m
                    if sale_order_id.opportunity_id.lead_m2<15:
                        sale_order_params['mail_template_id'] = arelux_automation_tc_part_sale_orders_mail_template_id_less_15_m                                                                    
                    #automation_proces
                    sale_order_id.automation_proces(sale_order_params)                                                             
        
    @api.model    
    def cron_automation_todocesped_particular_sale_orders_mail2(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        #skip_cron
        skip_cron = True
        
        weekday = current_date.weekday()
        current_date_hour = current_date.strftime("%H")
                        
        hours_allow_by_weekday = {
            '0': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Lunes
            '1': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Martes
            '2': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Miercoles
            '3': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Jueves
            '4': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],#Viernes
            '5': ['11', '12', '13', '14', '15', '16'],#Sabado
        }

        if str(weekday) in hours_allow_by_weekday:
            hours_allow = hours_allow_by_weekday[str(weekday)]        
            if current_date_hour in hours_allow:            
                skip_cron = False                      
        
        if skip_cron==False:            
            arelux_automation_tc_part_sale_orders_mail2_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_sale_orders_mail2_mail_template_id'))
            #automation_log_ids_send_mail send_mail
            automation_log_ids_send_mail = self.env['automation.log'].search([('category', '=', 'sale_order'),('action', '=', 'send_mail')])        
            sale_order_ids_get_in = automation_log_ids_send_mail.mapped('res_id')
            #automation_log_ids_send_mail2 previously send_mail2
            automation_log_ids_send_mail2 = self.env['automation.log'].search([('category', '=', 'sale_order'),('action', '=', 'send_mail2')])
            sale_order_ids_get_not_in = automation_log_ids_send_mail2.mapped('res_id')
            #sale_orders
            current_date = datetime.today()
            date_order_management_filter = current_date + relativedelta(days=-2, minutes=-5)
            
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('state', '=', 'sent'),
                    ('claim', '=', False),
                    ('id', 'in', sale_order_ids_get_in),
                    ('id', 'not in', sale_order_ids_get_not_in),
                    ('date_order_management', '<=', date_order_management_filter.strftime("%Y-%m-%d %H:%M:%S")),
                    ('opportunity_id', '!=', False),
                    ('opportunity_id.probability', '>', 0),
                    ('opportunity_id.probability', '<', 100)                
                 ]
            )        
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    sale_order_id.action_sale_order_mail2(arelux_automation_tc_part_sale_orders_mail2_mail_template_id)
                    
    @api.model    
    def cron_automation_todocesped_particular_repaso_mail(self):
        _logger.info('cron_automation_todocesped_particular_repaso_mail')
        #def
        arelux_automation_tc_part_repaso_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('arelux_automation_tc_part_repaso_mail_template_id'))        
        current_date = datetime.today()
        shipping_expedition_date = current_date + relativedelta(days=-4)
        #leads
        total_items = 0
        crm_lead_ids = self.env['crm.lead'].search(
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
        #quizas limitar la consulta a 1000 puesto que si devuelve como ahora 11800 no dara tiempo en 30 minutos de odoo.conf
        if len(crm_lead_ids)>0:
            for crm_lead_id in crm_lead_ids:
                #sale.order
                sale_order_ids = self.env['sale.order'].search(
                    [
                        ('opportunity_id', '=', crm_lead_id.id),
                        ('claim', '=', False),
                        ('amount_total', '=', 0),
                        ('carrier_id.carrier_type', '=', 'nacex')                                        
                     ]
                )
                if len(sale_order_ids)>0:
                    sale_order_id = sale_order_ids[0]
                    #stock.picking (shipping.expedition)
                    stock_picking_ids = self.env['stock.picking'].search(
                        [
                            ('origin', '=', sale_order_id.name),
                            ('state', '=', 'done'),
                            ('carrier_id.carrier_type', '=', 'nacex'),
                            ('shipping_expedition_id', '!=', False),
                            ('shipping_expedition_id.state', '=', 'delivered'),
                            ('shipping_expedition_id.date', '<=', shipping_expedition_date.strftime("%Y-%m-%d"))                            
                        ]
                    )
                    if len(stock_picking_ids)>0:
                        #search opposite sale.order
                        sale_order_ids_operations = self.env['sale.order'].search(
                            [
                                ('opportunity_id', '=', crm_lead_id.id),
                                ('claim', '=', False),
                                ('amount_total', '>', 0),
                                ('state', '=', 'sent')                                        
                             ]
                        )
                        if len(sale_order_ids_operations)>0:
                            sale_order_id_operations = sale_order_ids_operations[0]
                            #send_mail (sale.order)
                            #change state_id (opportunity_id)
                            _logger.info('Operaciones del presupuesto '+str(sale_order_id_operations.name))
                            #automation_proces
                            '''
                            sale_order_id_operations.automation_proces({
                                'action_log': 'repaso_mail',
                                'mail_template_id': arelux_automation_tc_part_repaso_mail_template_id,
                                'lead_stage_id': 3#Repaso
                            })
                            '''
                            #total_items
                            total_items += 1
        #log total_items
        _logger.info('Total items aplicados '+str(total_items))                            
    
    @api.one
    def action_sale_order_mail2(self, template_id=False):
        need_send_mail = False        
        automation_log_ids = self.env['automation.log'].search([('category', '=', 'sale_order'),('action', '=', 'send_mail2'),('res_id', '=', self.id)])
        if len(automation_log_ids)==0:                    
            if self.claim==False and self.state=='sent' and self.amount_untaxed>0:
                current_date = datetime.today()
                date_order_management_filter = current_date + relativedelta(days=-2, minutes=-5)                        
                
                if self.date_order_management<=date_order_management_filter.strftime("%Y-%m-%d %H:%M:%S"):
                    need_send_mail = True
                    
                    date_order_management_check = datetime.strptime(self.date_order_management, "%Y-%m-%d %H:%M:%S") + relativedelta(minutes=5)                    
                    #1- Que no exista un email enviado por nosotros desde el flujo o pto > fecha gestion
                    if self.user_id.id>0:
                        mail_message_ids_sale_order_author_id_user_id = self.env['mail.message'].search(
                            [
                                ('model', '=', 'sale.order'),
                                ('res_id', '=', self.id),
                                ('subtype_id', '=', 1),
                                ('author_id', '=', self.user_id.partner_id.id),
                                ('date', '>', date_order_management_check.strftime("%Y-%m-%d %H:%M:%S"))                
                             ]
                        )
                        if len(mail_message_ids_sale_order_author_id_user_id)>0:
                            need_send_mail = False
                        
                        if self.opportunity_id.id>0 and need_send_mail==True:
                            mail_message_ids_crm_lead_author_id_user_id = self.env['mail.message'].search(
                                [
                                    ('model', '=', 'crm.lead'),
                                    ('res_id', '=', self.opportunity_id.id),
                                    ('subtype_id', '=', 1),
                                    ('author_id', '=', self.user_id.partner_id.id),
                                    ('date', '>', date_order_management_check.strftime("%Y-%m-%d %H:%M:%S"))                
                                 ]
                            )
                            if len(mail_message_ids_crm_lead_author_id_user_id)>0:
                                need_send_mail = False
                    #2- Que no exista un email creado por el cliente (author_id) > a la fecha gestion
                    if need_send_mail==True:
                        mail_message_ids_sale_order_author_id_partner_id = self.env['mail.message'].search(
                            [
                                ('model', '=', 'sale.order'),
                                ('res_id', '=', self.id),
                                ('author_id', '=', self.partner_id.id),
                                ('message_type', '=', 'email'),                                
                                ('date', '>', date_order_management_check.strftime("%Y-%m-%d %H:%M:%S"))                
                             ]
                        )
                        if len(mail_message_ids_sale_order_author_id_partner_id)>0:
                            need_send_mail = False                                    
                    #3- Que no exista ninguna llamada en el flujo > a la fecha gestion
                    if self.opportunity_id.id>0 and need_send_mail==True:
                        mail_message_ids_crm_lead_subtype_5 = self.env['mail.message'].search(
                            [
                                ('model', '=', 'crm.lead'),
                                ('res_id', '=', self.opportunity_id.id),
                                ('subtype_id', '=', 5),#Llamada
                                ('date', '>', date_order_management_check.strftime("%Y-%m-%d %H:%M:%S"))                
                             ]
                        )
                        if len(mail_message_ids_crm_lead_subtype_5)>0:
                            need_send_mail = False                                                    
        
        if need_send_mail==True:
            self.action_send_mail_with_template_id(template_id)
            #save_log
            automation_log_vals = {                    
                'model': 'sale.order',
                'res_id': self.id,
                'category': 'sale_order',
                'action': 'send_mail2',                                                                                                                                                                                           
            }
            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
                                        
    @api.one
    def action_send_mail_with_template_id(self, template_id=False):
        if template_id!=False:                                        
            mail_template_item = self.env['mail.template'].search([('id', '=', template_id)])[0]                                
            mail_compose_message_vals = {                    
                'author_id': self.user_id.partner_id.id,
                'record_name': self.name,                                                                                                                                                                                           
            }
            mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo(self.user_id.id).create(mail_compose_message_vals)
            return_onchange_template_id = mail_compose_message_obj.onchange_template_id(mail_template_item.id, 'comment', 'sale.order', self.id)

            mail_compose_message_obj_vals = {
                'author_id': mail_compose_message_vals['author_id'],
                'template_id': mail_template_item.id,
                'composition_mode': 'comment',
                'model': 'sale.order',
                'res_id': self.id,
                'body': return_onchange_template_id['value']['body'],
                'subject': return_onchange_template_id['value']['subject'],
                #'attachment_ids': return_onchange_template_id['value']['attachment_ids'],
                'record_name': mail_compose_message_vals['record_name'],
                'no_auto_thread': False,
            }
            # email_from
            if 'email_from' in return_onchange_template_id['value']:
                mail_compose_message_obj_vals['email_from'] = return_onchange_template_id['value']['email_from']
            #partner_ids
            if 'partner_ids' in return_onchange_template_id['value']:
                mail_compose_message_obj_vals['partner_ids'] = return_onchange_template_id['value']['partner_ids']
            #update
            mail_compose_message_obj.update(mail_compose_message_obj_vals)
            mail_compose_message_obj.send_mail_action()                                                                                                                
            return True