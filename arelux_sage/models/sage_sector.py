#-*- coding: utf-8 -*-
from openerp import models, fields

class SageSector(models.Model):
    _name = 'sage.sector'
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)    