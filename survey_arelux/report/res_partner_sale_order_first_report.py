# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools

import logging
_logger = logging.getLogger(__name__)

class ResPartnerSaleOrderFirstReport(models.Model):
    _name = 'res.partner.sale.order.first.report'
    _auto = False
    _description = "Res Partner Sale Order First Report"
    _rec_name = 'id'
    
    partner_id = fields.Many2one(
        'res.partner', 
        string='Res Partner'
    )
    order_id = fields.Many2one(
        'sale.order', 
        string='Sale Order'
    )
    confirmation_date = fields.Datetime('Confirmation date', readonly=True)
    date_done_picking = fields.Datetime('Date done picking', readonly=True)        
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'res_partner_sale_order_first_report')
        self._cr.execute("""
            CREATE VIEW res_partner_sale_order_first_report AS (
                SELECT 
                so.partner_invoice_id AS id,  
                so.partner_invoice_id AS partner_id,  
                MAX(so_1.confirmation_date) AS confirmation_date,
                MIN(so_1_1.order_id) AS order_id,
                MAX(sp_order_1.date_done) AS date_done_picking
                FROM sale_order AS so
                LEFT JOIN (
                 	SELECT so2.partner_invoice_id, MIN(so2.confirmation_date) AS confirmation_date
                 	FROM sale_order AS so2
                 	WHERE so2.claim = FALSE AND so2.amount_untaxed > 0 AND state in ('sale', 'done')
                 	GROUP BY so2.partner_invoice_id
                 ) AS so_1 ON so_1.partner_invoice_id = so.partner_invoice_id
                 LEFT JOIN (
                 	SELECT so2.partner_invoice_id, so2.id AS order_id, so2.confirmation_date, so2.name
                 	FROM sale_order AS so2
                 	GROUP BY so2.partner_invoice_id, so2.id
                 ) AS so_1_1 ON (
                 	so_1_1.partner_invoice_id = so.partner_invoice_id AND so_1_1.confirmation_date = so_1.confirmation_date
                )
                LEFT JOIN (
                	SELECT sp.partner_id, MAX(sp.date_done) AS date_done, sp.origin
                	FROM stock_picking AS sp
                	WHERE sp.STATE  = 'done' AND sp.date_done IS NOT NULL AND sp.origin IS NOT NULL AND sp.picking_type_id = 4
                	GROUP BY sp.partner_id, sp.origin
                ) AS sp_order_1 ON sp_order_1.origin = so_1_1.name
                WHERE so.claim = FALSE AND so.amount_total > 0 AND STATE IN ('sale', 'done') AND order_id IS NOT NULL
                GROUP BY so.partner_invoice_id
                ORDER BY confirmation_date DESC
            )""")       