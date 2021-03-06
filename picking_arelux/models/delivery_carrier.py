# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    _order = 'position'

    position = fields.Integer(
        string='Position'
    )
