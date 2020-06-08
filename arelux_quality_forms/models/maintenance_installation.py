# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime

class MaintenanceInstallation(models.Model):
    _name = 'maintenance.installation'
    _description = 'Maintenance Installation'
    _order = 'date desc'
    
    date = fields.Date(        
        string='Fecha'
    )
    date_done = fields.Date(
        string='Fecha Hecho'
    )
    maintenance_installation_need_check_id = fields.Many2one(
        comodel_name='maintenance.installation.need.check',
        string='Accion a revisar'
    )
    incidence = fields.Text(        
        string='Incidencia'
    )
    solution = fields.Text(        
        string='Solucion'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsable'
    )
    close_measurement = fields.Date(
        string='Cierre incidencia'
    )
    state = fields.Selection(
        selection=[
            ('draft','Borrador'), 
            ('done','Hecho')
        ],
        string='Estado',
        default='draft',
    )

    @api.multi
    def action_done_multi(self):
        for obj in self:
            if obj.state == 'draft':
                obj.action_done()

    @api.one
    def action_done(self):
        if self.state == 'draft':
            self.state = 'done'
            self.date_done = fields.datetime.now()

    @api.model
    def maintenance_installation_generate(self, year, month):
        maintenance_installation_need_check_ids = self.env['maintenance.installation.need.check'].search(
            [
                ('month_' + str(month), '=', True)
            ]
        )
        if len(maintenance_installation_need_check_ids) > 0:
            date_next_month_item = str(year) + '-' + str(month) + '-01'

            for maintenance_installation_need_check_id in maintenance_installation_need_check_ids:
                if maintenance_installation_need_check_id.quality_team_id.user_id.id>0:
                    maintenance_installation_ids = self.env['maintenance.installation'].search(
                        [
                            ('date', '=', date_next_month_item),
                            ('maintenance_installation_need_check_id', '=', maintenance_installation_need_check_id.id)
                        ]
                    )
                    if len(maintenance_installation_ids) == 0:
                        maintenance_installation_vals = {
                            'date': date_next_month_item,
                            'maintenance_installation_need_check_id': maintenance_installation_need_check_id.id,
                            'user_id': maintenance_installation_need_check_id.quality_team_id.user_id.id,
                            'state': 'draft'
                        }
                        maintenance_installation_obj = self.env['maintenance.installation'].sudo().create(maintenance_installation_vals)

    @api.model
    def cron_autongenerate_maintenance_installation_next_month(self):
        current_date = datetime.today()
        date_next_month = current_date + relativedelta(months=+1, day=1)
        date_next_month_split = date_next_month.strftime("%Y-%m-%d").split('-')
        year_next_month = str(date_next_month_split[0])
        month_next_month = str(date_next_month_split[1])
        # maintenance_installation_generate
        self.maintenance_installation_generate(year_next_month, month_next_month)

    @api.model
    def cron_autongenerate_maintenance_installation_all_this_year(self):
        current_date = datetime.today()
        current_date_year = current_date.strftime("%Y")
        # operations
        for month_item in range(1, 13):
            # fix
            if len(str(month_item)) == 1:
                month_item = '0' + str(month_item)
            # maintenance_installation_generate
            self.maintenance_installation_generate(current_date_year, month_item)