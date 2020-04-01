#-*- coding: utf-8 -*-
from openerp import models, fields

class SageCategoriaCliente(models.Model):
    _name = 'sage.categoria.cliente'
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)    