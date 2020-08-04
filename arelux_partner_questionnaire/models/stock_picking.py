# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, fields
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
        
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),            
            ('both', 'Ambos'),        
        ],
        size=15, 
        string='Tipo de actividad'
    )
    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),        
        ],        
        string='Tipo de cliente',
    )
    
    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        
        res.ar_qt_activity_type = 'todocesped'
        res.ar_qt_customer_type = 'particular'
        
        if res.partner_id:
            res.ar_qt_activity_type = res.partner_id.ar_qt_activity_type
            res.ar_qt_customer_type = res.partner_id.ar_qt_customer_type
        
        if res.origin != "":
            origin_find = False
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('name', '=', return_stock_picking.origin)                    
                ]
            )
            for sale_order_id in sale_order_ids:
                res.ar_qt_activity_type = sale_order_id.ar_qt_activity_type
                res.ar_qt_customer_type = sale_order_id.ar_qt_customer_type
                
                origin_find = True
            
            if not origin_find:
                stock_picking_ids = self.env['stock.picking'].search(
                    [
                        ('name', '=', return_stock_picking.origin)                    
                    ]
                )
                for stock_picking_id in stock_picking_ids:
                    res.ar_qt_activity_type = stock_picking_id.ar_qt_activity_type
                    res.ar_qt_customer_type = stock_picking_id.ar_qt_customer_type
                    
                    origin_find = True                                                    
                    
        return res
