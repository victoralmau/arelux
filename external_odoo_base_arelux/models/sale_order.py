# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        # action_confirm
        res = super(SaleOrder, self).action_confirm()
        # operations
        for item in self:
            if item.state == 'sale':
                for picking_id in item.picking_ids:
                    if item.external_sale_order_id:
                        item_eso = item.external_sale_order_id
                        if item_eso.external_source_id:
                            item_eso_es = item_eso.external_source_id
                            item_eso_es_esopt = item_eso_es.external_sale_order_picking_type_id
                            for picking_id in item.picking_ids:
                                picking_id_pt = picking_id.picking_type_id
                                if picking_id_pt.id != item_eso_es_esopt.id:
                                    picking_id.picking_type_id = item_eso_es_esopt.id
                                    picking_id.name = self.env['ir.sequence'].next_by_code(
                                        self.env['stock.picking.type'].search(
                                            [
                                                ('id', '=', picking_id_pt.id)
                                            ]
                                        )[0].sequence_id.code
                                    )
        # return
        return res
