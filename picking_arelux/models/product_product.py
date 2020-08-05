# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def regenerate_stock_production_lot_product_qty_store(self):
        for item in self:
            lot_ids = self.env['stock.production.lot'].sudo().search(
                [
                    ('product_id', '=', self.id)
                ]
            )
            if lot_ids:
                for lot_id in lot_ids:
                    stock_quant_quantity_sum = 0
                    # stock_quant
                    quant_ids = self.env['stock.quant'].sudo().search(
                        [
                            ('product_id', '=', lot_id.product_id.id),
                            ('lot_id', '=', lot_id.id),
                            ('location_id.usage', '=', 'internal')
                        ]
                    )
                    if quant_ids:
                        for quant_id in quant_ids:
                            stock_quant_quantity_sum += quant_id.qty
                    # write
                    lot_id.sudo().write({
                        'product_qty_store': stock_quant_quantity_sum
                    })
