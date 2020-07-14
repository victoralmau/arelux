# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from openerp.http import request

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_acquirer_type_amount_paid = fields.Selection(
        selection=[
            ('total','Total'), 
            ('partial','Parcial')                                     
        ],
        string='Tipo de importe pago',
        default='total'
    )    
    payment_transaction_ids = fields.One2many('payment.transaction', 'sale_order_id', string='Transacciones de pago', domain=[('state', '!=', 'draft')])
    show_pay_button = fields.Boolean( 
        string='Show Pay button',
        compute='_show_pay_button',
        store=False
    )
    
    @api.one        
    def _show_pay_button(self):        
        tpv_payment_mode_id_show_pay_button = int(self.env['ir.config_parameter'].sudo().get_param('tpv_payment_mode_id_show_pay_button'))
    
        for sale_order_obj in self:
            sale_order_obj.show_pay_button = False
            if sale_order_obj.proforma==True:
                if sale_order_obj.payment_mode_id.id>0:
                    if sale_order_obj.payment_mode_id.id==tpv_payment_mode_id_show_pay_button:
                        sale_order_obj.show_pay_button = True    
                        #check if completyly pay
                        if len(sale_order_obj.payment_transaction_ids)>0:
                            transactions_amount = 0
                            for payment_transaction_id in sale_order_obj.payment_transaction_ids:
                                if payment_transaction_id.state=='done':
                                    transactions_amount += payment_transaction_id.amount
                            #check
                            if transactions_amount>=sale_order_obj.amount_total:
                                sale_order_obj.show_pay_button = False
            #override (url_return for payment form)
            if request:                           
                payment_ok_get = str(request.httprequest.args.get('payment_ok'))
                if payment_ok_get!=None:
                    if payment_ok_get=='1':
                        sale_order_obj.show_pay_button = False                        