# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    lot_ref = fields.Char(
        string='Referencia interna',
        related='lot_id.ref',
        store=False,
        readonly=True
    )
