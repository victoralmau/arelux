# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    @api.multi
    @api.onchange('user_id')
    def _onchange_user(self):
        for item in self:
            if item.user_id:
                team_id_old = item.team_id
                super(Lead2OpportunityPartner, self)._onchange_user()
                item.team_id = team_id_old
