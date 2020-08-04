# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    sale_order_sale_sum = fields.Monetary(
        compute='_compute_sale_order_sale_sum',
        string='Sum total ventas'
    )
    sale_order_count_store = fields.Integer( 
        string='Count ventas'
    )    
    sale_order_pto_count = fields.Integer(
        compute='_compute_sale_order_pto_count',
        string='Count pto'
    )
    
    @api.multi        
    def _compute_sale_order_sale_sum(self):
        for item in self:
            item.sale_order_sale_sum = 0
            order_ids = self.env['sale.order'].search(
                [
                    ('partner_id', 'child_of', item.ids),
                    ('state', 'in', ('sale','done')),
                    ('amount_total', '>', 0),
                    ('claim', '=', False) 
                 ]
            )
            if order_ids:
                for order_id in order_ids:
                    item.sale_order_sale_sum = item.sale_order_sale_sum + order_id.amount_untaxed
    
    @api.multi
    def _compute_sale_order_pto_count(self):
        for item in self:
            order_ids = self.env['sale.order'].search(
                [
                    ('claim', '=', False),
                    ('partner_id', 'child_of', item.ids),
                    '|', 
                    '&', 
                    ('state', 'in', ('sale','done')), 
                    ('amount_total', '=', 0), 
                    '&', 
                    ('state', 'in', ('draft','sent')), 
                    ('amount_total', '>', 0)
                ]
            )            
            item.sale_order_pto_count = len(order_ids)
            
    @api.model
    def create(self, values):
        record = super(ResPartner, self).create(values)
        # state_id
        if record.state_id:
            product_pricelist_ids = self.env['product.pricelist'].search(
                [
                    ('ar_qt_activity_type', '=', record.ar_qt_activity_type),
                    ('ar_qt_customer_type', '=', record.ar_qt_customer_type),
                    ('state_ids', 'in', (record.state_id.id))
                ]
            )
            if product_pricelist_ids:
                record.property_product_pricelist = product_pricelist_ids[0].id
            else:
                record.property_product_pricelist = 1                
        # return
        return record
    
    @api.model    
    def cron_operations_res_partners(self):
        # reset all 0
        self.env.cr.execute("UPDATE res_partner SET sale_order_count_store = 0 WHERE id > 0")
        # update only with sales
        sale_order_ids = self.env['sale.order'].search(
            [
                ('amount_total', '>', 0),
                ('claim', '=', False),
                ('state', 'in', ('sale', 'done'))
            ]
        )
        if sale_order_ids:
            _logger.info('Total pedidos a actualizar=%s' % len(sale_order_ids))
            res_partner_ids = self.env['res.partner'].search(
                [
                    ('id', 'in', sale_order_ids.mapped('partner_id').ids)
                ]
            )
            if res_partner_ids:
                _logger.info('Total contactos a actualizar=%' % len(res_partner_ids))
                for res_partner_id in res_partner_ids:
                    sale_order_ids = self.env['sale.order'].search(
                        [
                            ('partner_id', '=', res_partner_id.id),
                            ('amount_total', '>', 0),
                            ('claim', '=', False),
                            ('state', 'in', ('sale', 'done'))
                        ]
                    )
                    res_partner_id.sale_order_count_store = len(sale_order_ids)
