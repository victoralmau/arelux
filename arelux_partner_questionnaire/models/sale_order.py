# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, fields, _
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),
        ],
        size=15,
        string='Tipo de actividad'
    )
    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),
        ],
        string='Tipo de cliente',
    )

    @api.multi
    @api.onchange('partner_shipping_id')
    def onchange_partner_shipping_id(self):
        for item in self:
            if item.partner_id:
                if item.opportunity_id.id == 0:
                    item.ar_qt_activity_type = item.partner_id.ar_qt_activity_type
                    item.ar_qt_customer_type = item.partner_id.ar_qt_customer_type

    @api.multi
    @api.onchange('opportunity_id')
    def onchange_opportunity_id(self):
        for item in self:
            if item.opportunity_id:
                item.ar_qt_activity_type = item.opportunity_id.ar_qt_activity_type
                item.ar_qt_customer_type = item.opportunity_id.ar_qt_customer_type

    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        # operations
        if res.opportunity_id:
            # ar_qt_activity_type
            if not res.ar_qt_activity_type:
                res.ar_qt_activity_type = res.opportunity_id.ar_qt_activity_type
            # ar_qt_customer_type
            if not res.ar_qt_customer_type:
                res.ar_qt_customer_type = res.opportunity_id.ar_qt_customer_type
        # return
        return res

    @api.multi
    def write(self, vals):
        allow_write = True
        # fix validate template_id
        if 'sale_order_template_id' in vals:
            if vals['sale_order_template_id']:
                sale_order_template_id_check = vals['sale_order_template_id']
                template_obj = self.env['sale.order.template'].browse(
                    sale_order_template_id_check
                )
                if template_obj.ar_qt_activity_type:
                    if template_obj.ar_qt_activity_type != self.ar_qt_activity_type:
                        allow_write = False
                        raise Warning(
                            _("La plantilla de presupuesto no corresponde con "
                              "el tipo de actividad")
                        )
        # allow_write
        if allow_write:
            return_object = super(SaleOrder, self).write(vals)
            return return_object
