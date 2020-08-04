# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_survey_id(self):
        survey_id = 0
        if self.ar_qt_activity_type and self.partner_id.ar_qt_customer_type:
            survey_ids = self.env['survey.survey'].search(
                [
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type),
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type),
                    ('survey_type', '=', 'popup'),
                    ('survey_subtype', '=', 'why_not'),
                    ('active', '=', True)
                ]
            )
            if survey_ids:
                survey_id = survey_ids[0].id
                    
        return survey_id