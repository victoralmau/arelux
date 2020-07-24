# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'

    @api.model
    def create(self, values):
        return_object = super(ShippingExpedition, self).create(values)
        # operations
        if return_object.user_id.id == 0:
            if return_object.picking_id:
                if return_object.picking_id.external_stock_picking_id:
                    if return_object.picking_id.external_stock_picking_id.external_source_id:
                        if return_object.picking_id.external_stock_picking_id.external_source_id.external_stock_picking_user_id:
                            return_object.user_id = return_object.picking_id.external_stock_picking_id.external_source_id.external_stock_picking_user_id.id
        # return
        return return_object