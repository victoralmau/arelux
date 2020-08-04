# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
                
    product_qty_store = fields.Float(     
        string='Cantidad Store'
    )
    
    @api.model
    def create(self, vals):
        return_object = super(StockProductionLot, self).create(vals)
        return_object.product_qty_store = 0
        # return
        return return_object
    
    @api.model
    def cron_odoo_stock_production_lot_product_qty_store(self):
        lot_ids = self.env['stock.production.lot'].search(
            [
                ('id', '>', 0)
            ]
        )
        if lot_ids:
            product_ids = lot_ids.mapped('product_id')
            if product_ids:
                for product_id in product_ids:
                    product_id.regenerate_stock_production_lot_product_qty_store()
