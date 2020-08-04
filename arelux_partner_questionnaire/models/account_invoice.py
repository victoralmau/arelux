# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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
        res = super(AccountInvoice, self)._prepare_refund(
            invoice, date_invoice, date, description, journal_id
        )
        res['ar_qt_activity_type'] = invoice.ar_qt_activity_type
        res['ar_qt_customer_type'] = invoice.ar_qt_customer_type
        return return_prepare_refund    

    @api.multi
    def action_invoice_open(self):
        # action
        res = super(AccountInvoice, self).action_invoice_open()
        # operations
        for item in self:
            if not item.ar_qt_customer_type:
                item.ar_qt_customer_type = item.partner_id.ar_qt_customer_type

            if not item.ar_qt_activity_type:
                if item.partner_id.ar_qt_activity_type == 'both':
                    item.ar_qt_activity_type = 'todocesped'
                else:
                    item.ar_qt_activity_type = item.partner_id.ar_qt_activity_type

            if item.origin:
                origins = item.origin.split(',')
                sale_order_ids = self.env['sale.order'].sudo().search(
                    [
                        ('name', '=', origins[0])
                    ]
                )
                find_sale_order_ids = False
                if sale_order_ids:
                    for sale_order_id in sale_order_ids:
                        item.ar_qt_activity_type = sale_order_id.ar_qt_activity_type
                        item.ar_qt_customer_type = sale_order_id.ar_qt_customer_type

                        find_sale_order_ids = True

                if not find_sale_order_ids:
                    account_invoice_ids = self.env['account.invoice'].sudo().search(
                        [
                            ('number', '=', origins[0]),
                            ('type', '=', 'out_invoice')
                        ]
                    )
                    if account_invoice_ids:
                        for account_invoice_id in account_invoice_ids:
                            item.ar_qt_activity_type = account_invoice_id.ar_qt_activity_type
                            item.ar_qt_customer_type = account_invoice_id.ar_qt_customer_type
        # return
        return res
