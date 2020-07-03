# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

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
        return_account_invoice = super(AccountInvoice, self).action_invoice_open()
        
        if self.ar_qt_customer_type==False:
            self.ar_qt_customer_type = self.partner_id.ar_qt_customer_type
        
        if self.ar_qt_activity_type==False:
            if self.partner_id.ar_qt_activity_type=='both':
                self.ar_qt_activity_type = 'todocesped'
            else:
                self.ar_qt_activity_type = self.partner_id.ar_qt_activity_type        
        
        if self.origin!=False:
            origins = self.origin.split(',')
            sale_order_ids = self.env['sale.order'].search([('name', '=', origins[0])])
                        
            find_sale_order_ids = False
            if len(sale_order_ids)>0:                                                        
                for sale_order_id in sale_order_ids:
                    self.ar_qt_activity_type = sale_order_id.ar_qt_activity_type
                    self.ar_qt_customer_type = sale_order_id.ar_qt_customer_type
                    
                    find_sale_order_ids = True
                
            if find_sale_order_ids==False:
                account_invoice_ids = self.env['account.invoice'].search([('number', '=', origins[0]),('type', '=', 'out_invoice')])
                if len(account_invoice_ids)>0:
                    for account_invoice_id in account_invoice_ids:
                        self.ar_qt_activity_type = account_invoice_id.ar_qt_activity_type
                        self.ar_qt_customer_type = account_invoice_id.ar_qt_customer_type                
                
        return return_account_invoice                