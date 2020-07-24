# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SurveyMailComposeMessage(models.TransientModel):
    _inherit = 'survey.mail.compose.message'    
    
    @api.one
    def arelux_create_survey_user_input_log(self, survey_user_input):
        vals = {
            'model': 'survey.user_input',
            'res_id': survey_user_input.id,
            'category': 'survey_user_input',
            'action': 'send_mail',                                                                                                                                                                                           
        }
        self.env['automation.log'].sudo().create(vals)