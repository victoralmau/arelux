# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerSage(models.Model):
    _inherit = 'res.partner'
           
    installer = fields.Boolean(
        string="Installer"
    )                                       