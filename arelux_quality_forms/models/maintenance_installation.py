# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime

class MaintenanceInstallation(models.Model):
    _name = 'maintenance.installation'
    _description = 'Maintenance Installation'            
    
    date = fields.Date(        
        string='Fecha'
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
            ('valid','Validada')                          
        ],
        string='Estado',
        default='draft',
        track_visibility='onchange'
    )
    
    @api.model
    def cron_autongenerate_maintenance_installation_next_month(self):
        current_date = datetime.today()
        current_date_year = current_date.strftime("%Y")
        current_date_month = current_date.strftime("%m")
        
        next_month = str(int(current_date_month)+1)
        next_month = next_month.rjust(2, '0')
        
        job_user_ids = {
            'nodriza_manager': int(self.env['ir.config_parameter'].sudo().get_param('maintenance_installation_job_nodriza_manager_user_id')),
            'logistic_operator': int(self.env['ir.config_parameter'].sudo().get_param('maintenance_installation_job_logistic_operator_user_id')) 
        }                        
        
        maintenance_installation_need_check_ids = self.env['maintenance.installation.need.check'].search(
            [
                ('month_'+str(next_month), '=', True)
            ]
        )
        if len(maintenance_installation_need_check_ids)>0:
            date_next_month_item = current_date_year+'-'+next_month+'-01'
            
            
            for maintenance_installation_need_check_id in maintenance_installation_need_check_ids:
                maintenance_installation_ids = self.env['maintenance.installation'].search(
                    [
                        ('date', '=', date_next_month_item),
                        ('maintenance_installation_need_check_id', '=', maintenance_installation_need_check_id.id)
                    ]
                )
                if len(maintenance_installation_ids)==0:
                    maintenance_installation_vals = {
                        'date': date_next_month_item,
                        'maintenance_installation_need_check_id': maintenance_installation_need_check_id.id,
                        'user_id': job_user_ids[maintenance_installation_need_check_id.job],
                        'state': 'draft'                                                
                    }
                    maintenance_installation_obj = self.env['maintenance.installation'].sudo().create(maintenance_installation_vals)                                                 