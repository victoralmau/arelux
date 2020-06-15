# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),                    
        ],
        size=15, 
        string='Tipo de actividad',
        store=True
    )
    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),        
        ],        
        string='Tipo de cliente',
        store=True
    )
    
    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        return_prepare_refund = super(AccountInvoice, self)._prepare_refund(invoice, date_invoice, date, description, journal_id)
        return_prepare_refund['ar_qt_activity_type'] = invoice.ar_qt_activity_type
        return_prepare_refund['ar_qt_customer_type'] = invoice.ar_qt_customer_type
        return return_prepare_refund    

    @api.multi
    def action_invoice_open(self):
        #action
        return_account_invoice = super(AccountInvoice, self).action_invoice_open()
        #operations
        for item in self:
            if item.ar_qt_customer_type==False:
                item.ar_qt_customer_type = item.partner_id.ar_qt_customer_type

            if item.ar_qt_activity_type==False:
                if item.partner_id.ar_qt_activity_type=='both':
                    item.ar_qt_activity_type = 'todocesped'
                else:
                    item.ar_qt_activity_type = item.partner_id.ar_qt_activity_type

            if item.origin!=False:
                origins = item.origin.split(',')
                sale_order_ids = self.env['sale.order'].sudo().search([('name', '=', origins[0])])

                find_sale_order_ids = False
                if len(sale_order_ids)>0:
                    for sale_order_id in sale_order_ids:
                        item.ar_qt_activity_type = sale_order_id.ar_qt_activity_type
                        item.ar_qt_customer_type = sale_order_id.ar_qt_customer_type

                        find_sale_order_ids = True

                if find_sale_order_ids==False:
                    account_invoice_ids = self.env['account.invoice'].sudo().search([('number', '=', origins[0]),('type', '=', 'out_invoice')])
                    if len(account_invoice_ids)>0:
                        for account_invoice_id in account_invoice_ids:
                            item.ar_qt_activity_type = account_invoice_id.ar_qt_activity_type
                            item.ar_qt_customer_type = account_invoice_id.ar_qt_customer_type
        #return
        return return_account_invoice