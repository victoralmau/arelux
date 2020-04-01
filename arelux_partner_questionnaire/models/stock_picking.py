# -*- coding: utf-8 -*-
from openerp import api, models, fields

import logging
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
        return_stock_picking = super(StockPicking, self).create(vals)
        
        return_stock_picking.ar_qt_activity_type = 'todocesped'
        return_stock_picking.ar_qt_customer_type = 'particular'
        
        if return_stock_picking.partner_id.id>0:
            return_stock_picking.ar_qt_activity_type = return_stock_picking.partner_id.ar_qt_activity_type
            return_stock_picking.ar_qt_customer_type = return_stock_picking.partner_id.ar_qt_customer_type
        
        if return_stock_picking.origin!="":
            origin_find = False
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('name', '=', return_stock_picking.origin)                    
                ]
            )
            for sale_order_id in sale_order_ids:
                return_stock_picking.ar_qt_activity_type = sale_order_id.ar_qt_activity_type
                return_stock_picking.ar_qt_customer_type = sale_order_id.ar_qt_customer_type
                
                origin_find = True
            
            if origin_find==False:
                stock_picking_ids = self.env['stock.picking'].search(
                    [
                        ('name', '=', return_stock_picking.origin)                    
                    ]
                )
                for stock_picking_id in stock_picking_ids:
                    return_stock_picking.ar_qt_activity_type = stock_picking_id.ar_qt_activity_type
                    return_stock_picking.ar_qt_customer_type = stock_picking_id.ar_qt_customer_type
                    
                    origin_find = True                                                    
                    
        return return_stock_picking                                                                           