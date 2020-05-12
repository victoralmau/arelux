# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models
from datetime import datetime

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    date_invoice_send_mail = fields.Datetime(
        string='Fecha envio email' 
    )
    
    @api.one    
    def action_custom_send_mail_slack(self):
        return True
    
    @api.one 
    def cron_account_invoice_auto_send_mail_item(self):
        if self.type=='out_invoice' and self.date_invoice_send_mail==False and (self.state=='open' or self.state=='paid'):
            current_date = fields.Datetime.from_string(str(datetime.today().strftime("%Y-%m-%d")))
            days_difference = (current_date - fields.Datetime.from_string(self.date_invoice)).days
            if days_difference>=3:        
                account_invoice_auto_send_mail_author_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_author_id'))
                
                if self.ar_qt_activity_type=='arelux':
                    account_invoice_auto_send_mail_customer_activity_type_arelux_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_arelux_template_id'))
                    mail_template_item = self.env['mail.template'].search([('id', '=', account_invoice_auto_send_mail_customer_activity_type_arelux_template_id)])[0]
                elif self.ar_qt_activity_type=='todocesped':
                    account_invoice_auto_send_mail_customer_activity_type_todocesped_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_todocesped_template_id'))
                    mail_template_item = self.env['mail.template'].search([('id', '=', account_invoice_auto_send_mail_customer_activity_type_todocesped_template_id)])[0]
                elif self.ar_qt_activity_type=='evert':
                    account_invoice_auto_send_mail_customer_activity_type_evert_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_evert_template_id'))
                    mail_template_item = self.env['mail.template'].search([('id', '=', account_invoice_auto_send_mail_customer_activity_type_evert_template_id)])[0]
                elif self.ar_qt_activity_type=='both':
                    account_invoice_auto_send_mail_customer_activity_type_both_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_both_template_id'))
                    mail_template_item = self.env['mail.template'].search([('id', '=', account_invoice_auto_send_mail_customer_activity_type_both_template_id)])[0]
                else:
                    account_invoice_auto_send_mail_customer_activity_type_none_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_none_template_id'))
                    mail_template_item = self.env['mail.template'].search([('id', '=', account_invoice_auto_send_mail_customer_activity_type_none_template_id)])[0]                
                    
                mail_compose_message_vals = {                    
                    'author_id': account_invoice_auto_send_mail_author_id,
                    'record_name': self.number,                                                                                                                                                                                           
                }
                mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo().create(mail_compose_message_vals)
                return_onchange_template_id = mail_compose_message_obj.onchange_template_id(mail_template_item.id, 'comment', 'account.invoice', self.id)
                                
                mail_compose_message_obj.update({
                    'author_id': account_invoice_auto_send_mail_author_id,
                    'template_id': mail_template_item.id,                    
                    'composition_mode': 'comment',                    
                    'model': 'account.invoice',
                    'res_id': self.id,
                    'body': return_onchange_template_id['value']['body'],
                    'subject': return_onchange_template_id['value']['subject'],
                    'email_from': return_onchange_template_id['value']['email_from'],
                    'attachment_ids': return_onchange_template_id['value']['attachment_ids'],                    
                    'record_name': self.number,
                    'no_auto_thread': False,                     
                })                                                   
                mail_compose_message_obj.send_mail_action()
                #save_log
                automation_log_vals = {                    
                    'model': 'account.invoice',
                    'res_id': self.id,
                    'category': 'account_invoice',
                    'action': 'send_mail',                                                                                                                                                                                           
                }
                automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
                #other                                                
                self.date_invoice_send_mail = datetime.today()
                self.action_custom_send_mail_slack()#Fix Slack
        
    @api.model    
    def cron_account_invoice_auto_send_mail(self):                                          
        account_invoice_ids = self.env['account.invoice'].search(
            [
                ('state', 'in', ('open', 'paid')), 
                ('type', 'in', ('out_invoice', 'out_refund')),
                ('date_invoice_send_mail', '=', False)
             ]
        )        
        if account_invoice_ids!=False:            
            for account_invoice_id in account_invoice_ids:
                account_invoice_id.cron_account_invoice_auto_send_mail_item()                                                                                                                                                                                         