# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _


class SurveyMailComposeMessage(models.TransientModel):
    _inherit = 'survey.mail.compose.message'

    @api.multi
    def action_send_survey_mail_message_slack(self,
                                              user_input
                                              ):
        self.ensure_one()
        attachments = [
            {
                "title": _('The survey has been automatically sent by email'),
                "text": user_input.survey_id.title,
                "color": "#36a64f",
                "fields": [
                    {
                        "title": _('Customer'),
                        "value": '%s (%s - %s)' % (
                            user_input.partner_id.name,
                            user_input.order_id.ar_qt_activity_type.title(),
                            user_input.order_id.ar_qt_customer_type.title()
                        ),
                        'short': True,
                    },
                    {
                        "title": _('Order'),
                        "value": user_input.order_id.name,
                        'short': True,
                    }
                ],
            }
        ]
        vals = {
            'attachments': attachments,
            'model': 'survey.user_input',
            'res_id': user_input.id,
            'channel': self.env['ir.config_parameter'].sudo().get_param(
                'slack_log_calidad_channel'
            ),
        }
        self.env['slack.message'].sudo().create(vals)
