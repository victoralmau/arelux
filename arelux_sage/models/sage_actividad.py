#-*- coding: utf-8 -*-
from openerp import models, fields

class SageActividad(models.Model):
    _name = 'sage.actividad'
    _description = 'Sage Actividad'
    
    name = fields.Char('Nombre', required=True)    