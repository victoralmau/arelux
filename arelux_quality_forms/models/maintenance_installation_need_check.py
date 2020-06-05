# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class MaintenanceInstallationNeedCheck(models.Model):
    _name = 'maintenance.installation.need.check'
    _description = 'Maintenance Installation Need Check'            
    
    name = fields.Char(        
        string='Cuestion'
    )
    quality_team_id = fields.Many2one(
        comodel_name='quality.team',
        string='Equipo de calidad'
    )
    month_01 = fields.Boolean(        
        string='Enero'
    )
    month_02 = fields.Boolean(        
        string='Febrero'
    )
    month_03 = fields.Boolean(        
        string='Marzo'
    )
    month_04 = fields.Boolean(        
        string='Abril'
    )
    month_05 = fields.Boolean(        
        string='Mayo'
    )
    month_06 = fields.Boolean(        
        string='Junio'
    )
    month_07 = fields.Boolean(        
        string='Julio'
    )
    month_08 = fields.Boolean(        
        string='Agosto'
    )
    month_09 = fields.Boolean(        
        string='Septiembre'
    )
    month_10 = fields.Boolean(        
        string='Octubre'
    )
    month_11 = fields.Boolean(        
        string='Noviembre'
    )
    month_12 = fields.Boolean(        
        string='Diciembre'
    )        