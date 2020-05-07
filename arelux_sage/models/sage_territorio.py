#-*- coding: utf-8 -*-
from odoo import models, fields

class SageTerritorio(models.Model):
    _name = 'sage.territorio'
    _description = 'Sage Territorio'
    
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)    