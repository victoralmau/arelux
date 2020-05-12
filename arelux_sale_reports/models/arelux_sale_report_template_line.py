# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class AreluxSaleReportTemplateLine(models.Model):
    _name = 'arelux.sale.report.template.line'
    _description = 'Arelux Sale Report Template Line'
    _order = "position asc"    
        
    arelux_sale_report_template_id = fields.Many2one(
        comodel_name='arelux.sale.report.template',
        string='Arelux Sale Report Template'
    )
    arelux_sale_report_type_id = fields.Many2one(
        comodel_name='arelux.sale.report.type',
        string='Arelux Sale Report Type'
    )
    position = fields.Integer(
        string='Posicion'
    )                                       
    ar_qt_activity_type = fields.Selection(
        selection=[
            ('none','Ninguno'), 
            ('arelux','Arelux'), 
            ('todocesped','Todocesped'),
            ('evert','Evert')                         
        ],
        string='Tipo de actividad',
        default='none'
    )
    ar_qt_customer_type = fields.Selection(
        selection=[
            ('none','Ninguno'), 
            ('particular','Particular'), 
            ('profesional','Profesional')                         
        ],
        string='Tipo de cliente',
        default='none'
    )
    crm_team_id = fields.Many2one(
        comodel_name='crm.team',
        string='Equipo de ventas'
    )
    group_by_user = fields.Boolean(
        default=False,
        string='Group by user'
    )
    show_in_table_format = fields.Boolean(
        default=False,
        string='Show in table format'
    )