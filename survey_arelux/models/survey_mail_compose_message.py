# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import _, api, exceptions, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime

import urlparse
import logging
import uuid
import pytz

_logger = logging.getLogger(__name__)

class SurveyMailComposeMessage(models.TransientModel):
    _inherit = 'survey.mail.compose.message'    
    
    @api.one
    def arelux_create_survey_user_input_log(self, survey_user_input):
        return False
                
    @api.one    
    def arelux_send_partner_mails(self, partner_ids_orders, cr=None, uid=False, context=None):
        def create_survey_user_input(survey_survey, partner, order_id):
            response_ids = self.env['survey.user_input'].search([
                ('survey_id', '=', survey_survey.id), 
                ('state', 'in', ['new', 'skip']),                
                ('order_id', '=', order_id.id),
                 '|', 
                 ('partner_id', '=', partner.id), 
                 ('email', '=', partner.email)]
            )
            if response_ids:
                return response_ids[0]
                
            token = uuid.uuid4().__str__()            
            # create response with token
            survey_user_input_vals = {
                'survey_id': survey_survey.id,
                'date_create': datetime.now(),
                'type': 'link',
                'state': 'new',
                'token': token,
                'order_id': order_id.id,
                'user_id': order_id.user_id.id,
                'installer_id': order_id.installer_id.id,
                'partner_id': partner.id,
                'email': partner.email                                                                                                                                                                      
            }
            #deadline
            if survey_survey.deadline_days>0:
                current_date = datetime.now(pytz.timezone('Europe/Madrid'))
                deadline = current_date + relativedelta(days=survey_survey.deadline_days)
                survey_user_input_vals['deadline'] = deadline
            #survey_user_input_obj                                    
            survey_user_input_obj = self.env['survey.user_input'].sudo().create(survey_user_input_vals)                        
            return survey_user_input_obj            
            
        def create_response_and_send_mail(survey_mail_compose_message, survey_user_input):
            """ Create one mail by recipients and replace __URL__ by link with identification token """
            #url
            url = str(survey_user_input.survey_id.public_url)+'/'+str(survey_user_input.token)

            mail_mail_vals = {
                'auto_delete': True,
                'model': 'survey.user_input',
                'res_id': survey_user_input.id,                     
                'subject': self.subject,
                'body': survey_mail_compose_message.body.replace("__URL__", url),
                'body_html': survey_mail_compose_message.body.replace("__URL__", url),
                'record_name': survey_user_input.survey_id.title,
                'no_auto_thread': False,
                'reply_to': survey_mail_compose_message.reply_to,
                'message_type': 'email',
                'email_from': survey_mail_compose_message.email_from,
                'email_to': survey_user_input.partner_id.email,
                'partner_ids': survey_user_input.partner_id.id and [(4, survey_user_input.partner_id.id)] or None                                                                                                                                                                       
            }
            mail_mail_obj = self.env['mail.mail'].sudo().create(mail_mail_vals)
            mail_mail_obj.send()            
            self.action_send_survey_mail_message_slack(survey_user_input)#Fix Slack
            
        
        survey_survey_ids = self.env['survey.survey'].search([('id', '=', str(self.survey_id.id))])
        survey_survey_id = survey_survey_ids[0]
                            
        for partner_id in self.partner_ids:
            for order_id in partner_ids_orders[partner_id.id]:                        
                survey_user_input = create_survey_user_input(survey_survey_id, partner_id, order_id)
                create_response_and_send_mail(self, survey_user_input)
                self.arelux_create_survey_user_input_log(survey_user_input)#Fix log                          