# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    prod_lot_id_ref = fields.Char(
        string='Referencia interna',
        related='prod_lot_id.ref',
        store=False,
        readonly=True
    )
