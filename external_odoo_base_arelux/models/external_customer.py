# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ExternalCustomer(models.Model):
    _inherit = 'external.customer'

    @api.multi
    def operations_item(self):
        self.ensure_one()
        return_item = super(ExternalCustomer, self).operations_item()
        # partner_id
        if self.partner_id:
            if self.external_source_id:
                es = self.external_source_id
                # ar_qt_activity_type
                self.partner_id.ar_qt_activity_type = \
                    es.external_customer_ar_qt_activity_type
                # ar_qt_customer_type
                self.partner_id.ar_qt_customer_type = \
                    es.external_customer_ar_qt_customer_type
                # external_customer_res_partner_category_id
                if es.external_customer_res_partner_category_id:
                    self.partner_id.category_id = [
                        (4, es.external_customer_res_partner_category_id.id)
                    ]
                # external_customer_res_partner_contact_form
                if es.external_customer_res_partner_contact_form:
                    if self.partner_id.ar_qt_activity_type == 'arelux':
                        self.partner_id.ar_qt_arelux_contact_form = [
                            (4, es.external_customer_res_partner_contact_form.id)
                        ]
                    elif self.partner_id.ar_qt_activity_type == 'todocesped':
                        self.partner_id.ar_qt_todocesped_contact_form = [
                            (4, es.external_customer_res_partner_contact_form.id)
                        ]
        # return
        return return_item
