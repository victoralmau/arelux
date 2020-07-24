# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        # action_confirm
        return_data = super(SaleOrder, self).action_confirm()
        # operations
        for item in self:
            if item.state == 'sale':
                for picking_id in item.picking_ids:
                    if item.external_sale_order_id:
                        if item.external_sale_order_id.external_source_id:
                            for picking_id in item.picking_ids:
                                if picking_id.picking_type_id.id != item.external_sale_order_id.external_source_id.external_sale_order_picking_type_id.id:
                                    picking_id.picking_type_id = item.external_sale_order_id.external_source_id.external_sale_order_picking_type_id.id
                                    picking_id.name = self.env['ir.sequence'].next_by_code(self.env['stock.picking.type'].search([('id', '=', picking_id.picking_type_id.id)])[0].sequence_id.code)
        # return
        return return_data