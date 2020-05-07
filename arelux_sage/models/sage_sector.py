#-*- coding: utf-8 -*-
from odoo import models, fields

class SageSector(models.Model):
    _name = 'sage.sector'
    _description = 'Sage Sector'
    
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)    