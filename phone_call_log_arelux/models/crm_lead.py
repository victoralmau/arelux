# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    is_revision = fields.Boolean(
        string='Is revision?',
        default=False,
        readonly=True
    )
