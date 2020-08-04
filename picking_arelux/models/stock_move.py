# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    name = fields.Char( 
        compute='_compute_name',
        string='Descripcion',
        store=False
    )
    qty_to_lot_id_domain = fields.Float( 
        compute='_compute_qty_to_lot_id_domain'
    )    
        
    @api.one        
    def _compute_name(self):
        for item in self:
            item.name = item.product_id.name

            if item.picking_id:
                if item.picking_id.sale_id:
                    for order_line in item.picking_id.sale_id.order_line:
                        if order_line.product_id.id == item.product_id.id:
                            item.name = order_line.name
                elif item.picking_id.purchase_id:
                    for order_line in item.picking_id.purchase_id.order_line:
                        if order_line.product_id.id == item.product_id.id:
                            item.name = order_line.name
                        
    @api.multi
    def _compute_qty_to_lot_id_domain(self):
        for item in self:
            if item.picking_id.picking_type_id.code in ['outgoing', 'internal']:
                # regenerate_stock_production_lot_product_qty_store
                item.product_id.regenerate_stock_production_lot_product_qty_store()
                # define
                item.qty_to_lot_id_domain = item.product_qty
            else:
                item.qty_to_lot_id_domain = -300