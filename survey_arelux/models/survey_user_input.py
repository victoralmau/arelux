# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SurveyUserinput(models.Model):
    _inherit = 'survey.user_input'
    _transient = False

    installer_id = fields.Many2one(
        comodel_name='res.partner',
        domain="[('installer', '=', True)]",        
        string='Instalador'
    )
    lead_id_evert_create = fields.Many2one(
        comodel_name='crm.lead',        
        string='Lead Id Evert'
    )
    
    @api.multi
    def action_generate_lead_evert_slack(self):
        self.ensure_one()
        return super(SurveyUserinput, self).action_generate_lead_evert_slack()
    
    @api.model
    def create(self, values):                    
        return_object = super(SurveyUserinput, self).create(values)
        # installer_id
        if self.lead_id:
            for order_id in self.lead_id.order_ids:
                if order_id.amount_total > 0:
                    if order_id.installer_id:
                        self.installer_id = order_id.installer_id.id
        # return
        return return_object
