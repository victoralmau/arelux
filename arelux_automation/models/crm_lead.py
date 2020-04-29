# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.one
    def automation_proces(self, params):
        _logger.info('Aplicando automatizaciones del flujo')
        _logger.info(self.id)
        # example params
        '''
        params = {
            'action_log': 'custom_17_18_19_enero_2020',
            'user_id': 1,
            'next_activity': True,
            'next_activity_id': 3,
            'next_activity_date_action': '2020-01-01',
            'next_activity_title_action': 'Revisar flujo automatico',
            'mail_template_id': 133
            'lead_stage_id': 2
        }
        '''
        # special_log
        if 'action_log' in params:
            automation_log_vals = {
                'model': 'crm.lead',
                'res_id': self.id,
                'category': 'crm_lead',
                'action': str(params['action_log']),
            }
            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        # check_user_id crm_lead
        if 'user_id' in params:
            if self.user_id.id == 0:
                user_id_random = int(params['user_id'])
                #write
                self.write({
                    'user_id': user_id_random
                })
                # save_log
                automation_log_vals = {
                    'model': 'crm.lead',
                    'res_id': self.id,
                    'category': 'crm_lead',
                    'action': 'asign_user_id',
                }
                automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
                # fix change user_id res.partner
                if self.partner_id.user_id.id == 0:
                    self.partner_id.user_id = user_id_random
        # next_activity_id
        if 'next_activity' in params:
            if params['next_activity'] == True:
                self.write({
                    'next_activity_id': int(params['next_activity_id']),  # Tarea
                    'date_action': str(params['next_activity_date_action']),
                    'title_action': str(params['next_activity_title_action'])
                })
                # save_log
                automation_log_vals = {
                    'model': 'crm.lead',
                    'res_id': self.opportunity_id.id,
                    'category': 'crm_lead',
                    'action': 'assign_next_activity_id_' + str(params['next_activity_id']),
                }
                automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        # send_mail
        if 'mail_template_id' in params:
            self.action_send_mail_with_template_id(int(params['mail_template_id']))
            # save_log
            automation_log_vals = {
                'model': 'crm.lead',
                'res_id': self.id,
                'category': 'crm_lead',
                'action': 'send_mail',
            }
            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        # update crm.lead stage_id
        if 'lead_stage_id' in params:
            self.stage_id = int(params['lead_stage_id'])
            # save_log
            automation_log_vals = {
                'model': 'crm.lead',
                'res_id': self.id,
                'category': 'crm_lead',
                'action': 'change_stage_id',
            }
            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)

    @api.one
    def action_send_mail_with_template_id(self, template_id=False):
        if template_id!=False:
            mail_template_item = self.env['mail.template'].browse(template_id)
            mail_compose_message_vals = {                    
                'author_id': 1,
                'record_name': self.name,                                                                                                                                                                                           
            }
            #Fix user_id
            if self.user_id.id>0:
                mail_compose_message_vals['author_id'] = self.user_id.partner_id.id
                mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo(self.user_id.id).create(mail_compose_message_vals)
            else:
                mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo().create(mail_compose_message_vals)

            return_onchange_template_id = mail_compose_message_obj.onchange_template_id(mail_template_item.id, 'comment', 'crm.lead', self.id)
            #mail_compose_message_obj_vals
            mail_compose_message_obj_vals = {
                'author_id': mail_compose_message_vals['author_id'],
                'template_id': mail_template_item.id,
                'composition_mode': 'comment',
                'model': 'crm.lead',
                'res_id': self.id,
                'body': return_onchange_template_id['value']['body'],
                'subject': return_onchange_template_id['value']['subject'],
                # 'attachment_ids': return_onchange_template_id['value']['attachment_ids'],
                'record_name': mail_compose_message_vals['record_name'],
                'no_auto_thread': False,
            }
            # partner_ids
            if 'email_from' in return_onchange_template_id['value']:
                mail_compose_message_obj_vals['email_from'] = return_onchange_template_id['value']['email_from']
            #partner_ids
            if 'partner_ids' in return_onchange_template_id['value']:
                mail_compose_message_obj_vals['partner_ids'] = return_onchange_template_id['value']['partner_ids']
            #update
            mail_compose_message_obj.update(mail_compose_message_obj_vals)
            #send_mail_action
            mail_compose_message_obj.send_mail_action()
            #return
            return True

    @api.multi    
    def cron_automation_todocesped_profesional_potenciales(self, cr=None, uid=False, context=None):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        tomorrow_date = current_date + relativedelta(days=+1)                
        
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
        if res_partner_ids!=False:            
            res_partner_ids_potencial = []
            for res_partner_id in res_partner_ids:
                if res_partner_id.ref!=False:                    
                    res_partner_ids_potencial.append(res_partner_id.id)
                    partners[res_partner_id.id] = res_partner_id                                    
            #account_invoice
            account_invoice_ids = self.env['account.invoice'].search(
                [
                    ('state', 'in', ('open','paid')),
                    ('amount_total', '>', 0),
                    ('type', '=', 'out_invoice'),
                    ('partner_id', 'in', res_partner_ids_potencial)
                 ]
            )            
            if account_invoice_ids!=False:
                for account_invoice_id in account_invoice_ids:
                    if account_invoice_id.partner_id.id in res_partner_ids_potencial:
                        res_partner_ids_potencial.remove(account_invoice_id.partner_id.id)
            
            if res_partner_ids_potencial!=False:                                    
                #crm_lead_6_months
                start_date = current_date + relativedelta(months=-6)
                end_date = current_date
                
                for res_partner_id_potencial in res_partner_ids_potencial:
                    partner_item = partners[res_partner_id_potencial]
                                    
                    crm_activity_report_ids = self.env['crm.activity.report'].search(
                        [
                            ('subtype_id', 'in', (1,2,4)),
                            ('partner_id', '=', partner_item.id),
                            ('lead_id', '!=', False),
                            ('date', '>=', start_date.strftime("%Y-%m-%d")),
                            ('date', '<=', end_date.strftime("%Y-%m-%d"))
                         ]
                    )
                    if len(crm_activity_report_ids)==0:
                        crm_lead_ids = self.env['crm.lead'].search(
                            [
                                ('active', '=', True),
                                ('probability', '<', 100),
                                ('partner_id', '=', partner_item.id),                                
                                ('ar_qt_activity_type', '=', partner_item.ar_qt_activity_type),
                                ('ar_qt_customer_type', '=', partner_item.ar_qt_customer_type),                                
                             ]
                        )
                        if len(crm_lead_ids)>0:
                            for crm_lead_id in crm_lead_ids:
                                change_next_activity = True
                                if crm_lead_id.next_activity_id!=False and crm_lead_id.date_action!=False and crm_lead_id.date_action>current_date.strftime("%Y-%m-%d"):
                                    change_next_activity = False
                                
                                if change_next_activity==True:
                                    crm_lead_id.next_activity_id = 1#Email
                                    crm_lead_id.date_action = tomorrow_date.strftime("%Y-%m-%d")
                                    crm_lead_id.title_action = 'Email potencial'
                        else:
                            #Auto-create lead                                                        
                            crm_lead_vals = {
                                'active': True,                                
                                'type': 'opportunity',
                                'stage_id': 1,
                                'name': partner_item.name,
                                'partner_id': partner_item.id,
                                'ar_qt_activity_type': partner_item.ar_qt_activity_type,
                                'ar_qt_customer_type': partner_item.ar_qt_customer_type,
                                'user_id': partner_item.user_id.id,
                                'next_activity_id': 1,#Email
                                'date_action': tomorrow_date.strftime("%Y-%m-%d"),
                                'create_date': current_date,
                                'title_action': 'Email potencial'                                                                  
                            }
                            crm_lead_obj = self.env['crm.lead'].sudo(partner_item.user_id.id).create(crm_lead_vals)
                            crm_lead_obj._onchange_partner_id()
        
    @api.multi    
    def cron_automation_todocesped_profesional_potenciales_activo(self, cr=None, uid=False, context=None):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        tomorrow_date = current_date + relativedelta(days=+1)                                                                                                                                                                                                                          
        
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
        if res_partner_ids!=False:
            res_partner_ids_potencial_activo = []
            for res_partner_id in res_partner_ids:                    
                res_partner_ids_potencial_activo.append(res_partner_id.id)
                partners[res_partner_id.id] = res_partner_id                    
            #account_invoice
            account_invoice_ids = self.env['account.invoice'].search(
                [
                    ('state', 'in', ('open','paid')),
                    ('amount_total', '>', 0),
                    ('type', '=', 'out_invoice'),
                    ('partner_id', 'in', res_partner_ids_potencial_activo)
                 ]
            )                            
            if account_invoice_ids!=False:
                for account_invoice_id in account_invoice_ids:
                    if account_invoice_id.partner_id.id in res_partner_ids_potencial_activo:
                        res_partner_ids_potencial_activo.remove(account_invoice_id.partner_id.id)
            
            if res_partner_ids_potencial_activo!=False:
                #crm_lead_3_months
                start_date = current_date + relativedelta(months=-3)
                end_date = current_date
                
                for res_partner_id_potencial_activo in res_partner_ids_potencial_activo:
                    partner_item = partners[res_partner_id_potencial_activo]
                    
                    crm_activity_report_ids = self.env['crm.activity.report'].search(
                        [
                            ('subtype_id', 'in', (1,2,4)),
                            ('partner_id', '=', partner_item.id),
                            ('lead_id', '!=', False),
                            ('date', '>=', start_date.strftime("%Y-%m-%d")),
                            ('date', '<=', end_date.strftime("%Y-%m-%d"))
                         ]
                    )
                    if len(crm_activity_report_ids)==0:
                        crm_lead_ids = self.env['crm.lead'].search(
                            [
                                ('active', '=', True),
                                ('probability', '<', 100),
                                ('partner_id', '=', partner_item.id),                                
                                ('ar_qt_activity_type', '=', partner_item.ar_qt_activity_type),
                                ('ar_qt_customer_type', '=', partner_item.ar_qt_customer_type),
                             ]
                        )
                        if len(crm_lead_ids)>0:
                            for crm_lead_id in crm_lead_ids:
                                change_next_activity = True
                                if crm_lead_id.next_activity_id!=False and crm_lead_id.date_action!=False and crm_lead_id.date_action>current_date.strftime("%Y-%m-%d"):
                                    change_next_activity = False
                                
                                if change_next_activity==True:
                                    crm_lead_id.next_activity_id = 2#Llamada
                                    crm_lead_id.date_action = tomorrow_date.strftime("%Y-%m-%d")
                                    crm_lead_id.title_action = 'Llamada potencial activo'
                        else:
                            #Auto-create lead                                                        
                            crm_lead_vals = {
                                'active': True,                                
                                'type': 'opportunity',
                                'stage_id': 1,
                                'name': partner_item.name,
                                'partner_id': partner_item.id,
                                'ar_qt_activity_type': partner_item.ar_qt_activity_type,
                                'ar_qt_customer_type': partner_item.ar_qt_customer_type,
                                'user_id': partner_item.user_id.id,
                                'next_activity_id': 2,#Llamada
                                'date_action': tomorrow_date.strftime("%Y-%m-%d"),
                                'create_date': current_date,
                                'title_action': 'Llamada potencial activo'                                                                  
                            }
                            crm_lead_obj = self.env['crm.lead'].sudo(partner_item.user_id.id).create(crm_lead_vals)
                            crm_lead_obj._onchange_partner_id()
                            
    @api.multi    
    def cron_automation_todocesped_profesional_puntuales(self, cr=None, uid=False, context=None):
        _logger.info('cron_automation_todocesped_profesional_puntuales')
        
    @api.multi    
    def cron_automation_todocesped_profesional_recurrentes(self, cr=None, uid=False, context=None):
        _logger.info('cron_automation_todocesped_profesional_recurrentes')
        
    @api.multi    
    def cron_automation_todocesped_profesional_fidelizados(self, cr=None, uid=False, context=None):
        _logger.info('cron_automation_todocesped_profesional_fidelizados')                

    @api.multi    
    def cron_automation_todocesped_profesional(self, cr=None, uid=False, context=None):
        #potenciales
        #self.cron_automation_todocesped_profesional_potenciales()
        #potenciales_activo
        #self.cron_automation_todocesped_profesional_potenciales_activo()
        #puntuales
        #self.cron_automation_todocesped_profesional_puntuales()
        #recurrentes
        #self.cron_automation_todocesped_profesional_recurrentes()
        #fidelizados
        #self.cron_automation_todocesped_profesional_fidelizados()
        _logger.info('cron_automation_todocesped_profesional')                                                                                                              