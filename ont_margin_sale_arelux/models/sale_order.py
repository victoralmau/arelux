# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import decimal

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
            
    @api.one
    def action_regenerate_purchase_prices(self):
        if (self.state=='sale' or self.state=='done'):
            order_lines = {}
            for order_line in self.order_line:
                order_lines[order_line.product_id.id] = {
                    'is_delivery': order_line.is_delivery,                          
                    'purchase_price': 0,
                    'standard_price': order_line.product_id.standard_price,                     
                }
            #picking_ids                        
            if self.picking_ids!=False:
                for picking_id in self.picking_ids:
                    if picking_id.state=='done':                        
                        if picking_id.move_lines!=False:
                            for move_line in picking_id.move_lines:
                                if move_line.quant_ids!=False:
                                    for quant_id in move_line.quant_ids:
                                        #cost
                                        if quant_id.cost>0:
                                            order_lines[move_line.product_id.id]['purchase_price'] = quant_id.cost
                                        else: 
                                            order_lines[move_line.product_id.id]['purchase_price'] = (quant_id.inventory_value/quant_id.qty)
            #operations                                                    
            for order_line_key in order_lines:
                if order_lines[order_line_key]['is_delivery']==False:
                    if order_lines[order_line_key]['purchase_price']==0:
                        order_lines[order_line_key]['purchase_price'] = order_lines[order_line_key]['standard_price']
            #operations2
            margin_order = 0                    
            for order_line in self.order_line:
                #Fix Mer4
                if order_line.product_id.id!=277:
                    order_line.purchase_price = order_lines[order_line.product_id.id]['purchase_price']
                    #margin_line
                    margin_line = 0
                    #margin (qty delivered if not qty_invoiced)
                    if self.invoice_status=='invoiced':
                        margin_line = order_line.price_subtotal - (order_line.purchase_price * order_line.qty_invoiced)
                    elif self.invoice_status=='no':
                        if order_line.qty_delivered>0:
                            margin_line = order_line.price_subtotal - (order_line.purchase_price * order_line.qty_delivered)
                    #define                        
                    order_line.margin = "{:.2f}".format(margin_line)
                    #action_calculate_margin_percent
                    order_line.action_calculate_margin_percent()
                    #margin_order
                    margin_order += order_line.margin            
            #margin                    
            self.margin = "{:.2f}".format(margin_order)
            #action_calculate_margin_percent
            self.action_calculate_margin_percent()
            #invoices
            if self.invoice_ids!=False:
                for invoice_id in self.invoice_ids:
                    #action_regenerate_margin
                    invoice_id.action_regenerate_margin()                        