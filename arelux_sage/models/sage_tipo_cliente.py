#-*- coding: utf-8 -*-
from openerp import models, fields

class SageTipoCliente(models.Model):
    _name = 'sage.tipo.cliente'
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)