# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

class WizardMaintenanceInstallation(models.TransientModel):
    _name = 'wizard.maintenance.installation'
    _description = 'Wizard Maintenance Installation'

    year = fields.Integer(
        string='Año',
        required=True
    )

    @api.model
    def get_maintenance_installations_with_incidence(self):
        date_from = str(self.year)+'-01-01'
        date_to = str(self.year) + '-12-31'
        return self.env['maintenance.installation'].sudo().search([
            ('state', '=', 'done'),
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('incidence', '!=', False)
        ])

    @api.model
    def need_check_items(self):
        need_check_items = []
        maintenance_installation_need_check_ids = self.env['maintenance.installation.need.check'].sudo().search([
            ('id', '>', 0)
        ])
        if len(maintenance_installation_need_check_ids) > 0:
            for maintenance_installation_need_check_id in maintenance_installation_need_check_ids:
                need_check_item = {
                    'name': str(maintenance_installation_need_check_id.name),
                    'quality_team_id_name': str(maintenance_installation_need_check_id.quality_team_id.name),
                }
                # all_months
                for month_item in range(1, 13):
                    # fix
                    if len(str(month_item)) == 1:
                        month_item = '0' + str(month_item)
                    # month_key
                    month_key = 'month_' + str(month_item)
                    if month_key in maintenance_installation_need_check_id:
                        # date_item
                        date_item = str(self.year) + '-' + str(month_item) + '-01'
                        # get_total
                        maintenance_installation_need_check_ids = self.env['maintenance.installation'].sudo().search([
                            ('state', '=', 'done'),
                            ('maintenance_installation_need_check_id', '=', maintenance_installation_need_check_id.id),
                            ('date', '=', date_item)
                        ])
                        # define
                        need_check_item[month_key] = {
                            'need_check': maintenance_installation_need_check_id[month_key],
                            'total_items_done': len(maintenance_installation_need_check_ids)
                        }
                # append
                need_check_items.append(need_check_item)
        #return
        return need_check_items

    @api.multi
    def check_report(self):
        data = {}
        data['form'] = self.read()[0]
        return self._print_report(data)

    def _print_report(self, data):
        return self.env['report'].get_action(self, 'arelux_quality_forms.maintenance_installation_items', data=data)