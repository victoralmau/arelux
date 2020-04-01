#-*- coding: utf-8 -*-
from openerp import models, fields

class SageZona(models.Model):
    _name = 'sage.zona'
    name = fields.Char('Nombre', required=True)    