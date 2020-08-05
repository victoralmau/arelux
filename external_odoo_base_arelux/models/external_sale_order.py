# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, _
_logger = logging.getLogger(__name__)


class ExternalSaleOrder(models.Model):
    _inherit = 'external.sale.order'

    @api.multi
    def action_crm_lead_create(self):
        self.ensure_one()
        return_item = super(ExternalSaleOrder, self).action_crm_lead_create()
        # lead_id
        if self.lead_id:
            # external_customer_id
            if self.external_customer_id and self.external_customer_id.partner_id:
                ec_p = self.external_customer_id.partner_id
                self.lead_id.ar_qt_activity_type = ec_p.ar_qt_activity_type
                self.lead_id.ar_qt_customer_type = ec_p.ar_qt_customer_type
            else:
                self.lead_id.ar_qt_activity_type = 'arelux'
                self.lead_id.ar_qt_customer_type = 'particular'
        # return
        return return_item

    @api.multi
    def action_so_done_error_esa_id_without_country_id(self):
        self.ensure_one()
        _logger.info(
            _('No se puede confirmar el pedido %s porque la direccion de envio del '
              'cliente NO tiene PAIS mapeado')
            % self.sale_order_id.name
        )

    @api.multi
    def action_so_done_error_esa_id_without_country_state_id(self):
        self.ensure_one()
        _logger.info(
            _('No se puede confirmar el pedido %s porque la direccion de envio del '
              'cliente NO tiene PROVINCIA mapeada')
            % self.sale_order_id.name
        )

    @api.multi
    def action_sale_order_done(self):
        self.ensure_one()
        # antes
        if self.sale_order_id:
            if self.sale_order_id.state in ['draft', 'sent']:
                weight_total = 0
                for line in self.sale_order_id.order_line:
                    if line.product_id:
                        if line.product_uom_qty > 0:
                            if line.product_id.weight > 0:
                                weight = line.product_id.weight*line.product_uom_qty
                                weight_total += weight
                # operations
                if self.external_source_id:
                    es = self.external_source_id
                    if es.external_sale_order_carrier_id:
                        es_esoc = es.external_sale_order_carrier_id
                        if weight_total <= 10:
                            self.sale_order_id.carrier_id = es_esoc.id
        # check country_id and state_id
        allow_confirm = True
        if self.external_shipping_address_id:
            # check_country_id
            if self.external_shipping_address_id.country_id.id == 0:
                self.action_so_done_error_esa_id_without_country_id()
                allow_confirm = False
            if self.external_shipping_address_id.country_state_id.id == 0:
                self.action_so_done_error_esa_id_without_country_state_id()
                allow_confirm = False
        # allow_confirm
        if allow_confirm:
            return super(ExternalSaleOrder, self).action_sale_order_done()
