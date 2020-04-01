#-*- coding: utf-8 -*-
from openerp import models, fields

class SageActividad(models.Model):
    _name = 'sage.actividad'
    name = fields.Char('Nombre', required=True)    