#-*- coding: utf-8 -*-
from odoo import models, fields

class SageSubactividad(models.Model):
    _name = 'sage.subactividad'
    _description = 'Sage Subactividad'
    
    name = fields.Char('Nombre', required=True)
    sage_actividad_id = fields.Many2one(comodel_name='sage.actividad', ondelete='restrict')    