# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_regenerate_purchase_prices(self):
        for item in self:
            if item.state in ['sale', 'done']:
                order_lines = {}
                for order_line in item.order_line:
                    order_lines[order_line.product_id.id] = {
                        'is_delivery': order_line.is_delivery,
                        'purchase_price': 0,
                        'standard_price': order_line.product_id.standard_price,
                    }
                # picking_ids
                if item.picking_ids:
                    for picking_id in item.picking_ids:
                        if picking_id.state == 'done':
                            if picking_id.move_lines:
                                for move_line in picking_id.move_lines:
                                    if move_line.quant_ids:
                                        for q_id in move_line.quant_ids:
                                            # cost
                                            if q_id.cost > 0:
                                                order_lines[
                                                    move_line.product_id.id
                                                ]['purchase_price'] = q_id.cost
                                            else:
                                                order_lines[
                                                    move_line.product_id.id
                                                ]['purchase_price'] = \
                                                    (q_id.inventory_value/q_id.qty)
                # operations
                for order_line_key in order_lines:
                    if not order_lines[order_line_key]['is_delivery']:
                        if order_lines[order_line_key]['purchase_price'] == 0:
                            order_lines[order_line_key]['purchase_price'] = \
                                order_lines[order_line_key]['standard_price']
                # operations2
                margin_order = 0
                for line in item.order_line:
                    # Fix Mer4
                    if line.product_id.id != 277:
                        line.purchase_price = \
                            order_lines[line.product_id.id]['purchase_price']
                        # margin_line
                        margin_line = 0
                        # margin (qty delivered if not qty_invoiced)
                        if item.invoice_status == 'invoiced':
                            operation = (line.purchase_price * line.qty_invoiced)
                            margin_line = line.price_subtotal - operation
                        elif item.invoice_status == 'no':
                            if line.qty_delivered > 0:
                                operation = (line.purchase_price * line.qty_delivered)
                                margin_line = line.price_subtotal - operation
                        # define
                        line.margin = "{:.2f}".format(margin_line)
                        # action_calculate_margin_percent
                        line.action_calculate_margin_percent()
                        # margin_order
                        margin_order += line.margin
                # margin
                item.margin = "{:.2f}".format(margin_order)
                # action_calculate_margin_percent
                item.action_calculate_margin_percent()
                # invoices
                if item.invoice_ids:
                    for invoice_id in item.invoice_ids:
                        invoice_id.action_regenerate_margin()
