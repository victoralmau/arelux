# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerSage(models.Model):
    _inherit = 'res.partner'

    sage_actividad_id = fields.Many2one(
        comodel_name='sage.actividad', 
        string='Sage Actividad',
    )                                
    sage_subactividad_id = fields.Many2one(
        comodel_name='sage.subactividad', 
        string='Sage SubActividad',
    )
    sage_sector_id = fields.Many2one(
        comodel_name='sage.sector', 
        string='Sage Sector',
    )
    sage_categoria_cliente_id = fields.Many2one(
        comodel_name='sage.categoria.cliente', 
        string='Sage Categoria Cliente',
    )
    sage_tipo_cliente_id = fields.Many2one(
        comodel_name='sage.tipo.cliente', 
        string='Sage Tipo Cliente',
    )
    sage_colectivo_id = fields.Many2one(
        comodel_name='sage.colectivo', 
        string='Sage Colectivo',
    )
    sage_zona_id = fields.Many2one(
        comodel_name='sage.zona', 
        string='Sage Zona',
    )        
    installer = fields.Boolean(
        string="Instalador"
    )                                       