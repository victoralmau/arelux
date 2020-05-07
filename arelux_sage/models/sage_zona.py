#-*- coding: utf-8 -*-
from odoo import models, fields

class SageZona(models.Model):
    _name = 'sage.zona'
    _description = 'Sage Zona'
    
    name = fields.Char('Nombre', required=True)    