# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

class WizardWasteRemove(models.TransientModel):
    _name = 'wizard.waste.remove'
    _description = 'Wizard Waste Remove'

    date_from = fields.Date(
        string='Date from',
        required=True
    )
    date_to = fields.Date(
        string='Date to',
        required=True
    )

    @api.model
    def get_waste_remove_product_ids(self):
        return self.env['waste.remove.product'].sudo().search([
            ('id', '>', 0)
        ])

    @api.model
    def get_waste_remove_ids(self, date_from, date_to):
        return self.env['waste.remove'].sudo().search([
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])

    @api.model
    def get_waste_remove_total(self):
        data = []
        for item in self:
            waste_remove_product_ids = self.get_waste_remove_product_ids()
            waste_remove_ids = self.get_waste_remove_ids(item.date_from, item.date_to)
            if waste_remove_ids:
                details_by_key = {}
                for waste_remove_id in waste_remove_ids:
                    for waste_remove_detail_id in waste_remove_id.waste_remove_detail_ids:
                        if waste_remove_detail_id.waste_remove_product_id.id not in details_by_key:
                            details_by_key[waste_remove_detail_id.waste_remove_product_id.id] = waste_remove_detail_id.quantity
                        else:
                            details_by_key[waste_remove_detail_id.waste_remove_product_id.id] += waste_remove_detail_id.quantity
                # total
                for waste_remove_product_id in waste_remove_product_ids:
                    data_item = {
                        'name': waste_remove_product_id.name,
                        'uom': waste_remove_product_id.uom,
                        'with_details': False
                    }
                    # search
                    if waste_remove_product_id.id in details_by_key:
                        data_item['with_details'] = True
                        data_item['quantity'] = details_by_key[waste_remove_product_id.id]
                    # append
                    data.append(data_item)
        # return
        return data

    @api.model
    def get_waste_remove_items(self):
        data = []
        for item in self:
            waste_remove_product_ids = self.get_waste_remove_product_ids()
            waste_remove_ids = self.get_waste_remove_ids(item.date_from, item.date_to)
            if waste_remove_ids:
                for waste_remove_id in waste_remove_ids:
                    data_item = {
                        'date': waste_remove_id.date,
                        'retired_by_name': waste_remove_id.retired_by.name,
                        'sign_by_name': waste_remove_id.sign_by.name,
                        'destination': dict(waste_remove_id.fields_get(allfields=['destination'])['destination']['selection'])[waste_remove_id.destination],
                        'waste_remove_product_ids': []
                    }
                    # details_by_key
                    details_by_key = {}
                    for waste_remove_detail_id in waste_remove_id.waste_remove_detail_ids:
                        details_by_key[waste_remove_detail_id.waste_remove_product_id.id] = waste_remove_detail_id.quantity
                    # waste_remove_product_ids
                    for waste_remove_product_id in waste_remove_product_ids:
                        waste_remove_product_id_item = {
                            'name': waste_remove_product_id.name,
                            'uom': waste_remove_product_id.uom,
                            'with_detail': False
                        }
                        # search
                        if waste_remove_product_id.id in details_by_key:
                            waste_remove_product_id_item['with_detail'] = True
                            waste_remove_product_id_item['quantity'] = details_by_key[waste_remove_product_id.id]
                        # append
                        data_item['waste_remove_product_ids'].append(waste_remove_product_id_item)
                    # append
                    data.append(data_item)
        # return
        return data

    @api.multi
    def check_report(self):
        data = {}
        data['form'] = self.read()[0]
        return self._print_report(data)

    def _print_report(self, data):
        return self.env['report'].get_action(self, 'arelux_quality_forms.waste_remove_items', data=data)