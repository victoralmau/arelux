#-*- coding: utf-8 -*-
from openerp import models, fields

class SageTerritorio(models.Model):
    _name = 'sage.territorio'
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)    