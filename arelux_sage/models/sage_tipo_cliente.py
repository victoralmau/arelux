#-*- coding: utf-8 -*-
from odoo import models, fields

class SageTipoCliente(models.Model):
    _name = 'sage.tipo.cliente'
    _description = 'Sage Tipo Cliente'
    
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)