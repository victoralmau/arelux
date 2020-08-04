# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'

    ar_qt_activity_type = fields.Selection(
        related='picking_id.ar_qt_activity_type',
        string='Tipo de actividad',
        readonly=True
    )
    ar_qt_customer_type = fields.Selection(
        related='picking_id.ar_qt_customer_type',
        string='Tipo de cliente',
        readonly=True
    )
