# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        # operations
        for item in self:
            if item.carrier_id.id == 0:
                names = ['cbl', 'txt', 'tsb']
                # check note
                if item.note:
                    for name in names:
                        if name in item.note or name.upper() in item.note:
                            carrier_ids = self.env['delivery.carrier'].search(
                                [
                                    ('carrier_type', '=', name)
                                ]
                            )
                            if carrier_ids:
                                for carrier_id in carrier_ids:
                                    item.carrier_id = carrier_id.id
                # check  picking_note
                if item.picking_note:
                    for name in names:
                        if name in item.picking_note \
                                or name.upper() in item.picking_note:
                            carrier_ids = self.env['delivery.carrier'].search(
                                [
                                    ('carrier_type', '=', name)
                                ]
                            )
                            if carrier_ids:
                                for carrier_id in carrier_ids:
                                    item.carrier_id = carrier_id.id
        # action_confirm
        return_data = super(SaleOrder, self).action_confirm()
        # operations
        for item in self:
            if item.state == 'sale':
                for picking_id in item.picking_ids:
                    # operations
                    if picking_id.carrier_id:
                        if picking_id.carrier_id.carrier_type == 'nacex':
                            codes = []
                            for line in item.order_line:
                                if line.product_id.default_code:
                                    if line.product_id.default_code not in codes:
                                        codes.append(
                                            str(line.product_id.default_code)
                                        )
                            # only_prduct_MCH12
                            if len(codes) > 0:
                                if len(codes) == 1 and default_codes[0] == 'MCH12':
                                    type_ids = self.env[
                                        'stock.picking.type'
                                    ].sudo().search(
                                        [
                                            (
                                                'sequence_id.code',
                                                '=',
                                                'stock.picking.nacex.muestras'
                                            )
                                        ]
                                    )
                                    if type_ids:
                                        picking_id.picking_type_id = type_ids[0].id
                                        picking_id.name = self.env[
                                            'ir.sequence'
                                        ].next_by_code(
                                            self.env['stock.picking.type'].search(
                                                [
                                                    ('id', '=', picking_id.picking_type_id.id)
                                                ]
                                            )[0].sequence_id.code)
        # return
        return return_data
