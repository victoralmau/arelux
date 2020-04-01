#-*- coding: utf-8 -*-
from openerp import models, fields

class SageColectivo(models.Model):
    _name = 'sage.colectivo'
    name = fields.Char('Nombre', required=True)