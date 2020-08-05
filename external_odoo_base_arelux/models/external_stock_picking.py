# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ExternalStockPicking(models.Model):
    _inherit = 'external.stock.picking'

    @api.multi
    def action_run(self):
        self.ensure_one()
        res = super(ExternalStockPicking, self).action_run()
        # picking
        if self.picking_id:
            # external_customer_id > partner_id info
            if self.external_customer_id:
                ec = self.external_customer_id
                if ec.partner_id:
                    ec_p = ec.partner_id
                    self.picking_id.ar_qt_activity_type = ec_p.ar_qt_activity_type
                    self.picking_id.ar_qt_customer_type = ec_p.ar_qt_customer_type
            # carrier_id (nacex only if 10kg)
            if self.picking_id.weight <= 10:
                delivery_carrier_ids = self.env['delivery.carrier'].sudo().search(
                    [
                        ('carrier_type', '=', 'nacex')
                    ]
                )
                if delivery_carrier_ids:
                    self.picking_id.carrier_id = delivery_carrier_ids[0].id
        # return
        return res
