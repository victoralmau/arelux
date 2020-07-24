# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'                
                
    @api.one    
    def regenerate_stock_production_lot_product_qty_store(self):
        stock_production_lot_ids = self.env['stock.production.lot'].sudo().search(
            [
                ('product_id', '=', self.id)
            ]
        )
        if stock_production_lot_ids:
            for stock_production_lot_id in stock_production_lot_ids:                
                stock_quant_quantity_sum = 0 
                # stock_quant
                stock_quant_ids = self.env['stock.quant'].sudo().search(
                    [
                        ('product_id', '=', stock_production_lot_id.product_id.id),
                        ('lot_id', '=', stock_production_lot_id.id),
                        ('location_id.usage', '=', 'internal')
                    ]
                )                                
                if stock_quant_ids:
                    for stock_quant_id in stock_quant_ids:
                        stock_quant_quantity_sum += stock_quant_id.qty                        
                # write
                stock_production_lot_id.sudo().write({
                    'product_qty_store': stock_quant_quantity_sum
                })                           