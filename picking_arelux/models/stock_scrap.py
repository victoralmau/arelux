# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    cost = fields.Float(
        compute='_compute_cost',
        string='Coste',
        store=False
    )

    @api.multi
    def _compute_cost(self):
        for item in self:
            item.cost = 0
            if item.move_id:
                for quant_id in item.move_id.quant_ids:
                    if quant_id.cost > 0:
                        item.cost += (quant_id.cost*item.scrap_qty)
                    else:
                        item.cost += (quant_id.inventory_value/item.scrap_qty)
