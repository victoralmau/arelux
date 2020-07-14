# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools

import logging
_logger = logging.getLogger(__name__)

class ResPartnerSaleOrderReport(models.Model):
    _name = 'res.partner.sale.order.report'
    _auto = False
    _description = "Res Partner Sale Order Report"
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
        tools.drop_view_if_exists(self._cr, 'res_partner_sale_order_report')
        self._cr.execute("""
            CREATE VIEW res_partner_sale_order_report AS (
                SELECT 
                so.id AS id,  
                so.partner_invoice_id AS partner_id,  
                so.id AS order_id,
                so.confirmation_date AS confirmation_date,
                MAX(sp.date_done) AS date_done_picking
                FROM sale_order AS so
                LEFT JOIN (
                	SELECT sp.partner_id, MAX(sp.date_done) AS date_done, sp.origin
                	FROM stock_picking AS sp
                	WHERE sp.STATE  = 'done' AND sp.date_done IS NOT NULL AND sp.origin IS NOT NULL AND sp.picking_type_id = 4
                	GROUP BY sp.partner_id, sp.origin
                ) AS sp ON sp.origin = so.name
                WHERE so.claim = FALSE AND so.amount_total > 0 AND STATE IN ('sale', 'done')
                GROUP BY so.partner_invoice_id, order_id
                ORDER BY confirmation_date DESC
            )""")       