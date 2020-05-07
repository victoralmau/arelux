#-*- coding: utf-8 -*-
from odoo import models, fields

class SageCategoriaCliente(models.Model):
    _name = 'sage.categoria.cliente'
    _description = 'Sage Categoria Cliente'
    
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)    