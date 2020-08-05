# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields
from lxml import etree


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    out_refund_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Factura devolucion'
    )
    confirmation_date_order = fields.Datetime(
        string='Fecha confirmacion pedido',
        related='sale_id.confirmation_date',
        store=False
    )

    @api.model
    def fields_view_get(self,
                        view_id=None,
                        view_type='tree',
                        toolbar=False,
                        submenu=False
                        ):
        res = super(StockPicking, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu
        )
        if view_type == 'tree':            
            picking_type_id = self.env.context.get('default_picking_type_id')
            doc = etree.fromstring(res['arch'])
            
            if picking_type_id != 1:
                # fields_invisible = ['date', 'min_date']
                fields_invisible = ['date']
                
                fields = doc.findall('field')
                for field in fields:
                    field_name = field.get('name')
                    if field_name in fields_invisible:
                        # field.set('invisible', '1')
                        doc.remove(field)                    
            else:
                doc.set('default_order', 'min_date asc')
                fields_invisible = [
                    'carrier_id', 'shipping_expedition_id', 'management_date',
                    'confirmation_date_order', 'user_id_done', 'date'
                ]
                fields = doc.findall('field')
                for field in fields:
                    field_name = field.get('name')
                    if field_name in fields_invisible:
                        doc.remove(field)
            
            res['arch'] = etree.tostring(doc)                                                    
                                                                    
        return res    
    
    @api.multi
    def do_transfer(self):
        res = super(StockPicking, self).do_transfer()
        if res:
            if self.pack_operation_product_ids:
                for po_product_id in self.pack_operation_product_ids:
                    if po_product_id.product_id and po_product_id.product_id.tracking == 'lot':
                        if po_product_id.pack_lot_ids:
                            for lot_id in po_product_id.pack_lot_ids:
                                if lot_id.lot_id:
                                    quantity_sum = 0
                                    quant_ids = self.env['stock.quant'].search(
                                        [
                                            ('product_id', '=', po_product_id.product_id.id),
                                            ('lot_id', '=', lot_id.lot_id.id),
                                            ('location_id.usage', '=', 'internal')
                                        ]
                                    )                
                                    if quant_ids:
                                        for quant_id in quant_ids:
                                            quantity_sum += quant_id.qty
                                                                                                                        
                                    lot_id.product_qty_store = quantity_sum
        # return
        return res
        
    @api.multi
    def action_send_account_invoice_out_refund(self):
        self.ensure_one()
        return False
    
    @api.model
    def cron_operations_autogenerate_invoices_stock_picking_return(self):
        picking_ids = self.env['stock.picking'].search(
            [
                ('id', '>', 125958),
                ('picking_type_id', '=', 6),
                ('state', '=', 'done'),
                ('out_refund_invoice_id', '=', False)
            ]
        )
        if picking_ids:
            for picking_id in picking_ids:
                picking_ids_get = self.env['stock.picking'].search(
                    [
                        ('picking_type_id', '!=', 6),
                        ('state', '=', 'done'),
                        ('name', '=', picking_id.origin)
                    ]
                )
                if picking_ids_get:
                    picking_id_origin = picking_ids_get[0]
                    if picking_id_origin.sale_id:
                        need_create_out_invoice = True
                        crm_claim_ids_get = self.env['crm.claim'].search(
                            [
                                ('active', '=', True),
                                (
                                    'model_ref_id',
                                    '=',
                                    'sale.order,%s'
                                    % picking_id_origin.sale_id.id
                                )
                            ]
                        )
                        if crm_claim_ids_get:
                            need_create_out_invoice = False

                        if need_create_out_invoice:
                            if picking_id_origin.sale_id.invoice_status == 'invoiced':
                                if picking_id_origin.sale_id.invoice_ids:
                                    # invoice_id
                                    invoice_id = False
                                    for invoice_id_get in picking_id_origin.sale_id.invoice_ids:
                                        if invoice_id_get.type == 'out_invoice':
                                            invoice_id = invoice_id_get
                                    # contionue
                                    if invoice_id:
                                        # products_info
                                        products_info = {}
                                        for line_id in invoice_id.invoice_line_ids:
                                            if line_id.product_id.id>0:
                                                products_info[line_id.product_id.id] = {
                                                    'name': line_id.name,
                                                    'price_unit': line_id.price_unit,
                                                    'account_id': line_id.account_id.id,
                                                    'discount': line_id.discount,
                                                }
                                        # account.invoice
                                        vals = {
                                            'partner_id': invoice_id.partner_id.id,
                                            'partner_shipping_id':
                                                invoice_id.partner_shipping_id.id,
                                            'account_id': invoice_id.account_id.id,
                                            'journal_id': invoice_id.journal_id.id,
                                            'state': 'draft',
                                            'type': 'out_refund',
                                            'comment': ' ',
                                            'origin': invoice_id.number,
                                            'name': stock_picking_id.name,
                                            'ar_qt_activity_type': invoice_id.ar_qt_activity_type,
                                            'ar_qt_customer_type': invoice_id.ar_qt_customer_type,
                                            'payment_mode_id': invoice_id.payment_mode_id.id,
                                            'payment_term_id': invoice_id.payment_term_id.id,
                                            'fiscal_position_id': invoice_id.fiscal_position_id.id,
                                            'team_id': invoice_id.team_id.id,
                                            'user_id': invoice_id.user_id.id
                                        }
                                        # partner_bank_id
                                        if invoice_id.partner_bank_id:
                                            vals['partner_bank_id'] = invoice_id.partner_bank_id.id
                                        # mandate_id
                                        if invoice_id.mandate_id:
                                            vals['mandate_id'] = invoice_id.mandate_id.id
                                        # create
                                        invoice_obj = self.env['account.invoice'].sudo().create(vals)
                                        # lines
                                        for product_id in picking_id_origin.pack_operation_product_ids:
                                            line_vals = {
                                                'invoice_id': invoice_obj.id,
                                                'product_id': product_id.product_id.id,
                                                'quantity': product_id.qty_done,
                                                'price_unit':
                                                    products_info[product_id.product_id.id]['price_unit'],
                                                'discount':
                                                    products_info[product_id.product_id.id]['discount'],
                                                'account_id':
                                                    products_info[product_id.product_id.id]['account_id'],
                                                'name':
                                                    products_info[product_id.product_id.id]['name']
                                            }
                                            line_obj = self.env['account.invoice.line'].sudo().create(
                                                line_vals
                                            )
                                            line_obj._onchange_product_id()
                                            line_obj._onchange_account_id()
                                            # price
                                            price_unit_clean = line_vals['price_unit']

                                            if line_vals['discount'] > 0:
                                                pud = (line_vals['price_unit']/100)*line_vals['discount']
                                                price_unit_clean = line_vals['price_unit']-pud

                                            price_subtotal = price_unit_clean*line_vals['quantity']

                                            line_obj.update({
                                                'price_unit': round(line_vals['price_unit'], 4),
                                                'price_subtotal': round(price_subtotal, 4),
                                            })
                                        # compute_taxes
                                        invoice_obj.compute_taxes()
                                        invoice_obj.action_invoice_open()
                                        # update_stock_picking
                                        picking_id_origin.out_refund_invoice_id = invoice_obj.id
                                        # action_send_account_invoice_out_refund
                                        picking_id_origin.action_send_account_invoice_out_refund()
