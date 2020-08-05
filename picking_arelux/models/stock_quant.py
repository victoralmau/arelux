# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    lot_ref = fields.Char(
        string='Referencia interna',
        compute='_compute_lot_ref',
        store=False
    )

    @api.multi
    def _compute_lot_ref(self):
        for item in self:
            item.lot_ref = item.lot_id.ref
