# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, exceptions, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import uuid
import pytz
_logger = logging.getLogger(__name__)

class SurveyMailComposeMessage(models.TransientModel):
    _inherit = 'survey.mail.compose.message'    
    
    @api.multi
    def arelux_create_survey_user_input_log(self, survey_user_input):
        self.ensure_one()
        return False
                
    @api.multi
    def arelux_send_partner_mails(self, partner_ids_orders, cr=None, uid=False, context=None):
        self.ensure_one()
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
            vals = {
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
            # deadline
            if survey_survey.deadline_days > 0:
                current_date = datetime.now(pytz.timezone('Europe/Madrid'))
                deadline = current_date + relativedelta(
                    days=survey_survey.deadline_days
                )
                vals['deadline'] = deadline
            # survey_user_input_obj
            return self.env['survey.user_input'].sudo().create(vals)
            
        def create_response_and_send_mail(smcm, survey_user_input):
            #url
            url = '%s/%s' % (
                survey_user_input.survey_id.public_url,
                survey_user_input.token
            )
            vals = {
                'auto_delete': True,
                'model': 'survey.user_input',
                'res_id': survey_user_input.id,                     
                'subject': self.subject,
                'body': smcm.body.replace("__URL__", url),
                'body_html': smcm.body.replace("__URL__", url),
                'record_name': survey_user_input.survey_id.title,
                'no_auto_thread': False,
                'reply_to': smcm.reply_to,
                'message_type': 'email',
                'email_from': smcm.email_from,
                'email_to': survey_user_input.partner_id.email,
                'partner_ids': survey_user_input.partner_id.id and [(4, survey_user_input.partner_id.id)] or None                                                                                                                                                                       
            }
            mail_mail_obj = self.env['mail.mail'].sudo().create(vals)
            mail_mail_obj.send()            
            self.action_send_survey_mail_message_slack(
                survey_user_input
            )
            
        
        survey_ids = self.env['survey.survey'].search(
            [
                ('id', '=', self.survey_id.id)
            ]
        )
        if survey_ids:
            survey_id = survey_ids[0]
                            
            for partner_id in self.partner_ids:
                for order_id in partner_ids_orders[partner_id.id]:
                    survey_user_input = create_survey_user_input(
                        survey_id,
                        partner_id,
                        order_id
                    )
                    create_response_and_send_mail(self, survey_user_input)
                    self.arelux_create_survey_user_input_log(survey_user_input)
