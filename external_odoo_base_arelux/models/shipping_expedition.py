# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'

    @api.model
    def create(self, values):
        res = super(ShippingExpedition, self).create(values)
        # operations
        if res.user_id.id == 0:
            if res.picking_id:
                if res.picking_id.external_stock_picking_id:
                    picking_id_esp = res.picking_id.external_stock_picking_id
                    if picking_id_esp.external_source_id:
                        picking_id_esp_es = picking_id_esp.external_source_id
                        if picking_id_esp_es.external_stock_picking_user_id:
                            res.user_id = \
                                picking_id_esp_es.external_stock_picking_user_id
        # return
        return res
